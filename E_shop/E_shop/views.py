from django.shortcuts import render,redirect
from store_app.models import Product,Categories,Filter_Price,Colour,Brand,Contact_us
from django.conf import settings
#from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRATE))




def BASE(request):
    return render(request,'Main//base.html')

def HOME(request):
    product = Product.objects.filter(status = 'Publish')

    context = {
        'product':product,
    }

    return render(request,'Main/index.html',context)


def PRODUCT(request):
   product = Product.objects.filter(status = 'Publish')
   categories = Categories.objects.all()
   filter_price = Filter_Price.objects.all()
   colour = Colour.objects.all()
   brand = Brand.objects.all()


   CATID = request.GET.get('categories')
   PRICE_FILTER_ID =request.GET.get('filter_price')
   COLOURID = request.GET.get('colour')
   BRANDID = request.GET.get('brand')

   ATOZID = request.GET.get('ATOZ')
   ZTOAID = request.GET.get('ZTOA')

   PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH')
   PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')

   NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
   OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')

   if CATID:
        product = Product.objects.filter(categories = CATID, status = 'Publish')
   elif PRICE_FILTER_ID:
       product = Product.objects.filter(filter_price = PRICE_FILTER_ID, status = 'Publish')
   elif COLOURID:
       product = Product.objects.filter(colour = COLOURID,status = 'Publish')
   elif BRANDID:
       product = Product.objects.filter(brand = BRANDID,status = 'Publish')
   elif ATOZID:
       product = Product.objects.filter(status = 'Publish').order_by('name')
   elif ZTOAID:
       product = Product.objects.filter(status = 'Publish').order_by('-name')
   elif PRICE_LOWTOHIGHID:
       product = Product.objects.filter(status = 'Publish').order_by('price')
   elif PRICE_HIGHTOLOWID:
       product = Product.objects.filter(status = 'Publish').order_by('-price')
   elif NEW_PRODUCTID:
       product = Product.objects.filter(status = 'Publish',condition = 'New').order_by('-id')
   elif OLD_PRODUCTID:
       product = Product.objects.filter(status = 'Publish',condition = 'Old').order_by('-id')

   else:
        product = Product.objects.filter(status = 'Publish').order_by('-id')
           

   context = {
       'product':product,
       'categories':categories,
       'filter_price':filter_price,
       'colour':colour,
       'brand':brand,
   }
   
   return render(request,'Main/product.html',context)


def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains = query )

    context = {
        'product':product
    }

    return render(request,'Main/search.html',context)

def PRODUCT_DETAIL_PAGE(request,id):
    prod = Product.objects.filter(id = id).first()

    context = {
        'prod':prod
    }

    return render(request,'Main/product_single.html',context)



def Contact_Page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        contact.save()
        return redirect('home')
        
        # subject = subject
        # message = message
        # email_from = settings.EMAIL_HOST_USER
        #try:
        # send_mail(subject,message,email_from, ['pcpatel4445@gmail.com'])
        # contact.save()
        # return redirect('home')
        #except:
            #return redirect('contact')


    return render(request,'Main/contact.html')


def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
    
        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('register')

    return render(request,'Registration/auth.html')

def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        User = authenticate(username = username,password = password)
        if User is not None:
            login(request,User)
            return redirect('home')
        else:
            return redirect('login')


    return render(request,'Registration/auth.html')

def HandleLogout(request):
    logout(request)

    return redirect('home')




@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


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
    return render(request, 'Cart/cart_details.html')

def Check_out(request):
    payment = client.order.create({
        "amount":500,
        "currency": "INR",
        "payment_capture":"1",
    })

    order_id = payment['id']
    context = {
        'order_id':order_id,
        'payment':payment,
    }
    return render(request, 'Cart/checkout.html',context)

def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        firstname = request.POST.get('firstname')
        lastname =request.POST.get('lastname')
        country =request.POST.get('country')
        address =request.POST.get('address')
        city =request.POST.get('city')
        state =request.POST.get('state')
        postcode =request.POST.get('postcode')
        phone =request.POST.get('phone')
        email =request.POST.get('email')
        amount = request.POST.get('amount')

        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            city = city,
            address = address,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount = amount,
        )



    return render(request,'Cart/placeorder.html')