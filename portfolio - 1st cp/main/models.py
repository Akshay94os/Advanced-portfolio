"""Django models for the portfolio application."""
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    full_name = models.CharField(max_length=200, default='Akshay Subhash Borase')
    tagline = models.CharField(max_length=300, default='Full-Stack Developer & MCA Scholar')
    summary_intro = models.TextField(
        default='Hi, I am Akshay Subhash Borase, a Full-Stack Developer and MCA scholar at RCPET\'s IMRD, Shirpur.'
    )
    detail_intro = models.TextField(
        default=(
            'I am a passionate Full-Stack Developer and MCA scholar at RCPET\'s IMRD, Shirpur. '
            'In the software development process, I am deeply interested in designing scalable backend architectures & REST APIs '
            'and building automated system utilities.\n\n'
            'I specialize in backend development and web architectures using Python, Django, FastAPI, and SQL. '
            'I hold a 96% percentile rank in MCA CET and maintain a 9.15 current CGPA.\n\n'
            'I actively contribute to open-source projects, competitive coding, and modern UI engineering. '
            'My goal is to build robust, scalable systems that make a real difference.'
        )
    )
    intro_line1 = models.TextField(
        default='Hi, I am <strong>Akshay Subhash Borase</strong>, a Full-Stack Developer and MCA scholar at RCPET\'s IMRD, Shirpur.'
    )
    intro_line2 = models.TextField(
        default='In the software development process, I am deeply interested in <strong>designing scalable backend architectures & REST APIs</strong> and <strong>building automated system utilities</strong>.'
    )
    intro_line3 = models.TextField(
        default='I specialize in backend development and web architectures using <strong>Python, Django, FastAPI, and SQL</strong>.'
    )
    intro_line4 = models.TextField(
        default='I hold a <strong>96% percentile rank</strong> in MCA CET and maintain a <strong>9.15 current CGPA</strong>.'
    )
    intro_line5 = models.TextField(
        default='I actively contribute to <strong>open-source projects</strong>, competitive coding, and modern UI engineering.'
    )
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    contact_email = models.EmailField(default='akshayborase94@gmail.com')
    contact_phone = models.CharField(max_length=20, blank=True, default='')
    location = models.CharField(max_length=200, default='Shirpur, Maharashtra, India')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('language', 'Programming Language'),
        ('framework', 'Framework'),
        ('database', 'Database'),
        ('tool', 'Tool & Platform'),
        ('os', 'Operating System'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='language')
    proficiency = models.IntegerField(default=80, help_text='Proficiency 0-100')
    icon = models.CharField(max_length=100, blank=True, default='')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class SocialProfile(models.Model):
    platform_name = models.CharField(max_length=100)
    profile_url = models.URLField()
    icon_name = models.CharField(max_length=100, default='link', help_text='Font Awesome icon class or emoji')
    username = models.CharField(max_length=150, blank=True, default='')
    description = models.CharField(max_length=300, blank=True, default='')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'platform_name']

    def __str__(self):
        return f'{self.platform_name} - {self.username}'


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True, default='')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    live_url = models.URLField(blank=True, default='')
    repo_url = models.URLField(blank=True, default='')
    zip_file = models.FileField(upload_to='project_zips/', blank=True, null=True)
    tech_stack = models.CharField(max_length=500, blank=True, default='', help_text='Comma-separated technologies')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-created_at']

    def __str__(self):
        return self.title

    def get_tech_list(self):
        if self.tech_stack:
            return [t.strip() for t in self.tech_stack.split(',') if t.strip()]
        return []


class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, default='')
    live_url = models.URLField(blank=True, default='')
    notes_file = models.FileField(upload_to='notes/', blank=True, null=True)
    tags = models.CharField(max_length=300, blank=True, default='', help_text='Comma-separated tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Document(models.Model):
    title = models.CharField(max_length=200)
    document_file = models.FileField(upload_to='documents/')
    description = models.CharField(max_length=400, blank=True, default='')
    category = models.CharField(max_length=100, blank=True, default='General')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return self.title

    def file_extension(self):
        import os
        _, ext = os.path.splitext(self.document_file.name)
        return ext.lower().strip('.')

    def file_size_display(self):
        try:
            size = self.document_file.size
            if size < 1024:
                return f'{size} B'
            elif size < 1024 * 1024:
                return f'{size/1024:.1f} KB'
            else:
                return f'{size/1024/1024:.1f} MB'
        except Exception:
            return 'Unknown'


class Footer(models.Model):
    copyright_text = models.CharField(max_length=300, default='© 2024 Akshay Subhash Borase. All rights reserved.')
    tagline = models.CharField(max_length=300, default='Crafting scalable solutions, one line at a time.')
    contact_email = models.EmailField(default='akshayborase94@gmail.com')
    contact_phone = models.CharField(max_length=20, blank=True, default='')
    address = models.CharField(max_length=300, blank=True, default='Shirpur, Maharashtra, India')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Footer'

    def __str__(self):
        return 'Footer Settings'
