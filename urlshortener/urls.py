from urlshortener.views import LinkViewSet, UserViewSet, home, link_detail, new_link, redirect_link
from rest_framework.authtoken import views
from django.urls import path, include


user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

user_register = UserViewSet.as_view({
    'post': 'create'
})

link_list = LinkViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

link_detail = LinkViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('', home, name='home'),
    path('auth/', include('rest_framework.urls')),
    path('auth/token/', views.obtain_auth_token),
    path('auth/register/', user_register, name='register'),
    path('users/', user_list, name='user-list'),
    path('users/<str:username>/', user_detail, name='user-detail'),
    path('links/', link_list, name='link-list'),
    path('links/<slug:slug>/', link_detail, name='link-detail'),
    path('<slug:slug>', redirect_link, name='link-redirect'),
]
