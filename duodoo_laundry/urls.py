"""
URL configuration for duodoo_laundry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path , reverse
from django.shortcuts import redirect


def my_view(request):
    url = reverse('order_list')
    return redirect(url)

base_urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/' , include('UserManagement.urls')),
    path('services/' , include('ServiceManagement.urls')),
    path('orders/' , include('OrderManagement.urls')),
    path('finance/' , include('FinanceManagement.urls')),
    path('' , include('Core.urls'))
]



from django.conf.urls.static import static
from django.conf import settings

urlpatterns = base_urlpatterns + [path('i18n/', include('django.conf.urls.i18n'))] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)