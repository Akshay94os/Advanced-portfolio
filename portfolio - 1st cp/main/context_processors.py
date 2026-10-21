"""Context processors for global template variables."""
from .models import Profile, Footer


def global_context(request):
    """Inject global profile and footer data into all templates."""
    profile = Profile.objects.first()
    footer = Footer.objects.first()
    is_admin_logged_in = request.session.get('admin_logged_in', False)
    is_doc_gate_open = request.session.get('doc_gate_open', False)

    return {
        'global_profile': profile,
        'global_footer': footer,
        'is_admin_logged_in': is_admin_logged_in,
        'is_doc_gate_open': is_doc_gate_open,
    }
