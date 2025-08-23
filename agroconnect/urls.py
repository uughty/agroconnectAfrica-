# agroconnect/urls.py

from django.contrib import admin
from django.urls import path, include
from agroconnect.users.views import home, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users app routes
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/', include('agroconnect.users.urls')),  # register, dashboard, verify

    # API routes
    path('api/users/', include('agroconnect.users.urls')),
    path('api/products/', include(('agroconnect.products.urls', 'products'), namespace='products')),
    path('api/orders/', include('agroconnect.orders.urls')),
    path('api/reviews/', include('agroconnect.reviews.urls')),
    path('api/payments/', include('agroconnect.payments.urls')),
  


    # Homepage
    path('', home, name='home'),
]
