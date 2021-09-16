from django.template.defaulttags import register

@register.filter
def get_first_character(word):
    list_word = list(word)
    return list_word[0]
