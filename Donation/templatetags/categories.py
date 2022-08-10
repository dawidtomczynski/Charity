from django import template

register = template.Library()


@register.filter(name='categories')
def categories(arg):
    cat_list = []
    for cat in arg.categories.all():
        cat_list.append(cat.name)
    return ', '.join(cat_list)
