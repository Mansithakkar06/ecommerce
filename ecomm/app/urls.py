from django.urls import path
from . views import *

app_name = "ecomm"
urlpatterns = [
    path("",HomeView.as_view(),name="home"),
    path("about/",AboutView.as_view(),name="about"),
    path("contact_us/",ContactView.as_view(),name="contact"),
    path("all_products/",AllProductsView.as_view(),name="allproducts"),
    #path("category/<slug:slug>/",CategoryView.as_view(),name="category"),
    path("product/<slug:slug>/",ProductDetailView.as_view(),name="productdetail"),
    path("add_to_cart-<int:pro_id>/",AddToCartView.as_view(),name="addtocart"),
    path("my-cart/",MyCartView.as_view(),name="mycart"),
    path("manage-cart/<int:cp_id>/",ManageCartView.as_view(),name="managecart"),
    path("empty-cart/",EmptyCartView.as_view(),name="emptycart"),
    path("checkout/",CheckoutView.as_view(),name="checkout"),
    path("register/", CustomerRegistrationView.as_view(), name="customerregistration"), 
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),
    path("search/",SearchView.as_view(), name="search"),
    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),
]
