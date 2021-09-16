from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from .form import UsernameChat
from django.shortcuts import HttpResponse, render

from .models import Message

from .templates_filter import get_first_character


class Index(FormView):
    form_class = UsernameChat
    template_name = "chat/index.html"
    success_url = "#"

    def form_valid(self, form):
       self.kwargs['username'] = self.request.POST.get('username')
       return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('chat', kwargs={'nickname': self.kwargs.get('username')})

def chat(reques, nickname):
    test_list = []
    last_messages2 = Message.objects.raw('SELECT * FROM chat_message ORDER BY -id limit 5')
    for a in reversed(last_messages2):
        test_list.append(a)




    context = {
        "nickname": nickname,
        "last_messages":test_list
    }
    return render(reques, "chat/chat.html", context)