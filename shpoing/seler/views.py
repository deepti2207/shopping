from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from app.models import *
from django.http import HttpResponseRedirect
# from django.views.genric import CreateView,DetailView
from app.forms import  *
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User,Group
from app.models import *
from .forms import *
# Create your views here.
# def product(request):
def status_seler_count(request):
    user= request.user
    if user.groups.filter(name='seler').exists():
        ordersss = OrderPlaced.objects.filter(status='Pending')
        totall_order = OrderPlaced.objects.all()
        order_delevered = OrderPlaced.objects.filter(status='Delivered')
        pending_order = 0
        for k in ordersss:
            if k.product.author ==  request.user:
                b = k.product
                pending_order= pending_order+1
        total_order = 0
        for i in totall_order:
            if i.product.author ==  request.user:
                total_order= total_order+1
        delevered_order = 0
        for j in order_delevered:
            if j.product.author ==  request.user:
                delevered_order= delevered_order+1
        context = {
            'pending_order':pending_order,
            'total_order':total_order,
            'delevered_order':delevered_order,
            'orderssss':ordersss,
        }
        return render(request,'seler/status.html',context)
    else:
        return HttpResponse('You Are not authorised to view this  page')




def product_upload(request):
    user = request.user
    if user.groups.filter(name='seler').exists():
        if request.method == 'POST':
            productss= Product_Form(request.POST,request.FILES)
            if productss.is_valid():
                user = request.user
                productss.instance.author=user
                productss.save()
                return redirect('product_upload')
        else:
            productss= Product_Form()
        context={
                'product':productss
            }
        return render(request, 'seler/product_upload.html',context)
    else:
        return HttpResponse("You Are not authorised to add a product ")
def Product_detail(request,pk):
    products = Product.objects.filter(id = pk)
    return render(request,'seler/Product_detail.html',{'products':products})


#Sign Up
class CustomerRegistrationSelerView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratualations! Registered Successfully')
            user = form.save()
            group = Group.objects.get(name='seler')
            # print('group',group)
            user.groups.add(group)
        return render(request, 'app/customerregistration.html', {'form': form})


def seller_product(request):
    user = request.user
    if user.groups.filter(name='seler').exists():
    # ass = user.groups.filter(name = seler).exists()
    # ass = user.groups
    # print(ass)
    # print(user.groups())
        orders = OrderPlaced.objects.all()
        ordersss = OrderPlaced.objects.filter(status='Pending')[:20]
        totall_order = OrderPlaced.objects.all()
        order_delevered = OrderPlaced.objects.filter(status='Delivered')
        order_accepted = OrderPlaced.objects.filter(status='Accepted')
        order_Cancel = OrderPlaced.objects.filter(status='Cancel').count()
        order_count = OrderPlaced.objects.filter(status='Pending').count()
        print(order_count,"order_count")
        productss = Product.objects.filter(author=request.user)
        total_product = Product.objects.filter(author=request.user).count()
        customers = Customer.objects.all()
        total_customers = customers.count()
        total_orders = orders.count()
        pending_order = 0
        for k in ordersss:
            if k.product.author ==  request.user:
                b = k.product
                pending_order= pending_order+1
        total_order = 0
        for i in totall_order:
            if i.product.author ==  request.user:
                total_order= total_order+1
        delevered_order = 0
        for j in order_delevered:
            if j.product.author ==  request.user:
                delevered_order= delevered_order+1
        order_accept= 0
        for a in order_accepted:
            if k.product.author ==  request.user:
                b = k.product
                order_accept= order_accept+1
        # delivered = OrderPlaced.filter(status='Delivered').count()
        # pending = orders.filter(STATUS_CHOICES='Pending').count()
        context = {'orders':orders, 'customers':customers,
            'total_orders':total_orders,'productss':productss,'ordersss':ordersss,
            'pending_order':pending_order,
            'total_order':total_order,
            'delevered_order':delevered_order,
            'order_accept':order_accept,
            'total_product':total_product,
            'order_Cancel':order_Cancel,
            }
        return render(request,'seler/your_product.html', context)
    else:
        return HttpResponse("Bhaiya  namaste")
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	context = {'customer':customer, 'orders':orders, 'order_count':order_count}
	return render(request, 'accounts/customer.html',context)


def delete_order(request,pk):
    pass

def update_order(request,pk):
    user = request.user
    order = OrderPlaced.objects.get(id=pk)
    ord = OrderPlaced.objects.filter(id = pk)
    for k in ord:
        a = k.product.author
        print(a,"aaa",user)
    if user == a:
        form = update_product(instance=OrderPlaced)
        if request.method == 'POST':
            form = update_product(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('/')

        context = {'form':form}
        return render(request, 'seler/update_order.html',context)
    else:
        return HttpResponse('Nikal laude')
