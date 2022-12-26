from django.urls import path

from . import views

# Namespacing URL names
app_name = 'polls'
urlpatterns = [ 
    # path('', views.index, name='index'),
    # path('<int:question_id>/detail/', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),    
    path('<int:question_id>/vote/', views.vote, name='vote'),
    
    # Generic views
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
]