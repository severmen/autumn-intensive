
from django.urls import reverse_lazy
from django.views.generic import FormView
from .form import UsernameChat
from django.shortcuts import HttpResponse, render
from .models import Message

from .templates_filter import get_first_character


class Index(FormView):
    '''
    вывод главной страницы
    '''
    form_class = UsernameChat
    template_name = "chat/index.html"
    success_url = "#"

    def form_valid(self, form):
       '''
            Форма прошла все проверки записавет никнейм
             чтобы перенаправить его
       '''
       self.kwargs['username'] = self.request.POST.get('username')
       return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('chat', kwargs={'nickname': self.kwargs.get('username')})

def chat(reques, nickname):
    '''
    страница чата
    '''
    last_messages = []
    last_messages_from_DB = Message.objects.raw('SELECT * FROM chat_message ORDER BY -id limit 10')

    for a in reversed(last_messages_from_DB):
        '''
        переварачивает список чтобы более нолвые сообщение были внизу
        '''
        last_messages.append(a)
    context = {
        "nickname": nickname,
        "last_messages":last_messages
    }
    return render(reques, "chat/chat.html", context)