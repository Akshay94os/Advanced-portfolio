"""Views for the portfolio application."""
import json
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages

from .models import Profile, Skill, SocialProfile, Project, Note, Document, Footer
from .forms import (
    ProfileForm, SkillForm, SocialProfileForm, ProjectForm,
    NoteForm, DocumentForm, FooterForm, AdminLoginForm, DocumentGatekeeperForm
)


# ─── Helper ───────────────────────────────────────────────────────────────────

def json_response(success=True, data=None, message='', status=200):
    payload = {'success': success, 'message': message}
    if data is not None:
        payload['data'] = data
    return JsonResponse(payload, status=status)


def admin_required(view_func):
    """Decorator: only allow requests when admin session is active."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            return json_response(False, message='Unauthorized. Please log in as admin.', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


# ─── Auth ─────────────────────────────────────────────────────────────────────

def admin_login(request):
    if request.method == 'POST':
        password = request.POST.get('password', '')
        if password == settings.ADMIN_EDIT_PASSWORD:
            request.session['admin_logged_in'] = True
            return json_response(True, message='Logged in successfully.')
        return json_response(False, message='Incorrect password.', status=401)
    return json_response(False, message='Method not allowed.', status=405)


def admin_logout(request):
    request.session.pop('admin_logged_in', None)
    return json_response(True, message='Logged out.')


def doc_gate_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()
        expected_email = settings.DOCUMENT_GATE_EMAIL.lower()
        expected_password = settings.DOCUMENT_GATE_PASSWORD
        if email == expected_email and password == expected_password:
            request.session['doc_gate_open'] = True
            return json_response(True, message='Access granted.')
        return json_response(False, message='Invalid email or password.', status=401)
    return json_response(False, message='Method not allowed.', status=405)


def doc_gate_logout(request):
    request.session.pop('doc_gate_open', None)
    return redirect('documents')


def doc_gate_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if email == settings.DOCUMENT_GATE_EMAIL.lower():
            try:
                send_mail(
                    subject='Portfolio Documents – Password Reminder',
                    message=(
                        f'Hello Akshay,\n\n'
                        f'Your document repository password is: {settings.DOCUMENT_GATE_PASSWORD}\n\n'
                        f'Keep it safe!\n\nYour Portfolio System'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                return json_response(True, message='Password sent to your email.')
            except Exception as e:
                return json_response(False, message=f'Email send failed: {str(e)}', status=500)
        return json_response(False, message='Email not found.', status=404)
    return json_response(False, message='Method not allowed.', status=405)


# ─── Resume Extraction ────────────────────────────────────────────────────────

def extract_resume(request):
    """Extract text from resume PDF and return as JSON."""
    try:
        import PyPDF2
        # Try local resume.pdf first, then stored resume
        local_path = os.path.join(settings.BASE_DIR, 'resume.pdf')
        profile = Profile.objects.first()

        pdf_path = None
        if os.path.exists(local_path):
            pdf_path = local_path
        elif profile and profile.resume_file:
            pdf_path = profile.resume_file.path

        if not pdf_path:
            return json_response(False, message='Resume file not found.', status=404)

        text_pages = []
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ''
                text_pages.append({'page': i + 1, 'text': text.strip()})

        full_text = '\n\n'.join(p['text'] for p in text_pages)
        return json_response(True, data={'pages': text_pages, 'full_text': full_text, 'page_count': len(text_pages)})
    except ImportError:
        return json_response(False, message='PyPDF2 not installed.', status=500)
    except Exception as e:
        return json_response(False, message=str(e), status=500)


# ─── Pages ────────────────────────────────────────────────────────────────────

def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    social_profiles = SocialProfile.objects.all()
    projects = Project.objects.all()[:6]
    footer = Footer.objects.first()

    # Build 5-line intro list from profile
    intro_lines = []
    if profile:
        for field in ['intro_line1', 'intro_line2', 'intro_line3', 'intro_line4', 'intro_line5']:
            val = getattr(profile, field, '')
            if val:
                intro_lines.append(val)

    context = {
        'profile': profile,
        'intro_lines': intro_lines,
        'skills': skills,
        'social_profiles': social_profiles,
        'projects': projects,
        'footer': footer,
        'profile_form': ProfileForm(instance=profile) if profile else ProfileForm(),
        'skill_form': SkillForm(),
        'social_form': SocialProfileForm(),
        'footer_form': FooterForm(instance=footer) if footer else FooterForm(),
    }
    return render(request, 'home.html', context)


def projects_page(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
        'project_form': ProjectForm(),
    }
    return render(request, 'projects.html', context)


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {
        'project': project,
        'project_form': ProjectForm(instance=project),
    }
    return render(request, 'project_detail.html', context)


def profiles_page(request):
    social_profiles = SocialProfile.objects.all()
    context = {
        'social_profiles': social_profiles,
        'social_form': SocialProfileForm(),
    }
    return render(request, 'profiles.html', context)


def notes_page(request):
    notes = Note.objects.all()
    context = {
        'notes': notes,
        'note_form': NoteForm(),
    }
    return render(request, 'notes.html', context)


def documents_page(request):
    if not request.session.get('doc_gate_open'):
        return render(request, 'documents_gate.html', {'gate_form': DocumentGatekeeperForm()})

    documents = Document.objects.all()
    doc_form = DocumentForm()
    context = {
        'documents': documents,
        'doc_form': doc_form,
        'categories': documents.values_list('category', flat=True).distinct(),
    }
    return render(request, 'documents.html', context)


# ─── Profile CRUD ─────────────────────────────────────────────────────────────

@admin_required
def profile_update(request):
    if request.method == 'POST':
        profile = Profile.objects.first()
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return json_response(True, message='Profile updated successfully.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(False, message='Method not allowed.', status=405)


# ─── Skill CRUD ───────────────────────────────────────────────────────────────

@admin_required
def skill_create(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            return json_response(True, data={
                'id': skill.id, 'name': skill.name,
                'category': skill.get_category_display(),
                'proficiency': skill.proficiency, 'icon': skill.icon
            }, message='Skill added.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(False, message='Method not allowed.', status=405)


@admin_required
def skill_update(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return json_response(True, message='Skill updated.')
        return json_response(False, message=str(form.errors), status=400)
    # GET – return current data
    return json_response(True, data={
        'id': skill.id, 'name': skill.name, 'category': skill.category,
        'proficiency': skill.proficiency, 'icon': skill.icon, 'order': skill.order
    })


@admin_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        return json_response(True, message='Skill deleted.')
    return json_response(False, message='Method not allowed.', status=405)


# ─── SocialProfile CRUD ───────────────────────────────────────────────────────

@admin_required
def social_create(request):
    if request.method == 'POST':
        form = SocialProfileForm(request.POST)
        if form.is_valid():
            sp = form.save()
            return json_response(True, data={
                'id': sp.id, 'platform_name': sp.platform_name,
                'profile_url': sp.profile_url, 'icon_name': sp.icon_name,
                'username': sp.username, 'description': sp.description
            }, message='Profile added.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(False, message='Method not allowed.', status=405)


@admin_required
def social_update(request, pk):
    sp = get_object_or_404(SocialProfile, pk=pk)
    if request.method == 'POST':
        form = SocialProfileForm(request.POST, instance=sp)
        if form.is_valid():
            form.save()
            return json_response(True, message='Profile updated.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(True, data={
        'id': sp.id, 'platform_name': sp.platform_name,
        'profile_url': sp.profile_url, 'icon_name': sp.icon_name,
        'username': sp.username, 'description': sp.description, 'order': sp.order
    })


@admin_required
def social_delete(request, pk):
    sp = get_object_or_404(SocialProfile, pk=pk)
    if request.method == 'POST':
        sp.delete()
        return json_response(True, message='Profile deleted.')
    return json_response(False, message='Method not allowed.', status=405)


# ─── Project CRUD ─────────────────────────────────────────────────────────────

@admin_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            return json_response(True, data={
                'id': project.id, 'title': project.title,
                'image_url': project.image.url if project.image else '',
                'live_url': project.live_url,
            }, message='Project created.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(False, message='Method not allowed.', status=405)


@admin_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return json_response(True, message='Project updated.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(True, data={
        'id': project.id, 'title': project.title,
        'description': project.description,
        'short_description': project.short_description,
        'live_url': project.live_url, 'repo_url': project.repo_url,
        'tech_stack': project.tech_stack, 'featured': project.featured,
    })


@admin_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return json_response(True, message='Project deleted.')
    return json_response(False, message='Method not allowed.', status=405)


# ─── Note CRUD ────────────────────────────────────────────────────────────────

@admin_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save()
            return json_response(True, data={
                'id': note.id, 'title': note.title,
                'live_url': note.live_url,
                'has_file': bool(note.notes_file),
            }, message='Note added.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(False, message='Method not allowed.', status=405)


@admin_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return json_response(True, message='Note updated.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(True, data={
        'id': note.id, 'title': note.title, 'description': note.description,
        'live_url': note.live_url, 'tags': note.tags,
    })


@admin_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return json_response(True, message='Note deleted.')
    return json_response(False, message='Method not allowed.', status=405)


# ─── Document CRUD ────────────────────────────────────────────────────────────

@admin_required
def document_create(request):
    if not request.session.get('doc_gate_open'):
        return json_response(False, message='Document access not granted.', status=403)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            return json_response(True, data={
                'id': doc.id, 'title': doc.title,
                'file_url': doc.document_file.url,
                'extension': doc.file_extension(),
                'size': doc.file_size_display(),
                'category': doc.category,
            }, message='Document uploaded.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(False, message='Method not allowed.', status=405)


@admin_required
def document_update(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    if not request.session.get('doc_gate_open'):
        return json_response(False, message='Document access not granted.', status=403)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            return json_response(True, message='Document updated.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(True, data={
        'id': doc.id, 'title': doc.title,
        'description': doc.description, 'category': doc.category,
    })


@admin_required
def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    if not request.session.get('doc_gate_open'):
        return json_response(False, message='Document access not granted.', status=403)
    if request.method == 'POST':
        doc.delete()
        return json_response(True, message='Document deleted.')
    return json_response(False, message='Method not allowed.', status=405)


# ─── Footer CRUD ──────────────────────────────────────────────────────────────

@admin_required
def footer_update(request):
    if request.method == 'POST':
        footer = Footer.objects.first()
        form = FooterForm(request.POST, instance=footer)
        if form.is_valid():
            form.save()
            return json_response(True, message='Footer updated.')
        return json_response(False, message=str(form.errors), status=400)
    return json_response(False, message='Method not allowed.', status=405)


# ─── File Download ────────────────────────────────────────────────────────────

def download_document(request, pk):
    if not request.session.get('doc_gate_open'):
        return redirect('documents')
    doc = get_object_or_404(Document, pk=pk)
    try:
        response = FileResponse(open(doc.document_file.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(doc.document_file.name)}"'
        return response
    except FileNotFoundError:
        raise Http404('File not found.')


def download_project_zip(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not project.zip_file:
        raise Http404('No zip file for this project.')
    try:
        response = FileResponse(open(project.zip_file.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(project.zip_file.name)}"'
        return response
    except FileNotFoundError:
        raise Http404('File not found.')


def download_note_file(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if not note.notes_file:
        raise Http404('No file for this note.')
    try:
        response = FileResponse(open(note.notes_file.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(note.notes_file.name)}"'
        return response
    except FileNotFoundError:
        raise Http404('File not found.')
