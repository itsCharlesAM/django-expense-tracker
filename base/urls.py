from django.urls import path

from . import views

urlpatterns = [

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

    path('', views.home, name="home"),
    path('all_transactions/',
         views.show_all_transactions, name="transactions"),
    path('day/', views.day, name="day"),

    path('add_transaction/', views.add_transaction, name="add_transaction"),

    path('edit_transaction/<str:id>',
         views.edit_transaction, name="edit_transaction"),

    path('delete_transaction/<str:id>',
         views.delete_transaction, name="delete_transaction"),
]
