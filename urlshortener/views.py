from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from urlshortener.permissions import IsOwnerOrReadOnly
from urlshortener.models import Link
from urlshortener.serializers import LinkSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import AnonymousUser, User
from django.http.response import HttpResponseRedirect
from urlshortener.forms import LinkForm
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.pagination import PageNumberPagination

class NumberPagination(PageNumberPagination):
    page_size = 10

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ['username', 'email', 'id']
    ordering = ['id']
    search_fields = ['username', 'email']
    filterset_fields = ['username', 'email']
    lookup_field = "username"
    template_name = 'user_detail.html'
    list_template_name = 'user_list.html'
    pagination_class = NumberPagination

    def get_template_names(self):
        if self.action == 'list':
            return [self.list_template_name]
        else:
            return [self.template_name]

    def get_object(self):
        username = self.kwargs.get('username')
        if username == "me":
            if type(self.request.user) is AnonymousUser:
                # Unsure of the best response to return here. Right now just returning a 404.
                raise NotFound
            else:
                return self.request.user
        return super(UserViewSet, self).get_object()


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [ IsOwnerOrReadOnly ]
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ['click_count', 'slug', 'owner', 'created_at']
    ordering = ['-click_count', 'owner']
    filterset_fields = ['owner']
    search_fields = ['slug', 'url', 'owner']
    lookup_field = 'slug'
    template_name = 'link_detail.html'
    list_template_name = 'link_list.html'
    pagination_class = NumberPagination


            
    def get_template_names(self):
        if self.action == 'list':
            return [self.list_template_name]
        else:
            return [self.template_name]

    def perform_create(self, serializer):
        if type(self.request.user) is AnonymousUser:
            serializer.save()
        else:
            serializer.save(owner=self.request.user)


def home(request):
    links = Link.objects.order_by("-click_count")[:20]
    serializer = LinkSerializer()
    return render(request, 'home.html', {'links': links, 'serializer': serializer})

def new_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            slug = form.cleaned_data['slug']
            return HttpResponseRedirect(f"/link/{slug}")
    else:
        form = LinkForm()
    return render(request, 'link_form.html', {'form': form})

def link_detail(request, slug):
    link = get_object_or_404(Link, slug=slug)
    return render(request, 'link.html', {'link': link})

def redirect_link(request, slug):
    link = get_object_or_404(Link, slug=slug)
    link.increment_clicks()
    return HttpResponseRedirect(link.url)
