from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from requests import Session
from Customer.models import *
from News.models import *
from Shop.models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    newsData=news.objects.all()[:3]
    productData=product.objects.all()[:3]
    data={
        'news':newsData,'products':productData
        }
    return render(request,"index.html",data)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def shop(request):
    shopData=product.objects.all()
    paginator=Paginator(shopData,10)
    page_number=request.GET.get('page')
    shopDatafinal=paginator.get_page(page_number)
    totalpage=shopDatafinal.paginator.num_pages

    data={
        'products':shopDatafinal,
        'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
        }
    return render(request,'shop.html',data)



def singleProduct(request,productid):
    productDetail=product.objects.get(id=productid)
    data={
     'productDetail':productDetail   
    }
    return render(request,'single-product.html',data)




def services(request):
   return render(request,'services.html')







def checkout(request):
    
     if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        cartItemData = cartItems.objects.filter(cartF__Customer_id=customer_id)
        cartData =  cart.objects.get(Customer_id=customer_id) 

        data = {
            'cartItem': cartItemData,
            'cart': cartData
        }

        return render(request, 'checkout.html', data)
     else:
        # Handle case where user is not logged in
        return redirect('/login')
    




def newsPage(request):
    newsData=news.objects.all()
    paginator=Paginator(newsData,9)
    page_number=request.GET.get('page')
    shopDatafinal=paginator.get_page(page_number)
    totalpage=shopDatafinal.paginator.num_pages

    data={
        'news':shopDatafinal,
        'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)]
        }

    data={
        'news':newsData
        }
    return render(request,'news.html',data)



def singleNews(request,newsid):
    newsDetail=news.objects.get(id=newsid)
    data={
     'newsDetail':newsDetail   
    }
    return render(request,'single-news.html',data)




def cartPage(request):

    #  if 'customer_id' in request.session:
    #     customer_id = request.session['customer_id']
    #     cartItemData = cartItems.objects.filter(cartF__Customer_id=customer_id)
    #     cartData =  cart.objects.get(Customer_id=customer_id) 

    #     data = {
    #         'cartItem': cartItemData,
    #         'cart': cartData
    #     }

    #     return render(request, 'cart.html', data)
    #  else:
    #     # Handle case where user is not logged in
        # return redirect('/login')
     
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        try:
            cartItemData = cartItems.objects.filter(cartF__Customer_id=customer_id)
            cartData = cart.objects.get(Customer_id=customer_id)

            data = {
                'cartItem': cartItemData,
                'cart': cartData
            }

            return render(request, 'cart.html', data)
        except cart.DoesNotExist:
            # If cart does not exist for the customer, render an empty cart
            return render(request, 'cart.html', {'cartItem': [], 'cart': None})
    else:
        # If customer_id is not in session, render an empty cart
        return render(request, 'cart.html', {'cartItem': [], 'cart': None})


    # cartItemData=cartItems.objects.all()
    # cartData=cart.objects.get(pk=1)
    # data={
    #     'cartItem':cartItemData,
    #     'cart':cartData

    #     }

    # return render(request,'cart.html',data)




def add_to_cart(request,pid):
    # if request.session.get('customer_id'):
    #     productC = product.objects.get(id=pid)
    #     customer = request.session['customer_id']

    #     cartInfo = cart.objects.get_or_create(Customer=customer, is_paid=False)
    #     cartItem = cartItems.objects.create(cartF=cartInfo, productF=productC)
    #     cartItem.save()
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # else:
    #     return redirect("/userLogin/")

    if request.session.get('customer_id'):
        productC = product.objects.get(id=pid)
        customer_id = request.session['customer_id']
        
        # Fetch the Customer instance using the customer_id
        customer = Customer.objects.get(id=customer_id)

        # Assuming your cart model has a field named "Customer"
        # which is a ForeignKey to the Customer model
        cartInfo, created = cart.objects.get_or_create(Customer=customer, is_paid=False)
        
        cartItem = cartItems.objects.create(cartF=cartInfo, productF=productC)
        cartItem.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect("/userLogin/")

def remove_cart(request , cid):
    try:
        cartItem=cartItems.objects.get(id=cid)
        cartItem.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# def update_cart(request,cid):
#     update_qty = request.GET.get('qty')
#     cartItem = cartItems.objects.get(id=cid)
    
#     if update_qty != cartItem.quantity:
#         cartItem.quantity = update_qty
#         cartItem.save()
#     else:
#         pass
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
      
# Not found errror
def error(request):
    return render(request,'404.html')



# Authantication
def register(request):
    if request.method=="POST":
        fname=request.POST["firstName"]
        eml=request.POST["email"]
        pwd=request.POST["password"]

        if Customer.objects.filter(customer_email=eml).exists() :
            messages.error(request , 'Email Already Exist')
            return redirect('/userRegister')
        else:
            new_user=Customer(customer_name=fname,customer_email=eml,customer_password=pwd)
            new_user.save()
            customer = Customer.objects.get(customer_email=eml , customer_password=pwd)
            if customer is not None:

                request.session['customer_id'] = customer.id
                request.session['customer_name'] = customer.customer_name
                
            
                return redirect('/')

    return render(request,"register.html")



def login(request):
    if request.method == 'POST':
        eml = request.POST['email']
        pwd = request.POST['password']

        try:
            customer = Customer.objects.get(customer_email=eml , customer_password=pwd)

            request.session['customer_id'] = customer.id
            request.session['customer_name'] = customer.customer_name
            return redirect('/')
        

        except Customer.DoesNotExist:
            messages.error(request,'Invalid Email And Password')
            return redirect ('/userLogin')

    return render(request, 'login.html')

def logout(request):
          # Flush or clear the session to destroy it
    request.session.flush()
    # OR
    request.session.clear()
    # You can also delete the session from the database
    session_key = request.session.session_key
    if session_key:
        Session.objects.filter(session_key=session_key).delete()
    # Redirect to the index page or any other page
    return redirect('index')
def plus(request, cid):
    cartItem=cartItems.objects.get(id=cid)
    cartItem.quantity += 1  # Increment the quantity
    cartItem.save() 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def minus(request,cid):
     cartItem=cartItems.objects.get(id=cid)
     cartItem.quantity -= 1  # Increment the quantity
     cartItem.save() 
     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))