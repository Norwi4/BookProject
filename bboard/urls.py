"""BookProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import index, add_post, my_posts, BbByRubricView, post_detail, BbEditView, BbDeleteView, profile_view, \
    AddResponse, update_profile

urlpatterns = [
    #path('me/', view_profile, name='me'),
    path('profile/<int:pk>/', profile_view, name='profile_view'),
    path('add/', add_post, name='add'),
    path('detail/<int:pk>/', post_detail, name='detail'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    #path('my_posts/', my_posts, name='my_posts'),
    path('response/<int:pk>/', AddResponse.as_view(), name='add_response'),
    path('update_profile/', update_profile, name='update_profile'),
    path('', index, name='index')
]