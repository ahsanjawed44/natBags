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
from django.db.models import Avg
import uuid

import logging
from django.conf import settings

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

def index(request):

    customer_id = request.session.get('customer_id')
    cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first() 
    
    if cartObj:    
        cartID = cartObj.id
        cartItemCount = cartItems.objects.filter(cartF=cartID).count()
    else:        
        cartItemCount = 0
    

    

    newsData=news.objects.all()[:3]
    productData=product.objects.all()[:3]
    data={
        'news':newsData,
        'products':productData,
        'cartItemCount': cartItemCount
    }
    
    return render(request,"index.html",data)



# Static pages Start
def about(request):
    customer_id = request.session.get('customer_id')
    cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first() 
    
    if cartObj:    
        cartID = cartObj.id
        cartItemCount = cartItems.objects.filter(cartF=cartID).count()
    else:        
        cartItemCount = 0

    
    data={
        'cartItemCount':cartItemCount
    }

    return render(request,'about.html', data)

def contact(request):
    customer_id = request.session.get('customer_id')
    cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first() 
    
    if cartObj:    
        cartID = cartObj.id
        cartItemCount = cartItems.objects.filter(cartF=cartID).count()
    else:
        cartItemCount = 0
    
    data={
        'cartItemCount':cartItemCount
    }
    return render(request,'contact.html', data)

def services(request):
    customer_id = request.session.get('customer_id')
    cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first() 
    
    if cartObj:    
        cartID = cartObj.id
        cartItemCount = cartItems.objects.filter(cartF=cartID).count()
    else:        
        cartItemCount = 0

    data={
        'cartItemCount':cartItemCount   
    }

    return render(request,'services.html', data)
# Static pages End


# Shop Session Start
def shop(request):
    customer_id = request.session.get('customer_id')
    cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first()

    if cartObj:
        cartID = cartObj.id
        cartItemCount = cartItems.objects.filter(cartF=cartID).count()
    else:
        cartItemCount = 0

    shopData = product.objects.all()
    paginator = Paginator(shopData, 9)
    page_number = request.GET.get('page')
    shopDatafinal = paginator.get_page(page_number)
    totalpage = shopDatafinal.paginator.num_pages

    data = {
        'products': shopDatafinal,
        'lastpage': totalpage,
        'totalpagelist': [n+1 for n in range(totalpage)],
        'cartItemCount': cartItemCount,
        
    }
    return render(request, 'shop.html', data)

def singleProduct(request, productid):
    customer_id = request.session.get('customer_id')
    cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first() 
    
    if cartObj:    
        cartID = cartObj.id
        cartItemCount = cartItems.objects.filter(cartF=cartID).count()
    else:        
        cartItemCount = 0

    productDetail = product.objects.get(id=productid)    
    reviewData = review_product.objects.filter(productid=productid)
    review_count = review_product.objects.filter(productid=productid).count()

    
    # Aggregate average rating for the product
    product_ratings = review_product.objects.filter(productid=productid).aggregate(avg_rating=Avg('rating'))
    average_rating = product_ratings.get('avg_rating', 0)  # Get the average rating value or default to 0 if no rating
    if average_rating is None:
        average_rating = 0
    else:
     average_rating = round(average_rating)
    
    # Update the product instance with the calculated average rating
    productDetail.product_rating = average_rating
    productDetail.save()

    data = {
        'productDetail': productDetail,
        'reviewData': reviewData,
        'review_count': review_count,
        'cartItemCount': cartItemCount,
        'average_rating': average_rating,  # Pass the average rating to the template
    }
    return render(request, 'single-product.html', data)

def search(request):
    customer_id = request.session.get('customer_id')
    cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first()

    if cartObj:
        cartID = cartObj.id
        cartItemCount = cartItems.objects.filter(cartF=cartID).count()
    else:
        cartItemCount = 0

    usersearch = request.GET.get('search')
    # Pagination
    shopData = product.objects.filter(product_name__icontains=usersearch , product_catagory__catagory_name__icontains=usersearch) 
    
    paginator = Paginator(shopData, 9)
    page_number = request.GET.get('page')
    shopDatafinal = paginator.get_page(page_number)
    totalpage = shopDatafinal.paginator.num_pages

    if not shopData:  # If shopData is empty
        data = {
            'no_items_found': True,
            'cartItemCount': cartItemCount,
        }
    else:
        data = {
            'products': shopDatafinal,
            'lastpage': totalpage,
            'totalpagelist': [n+1 for n in range(totalpage)],
            'cartItemCount': cartItemCount,
        }

    return render(request, 'search.html', data)

