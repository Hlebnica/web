from django.urls import include, path
from app import views

urlpatterns = [
    path('book/', views.BookListView.as_view(), name='index'),
    path('book/create/', views.create, name='create'),
    path('book/edit/<int:pk>/', views.edit, name='edit'),
    path('book/delete/<int:pk>/', views.delete, name='delete'),
    path('book/add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('book/cart/', views.cart, name='cart'),
    path('book/edit_user', views.edit_user, name='edit_user'),
    path('book/order_list', views.orders, name='orders'),
    path('book/login', views.logform, name='logform'),
    path('book/login/', views.login, name='login'),
    path('book/register', views.register, name='register'),
    path('book/check_login/', views.check_login, name='check_login'),
    path('book/check_email/', views.check_email, name='check_email'),
    path('book/check_password/', views.check_passwordlen, name='check_password'),
    path('book/logout', views.logout, name='logout'),
]
