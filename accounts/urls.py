from accounts import views as user_views
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path('login/', user_views.login_view,name='login_view'),
    path('profile/', user_views.user_profile, name='profile'),
    path('userupdate/', user_views.user_update, name='userupdate'),
    path('logout/', user_views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)