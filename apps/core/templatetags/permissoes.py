from django import template

register = template.Library()


@register.filter
def has_perm(user, permissao):
    return user.has_permissao(permissao)