# Shop Session End


# News Session Start
def newsPage(request):

    customer_id = request.session.get('customer_id')
    cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first() 
    
    if cartObj:    
        cartID = cartObj.id
        cartItemCount = cartItems.objects.filter(cartF=cartID).count()
    else:        
        cartItemCount = 0

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
    cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first() 
    
    if cartObj:    
        cartID = cartObj.id
        cartItemCount = cartItems.objects.filter(cartF=cartID).count()
    else:        
        cartItemCount = 0

    newsDetail=news.objects.get(id=newsid)
    data={
     'newsDetail':newsDetail,
     'cartItemCount': cartItemCount
    }
    return render(request,'single-news.html',data)
# News Session End


# Order Session Start
def checkout(request):

    customer_id = request.session.get('customer_id')
    if customer_id:
        try:
            cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first()
            if cartObj:
                cartID = cartObj.id
                cartItemCount = cartItems.objects.filter(cartF=cartID).count()
                cartItemData = cartItems.objects.filter(cartF=cartID)

                data = {
                    'cartItem': cartItemData,
                    'cart': cartObj,
                    'cartItemCount': cartItemCount
                }

                return render(request, 'checkout.html', data)
            else:
                # If no unpaid cart exists for the customer, render an empty cart
                return render(request, 'checkout.html', {'cartItem': [], 'cart': None, 'cartItemCount': 0})
        except cart.DoesNotExist:
            # If cart does not exist for the customer, render an empty cart
            return render(request, 'checkout.html', {'cartItem': [], 'cart': None, 'cartItemCount': 0})
    else:
        # If customer_id is not in session, render an empty cart
        return render(request, 'index.html', {'cartItem': [], 'cart': None, 'cartItemCount': 0})  

def order(request):
    if request.method == "POST":
        address = request.POST["address"]
        phone = request.POST["phone"]
        payment_method = request.POST["payment"]
        details=request.POST["special"]
        customer_id = request.session.get('customer_id')
        if 'customer_id' in request.session:
           
            try:
                customer = Customer.objects.get(id=customer_id)
                customer_name = customer.customer_name
                customer_email = customer.customer_email

            except Customer.DoesNotExist:
                # Handle the case where the customer does not exist
                return HttpResponse('Customer not found.')

            cart_instance = cart.objects.get(Customer=customer, is_paid=False)

            total_bill = cart_instance.get_total() 
            
            url = 'verifyOrder'
            token = str(uuid.uuid4())
            
            if customer_email:  # Check if customer_email is not None or empty                
                # Call the function to send the email token
                send_email_token(customer_email, token, url)
                addOrder = orderModel.objects.create(customer_name=customer_name, customer_email=customer_email, address=address, phone=phone, total_bill=total_bill, email_token=token, customer_id=customer, cart=cart_instance, payment_method=payment_method, details=details)


                cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first()

                if cartObj:    
                    cartID = cartObj.id
                    
                    # Step 2: Retrieve details of items in the cart
                    cartItemsInCart = cartItems.objects.filter(cartF=cartID)
                    
                    # Step 3: Update product quantities
                    for cartItem in cartItemsInCart:
                        product = cartItem.productF
                        product.product_quantity = product.product_quantity - cartItem.quantity
                        product.save()
                messages.success(request, 'Email is been send for verification. Confirm your order from your Gmail account.')
                return HttpResponseRedirect('/checkout/')
            else:
                return HttpResponse('Customer email is missing.')
        else:
            return render(request, 'login.html')
    else:
        return render(request, '404.html')



    try:  
        orderC = orderModel.objects.get(email_token=token)
        cartF=orderC.cart
        cartF.is_paid=True
        cartF.save()
        orderC.save()
        
        
        messages.success(request, 'Your order has been verified successfully!')

        # Redirect to the cart page
        return redirect('cart') 
        
    
    except Customer.DoesNotExist:
        return HttpResponse('Invalid token')
# Order Session End



# Email Verification Start

