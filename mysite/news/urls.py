from django.urls import path
# from django.contrib.auth import views as auth_views
from . import  views
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('',detect_news, name="detect_news"),
    path('feedback/',news_feedback, name="feedback"),
    path('login',views.login_view, name='login'),
    path('logout',views.logout,name='logout'),
    path('signup/', views.signup_view , name= "signup"),
    path('follow',follow ,name='follow'),
    path('details/<int:id>',details ,name='details'),
    path('feed_model',feed_model ,name='feed_model'),
    path('upload',upload_csv, name='upload'),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns 