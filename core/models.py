from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class Patient(models.Model):
    """患者信息模型"""
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]
    
    patient_id = models.CharField(max_length=20, unique=True, verbose_name="患者ID")
    name = models.CharField(max_length=100, verbose_name="姓名")
    age = models.PositiveIntegerField(verbose_name="年龄")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="性别")
    date_registered = models.DateField(default=timezone.now, verbose_name="注册日期")
    caregiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name="patients", verbose_name="负责照护人员")
    
    # 临床测验数据
    mmse_score = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="MMSE分数")
    cdr_score = models.FloatField(null=True, blank=True, verbose_name="CDR分数")
    
    def __str__(self):
        return f"{self.name} ({self.patient_id})"
    
    class Meta:
        verbose_name = "患者"
        verbose_name_plural = "患者"


class Conversation(models.Model):
    """对话记录模型"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="conversations", 
                              verbose_name="患者")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="开始时间")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    
    def __str__(self):
        return f"与{self.patient.name}的对话 - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    def complete_conversation(self):
        """结束对话"""
        self.end_time = timezone.now()
        self.save()
    
    class Meta:
        verbose_name = "对话记录"
        verbose_name_plural = "对话记录"


class Message(models.Model):
    """对话消息模型"""
    MESSAGE_TYPE = [
        ('patient', '患者'),
        ('system', '系统'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, 
                                    related_name="messages", verbose_name="对话")
    sender_type = models.CharField(max_length=10, choices=MESSAGE_TYPE, verbose_name="发送者类型")
    content = models.TextField(verbose_name="内容")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="时间戳")
    
    def __str__(self):
        return f"{self.get_sender_type_display()}: {self.content[:30]}..."
    
    class Meta:
        verbose_name = "消息"
        verbose_name_plural = "消息"
        ordering = ['timestamp']


class DementiaAssessment(models.Model):
    """失智症评估模型"""
    SEVERITY_CHOICES = [
        ('normal', '正常'),
        ('mild', '轻度'),
        ('moderate', '中度'),
        ('severe', '重度'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, 
                              related_name="assessments", verbose_name="患者")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, 
                                   related_name="assessments", verbose_name="相关对话")
    assessment_date = models.DateTimeField(auto_now_add=True, verbose_name="评估日期")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, verbose_name="严重程度")
    confidence_score = models.FloatField(verbose_name="置信度分数")
    
    # 存储详细评估结果的JSON字段
    detailed_results = models.JSONField(default=dict, verbose_name="详细评估结果")
    
    def get_detailed_results(self):
        """获取详细评估结果"""
        return self.detailed_results
    
    def set_detailed_results(self, results_dict):
        """设置详细评估结果"""
        self.detailed_results = results_dict
        self.save()
    
    def __str__(self):
        return f"{self.patient.name}的评估 - {self.assessment_date.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = "失智症评估"
        verbose_name_plural = "失智症评估"
