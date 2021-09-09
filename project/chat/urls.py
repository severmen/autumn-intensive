from django.urls import path,re_path, include
from .views import (Index,
                    chat
                    )

urlpatterns = [
    path("", Index.as_view()),
    path("chat/<str:nikname>/",chat, name = "chat" )
]
