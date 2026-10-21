"""
seed_data.py – Auto-seed script for Akshay Borase's portfolio.
Run with: python seed_data.py
(Must be run from the portfolio project root where manage.py lives)
"""
import os
import sys
import shutil
import django

# ── Django setup ─────────────────────────────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings
from main.models import Profile, Skill, SocialProfile, Footer, Document

BASE_DIR = settings.BASE_DIR
MEDIA_DOCS = settings.MEDIA_ROOT / 'documents'
MEDIA_PROFILE = settings.MEDIA_ROOT / 'profile'
MEDIA_RESUME  = settings.MEDIA_ROOT / 'resume'

# ── Ensure media dirs ─────────────────────────────────────────────────────────
for d in [MEDIA_DOCS, MEDIA_PROFILE, MEDIA_RESUME]:
    d.mkdir(parents=True, exist_ok=True)
print("✓ Media directories ready.")

# ── 1. Profile ────────────────────────────────────────────────────────────────
if not Profile.objects.exists():
    profile = Profile.objects.create(
        full_name='Akshay Subhash Borase',
        tagline='Full-Stack Developer & MCA Scholar',
        summary_intro='Hi, I am Akshay Subhash Borase, a Full-Stack Developer and MCA scholar at RCPET\'s IMRD, Shirpur.',
        intro_line1='Hi, I am <strong>Akshay Subhash Borase</strong>, a Full-Stack Developer and MCA scholar at RCPET\'s IMRD, Shirpur.',
        intro_line2='In the software development process, I am deeply interested in <strong>designing scalable backend architectures & REST APIs</strong> and <strong>building automated system utilities</strong>.',
        intro_line3='I specialize in backend development and web architectures using <strong>Python, Django, FastAPI, and SQL</strong>.',
        intro_line4='I hold a <strong>96% percentile rank</strong> in MCA CET and maintain a <strong>9.15 current CGPA</strong>.',
        intro_line5='I actively contribute to <strong>open-source projects</strong>, competitive coding, and modern UI engineering.',
        detail_intro=(
            'I am a passionate Full-Stack Developer and MCA scholar at RCPET\'s IMRD, Shirpur.\n\n'
            'In the software development process, I am deeply interested in designing scalable backend architectures & REST APIs '
            'and building automated system utilities.\n\n'
            'I specialize in backend development and web architectures using Python, Django, FastAPI, and SQL. '
            'I hold a 96% percentile rank in MCA CET and maintain a 9.15 current CGPA.\n\n'
            'I actively contribute to open-source projects, competitive coding, and modern UI engineering. '
            'I believe in writing clean, maintainable code and building systems that scale. '
            'My goal is to bridge the gap between robust backend systems and beautiful frontend experiences.'
        ),
        contact_email='akshayborase94@gmail.com',
        location='Shirpur, Maharashtra, India',
    )
    print("✓ Profile created.")

    # Copy profile photo if exists
    src_photo = BASE_DIR / 'my profile photo.jpeg'
    if src_photo.exists():
        dest = MEDIA_PROFILE / 'profile_photo.jpeg'
        shutil.copy2(src_photo, dest)
        profile.profile_image = 'profile/profile_photo.jpeg'

    # Copy resume.pdf if exists
    src_resume = BASE_DIR / 'resume.pdf'
    if src_resume.exists():
        dest = MEDIA_RESUME / 'resume.pdf'
        shutil.copy2(src_resume, dest)
        profile.resume_file = 'resume/resume.pdf'

    profile.save()
    print("  → Profile photo & resume linked." if src_photo.exists() else "  → No profile photo found, skipping.")
else:
    print("✓ Profile already exists, skipping.")

# ── 2. Skills ─────────────────────────────────────────────────────────────────
SKILLS = [
    {'name': 'Python',          'category': 'language',  'proficiency': 90, 'icon': '🐍', 'order': 1},
    {'name': 'Django',          'category': 'framework', 'proficiency': 88, 'icon': '🎸', 'order': 2},
    {'name': 'FastAPI',         'category': 'framework', 'proficiency': 80, 'icon': '⚡', 'order': 3},
    {'name': 'SQL',             'category': 'database',  'proficiency': 85, 'icon': '🗄️', 'order': 4},
    {'name': 'PostgreSQL',      'category': 'database',  'proficiency': 78, 'icon': '🐘', 'order': 5},
    {'name': 'HTML',            'category': 'language',  'proficiency': 85, 'icon': '🌐', 'order': 6},
    {'name': 'Linux Command',   'category': 'os',        'proficiency': 75, 'icon': '🐧', 'order': 7},
    {'name': 'Shell Scripting', 'category': 'tool',      'proficiency': 70, 'icon': '💻', 'order': 8},
]

