import paypalrestsdk
from typing import Any
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import View,TemplateView,CreateView, FormView, DetailView, ListView, View
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CheckoutForm, CustomerRegistrationForm, CustomerLoginForm, PasswordChangeForm, SellerRegistrationForm #UserProfileForm
from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import logging




# common pages
class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
    


class HomeView(EcomMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list']=Product.objects.all().order_by("-id")
        if self.request.COOKIES.get("messages_shown"):
            
            messages.get_messages(self.request).used = True  # Clear messages
            self.request.COOKIES.pop("messages_shown", None)
            
        return context
        
    
    def post(self,request):
        
        pId = request.POST.get('pid')
        
        product_obj = Product.objects.get(id=pId)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product = product_obj)
            #item already exists in cart
            if this_product_in_cart.exists():
                
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                
                cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            messages.success(self.request, 'Your action was successful!')
        else:
            
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            
        response = redirect("/")
        response.set_cookie("messages_shown", True, max_age=2)
        
        return response 

class CategoryView(EcomMixin,TemplateView):
    template_name="category.html"

    def get_context_data(self,**kwargs):
        cat = kwargs['cat']
        cat = cat.replace('-',' ')
        category = Category.objects.get(title=cat)
        products = Product.objects.filter(category=category)
        context = {}
        context['products'] = products
        context['cat'] = category
        
        if self.request.COOKIES.get("messages_shown"):
            messages.get_messages(self.request).used = True  # Clear messages
            self.request.COOKIES.pop("messages_shown", None)
        return context
        
    
    def post(self,request,**kwargs):
        
        pId = request.POST.get('pid')
        
        cat = kwargs['cat']
        cat = cat.replace('-','')
        
        product_obj = Product.objects.get(id=pId)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product = product_obj)
            #item already exists in cart
            if this_product_in_cart.exists():
                
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                
                cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            messages.success(self.request, 'Your action was successful!')
        else:
            
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            
        response = redirect(f"/category/{cat}")
        response.set_cookie("messages_shown", True, max_age=2)
        
        return response 
    
    
class AllProductsView(EcomMixin, TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        
        if self.request.COOKIES.get("messages_shown"):
            messages.get_messages(self.request).used = True  # Clear messages
            self.request.COOKIES.pop("messages_shown", None)
            
        return context
    
    def post(self,request):
        
        pId = request.POST.get('pid')
        
        product_obj = Product.objects.get(id=pId)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product = product_obj)
            #item already exists in cart
            if this_product_in_cart.exists():
                
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                
                cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            messages.success(self.request, 'Your action was successful!')
        else:
            
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            
        response = redirect("/all_products")
        response.set_cookie("messages_shown", True, max_age=2)
        
        return response        
            
        

class ProductDetailView(EcomMixin, TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         url_slug = self.kwargs['slug']
         product = Product.objects.get(slug= url_slug)
         product.view_count += 1
         product.save()
         context['product'] = product
         
         if self.request.COOKIES.get("messages_shown"):
            messages.get_messages(self.request).used = True  # Clear messages
            self.request.COOKIES.pop("messages_shown", None)

        # Pass a boolean indicating if the product is a favorite
         if self.request.user.is_authenticated and hasattr(self.request.user, 'customer'):
            context['is_favorite'] = Favorite.objects.filter(
                customer=self.request.user.customer,
                product=product
            ).exists()
         else:
            context['is_favorite'] = False

         return context
     
    def post(self,request,**kwargs):
        
        pId = request.POST.get('pid')
        
        product_obj = Product.objects.get(id=pId)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product = product_obj)
            #item already exists in cart
            if this_product_in_cart.exists():
                
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                
                cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            messages.success(self.request, 'Your action was successful!')
        else:
            
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            
        response = redirect(f"/product/{product_obj.slug}/")
        response.set_cookie("messages_shown", True, max_age=2)
        
        return response 
    
class AddToCartView(EcomMixin, TemplateView):
    template_name = "addtocart.html"
    
    def get_success_url(self):
        print("in get url")
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            print("working")
            return next_url
        else:
            return self.success_url
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #get product id from requested url
        product_id = self.kwargs['pro_id']
        #get product
        product_obj = Product.objects.get(id=product_id)
        #check if cart exists
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product = product_obj)
            #item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            #new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
                messages.success(self.request, 'Your action was successful!')
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            

        #check if product already exists in cart
        
        # if "next" in self.request.GET:
        #     next_url = self.request.GET.get("next")
        #     print("working")
        #     return next_url
        # else:
        #     return context
        
        return context

class BuyNowView(EcomMixin,TemplateView):
     template_name = "buynow.html"
    
     def get_success_url(self):
        print("in get url")
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            print("working")
            return next_url
        else:
            return self.success_url
    

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #get product id from requested url
        product_id = self.kwargs['pro_id']
        #get product
        product_obj = Product.objects.get(id=product_id)
        #check if cart exists
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product = product_obj)
            #item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            #new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
                messages.success(self.request, 'Your action was successful!')
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj, rate = product_obj.selling_price, quantity = 1, subtotal = product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            

        #check if product already exists in cart
        
        # if "next" in self.request.GET:
        #     next_url = self.request.GET.get("next")
        #     print("working")
        #     return next_url
        # else:
        #     return context
        
        return context
     
class ToggleFavoriteView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'customer'):
            return JsonResponse({"success": False, "message": "Login required"}, status=401)

        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        customer = request.user.customer

        favorite, created = Favorite.objects.get_or_create(customer=customer, product=product)

        if not created:  # Already favorited, so remove it
            favorite.delete()
            return JsonResponse({"success": True, "message": "Removed from favorites"})

        return JsonResponse({"success": True, "message": "Added to favorites"})
    
class FavoriteProductsView(EcomMixin, TemplateView):
    template_name = "toggle_favorite.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'customer'):
            # Get all favorite products for the logged-in user
            favorites = Favorite.objects.filter(customer=self.request.user.customer)
            context['favorites'] = favorites  # Pass the favorite objects to the template
        return context



class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        print("this manage cart section")
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("ecomm:mycart")

class EmptyCartView(EcomMixin, View):
    def get(self,request,*args,**kwargs):
        cart_id = request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecomm:mycart")
    
