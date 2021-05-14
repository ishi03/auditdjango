from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.loginPage, name="login"),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('register/', views.registerPage, name="register"),
	path('logout/', views.logoutUser, name="logout"),

	path('update_item/', views.updateItem, name="update_item"),
	# path('process_order/', views.processOrder, name="process_order"),

	path('description/<str:pk>/', views.description, name="description"),

]