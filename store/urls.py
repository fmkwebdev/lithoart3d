from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('pay/', views.pay, name="pay"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('confirmation_page/', views.confirmation_page, name="confirmation_page"),
    path('confirmation_page_sr/', views.confirmation_page_sr, name="confirmation_page_sr"),
	path('complete/', views.paymentComplete, name="complete"),
    path('confirmation_success/', views.confirmation_success, name='confirmation_success'),
    path('unauthorized/', views.unauthorized, name="unauthorized"),
    path('sr', views.storesr, name="sr"),
    path('sr/cart', views.cartsr, name="cartsr"),
    path('sr/checkout/', views.checkoutsr, name="checkoutsr")
]