class MyCartView(EcomMixin, TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context
class FavProductsView(EcomMixin,TemplateView):
    template_name="favproducts.html"
    
class CheckoutView(EcomMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    
    success_url = reverse_lazy("ecomm:home")
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)
        
    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            initial['ordered_by'] = customer.full_name
            initial['shipping_address'] = customer.address
            initial['mobile'] = customer.mobile
            initial['email'] = self.request.user.email
        return initial
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context
    
    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']

        else:
            return redirect("ecomm:home")
        return super().form_valid(form)
 
 
class SearchView(TemplateView):
    template_name="search.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        kw=self.request.GET.get("keyword")
        results=Product.objects.filter(Q(title__icontains=kw)| Q(description__icontains=kw) | Q(return_policy__icontains=kw))
        print(results)
        context["results"]=results
        return context


class AboutView(EcomMixin, TemplateView):
    template_name = "about.html"

class ContactView(EcomMixin, TemplateView):
    template_name = "contactus.html"



# customer pages

class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomm:home")
    
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username,email,password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomm:home")
    
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form":self.form_class, "error": "Invalid credentials"})
        
        return super().form_valid(form)
    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomm:home")


class PasswordChangeView(FormView):
    template_name = "changepassword.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("ecomm:home")
    
    def form_valid(self, form):
        old = form.cleaned_data["oldpassword"]
        new = form.cleaned_data["newpassword"]
        confirm = form.cleaned_data["confirmpassword"]
        print(old, new, confirm)
        print("***Session user*****",self.request.user.password)
        checkhash = check_password(old, self.request.user.password)
        print(checkhash)
        try:
            if checkhash:
                cstmr = Customer.objects.get(user=self.request.user)
                print("Inside Try")
            else:
                cstmr = None
        except:
            cstmr = None
            print("Inside Except")
        if new == confirm and cstmr is not None:
            loggeduser = User.objects.get(username=self.request.user.username, password=self.request.user.password)
            loggeduser.password = make_password(new)
            loggeduser.save()
            return redirect ("ecomm:home")
        else:
            return render(self.request, self.template_name, {"form":self.form_class, "error": "Invalid credentials"})
            
        return super().form_valid(form)


class MyOrdersView(TemplateView):
    template_name = "myorders.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/my-orders/")
        return super().dispatch(request,*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context['orders'] = orders
        return context
    
class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("ecomm:myorders")
            
        else:
            return redirect("/login/?next=/my-orders/")
        return super().dispatch(request, *args, **kwargs)


class MyProfileView(FormView):
    def get(self,request):
        if request.user.is_authenticated:
            try:
                try:
                    current_user = Seller.objects.get(user__id=request.user.id)
                except:
                    current_user = Customer.objects.get(user__id=request.user.id)
            except:
                return redirect("/login/?next=/my-profile/")
            if current_user is not None:
                #messages = None
                return render(request, "myprofile.html", locals())
            
            # form = UserProfileForm(request.POST or None, instance=current_user)
            
            # if form.is_valid():
            #     form.save()
            #     messages.success(request, "Your profile has been updated")
            #     return redirect('home')
            #return render(request, "myprofile.html")
        else:
            return redirect("/login/?next=/my-profile/")
        
    def post(self,request):
        if request.user.is_authenticated:
            username = request.POST.get('uname')
            # print("****************************",username)
            fullname = request.POST.get('fullname')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            address = request.POST.get('address')
            try:
                try:
                    current_user = Seller.objects.get(user__id=request.user.id)
                except:
                    current_user = Customer.objects.get(user__id=request.user.id)
            except:
                return redirect("/login/?next=/my-profile/")
            if current_user is not None:
                #current_user.user.username=username
                absUser = User.objects.get(id=current_user.user.id)
                absUser.email = email
                absUser.username=username
                absUser.save()
                current_user.full_name=fullname
                current_user.mobile=mobile
                #current_user.user.email=email
                current_user.address=address
                current_user.save()
                messages.success(request, "Your profile has been updated")
                return redirect('/my-profile')
            
            # form = UserProfileForm(request.POST or None, instance=current_user)
            
            # if form.is_valid():
            #     form.save()
            #     messages.success(request, "Your profile has been updated")
            #     return redirect('home')
            #return render(request, "myprofile.html")
        else:
            return redirect("/login/?next=/my-profile/")
        
        
    
    # def user_info(request):
    #     if request.user.is_authenticated:
    #         current_user = Profile.objects.get(user__id=request.user.id)
    #         form = UserProfileForm(request.POST or None, instance=current_user)
            
    #         if form.is_valid():
    #             form.save()
    #             messages.success(request, "Your profile has been updated")
    #             return redirect('home')
    #         return render(request, "myprofile.html", {'form':form})
    #     else:
    #         return redirect("/login/?next=/my-profile/")
        
        

    # template_name = "myprofile.html"
    # form_class = UserProfileForm
    # success_url = reverse_lazy("ecomm:home")
    
    # def form_valid(self, form):
    #     uname = form.cleaned_data.get("username")
    #     model = Customer
        
    #     def dispatch(self, request, *args, **kwargs):
    #         if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
    #             current_user = Profile.objects.get(user__id=request.user.id)
    #             form = UserProfileForm(request.POST or None, instance=current_user)
    #             if form.is_valid():
    #                 form.save()
    #                 messages.success(request, "Your profile has been updated")
    #                 return redirect('home')
    #         else:
    #             return redirect("/login/?next=/my-orders/")
    #         return super().dispatch(request, *args, **kwargs)         


#seller pages

class SellerProfileView(FormView):
    def get(self,request):
        if request.user.is_authenticated:
            try:
                try:
                    current_user = Seller.objects.get(user__id=request.user.id)
                except:
                    current_user = Customer.objects.get(user__id=request.user.id)
            except:
                return redirect("/login/?next=/seller-profile/")
            if current_user is not None:
                #messages = None
                return render(request, "adminpages/sellerprofile.html", locals())
            
            # form = UserProfileForm(request.POST or None, instance=current_user)
            
            # if form.is_valid():
            #     form.save()
            #     messages.success(request, "Your profile has been updated")
            #     return redirect('home')
            #return render(request, "myprofile.html")
        else:
            return redirect("/login/?next=/seller-profile/")
        
    def post(self,request):
        if request.user.is_authenticated:
            username = request.POST.get('uname')
            fullname = request.POST.get('fullname')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            address = request.POST.get('address')
            try:
                try:
                    current_user = Seller.objects.get(user__id=request.user.id)
                except:
                    current_user = Customer.objects.get(user__id=request.user.id)
            except:
                return redirect("/login/?next=/seller-profile/")
            if current_user is not None:
                #current_user.user.username=username
                absUser = User.objects.get(id=current_user.user.id)
                absUser.email = email
                absUser.username=username
                absUser.save()
                current_user.full_name=fullname
                current_user.mobile=mobile
                #current_user.user.email=email
                current_user.address=address
                current_user.save()
                messages.success(request, "Your profile has been updated")
                return redirect('/seller-profile')
            
            # form = UserProfileForm(request.POST or None, instance=current_user)
            
            # if form.is_valid():
            #     form.save()
            #     messages.success(request, "Your profile has been updated")
            #     return redirect('home')
            #return render(request, "myprofile.html")
        else:
            return redirect("/login/?next=/seller-profile/")


class SellerRegistrationView(CreateView):
    template_name = "adminpages/sellerregistration.html"
    form_class = SellerRegistrationForm
    success_url = reverse_lazy("ecomm:adminhome")
    
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username,email,password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)
        # username = form.cleaned_data.get("username")
        # password = form.cleaned_data.get("password")
        # email = form.cleaned_data.get("email")
        # user = User.objects.create_user(username,email,password)
        # form.user = user
        # login(self.request, user)
        # return super().form_valid(form)

class SellerLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomm:adminhome")
    
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Seller.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form":self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


class SellerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomm:home")
    

class SellerPasswordChangeView(FormView):
    template_name = "adminpages/sellerchangepassword.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("ecomm:adminhome")
    
    def form_valid(self, form):
        print("*****************Change Password********************")
        old = form.cleaned_data["oldpassword"]
        new = form.cleaned_data["newpassword"]
        confirm = form.cleaned_data["confirmpassword"]
        print(old, new, confirm)
        print("***Session user*****",self.request.user.password)
        checkhash = check_password(old, self.request.user.password)
        print(checkhash)
        try:
            if checkhash:
                cstmr = Seller.objects.get(user=self.request.user)
                print("Inside Try")
            else:
                cstmr = None
        except:
            cstmr = None
            print("Inside Except")
        if new == confirm and cstmr is not None:
            loggeduser = User.objects.get(username=self.request.user.username, password=self.request.user.password)
            loggeduser.password = make_password(new)
            loggeduser.save()
            return redirect("ecomm:adminhome")
        else:
            return render(self.request, self.template_name, {"form":self.form_class, "error": "Invalid credentials"})
            
        return super().form_valid(form)


class SellerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Seller.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request,*args, **kwargs)

class SellerHomeView(SellerRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the logged-in seller
        seller = Seller.objects.get(user=self.request.user)
        
        # Filter pending orders that contain products from this seller
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received",
            cart__cartproduct__product__seller=seller
        ).distinct().order_by("-id")
        
        return context


class  SellerOrderDetailView(SellerRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_queryset(self):
        # Ensure the seller can only access orders with their products
        seller = Seller.objects.get(user=self.request.user)
        return Order.objects.filter(cart__cartproduct__product__seller=seller).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the logged-in seller
        seller = Seller.objects.get(user=self.request.user)

        # Filter CartProducts for this order that belong to the seller
        order = self.object
        
        context["seller_products"] = order.cart.cartproduct_set.filter(product__seller=seller)
        
        totalPrice = 0
        for product in context['seller_products']:
            totalPrice += product.subtotal
            
        context['totalPrice'] = totalPrice
        
        context["allstatus"] = ORDER_STATUS  # For order status options
        return context

class SellerOrderListView(SellerRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    context_object_name = "allorders"
   
    def get_queryset(self):
        # Get the logged-in seller
        seller = Seller.objects.get(user=self.request.user)
        
        # Filter orders based on cart products belonging to this seller
        return Order.objects.filter(
            cart__cartproduct__product__seller=seller
        ).distinct().order_by("-id")


class SellerOrderStatusChangeView(SellerRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomm:adminorderlist"))


class AddProductView(SellerRequiredMixin, TemplateView):
    def get(self, request):
        categories = Category.objects.all()
        #print(categories)
        return render(request, 'adminpages/addproduct.html',locals())
    def post(self,request):
        categoryId = request.POST.get('category')
        title = request.POST.get('title')
        mrp = request.POST.get('mrp')
        sp = request.POST.get('sp')
        description = request.POST.get('description')
        warranty = request.POST.get('warranty')
        returnPolicy = request.POST.get('returnPolicy')
        pImage = request.FILES['ProductImage']
        print(categoryId,title,mrp,sp,description,warranty,returnPolicy,pImage)
        try:
            category = Category.objects.get(id=categoryId)
        except:
            category = None
        if category is not None:
            seller = Seller.objects.get(user=self.request.user)
            newProduct = Product(category=category,title=title,seller=seller,slug=title,marked_price=mrp,selling_price=sp,description=description,warranty=warranty,return_policy=returnPolicy,image=pImage)
            newProduct.save()
            messages.success(request, "Product Added Successfully")
            return redirect('/add-product')
        else:
            messages.error(request, "Error In Adding Product")
            return redirect('/add-product')
        


# class AllProductView(SellerRequiredMixin, TemplateView):
#     def get(self, request):
#         return render(request, 'adminpages/allproduct.html')

class AllProductView(SellerRequiredMixin, ListView):
    template_name = "adminpages/allproduct.html"
    context_object_name = "allproducts"
    
    def get_queryset(self):
        seller = Seller.objects.get(user=self.request.user)
        
        
        
        products =  Product.objects.filter(seller=seller).order_by("-id")
        return products
    
    def post(self, request, *args, **kwargs):
        # Handle product deletion
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("ecomm:allproducts")


class UpdateProductView(FormView):
        
    def post(self,request):
        productId = request.POST.get('productId')
        title = request.POST.get('title')
        mrp = request.POST.get('mrp')
        sp = request.POST.get('sp')
        description = request.POST.get('description')
        warranty = request.POST.get('warranty')
        returnPolicy = request.POST.get('returnPolicy')
        try:
            UpdatedProduct = Product.objects.get(id=productId)
        except:
            UpdatedProduct = None
        if UpdatedProduct is not None:
            UpdatedProduct.title=title
            UpdatedProduct.marked_price=mrp
            UpdatedProduct.selling_price=sp
            UpdatedProduct.description=description
            UpdatedProduct.warranty=warranty
            UpdatedProduct.return_policy=returnPolicy
            UpdatedProduct.save()
            messages.success(request, "Product Updated Successfully")
            return redirect('/all-products')
        else:
            messages.error(request, "Error In Updating Product")
            return redirect('/all-products')



class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'  # Your confirmation template
    success_url = reverse_lazy('product_list')  # Redirect after successful deletion

#payment
import paypalrestsdk
from django.shortcuts import redirect
from django.http import JsonResponse

# PayPal configuration
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # 'sandbox' or 'live'
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

logger = logging.getLogger(__name__)

def create_payment(request):
    if request.method == 'POST':
        cart_id = request.session.get("cart_id")
        if not cart_id:
            return JsonResponse({"error": "No cart found"}, status=400)
        
        cart = Cart.objects.get(id=cart_id)
        items = []
        
        for cp in cart.cartproduct_set.all():
            items.append({
                "name": cp.product.title,
                "sku": str(cp.product.id),
                "price": str(cp.rate),
                "currency": "USD",
                "quantity": cp.quantity
            })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "item_list": {"items": items},
                "amount": {
                    "total": str(cart.total),
                    "currency": "USD"
                },
                "description": f"Order Payment for Cart {cart_id}"
            }],
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/execute_payment/'),
                "cancel_url": request.build_absolute_uri('/cancel_payment/')
            }
        })

        if payment.create():
            approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
            logger.info(f"Payment created successfully. Approval URL: {approval_url}")
            return redirect(approval_url)
        else:
            logger.error(f"Payment creation failed: {payment.error}")
            return JsonResponse({"error": payment.error}, status=400)


