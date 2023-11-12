from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('all_transactions/',
         views.show_all_transactions, name="transactions"),
    path('day/', views.day, name="day"),

    path('add_transaction/', views.add_transaction, name="add_transaction"),

    path('edit_transaction/<str:id>',
         views.edit_transaction, name="edit_transaction"),

]
