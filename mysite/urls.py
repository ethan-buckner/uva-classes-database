from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
   path('admin/', admin.site.urls),
   path("accounts/", include("allauth.urls")), #most important
   path('', include("louslist.urls")), #my app urls
   path('logout', LogoutView.as_view()),
   #path('classes/',include("louslist.urls"))
]
