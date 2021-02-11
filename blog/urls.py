from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('posts/', views.Posts, name='posts'),
    path('friends/', views.Friends_view, name='friends'),
    path('profile/<int:user_id>', views.Profile_view, name='profile'),
    path('profile/settings', views.Profile_settings, name="profile_settings"),
    path('logout/', views.Logout, name='logout'),
    path('remove_post/<int:id>', views.Remove_post, name='remove_post'),
]