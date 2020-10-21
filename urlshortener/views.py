from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from urlshortener.forms import LinkForm
from django.shortcuts import render, get_object_or_404
from .models import Link
# Create your views here.
def home(request):
    links = Link.objects.order_by("-click_count")[:20]
    return render(request, 'home.html', {'links': links})

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
    link.click_count += 1
    link.save()
    return HttpResponseRedirect(link.url)