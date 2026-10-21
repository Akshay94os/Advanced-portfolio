"""Forms for the portfolio application."""
from django import forms
from .models import Profile, Skill, SocialProfile, Project, Note, Document, Footer


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'tagline', 'intro_line1', 'intro_line2',
            'intro_line3', 'intro_line4', 'intro_line5',
            'detail_intro', 'profile_image', 'resume_file',
            'contact_email', 'contact_phone', 'location'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tagline'}),
            'intro_line1': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Intro line 1'}),
            'intro_line2': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Intro line 2'}),
            'intro_line3': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Intro line 3'}),
            'intro_line4': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Intro line 4'}),
            'intro_line5': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Intro line 5'}),
            'detail_intro': forms.Textarea(attrs={'class': 'form-input', 'rows': 6, 'placeholder': 'Full bio / detail intro'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Location'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'proficiency', 'icon', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Python'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'proficiency': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 100}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 🐍 or fab fa-python'}),
            'order': forms.NumberInput(attrs={'class': 'form-input'}),
        }


class SocialProfileForm(forms.ModelForm):
    class Meta:
        model = SocialProfile
        fields = ['platform_name', 'profile_url', 'icon_name', 'username', 'description', 'order']
        widgets = {
            'platform_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. GitHub'}),
            'profile_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'icon_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'fab fa-github'}),
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '@username'}),
            'description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Short description'}),
            'order': forms.NumberInput(attrs={'class': 'form-input'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'short_description', 'image', 'live_url', 'repo_url', 'zip_file', 'tech_stack', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'Full project description'}),
            'short_description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Short summary (max 300 chars)'}),
            'live_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://live-demo.com'}),
            'repo_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://github.com/...'}),
            'tech_stack': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Python, Django, PostgreSQL'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'live_url', 'notes_file', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Note Title'}),
            'description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Short description'}),
            'live_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'tags': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Python, Tutorial, Notes'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_file', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Document Title'}),
            'description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Short description'}),
            'category': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Academic, Certificate'}),
        }


class FooterForm(forms.ModelForm):
    class Meta:
        model = Footer
        fields = ['copyright_text', 'tagline', 'contact_email', 'contact_phone', 'address']
        widgets = {
            'copyright_text': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '© 2024 Your Name'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your tagline'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
        }


class AdminLoginForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Admin Password', 'id': 'admin-password-input'}),
        label='Admin Password'
    )


class DocumentGatekeeperForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address', 'id': 'gate-email-input'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password', 'id': 'gate-password-input'}),
        label='Password'
    )
