from django.template.defaulttags import register

@register.filter
def get_first_character(word):
    '''
    возврощает первый символ слова
    нужан для одобращение логи в чате
    '''
    list_word = list(word)
    return list_word[0]
