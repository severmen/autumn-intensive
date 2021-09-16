from django import forms
from django.core.exceptions import ValidationError

from project.settings import mongoDB_services

class UsernameChat(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'text_form',
                                                             'placeholder':'Nikname'}))

    def clean(self):
        '''
        проверяет чтобы никнейм не был занят другим пользователем
        и чтобы длина была в диапазоне от 3 до 7 включительно
        '''
        cleaned_data = super().clean()
        if mongoDB_services.count_documents({"nickname": cleaned_data['username']}) != 0:
            raise ValidationError("Данное имя пользователя занято")

        if not(len(cleaned_data['username']) >= 3 and len(cleaned_data['username']) <= 7):
            raise ValidationError("Необходимая длина никнейма от 3 до 7 символов")