def send_email_token(email, token, url):
    try:
        subject = "Email Verification"
        message = f"Please click on the following link for validation : http://127.0.0.1:8000/{url}/{token}"
        email_from = settings.EMAIL_HOST_USER
        recipients_list = [email]
        send_mail(subject, message, email_from, recipients_list)
        return True
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise  
def verifyCustomer(request, token):
    try:
        
        customer = Customer.objects.get(email_token=token)
        customer.is_verified = True
        customer.save()


        
        request.session['customer_id'] = customer.id
        request.session['customer_name'] = customer.customer_name
        request.session['customer_email'] =customer.customer_email
        return redirect('/')
        
        return render(request, "login.html")
    except Customer.DoesNotExist:
        return HttpResponse('Invalid token')

def verifyOrder(request, token):
    try:  
        orderC = orderModel.objects.get(email_token=token)
        cartF=orderC.cart
        cartF.is_paid=True
        cartF.save()
        orderC.save()
        
        
        messages.success(request, 'Your order has been verified successfully!')

        # Redirect to the cart page
        return redirect('cart') 
        
    
    except Customer.DoesNotExist:
        return HttpResponse('Invalid token')
# Email Verification End     

# User authantication Start
def register(request):
    if request.method == "POST":
        fname = request.POST["firstName"]
        eml = request.POST["email"]
        pwd = request.POST["password"]

        if Customer.objects.filter(customer_email=eml).exists():
            messages.error(request, 'Email Already Exists, try again with different email')
            return redirect('/userRegister')
        else:
            url='verifyCustomer'
            email_token = str(uuid.uuid4())
            new_user = Customer.objects.create(customer_name=fname, customer_email=eml, customer_password=pwd, email_token=email_token)
            send_email_token(eml, email_token,url)
            messages.error(request, 'Verification Link is been sent to your Email.')
            return render(request, "register.html")
        
    return render(request, "register.html")

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
                    request.session['customer_email'] =customer.customer_email
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
# User authantication End



# Cart page and its operation Start
def cartPage(request):

    customer_id = request.session.get('customer_id')

    if customer_id:
        try:
            cartObj = cart.objects.filter(Customer=customer_id, is_paid=False).first()
            if cartObj:
                cartID = cartObj.id
                cartItemCount = cartItems.objects.filter(cartF=cartID).count()
                cartItemData = cartItems.objects.filter(cartF=cartID)

                data = {
                    'cartItem': cartItemData,
                    'cart': cartObj,
                    'cartItemCount': cartItemCount
                }

                return render(request, 'cart.html', data)
            else:
                # If no unpaid cart exists for the customer, render an empty cart
                return render(request, 'cart.html', {'cartItem': [], 'cart': None, 'cartItemCount': 0})
        except cart.DoesNotExist:
            # If cart does not exist for the customer, render an empty cart
            return render(request, 'cart.html', {'cartItem': [], 'cart': None, 'cartItemCount': 0})
    else:
        # If customer_id is not in session, render an empty cart
        return render(request, '404.html', {'cartItem': [], 'cart': None, 'cartItemCount': 0})

def add_to_cart(request,pid):
    if request.session.get('customer_id'):
        productC = product.objects.get(id=pid)
        customer_id = request.session['customer_id']

        # Fetch the Customer instance using the customer_id
        customer = Customer.objects.get(id=customer_id)
        cartInfo, created = cart.objects.get_or_create(Customer=customer, is_paid=False)

        # Check if the product already exists in the cart items
        existing_cart_item = cartItems.objects.filter(cartF=cartInfo, productF=productC).first()

        if existing_cart_item:
            # If the product already exists in the cart, increase its quantity
            existing_cart_item.quantity += 1
            existing_cart_item.save()
        else:
            # If the product is not in the cart, create a new cart item
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

def plus(request, cid):
    cartItem=cartItems.objects.get(id=cid)
    cartItem.quantity += 1 
    cartItem.save() 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def minus(request,cid):
     cartItem=cartItems.objects.get(id=cid)
     cartItem.quantity -= 1 
     cartItem.save() 
     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
# Cart page and its operation Start


# Customer Feedback Start
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
                return HttpResponse("Customer does not exist.")  
            except product.DoesNotExist:
                return HttpResponse("Product does not exist.")  
        else:
            return HttpResponse("Customer ID not found in session.")  
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
# Customer Feedback End

# Not found errror
def error(request):
    return render(request,'404.html')