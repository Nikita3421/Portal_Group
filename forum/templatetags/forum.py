from django import template

register = template.Library()


@register.filter(name="model_name")
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
    
@register.filter(name="is_voted")
def is_voted(voting,user):
    return voting.is_voted(user)

@register.filter(name="has_perms")
def has_perms(user,perms):
    if isinstance(perms, str):
        perms = (perms,)
    return user.has_perms(perms)


