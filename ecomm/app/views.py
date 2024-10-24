from typing import Any
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import View,TemplateView,CreateView, FormView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CheckoutForm, CustomerRegistrationForm, CustomerLoginForm, PasswordChangeForm
from .models import *
from django.db.models import Q



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
        self.request.COOKIES.pop("messages", "")
        return context
    
    
class AllProductsView(EcomMixin, TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context

class ProductDetailView(EcomMixin, TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         url_slug = self.kwargs['slug']
         product = Product.objects.get(slug= url_slug)
         product.view_count += 1
         product.save()
         context['product'] = product
         return context
    
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


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomm:home")


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
                cstmr = Admin.objects.get(user=self.request.user)
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



class PasswordChangeView(FormView):
    template_name = "changepassword.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("ecomm:home")
    
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
    
    
    
class AboutView(EcomMixin, TemplateView):
    template_name = "about.html"

class ContactView(EcomMixin, TemplateView):
    template_name = "contactus.html"


class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
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
                return redirect("ecomm:customerprofile")
            
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

#admin pages
class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomm:adminhome")
    
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form":self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request,*args, **kwargs)

class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["pendingorders"] = Order.objects.filter(order_status="Order Received").order_by("-id")
            return context


class  AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"


class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomm:adminorderdetail", kwargs={"pk": order_id}))

class SearchView(TemplateView):
    template_name="search.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        kw=self.request.GET.get("keyword")
        results=Product.objects.filter(Q(title__icontains=kw)| Q(description__icontains=kw) | Q(return_policy__icontains=kw))
        print(results)
        context["results"]=results
        return context