if not Skill.objects.exists():
    for s in SKILLS:
        Skill.objects.create(**s)
    print(f"✓ {len(SKILLS)} skills seeded.")
else:
    print("✓ Skills already exist, skipping.")

# ── 3. Social Profiles ────────────────────────────────────────────────────────
SOCIALS = [
    {
        'platform_name': 'GitHub',
        'profile_url': 'https://github.com/Akshay94os/',
        'icon_name': 'fab fa-github',
        'username': 'Akshay94os',
        'description': 'Open-source projects & code repositories',
        'order': 1,
    },
    {
        'platform_name': 'LinkedIn',
        'profile_url': 'https://linkedin.com/in/akshay-borase-41a028262',
        'icon_name': 'fab fa-linkedin',
        'username': 'akshay-borase-41a028262',
        'description': 'Professional network & career updates',
        'order': 2,
    },
    {
        'platform_name': 'Instagram',
        'profile_url': 'https://www.instagram.com/official_akshay_xd/',
        'icon_name': 'fab fa-instagram',
        'username': 'official_akshay_xd',
        'description': 'Personal life & creative moments',
        'order': 3,
    },
]

if not SocialProfile.objects.exists():
    for sp in SOCIALS:
        SocialProfile.objects.create(**sp)
    print(f"✓ {len(SOCIALS)} social profiles seeded.")
else:
    print("✓ Social profiles already exist, skipping.")

# ── 4. Footer ─────────────────────────────────────────────────────────────────
if not Footer.objects.exists():
    Footer.objects.create(
        copyright_text='© 2024 Akshay Subhash Borase. All rights reserved.',
        tagline='Crafting scalable solutions, one line at a time.',
        contact_email='akshayborase94@gmail.com',
        address='Shirpur, Maharashtra, India',
    )
    print("✓ Footer created.")
else:
    print("✓ Footer already exists, skipping.")

# ── 5. Documents from ./documents folder ─────────────────────────────────────
src_docs = BASE_DIR / 'documents'

# Category mapping based on file names
def guess_category(filename: str) -> str:
    fn = filename.lower()
    if any(x in fn for x in ['10th','ssc','hsc','12th','degree','marksheet','ty','sybsc']): return 'Academic'
    if any(x in fn for x in ['caste','income','domicile','nationality','validity','non-cre','non.']): return 'Certificate'
    if any(x in fn for x in ['adhar','maha','pan']): return 'ID Proof'
    if any(x in fn for x in ['admit','score','cet']): return 'Competitive Exam'
    if any(x in fn for x in ['cv','resume']): return 'Resume/CV'
    if any(x in fn for x in ['bonafied','affidavit','afidevite','fee','leaving','tc']): return 'College Docs'
    if any(x in fn for x in ['photo','pass','icard']): return 'Photos'
    return 'General'

if src_docs.exists() and not Document.objects.exists():
    added = 0
    for fname in sorted(src_docs.iterdir()):
        if fname.is_file() and not fname.name.startswith('~'):
            # Copy to media/documents
            dest = MEDIA_DOCS / fname.name
            try:
                if not dest.exists():
                    shutil.copy2(fname, dest)
                cat = guess_category(fname.name)
                # Clean title from filename
                title = fname.stem.replace('_', ' ').replace('-', ' ').title()
                Document.objects.create(
                    title=title,
                    document_file=f'documents/{fname.name}',
                    category=cat,
                    description=f'Imported from local documents folder',
                )
                added += 1
            except Exception as ex:
                print(f"  ⚠ Skipped {fname.name}: {ex}")
    print(f"✓ {added} documents imported from ./documents folder.")
else:
    if not src_docs.exists():
        print("⚠ ./documents folder not found, skipping document import.")
    else:
        print("✓ Documents already exist, skipping import.")

print("\n🎉 Seed complete! Run: py manage.py runserver")
