from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def has_permission(context, permission, obj=None):
    if obj is None:
        return context['user'].has_perm(permission)
    else:
        return context['user'].has_perm(permission, obj)
