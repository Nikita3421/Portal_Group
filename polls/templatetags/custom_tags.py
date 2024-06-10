from django import template

register = template.Library()

@register.filter(name="is_voted")
def is_voted(voting,user):
    return voting.is_voted(user)