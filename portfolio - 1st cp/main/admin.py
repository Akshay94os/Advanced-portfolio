"""Admin configuration for the portfolio application."""
from django.contrib import admin
from .models import Profile, Skill, SocialProfile, Project, Note, Document, Footer


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'contact_email', 'updated_at')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'order')
    list_editable = ('proficiency', 'order')
    list_filter = ('category',)


@admin.register(SocialProfile)
class SocialProfileAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'username', 'profile_url', 'order')
    list_editable = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'created_at')
    list_filter = ('featured',)
    list_editable = ('featured',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'live_url', 'created_at')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at', 'file_size_display')
    list_filter = ('category',)


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('copyright_text', 'contact_email', 'updated_at')
