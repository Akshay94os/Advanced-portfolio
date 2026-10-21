"""URL configuration for the main portfolio app."""
from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
    path('projects/', views.projects_page, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('profiles/', views.profiles_page, name='profiles'),
    path('notes/', views.notes_page, name='notes'),
    path('documents/', views.documents_page, name='documents'),

    # Auth
    path('auth/admin-login/', views.admin_login, name='admin_login'),
    path('auth/admin-logout/', views.admin_logout, name='admin_logout'),
    path('auth/doc-gate-login/', views.doc_gate_login, name='doc_gate_login'),
    path('auth/doc-gate-logout/', views.doc_gate_logout, name='doc_gate_logout'),
    path('auth/doc-gate-forgot/', views.doc_gate_forgot_password, name='doc_gate_forgot'),

    # Resume
    path('api/resume/', views.extract_resume, name='extract_resume'),

    # Profile CRUD
    path('api/profile/update/', views.profile_update, name='profile_update'),

    # Skill CRUD
    path('api/skills/create/', views.skill_create, name='skill_create'),
    path('api/skills/<int:pk>/update/', views.skill_update, name='skill_update'),
    path('api/skills/<int:pk>/delete/', views.skill_delete, name='skill_delete'),

    # SocialProfile CRUD
    path('api/socials/create/', views.social_create, name='social_create'),
    path('api/socials/<int:pk>/update/', views.social_update, name='social_update'),
    path('api/socials/<int:pk>/delete/', views.social_delete, name='social_delete'),

    # Project CRUD
    path('api/projects/create/', views.project_create, name='project_create'),
    path('api/projects/<int:pk>/update/', views.project_update, name='project_update'),
    path('api/projects/<int:pk>/delete/', views.project_delete, name='project_delete'),

    # Note CRUD
    path('api/notes/create/', views.note_create, name='note_create'),
    path('api/notes/<int:pk>/update/', views.note_update, name='note_update'),
    path('api/notes/<int:pk>/delete/', views.note_delete, name='note_delete'),

    # Document CRUD
    path('api/documents/create/', views.document_create, name='document_create'),
    path('api/documents/<int:pk>/update/', views.document_update, name='document_update'),
    path('api/documents/<int:pk>/delete/', views.document_delete, name='document_delete'),

    # Footer CRUD
    path('api/footer/update/', views.footer_update, name='footer_update'),

    # Downloads
    path('download/document/<int:pk>/', views.download_document, name='download_document'),
    path('download/project-zip/<int:pk>/', views.download_project_zip, name='download_project_zip'),
    path('download/note/<int:pk>/', views.download_note_file, name='download_note_file'),
]
