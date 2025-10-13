from django.urls import path
from . import views

app_name = 'food'

urlpatterns = [
    # ---------------------- MAIN PAGES ----------------------
    path('', views.main_page, name='main'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact'),

    # ---------------------- AUTH ----------------------
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),

    # ---------------------- ADMIN ----------------------
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_food/', views.add_food, name='add_food'),
    path('edit_food/<int:food_id>/', views.edit_food, name='edit_food'),
    path('delete_food/<int:food_id>/', views.delete_food, name='delete_food'),
    path('mark_gallery_done/<int:order_id>/', views.mark_gallery_done, name='mark_gallery_done'),


    # ---------------------- ORDERS ----------------------
    path('order/<int:item_id>/', views.order_page, name='order_page'),
    path('mark_done/<int:order_id>/', views.mark_done, name='mark_done'),
    path('order/mark_completed/<int:order_id>/', views.mark_order_completed, name='mark_order_completed'),

    # ---------------------- GALLERY ----------------------
    path('add_gallery/', views.add_gallery, name='add_gallery'),
    path('delete_gallery/<int:id>/', views.delete_gallery, name='delete_gallery'),
    path('gallery_order/<int:item_id>/', views.gallery_order_page, name='gallery_order'),

    # ---------------------- CHECKOUT & PAYMENT ----------------------
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('order_success/',views.order_sucess,name='order_success'),

    path('feedback/',views.feedback,name='feedback')
]
