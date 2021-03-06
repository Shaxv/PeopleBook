from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('friends/', views.Friends_view, name='friends'),
    path('profile/<int:user_id>', views.Profile_view, name='profile'),
    path('profile/settings', views.Profile_settings, name="profile_settings"),
    path('logout/', views.Logout, name='logout'),
    path('posts/settings/<int:id>', views.Post_settings, name='post_settings'),
    path('chat/<str:room_name>/', views.Room_view, name='chat_room'),
    path('chat/', views.Chat_view, name='chat'),
]
