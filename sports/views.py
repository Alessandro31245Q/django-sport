from datetime import datetime, timedelta, timezone
import json
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from sports.models import STATUS_CHOICES, Category, Court, SportRating
from django.db.models import Q

def sport_by_category(request, category_id):
    sports = Court.objects.filter(status='Disponible',category=category_id)
    #category = Category.objects.get(pk=category_id)
    # category = get_object_or_404(Category, pk=category_id)

    try:
        category = Category.objects.get(pk=category_id)
    except:
        return redirect('home')

    context = {
        'sports' : sports,
        'category' : category,
    }

    return render(request, 'sport_by_category.html', context)

def sports(request, slug):
    try:
        single_sport = Court.objects.get(slug=slug)
    except Court.DoesNotExist:
        return redirect('home')

    user_rating = None
    user_comment = ""  
    if request.user.is_authenticated:

        user_rating = SportRating.objects.filter(user=request.user, court=single_sport).first()
        if user_rating:
            user_comment = user_rating.comment

    if request.method == 'POST' and 'rating' in request.POST:
        score = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '').strip()

   
        if user_rating:
            user_rating.score = score
            user_rating.comment = comment
            user_rating.save()
        else:
            SportRating.objects.create(user=request.user, court=single_sport, score=score, comment=comment)

        return redirect('sports', slug=slug)

    
    all_ratings = SportRating.objects.filter(court=single_sport).order_by('-created_at')

    return render(request, 'sports.html', {
        'single_sport': single_sport,
        'user_rating': user_rating,
        'all_ratings': all_ratings,
        'user_comment': user_comment  
    })

def search(request):
    keyword = request.GET.get('keyword')

    courts = Court.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(sport_body__icontains=keyword))

    context = {
        'courts' : courts,
        'keyword' : keyword
    } 

    return render(request, 'search.html', context)

@login_required(login_url='/') 
def sports_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    categories = Category.objects.all() 
    return render(request, 'sports_list.html', {'categories': categories})
        

@login_required(login_url='/') 
def create_category(request):
    if not request.user.is_superuser:  
        return redirect('home')
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(category_name=category_name)  
            return redirect('sports_list')  
    return render(request, 'create_category.html')

@login_required(login_url='/') 
def update_category(request, category_id):
    if not request.user.is_superuser:
        return redirect('home')
    category = get_object_or_404(Category, id=category_id)  

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            category.category_name = category_name
            category.save() 
            return redirect('sports_list')

    return render(request, 'update_category.html', {'category': category})
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)  
    category.delete()  
    return redirect('sports_list')

@login_required(login_url='/') 
def court_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    courts = Court.objects.all() 
    return render(request, 'court_list.html', {'courts': courts})

@login_required(login_url='/') 
def create_court(request):
    if not request.user.is_superuser:
        return redirect('home')

    with open('Barrios_de_Cartagena.geojson', 'r') as f:
        data = json.load(f)

    barrios = [feature['properties']['NOMBRE'] for feature in data['features']]

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        featured_image = request.FILES.get('featured_image')
        short_description = request.POST.get('short_description')
        sport_body = request.POST.get('sport_body')
        status = request.POST.get('status')
        barrio = request.POST.get('barrio')
        is_featured = request.POST.get('is_featured') == 'on'

        slug = slugify(title)

        category = Category.objects.get(id=category_id)

        Court.objects.create(
            title=title,
            slug=slug,
            category=category,
            owner=request.user,
            featured_image=featured_image,
            short_description=short_description,
            sport_body=sport_body,
            status=status,
            barrio=barrio,
            is_featured=is_featured
        )

        return redirect('court_list')

    categories = Category.objects.all()

    return render(request, 'create_court.html', {
        'categories': categories,
        'court_status_choices': STATUS_CHOICES,
        'barrios': barrios,  
    })

@login_required(login_url='/') 
def update_court(request, court_id):
    if not request.user.is_superuser:
        return redirect('home')

    court = get_object_or_404(Court, id=court_id, owner=request.user)

    with open('Barrios_de_Cartagena.geojson', 'r') as f:
        data = json.load(f)
    barrios = [feature['properties']['NOMBRE'] for feature in data['features']]

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        featured_image = request.FILES.get('featured_image')
        short_description = request.POST.get('short_description')
        sport_body = request.POST.get('sport_body')
        status = request.POST.get('status')
        barrio = request.POST.get('barrio')
        is_featured = request.POST.get('is_featured') == 'on'

        court.title = title
        court.slug = slugify(title) 
        court.category = Category.objects.get(id=category_id)
        if featured_image:
            court.featured_image = featured_image  
        court.sport_body = sport_body
        court.status = status
        court.barrio = barrio
        court.is_featured = is_featured

        court.save()

        return redirect('court_list')

    categories = Category.objects.all()

    return render(request, 'update_court.html', {
        'court': court,
        'categories': categories,
        'court_status_choices': STATUS_CHOICES,
        'barrios': barrios,
    })

@login_required
def delete_court(request, court_id):
    court = get_object_or_404(Court, id=court_id)
    court.delete()
    return redirect('court_list') 
