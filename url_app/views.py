from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
from django.http import Http404

def shorten_url_view(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if not original_url:
            # Handle empty URL case
            return render(request, 'url_app/home.html', {'error': 'Please enter a URL.'})

        # Check if the URL already exists to prevent duplicates
        url_obj, created = URL.objects.get_or_create(original_url=original_url)

        short_url = request.build_absolute_uri(f'/{url_obj.short_code}/')
        
        return render(request, 'url_app/result.html', {'short_url': short_url})
    
    return render(request, 'url_app/home.html')

def redirect_url_view(request, short_code):
    try:
        url_obj = URL.objects.get(short_code=short_code)
        return redirect(url_obj.original_url)
    except URL.DoesNotExist:
        raise Http404("Short URL not found")