from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileform
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User,Group
from .decorator import *
from django.utils.decorators import method_decorator
#Home page
def regis(request):
    return render(request,'app/registration_choise.html')


@method_decorator(allowed_user, name='dispatch')
class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request,'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears,'mobiles':mobiles})

#Product Details

class  ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
       
        return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})
#CART Start
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user) 
        amount = 0.0
        shipping_amount = 40.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temporary_amount = (p.quantity * p.product.discounted_price)
                amount += temporary_amount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')


@login_required
def  plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount =40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temporary_amount = (p.quantity * p.product.discounted_price)
            amount += temporary_amount
            
        
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def  minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount =40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temporary_amount = (p.quantity * p.product.discounted_price)
            amount += temporary_amount
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)


@login_required
def  remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount =40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temporary_amount = (p.quantity * p.product.discounted_price)
            amount += temporary_amount
        data = {
            
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)
#CART End

# @allowed_user
def buy_now(request,pk):
    return render(request, 'app/buynow.html')

#Customer Profile
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileform()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form = CustomerProfileform(request.POST)
        if form.is_valid():
            usr = request.user
            usr.save()
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'congratualation! Profile Updated successfully')
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
#Address
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})


@login_required
def orders(request):
    # user = request.user


    op = OrderPlaced.objects.filter(user=request.user)
    print(request.user,"user")

    # print(op.customer,"customer")

    return render(request, 'app/orders.html',{'order_placed':op})





#Mobile Details
def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data =='Redmi'or data == 'samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=7000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=7000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})





#Sign Up
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratualations! Registered Successfully')
            user = form.save()
            group = Group.objects.get(name='Customer')
            # print('group',group)
            user.groups.add(group)
        return render(request, 'app/customerregistration.html', {'form': form})




@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    print(cart_items,"cart_items")
    amount = 0.0
    shipping_amount = 40.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temporary_amount = (p.quantity * p.product.discounted_price)
            amount += temporary_amount
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})


@login_required
def payment_done(request):
    # if request.method == 'POST':
    #     form = request.POST
    #     if(form):
    #         f = form.cleaned_data('pid')

    #         return render(request, 'app/more.html', {'form': form,'f':f})



    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')






