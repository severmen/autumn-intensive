from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from .form import UsernameChat
from django.shortcuts import HttpResponse, render



class Index(FormView):
    form_class = UsernameChat
    template_name = "chat/index.html"
    success_url = "#"

    def form_valid(self, form):
       self.kwargs['username'] = self.request.POST.get('username')
       messages.add_message(self.request, messages.ERROR, 'Недопустимое имя полдзователя')
       return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('chat', kwargs={'nikname': self.kwargs.get('username')})

def chat(reques, nikname):
    context = {
        "nikname": nikname,
    }
    return render(reques, "chat/chat.html", context)