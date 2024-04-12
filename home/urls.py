from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("new/", views.create_post, name="new"),
    path("editpost/<int:post_id>", views.editpost, name="editpost"),
    path('mainhome/', views.home, name="mainhome"),
    path('particularcategory/<str:category_name>/', views.particularcategory, name='particularcategory'),
    path('userpost/', views.userpost, name="userpost"),
    path('specificpost/<int:post_id>', views.specificpost, name="specificpost"),
    path('generate-summary/', views.generate_summary, name='generate_summary'),
    path('generate-script/', views.generate_script, name='generate_script'),
    path('generate-blog/', views.generate_blog, name='generate_blog'),
    path('like_post/', views.like_post, name='like_post'),
    path('post/<int:post_id>/translate/', views.translate_post, name='translate_post'),
    path('index/', views.index_post, name='index'),
    path('create_anonymous_post/', views.create_anonymous_post, name='create_anonymous_post'),
    path('anonymous_post_list/', views.anonymous_post_list, name='anonymous_post_list'),
    path('anonymous_post_detail/<int:post_id>/', views.anonymous_post_detail, name='anonymous_post_detail'),
    path('call',views.read_text, name='call'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


