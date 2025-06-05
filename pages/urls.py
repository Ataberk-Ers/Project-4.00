from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.homePage, name='forum'),
    path('new-question', views.newQuestionPage, name='new-question'),
    path('question/<int:id>', views.questionPage, name='question'),
    path('reply', views.replyPage, name='reply'),
    path('like/response/<int:response_id>/', views.like_response, name='like_response'),
]
