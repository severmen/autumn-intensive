from django import forms


class UsernameChat(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'text_form',
                                                             'placeholder':'Nikname'}))

