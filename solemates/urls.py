"""
URL configuration for solemates project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from readApp import views
# from readApp.views import index
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.store,name="store"),
    # path('', index, name='index'),
    path('login/',views.Login_page,name="Login"),
    path('cart/login/',views.Login_page,name="Login"),
    path('checkout/login/',views.Login_page,name="Login"),
    path('logout/',views.logout_page,name="Logout"),
    path('register/',views.register,name="register"),
    path('cart/',views.cart,name="cart"), 
    path('checkout/',views.checkout,name="checkout"),
    path('admin/', admin.site.urls),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
