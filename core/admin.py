from django.contrib import admin
from .models import Patient, Conversation, Message, DementiaAssessment


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """患者管理界面"""
    list_display = ('patient_id', 'name', 'age', 'gender', 'mmse_score', 'cdr_score', 'caregiver', 'date_registered')
    list_filter = ('gender', 'caregiver')
    search_fields = ('patient_id', 'name')
    date_hierarchy = 'date_registered'
    ordering = ('-date_registered',)
    list_per_page = 20


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """对话管理界面"""
    list_display = ('id', 'patient', 'start_time', 'end_time', 'message_count', 'assessment_count')
    list_filter = ('start_time', 'patient')
    search_fields = ('patient__name', 'patient__patient_id')
    date_hierarchy = 'start_time'
    ordering = ('-start_time',)
    list_per_page = 20

    def message_count(self, obj):
        """消息数量"""
        return obj.messages.count()
    message_count.short_description = "消息数量"

    def assessment_count(self, obj):
        """评估数量"""
        return obj.assessments.count()
    assessment_count.short_description = "评估数量"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """消息管理界面"""
    list_display = ('id', 'conversation', 'sender_type', 'content_preview', 'timestamp')
    list_filter = ('sender_type', 'timestamp')
    search_fields = ('content', 'conversation__patient__name')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    list_per_page = 50

    def content_preview(self, obj):
        """内容预览"""
        if len(obj.content) > 50:
            return obj.content[:50] + "..."
        return obj.content
    content_preview.short_description = "内容预览"


@admin.register(DementiaAssessment)
class DementiaAssessmentAdmin(admin.ModelAdmin):
    """失智症评估管理界面"""
    list_display = ('id', 'patient', 'assessment_date', 'severity', 'confidence_score')
    list_filter = ('severity', 'assessment_date')
    search_fields = ('patient__name', 'patient__patient_id')
    date_hierarchy = 'assessment_date'
    ordering = ('-assessment_date',)
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        """只读字段"""
        if obj:  # 编辑时
            return ('patient', 'conversation', 'assessment_date', 'detailed_results')
        return ()
