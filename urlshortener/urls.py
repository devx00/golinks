from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.new_link, name='new-link'),
    path('link/<slug:slug>/', views.link_detail, name='link-detail'),
    path('<slug:slug>', views.redirect_link, name='link-redirect'),
]