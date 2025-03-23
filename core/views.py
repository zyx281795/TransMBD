from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q

import json
import datetime

from .models import Patient, Conversation, Message, DementiaAssessment
from .utils.text_processor import TextProcessor
from .utils.predictor import DementiaPredictor, ConversationManager
from .forms import PatientForm


def index(request):
    """系统首页"""
    context = {
        'title': 'TransMbD 失智监护辅助系统',
    }
    return render(request, 'index.html', context)


def patient_interface(request, patient_id=None):
    """患者交互界面"""
    # 如果提供了患者ID，则获取患者信息
    patient = None
    if patient_id:
        patient = get_object_or_404(Patient, patient_id=patient_id)
    
    # 创建一个新的对话或获取最近未完成的对话
    active_conversation = None
    if patient:
        active_conversation = Conversation.objects.filter(
            patient=patient, 
            end_time__isnull=True
        ).first()
        
        if not active_conversation:
            active_conversation = Conversation.objects.create(patient=patient)
    
    context = {
        'title': '对话界面',
        'patient': patient,
        'conversation_id': active_conversation.id if active_conversation else None,
    }
    return render(request, 'patient_interface.html', context)


@csrf_exempt
def process_message(request):
    """处理患者消息并生成回复"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    try:
        data = json.loads(request.body)
        patient_input = data.get('message', '')
        conversation_id = data.get('conversation_id')
        
        if not patient_input or not conversation_id:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
        
        # 获取对话
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # 保存患者消息
        Message.objects.create(
            conversation=conversation,
            sender_type='patient',
            content=patient_input
        )
        
        # 使用对话管理器生成回复并评估
        conversation_manager = ConversationManager()
        response, assessment = conversation_manager.generate_response(patient_input)
        
        # 保存系统回复
        Message.objects.create(
            conversation=conversation,
            sender_type='system',
            content=response
        )
        
        # 保存评估结果
        DementiaAssessment.objects.create(
            patient=conversation.patient,
            conversation=conversation,
            severity=assessment['severity_category'],
            confidence_score=assessment['confidence'],
            detailed_results=assessment
        )
        
        return JsonResponse({
            'response': response,
            'assessment': assessment
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def voice_to_text(request):
    """语音转文本接口（模拟）"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # 在实际应用中，这里会处理上传的音频文件并调用语音识别API
    # 为了演示，我们返回一个固定的文本
    return JsonResponse({
        'success': True,
        'text': '我今天感觉有点迷糊，想不起来刚才做了什么。'
    })


@login_required
def caregiver_dashboard(request):
    """照护人员仪表板"""
    # 获取照护人员负责的患者
    patients = Patient.objects.filter(
        Q(caregiver=request.user) | Q(caregiver__isnull=True)
    )
    
    context = {
        'title': '照护人员仪表板',
        'patients': patients,
    }
    return render(request, 'caregiver_dashboard.html', context)


@login_required
def patient_detail(request, patient_id):
    """患者详细信息页面"""
    patient = get_object_or_404(Patient, patient_id=patient_id)
    
    # 获取患者的评估历史
    assessments = DementiaAssessment.objects.filter(patient=patient).order_by('-assessment_date')
    
    # 获取患者的最近对话
    conversations = Conversation.objects.filter(patient=patient).order_by('-start_time')[:5]
    
    context = {
        'title': f'患者: {patient.name}',
        'patient': patient,
        'assessments': assessments,
        'conversations': conversations,
    }
    return render(request, 'patient_detail.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """对话详细信息页面"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # 获取对话中的所有消息
    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
    
    # 获取对话相关的评估
    assessments = DementiaAssessment.objects.filter(conversation=conversation).order_by('assessment_date')
    
    context = {
        'title': f'对话详情',
        'conversation': conversation,
        'messages': messages,
        'assessments': assessments,
    }
    return render(request, 'conversation_detail.html', context)


@login_required
def add_patient(request):
    """添加新患者"""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.caregiver = request.user
            patient.save()
            messages.success(request, f'患者 {patient.name} 已成功添加！')
            return redirect('patient_detail', patient_id=patient.patient_id)
    else:
        form = PatientForm()
    
    context = {
        'title': '添加新患者',
        'form': form,
    }
    return render(request, 'add_patient.html', context)


@login_required
def edit_patient(request, patient_id):
    """编辑患者信息"""
    patient = get_object_or_404(Patient, patient_id=patient_id)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'患者 {patient.name} 的信息已更新！')
            return redirect('patient_detail', patient_id=patient.patient_id)
    else:
        form = PatientForm(instance=patient)
    
    context = {
        'title': f'编辑患者: {patient.name}',
        'form': form,
        'patient': patient,
    }
    return render(request, 'edit_patient.html', context)


@login_required
def assessment_report(request, assessment_id):
    """查看评估报告"""
    assessment = get_object_or_404(DementiaAssessment, id=assessment_id)
    
    # 生成评估报告
    predictor = DementiaPredictor()
    report = predictor.generate_report(assessment.detailed_results)
    
    context = {
        'title': '评估报告',
        'assessment': assessment,
        'report': report,
        'patient': assessment.patient,
    }
    return render(request, 'assessment_report.html', context)


@login_required
def export_assessment_data(request, patient_id):
    """导出患者评估数据（CSV格式）"""
    patient = get_object_or_404(Patient, patient_id=patient_id)
    
    # 获取患者的所有评估
    assessments = DementiaAssessment.objects.filter(patient=patient).order_by('assessment_date')
    
    # 创建CSV数据
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{patient.name}_assessments.csv"'
    
    # 写入CSV头
    response.write('日期,严重程度,置信度,记忆,方向感,语言,注意力,问题解决\n')
    
    # 写入数据行
    for assessment in assessments:
        detailed = assessment.detailed_results
        dimension_scores = detailed.get('dimension_scores', {})
        
        date = assessment.assessment_date.strftime('%Y-%m-%d %H:%M')
        severity = assessment.severity
        confidence = assessment.confidence_score
        
        memory = dimension_scores.get('memory', 'N/A')
        orientation = dimension_scores.get('orientation', 'N/A')
        language = dimension_scores.get('language', 'N/A')
        attention = dimension_scores.get('attention', 'N/A')
        problem_solving = dimension_scores.get('problem_solving', 'N/A')
        
        line = f'{date},{severity},{confidence},{memory},{orientation},{language},{attention},{problem_solving}\n'
        response.write(line)
    
    return response


@login_required
def patient_progress(request, patient_id):
    """患者进展分析页面"""
    patient = get_object_or_404(Patient, patient_id=patient_id)
    
    # 获取患者的所有评估，按时间排序
    assessments = DementiaAssessment.objects.filter(patient=patient).order_by('assessment_date')
    
    # 准备图表数据
    dates = [assessment.assessment_date.strftime('%Y-%m-%d') for assessment in assessments]
    severity_scores = [assessment.detailed_results.get('severity_score', 0) for assessment in assessments]
    
    # 按维度准备数据
    dimensions = ['memory', 'orientation', 'language', 'attention', 'problem_solving']
    dimension_data = {}
    
    for dimension in dimensions:
        dimension_data[dimension] = []
        for assessment in assessments:
            score = assessment.detailed_results.get('dimension_scores', {}).get(dimension, 0)
            dimension_data[dimension].append(score)
    
    context = {
        'title': f'患者进展: {patient.name}',
        'patient': patient,
        'dates': json.dumps(dates),
        'severity_scores': json.dumps(severity_scores),
        'dimension_data': json.dumps(dimension_data),
        'assessments': assessments,
    }
    return render(request, 'patient_progress.html', context)
