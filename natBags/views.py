from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect
from requests import Session
from Customer.models import *
from News.models import *
from Shop.models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
import uuid


def index(request):

    customer_id = request.session.get('customer_id')

    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()

    newsData=news.objects.all()[:3]
    productData=product.objects.all()[:3]
    data={
        'news':newsData,
        'products':productData,
        'cartItemCount': cartItemCount
    }
    
    return render(request,"index.html",data)

def about(request):
    customer_id = request.session.get('customer_id')
    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()

    data={
        'cartItemCount':cartItemCount
    }

    return render(request,'about.html', data)

def contact(request):
    customer_id = request.session.get('customer_id')
    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()
    data={
        'cartItemCount':cartItemCount
    }
    return render(request,'contact.html', data)

def shop(request):

    customer_id = request.session.get('customer_id')
    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()

    shopData=product.objects.all()
    paginator=Paginator(shopData,10)
    page_number=request.GET.get('page')
    shopDatafinal=paginator.get_page(page_number)
    totalpage=shopDatafinal.paginator.num_pages

    data={
        'products':shopDatafinal,
        'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)],
        'cartItemCount':cartItemCount
        }
    return render(request,'shop.html',data)



def singleProduct(request,productid):
    customer_id = request.session.get('customer_id')
    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()

    productDetail=product.objects.get(id=productid)    
    reviewData = review_product.objects.filter(productid=productid)
    review_count = review_product.objects.filter(productid=productid).count()
    
    data={
     'productDetail':productDetail,
     'reviewData': reviewData,
     'review_count': review_count,
     'cartItemCount': cartItemCount
    }
    return render(request,'single-product.html',data)




def services(request):
    customer_id = request.session.get('customer_id')
    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()

    data={
        'cartItemCount':cartItemCount   
    }

    return render(request,'services.html', data)


def order(request):
      customerName = request.session.get('customer_name')




def checkout(request):
    
    customer_id = request.session.get('customer_id')
    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()

    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        cartItemData = cartItems.objects.filter(cartF__Customer_id=customer_id)
        cartData =  cart.objects.get(Customer_id=customer_id) 

        data = {
            'cartItem': cartItemData,
            'cart': cartData,
            'cartItemCount': cartItemCount
        }

        return render(request, 'checkout.html', data)
    else:
        # Handle case where user is not logged in
        return redirect('/login')
    




def newsPage(request):

    customer_id = request.session.get('customer_id')
    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()

    newsData=news.objects.all()
    paginator=Paginator(newsData,9)
    page_number=request.GET.get('page')
    shopDatafinal=paginator.get_page(page_number)
    totalpage=shopDatafinal.paginator.num_pages

    data={
        'news':shopDatafinal,
        'lastpage':totalpage,
        'totalpagelist':[n+1 for n in range(totalpage)],
        'cartItemCount': cartItemCount
    }
    
    return render(request,'news.html',data)



