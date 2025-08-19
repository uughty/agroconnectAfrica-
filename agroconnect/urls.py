from django.contrib import admin
from django.urls import path, include
from .views import home 
from django.contrib.auth import views as auth_views
from . import views 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('agroconnect.users.urls')),
    path('api/products/', include(('agroconnect.products.urls', 'products'), namespace='products')),

    path('api/orders/', include('agroconnect.orders.urls')),
    path('api/reviews/', include('agroconnect.reviews.urls')),
    path('api/payments/', include('agroconnect.payments.urls')),
    path('', home, name='home'),  # Homepage route
      path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),


     path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path('', views.home, name='home'), 
    
     path('api/cart/', include('cart.urls')),

      

    
 


    

]
