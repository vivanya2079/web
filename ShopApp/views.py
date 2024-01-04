from django.shortcuts import render,get_object_or_404,redirect
from ShopApp.models import Product,Categories,Filter_Price,Contact_us
from django.conf import settings as conf_settings 
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate,login as auth_login 
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.conf import settings
import razorpay
from razorpay import Client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRECT))



#Main page

def base(request):
    return render(request,'base.html')


#Index page with fetch the objects

def index(request):
    product=Product.objects.filter(status='Publish')###fetch all item
    #filter is used to filter the object
    context={
        'product':product,
    }
    return render(request,'index.html',context)

   



#Product Page::
def product(request):
    product = Product.objects.filter(status='Publish')
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    ##To id
    CATID = request.GET.get('categories')
    #with price
    PRICE_FILTER_ID = request.GET.get('filter_price')
    print(PRICE_FILTER_ID)
    if CATID:
        product = Product.objects.filter(categories=CATID)
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price=PRICE_FILTER_ID)

    else:
        product = Product.objects.filter(status='Publish')




    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
    }
    return render(request, 'product.html', context)

###SEARCH VIEWS
def search(request):
    # Get the search query from the GET parameters
    query = request.GET.get('query', '')

    # Filter products based on a case-insensitive partial match on the 'name' field
    product = Product.objects.filter(name__icontains=query)

    # Prepare the context to be passed to the template
    context = {
        'query': query,
        'product': product,
    }

    # Render the search results using the 'search.html' template
    return render(request, 'search.html', context)

    ###FOR SINGLE PAGE PRODUCT

def product_details_page(request,id):
    #FILTER WITH ID
    prod=Product.objects.filter(id=id).first()
    context={
        'prod':prod
    }
    return render(request, 'product_single.html',context)


###FOR CONTACT
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Create and save a new Contact_us object
        contact = Contact_us(name=name, email=email, subject=subject, message=message)
        contact.save()
        return redirect('index')

    return render(request, 'contact.html')
###############LOGIB##############AND REGISTER
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # Create a new user
        customer = User.objects.create_user(username, email, pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()

        # Redirect to the 'index' view after successful registration
        return redirect('login')

    return render(request, 'register.html')

####LOGIN##
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use the correct function name and pass the user object
            return redirect('index')
        else:
            # Handle the case where authentication fails
            return redirect('login')

    return render(request, 'auth.html')

####LOGOUT###
def logout(request):
    auth_logout(request)
    return redirect('/')

##CART PAge

####CART FUNCTION####
@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart.html')


#### check out page#####



def checkout(request):
    # Create a Razorpay payment order
    payment = client.order.create({
        'amount': 500,  # Replace with the actual amount
        'currency': 'INR',
        'payment_capture': '1'
    })
    
    order_id=payment['id']
    print(order_id)
    context={
        'order_id':order_id,
        'payment':payment,
    }
    return render(request, 'cartcheckout.html',context)



##PLACE Order###
def placeorder(request):
    if request.method == 'POST':  # 'POST' should be uppercase
        uid = request.session.get('-auth_user_id')
        user=Use.objects.all(id=uid)
        cart=request.session.get('cart')
        print(cart)
       
        firstname = request.POST.get('firstname')  # 'POST' should be uppercase
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        # Now, you can print or process the collected data as needed
        order=Order(
             user=user,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            payment_id=order_id,
            amount=amount,
        )
        order.save()
        for i in cart:
            a=( int(cart[i]['price']))
            b==cart[i]['quantity']

            total=a*b
            price(total)
            item=OrderItem(
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total
            )
            item.save()

    return render(request, 'place.html')


##############PAYMENT###############
# def payment_receipt(request):
#     # Assuming you have obtained these details from the Razorpay response
#     razorpay_payment_id = 'pay_NK0ZDsCfnFz7sT'
   

#     # Calculate the total amount based on cart items (similar to your existing logic)
#     total_amount = calculate_total_amount(request.session.cart)

#     context = {
#         'razorpay_payment_id': razorpay_payment_id,
        
#         'total_amount': total_amount,
#         # Add more context variables as needed
#     }

#     return render(request, 'payment_receipt.html', context)

# def calculate_total_amount(items):
#     # Replace this with your actual calculation logic
#     total = sum(item.get('price', 0) for item in items)
#     return tota###
#################ORDER COMPLETE#############




def receipt(request):
    totalAmount = calculateTotalAmount(request)  # Pass the request object to the function
    response = get_payment_response()  # Implement this function to get the Razorpay payment response

    context = {
        'totalAmount': totalAmount,
        'response': response,
    }

    return render(request, 'receipt.html', context)


def calculateTotalAmount(request):
    # Ensure that the quantities and prices are converted to integers before performing calculations
    totalAmount = 0
    for key, value in request.session.get('cart', {}).items():
        totalAmount += int(value['price']) * int(value['quantity'])
    return totalAmount

def get_payment_response():
    # Implement your logic to get the Razorpay payment response
    # This can include fetching data from the payment gateway or any other source
    # For demonstration purposes, a dummy response is returned
    return {
        'razorpay_payment_id': 'pay_NK5ME8EEM3yVCF',
        'razorpay_order_id': 'order_NK57u8SqZbpznn',
        
    }
    
    
def about(request):
    return render(request,'about.html')