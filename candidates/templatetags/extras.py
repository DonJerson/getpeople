from django import template
register = template.Library()

@register.inclusion_tag('candidates_view.html')
def show_logs(candidate):
    logs = candidate.log_set.all()
    return {'logs': logs}