def singleNews(request,newsid):
    customer_id = request.session.get('customer_id')
    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()

    newsDetail=news.objects.get(id=newsid)
    data={
     'newsDetail':newsDetail,
     'cartItemCount': cartItemCount
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
     
    customer_id = request.session.get('customer_id')
    cartItemCount = cartItems.objects.filter(cartF=customer_id).count()

    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        try:
            cartItemData = cartItems.objects.filter(cartF__Customer_id=customer_id)
            cartData = cart.objects.get(Customer_id=customer_id)

            data = {
                'cartItem': cartItemData,
                'cart': cartData,
                'cartItemCount': cartItemCount
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

def order(request):
    # Check if the user is logged in
    if request.method == "POST":
        address = request.POST["address"]
        phone = request.POST["email"]
        pwd = request.POST["password"]
        if 'customer_id' not in request.session:
            customer_name = request.session.get('customer_name')
            customer_email = request.session.get('customer_email')

      
# Not found errror
def error(request):
    return render(request,'404.html')

# Send Email

def send_email_token(email, token):
    try:
        subject = "Email Verification"
        message = f"Please click on the following link to verify your email: http://127.0.0.1:8000/verify/{token}"
        email_from = settings.EMAIL_HOST_USER
        recipients_list = [email]
        send_mail(subject, message, email_from, recipients_list)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def register(request):
    if request.method == "POST":
        fname = request.POST["firstName"]
        eml = request.POST["email"]
        pwd = request.POST["password"]

        if Customer.objects.filter(customer_email=eml).exists():
            messages.error(request, 'Email Already Exists')
            return redirect('/userRegister')
        else:
            # Create a new user with email verification pending
            email_token = str(uuid.uuid4())
            new_user = Customer.objects.create(customer_name=fname, customer_email=eml, customer_password=pwd, email_token=email_token)
            # Send verification email
            send_email_token(eml, email_token)
            # Redirect to a page informing the user to check their email for verification
            return render(request, "404.html")
    return render(request, "register.html")

def verify(request, token):
    try:
        # Find the customer by email token
        customer = Customer.objects.get(email_token=token)
        # Mark the email as verified
        customer.is_verified = True
        customer.save()
        # Redirect the user to a success page
        return render(request, "login.html")
    except Customer.DoesNotExist:
        return HttpResponse('Invalid token')



# def send_email_token(email,token):
#     try:
#         subject="Test email"
#         massage="Verify your acccount by clicking on this link. http://127.0.0.1:8000/verify/{token}"
#         email_from= settings.EMAIL_HOST_USER
#         recipents_list=[email, ]
#         send_mail(subject,massage,email_from,recipents_list)

#     except Exception as e:
#         return False
    
#     return True 


# def verify(request,token):
#     try:
#         pObj=profile.objects.get(email_token=token)
#         pObj.is_verified=True
#         pObj.save()
#         return render(request,"login.html")
#     except Exception as e:
#         return HttpResponse('Envalid token',)

# # Authantication
# def register(request):
#     if request.method=="POST":
#         fname=request.POST["firstName"]
#         eml=request.POST["email"]
#         pwd=request.POST["password"]

#         if Customer.objects.filter(customer_email=eml).exists() :
#             messages.error(request , 'Email Already Exist')
#             return redirect('/userRegister')
#         else:
#             new_user=Customer(customer_name=fname,customer_email=eml,customer_password=pwd)
#             new_user.save()

#             p_obj= profile.objects.create(
#                 customer=new_user.customer_name,
#                 email_token=str(uuid.uuid4())
#             )
#             send_email_token(eml,p_obj.email_token)
            
#             # customer = Customer.objects.get(customer_email=eml , customer_password=pwd)
#             # if customer is not None:

#             #     request.session['customer_id'] = customer.id
#             #     request.session['customer_name'] = customer.customer_name
                
#             #     return redirect('/')

#     return render(request,"register.html")



def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            customer = Customer.objects.get(customer_email=email)
            if customer.customer_password == password:
                if customer.is_verified:
                    request.session['customer_id'] = customer.id
                    request.session['customer_name'] = customer.customer_name
                    return redirect('/')
                else:
                    messages.error(request, 'Your email is not verified. Verify it from your Gmail account.')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid email or password')

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


def PlaceReview(request):
    if request.method == "POST":
        rate = request.POST["rate"]
        comment = request.POST["comment"]
        productid = request.POST["productid"]
        customer_id = request.session.get('customer_id')

        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
                product_instance = product.objects.get(id=productid)
                review = review_product(userid=customer, productid=product_instance, review=comment, rating=rate)
                review.save()

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            except Customer.DoesNotExist:
                return HttpResponse("Customer does not exist.")  # Handle this case as per your requirement
            except product.DoesNotExist:
                return HttpResponse("Product does not exist.")  # Handle this case as per your requirement
        else:
            return HttpResponse("Customer ID not found in session.")  # Handle this case as per your requirement
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