def execute_payment(request):
    """
    Execute PayPal payment after user approval.
    """
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.delete()  # Clear cart after successful payment
            del request.session['cart_id']  # Clear session cart ID
        return redirect('ecomm:home')  # Redirect to success page
    else:
        return JsonResponse({"error": payment.error}, status=400)

def cancel_payment(request):
    """
    Handle payment cancellation.
    """
    return JsonResponse({"message": "Payment was cancelled."}, status=200)


paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_payment(request):
    """
    This view will create a PayPal payment.
    It prepares the payment details and redirects the user to PayPal for approval.
    """
    if request.method == 'POST':
        items = []  # Items to be purchased
        total_amount = 0  # Total amount to be charged

        # Assuming you have an order model where cart items are stored
        order = Order.objects.get(user=request.user, status="pending")

        for item in order.items.all():
            total_amount += item.product.selling_price * item.quantity
            items.append({
                "name": item.product.title,
                "sku": item.product.id,
                "price": item.product.selling_price,
                "currency": "USD",
                "quantity": item.quantity
            })

        # Create PayPal payment object
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "item_list": {
                    "items": items
                },
                "amount": {
                    "total": str(total_amount),
                    "currency": "USD"
                },
                "description": f"Order {order.id}"
            }],
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/execute_payment/'),
                "cancel_url": request.build_absolute_uri('/cancel_payment/')
            }
        })

        # Create the payment
        if payment.create():
            # Redirect the user to PayPal
            approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
            return redirect(approval_url)
        else:
            return JsonResponse({"error": "Payment creation failed"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

def execute_payment(request):
    """
    This view will execute the PayPal payment after the user approves it.
    """
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Payment executed successfully, now update the order status to 'completed'
        order = Order.objects.get(user=request.user, status="pending")
        order.status = "completed"
        order.save()

        # Redirect to a success page
        return redirect('order_success')  # Add your success URL here
    else:
        # Handle payment failure
        return JsonResponse({"error": "Payment execution failed"}, status=400)

def cancel_payment(request):
    """
    This view will be triggered if the user cancels the payment on PayPal.
    """
    return JsonResponse({"error": "Payment cancelled by user"}, status=400)
