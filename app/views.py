from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import JsonResponse

from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm, MyPasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

import razorpay
from .models import Product, Order


from groq import Groq
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)

            response = groq_client.chat.completions.create(
                model='llama-3.1-8b-instant',  # free and fast
                messages=[
                    {
                        'role': 'system',
                        'content': '''You are Lucky, a friendly fashion assistant 
for Lucky Store — an Indian online shopping store selling:
- Jewellery: Gold & Silver Necklaces, Gold & Silver Ear Rings
- Fashion: Top Wear (Black & White T-shirts under Rs.500), Bottom Wear (Black & Blue Jeans under Rs.600)

Help customers with outfit advice, colour suggestions, jewellery pairings, 
size guidance, seasonal fashion, and Indian occasion wear (Diwali, Holi, office, casual).
Keep responses friendly, concise (2-4 sentences), and always relate back to Lucky Store products.
End with a follow-up question to keep conversation going.'''
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ],
                max_tokens=300,
                temperature=0.7,
            )

            reply = response.choices[0].message.content
            return JsonResponse({'response': reply})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Groq error: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)




client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
# ==================================================
# HOME PAGE
# ==================================================
class ProductView(View):
    def get(self, request):
        context = {
            'topwears': Product.objects.filter(category='TW'),
            'bottomwears': Product.objects.filter(category='BW'),
            'necklace': Product.objects.filter(category='N'),
            'earrings': Product.objects.filter(category='E'),
        }
        return render(request, 'app/home.html', context)

# ==================================================
# PRODUCT DETAILS PAGE
# ==================================================
class ProductDetailsView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})

# ==================================================
# CATEGORY FILTER (COMMON)
# ==================================================
def category_filter(request, category, brand_list=None, price_limit=None, template=None, context_name=None, data=None):
    products = Product.objects.filter(category=category)

    if data:
        data_lower = str(data).lower()
        if brand_list and data_lower in [b.lower() for b in brand_list]:
            products = products.filter(brand__iexact=data)
        elif data_lower == 'below' and price_limit:
            products = products.filter(discounted_price__lt=price_limit)
        elif data_lower == 'above' and price_limit:
            products = products.filter(discounted_price__gt=price_limit)

    return render(request, template, {context_name: products})

def necklace(request, data=None):
    return category_filter(request, 'N', ['Gold', 'Silver'], 1000, 'app/necklace.html', 'necklace', data)

def earrings(request, data=None):
    return category_filter(request, 'E', ['Gold', 'Silver'], 1000, 'app/earrings.html', 'earrings', data)

def topwear(request, data=None):
    return category_filter(request, 'TW', ['Black', 'White'], 500, 'app/topwear.html', 'topwear', data)

def bottomwear(request, data=None):
    return category_filter(request, 'BW', ['Black', 'Blue'], 600, 'app/bottomwear.html', 'bottomwear', data)

# ==================================================
# CART LOGIC
# ==================================================
@login_required
def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        product_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        cart, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart.quantity += 1
            cart.save()

    return redirect('showcart')

@login_required
def show_cart(request):
    user = request.user
    carts = Cart.objects.filter(user=user)

    amount = sum(item.quantity * item.product.discounted_price for item in carts)
    totalamount = amount + 40  # shipping

    return render(request, 'app/addtocart.html', {
        'carts': carts,
        'amount': amount,
        'totalamount': totalamount
    })

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart = get_object_or_404(Cart, product__id=prod_id, user=request.user)
        cart.quantity += 1
        cart.save()
        return JsonResponse({'quantity': cart.quantity})

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart = get_object_or_404(Cart, product__id=prod_id, user=request.user)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        return JsonResponse({'quantity': cart.quantity})

@login_required
def remove_cart(request, id):
    cart = get_object_or_404(Cart, id=id, user=request.user)
    cart.delete()
    return redirect('showcart')

# ==================================================
# BUY / CHECKOUT / ORDERS
# ==================================================

@login_required
def buy_now(request):
    if request.method == "POST":
        user = request.user
        prod_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)

        # Clear cart and add selected product
        Cart.objects.filter(user=user).delete()
        Cart.objects.create(user=user, product=product, quantity=1)

        return redirect('checkout')

    return redirect('home')


@login_required
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    add = Customer.objects.filter(user=user)

    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    shipping_amount = 40
    totalamount = amount + shipping_amount

    context = {
        'cart_items': cart_items,
        'add': add,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'totalamount': totalamount,
    }

    return render(request, 'app/checkout.html', context)


@login_required
def payment(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    add = Customer.objects.filter(user=user)

    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    shipping_amount = 40
    totalamount = amount + shipping_amount

    context = {
        'cart_items': cart_items,
        'add': add,
        'totalamount': totalamount,
    }

    return render(request, 'app/payment.html', context)


@login_required
def payment_done(request):
    if request.method != "POST":
        return redirect('checkout')

    user = request.user
    custid = request.POST.get('custid')

    if not custid:
        messages.error(request, "Please select address")
        return redirect('payment')

    customer = get_object_or_404(Customer, id=custid, user=user)
    cart_items = Cart.objects.filter(user=user)

    for item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=item.product,
            quantity=item.quantity,
            is_paid=False,                   
            payment_method="COD",
            status="Order Placed"
        )
        item.delete()

    messages.success(request, "Order placed successfully 🎉")
    return redirect('orders')
# =======================================================================
# # Razorpay order data
# =======================================================================

@method_decorator(csrf_exempt, name='dispatch')
class CreatePaymentView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        shipping_amount = 40
        totalamount = amount + shipping_amount

        razorpay_order = client.order.create({
            "amount": int(totalamount * 100),  # paisa
            "currency": "INR",
            "payment_capture": "1"
        })

        # session me save (callback ke liye)
        request.session['razorpay_order_id'] = razorpay_order["id"]

        return JsonResponse({
            "order_id": razorpay_order["id"],
            "key": settings.RAZORPAY_KEY_ID,
            "amount": int(totalamount * 100)
        })



@method_decorator(csrf_exempt, name='dispatch')
class PaymentCallBackView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user

        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")
        custid = request.POST.get("custid")

        try:
            client.utility.verify_payment_signature({
                "razorpay_payment_id": payment_id,
                "razorpay_order_id": order_id,
                "razorpay_signature": signature
            })
        except:
            return JsonResponse({"status": "failed"})

        customer = get_object_or_404(Customer, id=custid, user=user)
        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                is_paid=True,
                payment_method="Razorpay",
                status="Order Placed"
            )
            item.delete()

        return JsonResponse({"status": "success"})


@login_required
def orders(request):
    orders = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'orders': orders})

# ==================================================
# USER ADDRESS & PROFILE
# ==================================================
@login_required
def address(request):
    addresses = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'addresses': addresses, 'active': 'btn-primary'})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            Customer.objects.create(user=request.user, **form.cleaned_data)
            messages.success(request, 'Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    
@login_required
def delete_address(request, id):
    address = get_object_or_404(Customer, id=id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address removed successfully.')
    return redirect('address')

# ==================================================
# PASSWORD CHANGE
# ==================================================
@login_required
def change_password(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = MyPasswordChangeForm(user=request.user)
    return render(request, 'app/changepassword.html', {'form': form})

# ==================================================
# REGISTRATION
# ==================================================
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        return render(request, 'app/customerregistration.html', {'form': form})
