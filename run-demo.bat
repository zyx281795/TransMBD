@echo off
setlocal

echo =================================================
echo   TransMbD 失智监护辅助系统 - 本地演示启动脚本   
echo =================================================

REM 检查Python环境
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo 错误: 未找到Python。请安装Python 3.9+后重试。
    exit /b 1
)

echo 使用Python: 
python --version

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo 错误: 无法创建虚拟环境。请确保已安装venv模块。
        exit /b 1
    )
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo 正在检查依赖项...
pip install -r requirements.txt

echo 初始化数据库...
python manage.py migrate

REM 检查超级用户是否存在
echo 检查管理员账户...
python -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(username='admin').exists() else 1)" 2>nul

if %ERRORLEVEL% neq 0 (
    echo 创建演示管理员账户...
    python manage.py shell < create_admin.py
    echo 已创建管理员账户：
    echo   用户名: admin
    echo   密码: admin
)

REM 创建管理员账户的临时Python脚本
echo from django.contrib.auth import get_user_model > create_admin.py
echo User = get_user_model() >> create_admin.py
echo User.objects.create_superuser('admin', 'admin@example.com', 'admin') >> create_admin.py

REM 创建演示数据
echo 加载演示数据...
python manage.py shell < create_demo_data.py

REM 创建演示数据的临时Python脚本
echo from core.models import Patient, Conversation, Message, DementiaAssessment > create_demo_data.py
echo from django.contrib.auth import get_user_model >> create_demo_data.py
echo from django.utils import timezone >> create_demo_data.py
echo import random >> create_demo_data.py
echo import json >> create_demo_data.py
echo import datetime >> create_demo_data.py
echo. >> create_demo_data.py
echo User = get_user_model() >> create_demo_data.py
echo admin = User.objects.get(username='admin') >> create_demo_data.py
echo. >> create_demo_data.py
echo # 检查是否已有演示数据 >> create_demo_data.py
echo if Patient.objects.count() == 0: >> create_demo_data.py
echo     # 创建示例患者 >> create_demo_data.py
echo     patients_data = [ >> create_demo_data.py
echo         {'patient_id': 'P001', 'name': '张志明', 'age': 72, 'gender': 'M', 'mmse_score': 24, 'cdr_score': 0.5}, >> create_demo_data.py
echo         {'patient_id': 'P002', 'name': '李秀珍', 'age': 68, 'gender': 'F', 'mmse_score': 27, 'cdr_score': 0}, >> create_demo_data.py
echo         {'patient_id': 'P003', 'name': '王大明', 'age': 75, 'gender': 'M', 'mmse_score': 20, 'cdr_score': 1}, >> create_demo_data.py
echo         {'patient_id': 'P004', 'name': '陈小红', 'age': 82, 'gender': 'F', 'mmse_score': 15, 'cdr_score': 2}, >> create_demo_data.py
echo         {'patient_id': 'P005', 'name': '郭美玲', 'age': 65, 'gender': 'F', 'mmse_score': 26, 'cdr_score': 0.5}, >> create_demo_data.py
echo     ] >> create_demo_data.py
echo. >> create_demo_data.py
echo     for patient_data in patients_data: >> create_demo_data.py
echo         Patient.objects.create( >> create_demo_data.py
echo             patient_id=patient_data['patient_id'], >> create_demo_data.py
echo             name=patient_data['name'], >> create_demo_data.py
echo             age=patient_data['age'], >> create_demo_data.py
echo             gender=patient_data['gender'], >> create_demo_data.py
echo             mmse_score=patient_data['mmse_score'], >> create_demo_data.py
echo             cdr_score=patient_data['cdr_score'], >> create_demo_data.py
echo             caregiver=admin >> create_demo_data.py
echo         ) >> create_demo_data.py
echo. >> create_demo_data.py
echo     # 为每个患者创建对话和评估 >> create_demo_data.py
echo     patients = Patient.objects.all() >> create_demo_data.py
echo. >> create_demo_data.py
echo     for patient in patients: >> create_demo_data.py
echo         # 创建几次对话 >> create_demo_data.py
echo         for i in range(3): >> create_demo_data.py
echo             # 计算日期，每次递减10天 >> create_demo_data.py
echo             conversation_date = timezone.now() - datetime.timedelta(days=i*10) >> create_demo_data.py
echo. >> create_demo_data.py
echo             conversation = Conversation.objects.create( >> create_demo_data.py
echo                 patient=patient, >> create_demo_data.py
echo                 start_time=conversation_date >> create_demo_data.py
echo             ) >> create_demo_data.py
echo. >> create_demo_data.py
echo             # 对话结束时间 >> create_demo_data.py
echo             if i ^> 0:  # 前两次对话已结束 >> create_demo_data.py
echo                 conversation.end_time = conversation_date + datetime.timedelta(minutes=random.randint(15, 45)) >> create_demo_data.py
echo                 conversation.save() >> create_demo_data.py
echo. >> create_demo_data.py
echo             # 添加消息 >> create_demo_data.py
echo             sample_questions = [ >> create_demo_data.py
echo                 "您今天感觉如何？", >> create_demo_data.py
echo                 "您能告诉我今天是几月几号吗？", >> create_demo_data.py
echo                 "您能回忆一下今天早上做了什么吗？", >> create_demo_data.py
echo                 "您最近睡眠质量如何？", >> create_demo_data.py
echo                 "您记得上次我们见面是什么时候吗？" >> create_demo_data.py
echo             ] >> create_demo_data.py
echo. >> create_demo_data.py
echo             sample_responses = [ >> create_demo_data.py
echo                 "我感觉还好，就是有点累。", >> create_demo_data.py
echo                 "今天是...我记不太清楚了，可能是6月？", >> create_demo_data.py
echo                 "我早上起床后吃了早饭，然后看了一会电视。具体做了什么有点记不清了。", >> create_demo_data.py
echo                 "我晚上睡得不太好，常常半夜醒来。", >> create_demo_data.py
echo                 "上次见面？我想想...应该是上周吧，我不太确定。" >> create_demo_data.py
echo             ] >> create_demo_data.py
echo. >> create_demo_data.py
echo             # 每次对话5轮 >> create_demo_data.py
echo             for j in range(5): >> create_demo_data.py
echo                 Message.objects.create( >> create_demo_data.py
echo                     conversation=conversation, >> create_demo_data.py
echo                     sender_type='system', >> create_demo_data.py
echo                     content=sample_questions[j %% len(sample_questions)], >> create_demo_data.py
echo                     timestamp=conversation_date + datetime.timedelta(minutes=j*3) >> create_demo_data.py
echo                 ) >> create_demo_data.py
echo. >> create_demo_data.py
echo                 Message.objects.create( >> create_demo_data.py
echo                     conversation=conversation, >> create_demo_data.py
echo                     sender_type='patient', >> create_demo_data.py
echo                     content=sample_responses[j %% len(sample_responses)], >> create_demo_data.py
echo                     timestamp=conversation_date + datetime.timedelta(minutes=j*3+1) >> create_demo_data.py
echo                 ) >> create_demo_data.py
echo. >> create_demo_data.py
echo             # 创建评估 >> create_demo_data.py
echo             severity_mapping = { >> create_demo_data.py
echo                 0: 'normal', >> create_demo_data.py
echo                 0.5: 'mild', >> create_demo_data.py
echo                 1: 'moderate', >> create_demo_data.py
echo                 2: 'severe', >> create_demo_data.py
echo                 3: 'severe' >> create_demo_data.py
echo             } >> create_demo_data.py
echo. >> create_demo_data.py
echo             # 基于CDR分数设置基础严重程度，但随时间略有变化 >> create_demo_data.py
echo             base_severity = severity_mapping.get(patient.cdr_score, 'mild') >> create_demo_data.py
echo             severity_score = { >> create_demo_data.py
echo                 'normal': random.uniform(0.05, 0.19), >> create_demo_data.py
echo                 'mild': random.uniform(0.25, 0.45), >> create_demo_data.py
echo                 'moderate': random.uniform(0.55, 0.7), >> create_demo_data.py
echo                 'severe': random.uniform(0.8, 0.95) >> create_demo_data.py
echo             }[base_severity] >> create_demo_data.py
echo. >> create_demo_data.py
echo             # 随着时间推移，病情略有加重 >> create_demo_data.py
echo             if i ^> 0: >> create_demo_data.py
echo                 severity_score += i * 0.05 >> create_demo_data.py
echo. >> create_demo_data.py
echo                 # 重新确定严重程度类别 >> create_demo_data.py
echo                 if severity_score ^< 0.2: >> create_demo_data.py
echo                     severity = 'normal' >> create_demo_data.py
echo                 elif severity_score ^< 0.5: >> create_demo_data.py
echo                     severity = 'mild' >> create_demo_data.py
echo                 elif severity_score ^< 0.75: >> create_demo_data.py
echo                     severity = 'moderate' >> create_demo_data.py
echo                 else: >> create_demo_data.py
echo                     severity = 'severe' >> create_demo_data.py
echo             else: >> create_demo_data.py
echo                 severity = base_severity >> create_demo_data.py
echo. >> create_demo_data.py
echo             # 生成维度分数 >> create_demo_data.py
echo             dimension_scores = { >> create_demo_data.py
echo                 'memory': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1))), >> create_demo_data.py
echo                 'orientation': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1))), >> create_demo_data.py
echo                 'language': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1))), >> create_demo_data.py
echo                 'attention': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1))), >> create_demo_data.py
echo                 'problem_solving': min(1.0, max(0.1, severity_score + random.uniform(-0.1, 0.1))) >> create_demo_data.py
echo             } >> create_demo_data.py
echo. >> create_demo_data.py
echo             detailed_results = { >> create_demo_data.py
echo                 'severity_score': round(severity_score, 2), >> create_demo_data.py
echo                 'severity_category': severity, >> create_demo_data.py
echo                 'confidence': round(random.uniform(0.75, 0.95), 2), >> create_demo_data.py
echo                 'dimension_scores': {k: round(v, 2) for k, v in dimension_scores.items()}, >> create_demo_data.py
echo                 'timestamp': conversation_date.isoformat() >> create_demo_data.py
echo             } >> create_demo_data.py
echo. >> create_demo_data.py
echo             DementiaAssessment.objects.create( >> create_demo_data.py
echo                 patient=patient, >> create_demo_data.py
echo                 conversation=conversation, >> create_demo_data.py
echo                 assessment_date=conversation_date + datetime.timedelta(minutes=15), >> create_demo_data.py
echo                 severity=severity, >> create_demo_data.py
echo                 confidence_score=detailed_results['confidence'], >> create_demo_data.py
echo                 detailed_results=detailed_results >> create_demo_data.py
echo             ) >> create_demo_data.py
echo. >> create_demo_data.py
echo     print("已创建演示数据：5位患者，每位患者3次对话和评估") >> create_demo_data.py
echo else: >> create_demo_data.py
echo     print("已存在演示数据，跳过创建") >> create_demo_data.py

echo 启动服务器...
python manage.py runserver

REM 清理临时文件
del create_admin.py
del create_demo_data.py

REM 脚本结束时的清理操作
call venv\Scripts\deactivate.bat
echo 服务已停止。

endlocal
