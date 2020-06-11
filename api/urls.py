from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    path('register/', views.register, name='register-user'),
    path('login/', views.login, name='user-login'),
    path('logout/', views.logout, name='user-logout'),
    path('stories/', views.ComposeList.as_view(), name='stories'),
    path('stories/<int:pk>/', views.ComposeDetail.as_view(), name='stories_details'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search')
]
