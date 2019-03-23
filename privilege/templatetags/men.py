from django import template

register = template.Library()

@register.inclusion_tag('men.html')
def get_menu(re):

    menu_list = re.session['men_list']

    return {'men_list':menu_list}

@register.inclusion_tag('username.html')
def get_user(re):

    user = re.session['username']
    print(user)
    return {'username':user}