from django.http import HttpResponse
from django.shortcuts import render,redirect
from requests import Session
from Customer.models import *
from News.models import *
from Shop.models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages


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
    productData=product.objects.all()
    data={
        'products':productData
        }
    return render(request,'shop.html',data)

def newsPage(request):
    newsData=news.objects.all()
    data={
        'news':newsData
        }
    return render(request,'news.html',data)

def services(request):
   return render(request,'services.html')

def cart(request):
    return render(request,'cart.html')

def checkout(request):
    return render(request,'checkout.html')

def singleNews(request,newsid):
    newsDetail=news.objects.get(id=newsid)
    data={
     'newsDetail':newsDetail   
    }
    return render(request,'single-news.html',data)

def singleProduct(request):
    return render(request,'single-product.html')

#Dashboard
def dashboard(request):
    pass


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
