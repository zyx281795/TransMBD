from django import forms
from .models import Patient, Conversation, Message, DementiaAssessment


class PatientForm(forms.ModelForm):
    """患者信息表单"""
    class Meta:
        model = Patient
        fields = ['patient_id', 'name', 'age', 'gender', 'mmse_score', 'cdr_score']
        widgets = {
            'patient_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入患者ID'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入患者姓名'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '输入患者年龄'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'mmse_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '输入MMSE分数 (0-30)'}),
            'cdr_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '输入CDR分数 (0, 0.5, 1, 2, 3)'}),
        }
        labels = {
            'patient_id': '患者ID',
            'name': '姓名',
            'age': '年龄',
            'gender': '性别',
            'mmse_score': 'MMSE分数',
            'cdr_score': 'CDR分数',
        }
        help_texts = {
            'mmse_score': '简易智能状态测验分数 (0-30), 越高越好',
            'cdr_score': '临床失智症评估工作单分数 (0, 0.5, 1, 2, 3), 0为正常, 3为重度失智',
        }


class ConversationForm(forms.ModelForm):
    """对话信息表单"""
    class Meta:
        model = Conversation
        fields = ['patient']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'patient': '患者',
        }


class MessageForm(forms.ModelForm):
    """消息表单"""
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '输入消息...'}),
        }
        labels = {
            'content': '消息内容',
        }


class VoiceInputForm(forms.Form):
    """语音输入表单"""
    audio_file = forms.FileField(
        label='语音文件',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'audio/*'}),
        required=False,
    )


class AssessmentFilterForm(forms.Form):
    """评估过滤表单"""
    start_date = forms.DateField(
        label='开始日期',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
    )
    end_date = forms.DateField(
        label='结束日期',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
    )
    severity = forms.ChoiceField(
        label='严重程度',
        choices=[('', '全部')] + list(DementiaAssessment.SEVERITY_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
    )
