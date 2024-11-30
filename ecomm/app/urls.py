from django.urls import path
from . views import *

app_name = "ecomm"
urlpatterns = [
    # common pages path
    path("",HomeView.as_view(),name="home"),
    path("about/",AboutView.as_view(),name="about"),
    path("contact_us/",ContactView.as_view(),name="contact"),
    path("all_products/",AllProductsView.as_view(),name="allproducts"),
    path("category/<str:cat>",CategoryView.as_view(),name="category"),
    path("product/<slug:slug>/",ProductDetailView.as_view(),name="productdetail"),
    path("add_to_cart-<int:pro_id>/",AddToCartView.as_view(),name="addtocart"),
    path("buy_now-<int:pro_id>/",BuyNowView.as_view(),name="buynow"),
    path("my-cart/",MyCartView.as_view(),name="mycart"),
    path("fav-products/",FavProductsView.as_view(),name="favproducts"),
    path("manage-cart/<int:cp_id>/",ManageCartView.as_view(),name="managecart"),
    path("empty-cart/",EmptyCartView.as_view(),name="emptycart"),
    path("checkout/",CheckoutView.as_view(),name="checkout"),
    path("search/",SearchView.as_view(), name="search"),
    # customer pages path
    path("register/", CustomerRegistrationView.as_view(), name="customerregistration"), 
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),
    path("my-orders/", MyOrdersView.as_view(), name="myorders"),
    path("my-order/order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),
    path("my-profile/", MyProfileView.as_view(), name="myprofile"),
    # seller pages path
    path("admin-login/", SellerLoginView.as_view(), name="adminlogin"),
    path("admin-home/", SellerHomeView.as_view(), name="adminhome"),
    path("admin-order/<int:pk>/", SellerOrderDetailView.as_view(), name="adminorderdetail"),
    path("admin-all-orders/", SellerOrderListView.as_view(), name="adminorderlist"),
    path("admin-order-<int:pk>-change/", SellerOrderStatusChangeView.as_view(), name="adminorderstatuschange"),
    path("change-password/", PasswordChangeView.as_view(), name="changepassword"),
    path("seller-change-password/", SellerPasswordChangeView.as_view(), name="changepassword"),
    path("seller-register/", SellerRegistrationView.as_view(), name="sellerregistration"), 
    path("add-product/", AddProductView.as_view(), name="addproduct"), 
    path("all-products/", AllProductView.as_view(), name="allproducts"), 
    path("seller-profile/", SellerProfileView.as_view(), name="sellerprofile"),
    path("update-product/", UpdateProductView.as_view(), name="updateproduct"),
]
