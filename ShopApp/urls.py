from.import views
from django.urls import path
urlpatterns = [
   path('base/',views.base,name='base'),
   path('',views.index,name='index'),
   path('product/',views.product,name='product'),
   path('search/',views.search,name='search'),
   path('product/<str:id>', views.product_details_page, name='product_detalis'),
   path('contact/',views.contact,name='contact'),
   ##############LOGIN###########
   
   path('login/',views.login,name='login'),

   path('logout/', views.logout,name='logout'),
   path('register/',views.register,name='register'),

   #############CART#######
#    path('cart/',views.cart,name='cart'),


###CART PATH

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),



#####CHECKOut PAGE##########
    path('cart/checkout/',views.checkout,name='checkout'),

###########PALCE ORDER
    path('cart/placeorder/',views.placeorder,name='placeorder'),
 ]

