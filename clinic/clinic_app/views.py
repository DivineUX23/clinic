from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):
    new_arrivals = Product.objects.filter(category='new_arrival')
    most_popular = Product.objects.filter(category='most_popular')
    return render(request, 'home.html', {
        'new_arrivals': new_arrivals,
        'most_popular': most_popular
    })

