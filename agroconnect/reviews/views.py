from django.shortcuts import render
from .models import Review

def review_list(request):
    # This view can display all reviews or reviews for a specific product.
    reviews = Review.objects.all()
    context = {'reviews': reviews}
    return render(request, 'reviews/review_list.html', context)
