from django.urls import path
from . import views

urlpatterns = [
    # 公共页面
    path('', views.index, name='index'),
    
    # 患者界面
    path('patient/', views.patient_interface, name='patient_interface'),
    path('patient/<str:patient_id>/', views.patient_interface, name='patient_interface_with_id'),
    path('api/process-message/', views.process_message, name='process_message'),
    path('api/voice-to-text/', views.voice_to_text, name='voice_to_text'),
    
    # 照护人员界面
    path('caregiver/', views.caregiver_dashboard, name='caregiver_dashboard'),
    
    # 患者管理 - 先放具体路径
    path('caregiver/patient/add/', views.add_patient, name='add_patient'),
    
    # 详情页面 - 再放带参数的路径
    path('caregiver/patient/<str:patient_id>/', views.patient_detail, name='patient_detail'),
    path('caregiver/patient/<str:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('caregiver/patient/<str:patient_id>/progress/', views.patient_progress, name='patient_progress'),
    path('caregiver/patient/<str:patient_id>/export/', views.export_assessment_data, name='export_assessment_data'),
    
    path('caregiver/conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('caregiver/assessment/<int:assessment_id>/', views.assessment_report, name='assessment_report'),
]
