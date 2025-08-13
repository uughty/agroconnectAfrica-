from django.contrib import admin
from django.urls import path, include
from .views import home  # Import your home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('agroconnect.users.urls')),
    path('api/products/', include('agroconnect.products.urls')),
    path('api/orders/', include('agroconnect.orders.urls')),
    path('api/reviews/', include('agroconnect.reviews.urls')),
    path('api/payments/', include('agroconnect.payments.urls')),
    path('', home, name='home'),  # Homepage route
     path('accounts/', include('allauth.urls')),
 


    

]
