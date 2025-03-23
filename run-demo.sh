#!/bin/bash

# TransMbD 失智监护辅助系统演示启动脚本

echo "================================================="
echo "  TransMbD 失智监护辅助系统 - 本地演示启动脚本   "
echo "================================================="

# 检查Python环境
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "错误: 未找到Python。请安装Python 3.9+后重试。"
    exit 1
fi

echo "使用Python: $($PYTHON --version)"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    $PYTHON -m venv venv
    if [ $? -ne 0 ]; then
        echo "错误: 无法创建虚拟环境。请确保已安装venv模块。"
        exit 1
    fi
fi

# 激活虚拟环境
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

if [ $? -ne 0 ]; then
    echo "错误: 无法激活虚拟环境。"
    exit 1
fi

echo "正在检查依赖项..."
pip install -r requirements.txt

echo "初始化数据库..."
$PYTHON manage.py migrate

# 检查超级用户是否存在
echo "检查管理员账户..."
$PYTHON -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(username='admin').exists() else 1)" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "创建演示管理员账户..."
    cat << EOF | $PYTHON manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF
    echo "已创建管理员账户："
    echo "  用户名: admin"
    echo "  密码: admin"
fi

# 创建演示数据
echo "加载演示数据..."
cat << EOF | $PYTHON manage.py shell
from core.models import Patient, Conversation, Message, DementiaAssessment
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import json
import datetime

User = get_user_model()
admin = User.objects.get(username='admin')

# 检查是否已有演示数据
if Patient.objects.count() == 0:
    # 创建示例患者
    patients_data = [
        {'patient_id': 'P001', 'name': '张志明', 'age': 72, 'gender': 'M', 'mmse_score': 24, 'cdr_score': 0.5},
        {'patient_id': 'P002', 'name': '李秀珍', 'age': 68, 'gender': 'F', 'mmse_score': 27, 'cdr_score': 0},
        {'patient_id': 'P003', 'name': '王大明', 'age': 75, 'gender': 'M', 'mmse_score': 20, 'cdr_score': 1},
        {'patient_id': 'P004', 'name': '陈小红', 'age': 82, 'gender': 'F', 'mmse_score': 15, 'cdr_score': 2},
        {'patient_id': 'P005', 'name': '郭美玲', 'age': 65, 'gender': 'F', 'mmse_score': 26, 'cdr_score': 0.5},
    ]
    
    for patient_data in patients_data:
        Patient.objects.create(
            patient_id=patient_data['patient_id'],
            name=patient_data['name'],
            age=patient_data['age'],
            gender=patient_data['gender'],
            mmse_score=patient_data['mmse_score'],
            cdr_score=patient_data['cdr_score'],
            caregiver=admin
        )
    
    # 为每个患者创建对话和评估
    patients = Patient.objects.all()
    
    for patient in patients:
        # 创建几次对话
        for i in range(3):
            # 计算日期，每次递减10天
            conversation_date = timezone.now() - datetime.timedelta(days=i*10)
            
            conversation = Conversation.objects.create(
                patient=patient,
                start_time=conversation_date
            )
            
            # 对话结束时间
            if i > 0:  # 前两次对话已结束
                conversation.end_time = conversation_date + datetime.timedelta(minutes=random.randint(15, 45))
                conversation.save()
            
            # 添加消息
            sample_questions = [
                "您今天感觉如何？",
                "您能告诉我今天是几月几号吗？",
                "您能回忆一下今天早上做了什么吗？",
                "您最近睡眠质量如何？",
                "您记得上次我们见面是什么时候吗？"
            ]
            
            sample_responses = [
                "我感觉还好，就是有点累。",
                "今天是...我记不太清楚了，可能是6月？",
                "我早上起床后吃了早饭，然后看了一会电视。具体做了什么有点记不清了。",
                "我晚上睡得不太好，常常半夜醒来。",
                "上次见面？我想想...应该是上周吧，我不太确定。"
            ]
            
            # 每次对话5轮
            for j in range(5):
                Message.objects.create(
                    conversation=conversation,
                    sender_type='system',
                    content=sample_questions[j % len(sample_questions)],
                    timestamp=conversation_date + datetime.timedelta(minutes=j*3)
                )
                
                Message.objects.create(
                    conversation=conversation,
                    sender_type='patient',
                    content=sample_responses[j % len(sample_responses)],
                    timestamp=conversation_date + datetime.timedelta(minutes=j*3+1)
                )
            
            # 创建评估
            severity_mapping = {
                0: 'normal',
                0.5: 'mild',
                1: 'moderate',
                2: 'severe',
                3: 'severe'
            }
            
            # 基于CDR分数设置基础严重程度，但随时间略有变化
            base_severity = severity_mapping.get(patient.cdr_score, 'mild')
            severity_score = {
                'normal': random.uniform(0.05, 0.19),
                'mild': random.uniform(0.25, 0.45),
                'moderate': random.uniform(0.55, 0.7),
                'severe': random.uniform(0.8, 0.95)
            }[base_severity]
            
            # 随着时间推移，病情略有加重
            if i > 0:
                severity_score += i * 0.05
                
                # 重新确定严重程度类别
                if severity_score < 0.2:
                    severity = 'normal'
                elif severity_score < 0.5:
                    severity = 'mild'
                elif severity_score < 0.75:
                    severity = 'moderate'
                else:
                    severity = 'severe'
            else:
                severity = base_severity
            
            # 生成维度分数
            dimension_scores = {
                'memory': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1))),
                'orientation': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1))),
                'language': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1))),
                'attention': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1))),
                'problem_solving': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1)))
            }
            
            detailed_results = {
                'severity_score': round(severity_score, 2),
                'severity_category': severity,
                'confidence': round(random.uniform(0.75, 0.95), 2),
                'dimension_scores': {k: round(v, 2) for k, v in dimension_scores.items()},
                'timestamp': conversation_date.isoformat()
            }
            
            DementiaAssessment.objects.create(
                patient=patient,
                conversation=conversation,
                assessment_date=conversation_date + datetime.timedelta(minutes=15),
                severity=severity,
                confidence_score=detailed_results['confidence'],
                detailed_results=detailed_results
            )
    
    print("已创建演示数据：5位患者，每位患者3次对话和评估")
else:
    print("已存在演示数据，跳过创建")
EOF

echo "启动服务器..."
$PYTHON manage.py runserver

# 脚本结束时的清理操作
deactivate
echo "服务已停止。"
