from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, BootstrapAuthenticationForm, DeliveryForm, PartForm
from .models import Part, CustomUser, ShoppingCart, CartItem, Order, Delivery


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            cart = ShoppingCart.objects.filter(
                user=CustomUser.objects.all().filter(user=form.get_user()).first()).first()
            if not cart:
                create_new_shopping_cart_for_user(form.get_user())
            return redirect('/')
    else:
        form = BootstrapAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def parts_view(request):
    return render(request, 'parts.html', {'parts': Part.objects.all()})


def part_details(request, pk):
    part = get_object_or_404(Part, pk=pk)
    shoppingCart = get_current_custom_user_shopping_cart(request)
    cart_items = CartItem.objects.all().filter(cart=shoppingCart)
    isAlreadyInCart = False
    for cart_item in cart_items:
        if cart_item.part == part:
            isAlreadyInCart = True
            break
        else:
            isAlreadyInCart = False
    return render(request, 'part_details.html', {'part': part, 'isAlreadyInCart': isAlreadyInCart})


def add_to_cart(request, pk):
    part = get_object_or_404(Part, pk=pk)
    quantity = request.POST.get('quantity')
    if part.available < int(quantity):
        return render(request, 'parts.html', {'part': part, 'quantity': quantity})
    else:
        cart_item = CartItem(part=part, quantity=quantity, cart=ShoppingCart.objects.all().filter(
            user=get_current_custom_user(request)).first())
        cart_item.save()
        return render(request, 'added_to_cart.html', {'part': part, 'quantity': quantity})


def shopping_cart(request):
    shoppingCart = get_current_custom_user_shopping_cart(request)
    cart_items = CartItem.objects.all().filter(cart=shoppingCart)
    total_price = calculate_total_price_for_current_user_shopping_cart(request)
    return render(request, 'shopping_cart.html', {
        'shoppingCart': shoppingCart,
        'cart_items': cart_items,
        'total_price': total_price
    })


def home(request):
    return render(request, 'home.html', {})


def logout_view(request):
    logout(request)
    return redirect('/')


def profile_view(request):
    return render(request, 'profile.html', {
        'currentUser': get_current_custom_user(request),
        'order_number': get_current_custom_user_orders(request).count(),
        'system_orders': Order.objects.all().count(),
        'in_progress_orders': Order.objects.all().filter(order_status='In progress').count(),
    })


def my_orders_view(request):
    return render(request, 'my_orders.html', {
        'orders': get_current_custom_user_orders(request)
    })


def delivery_info(request):
    total_price = calculate_total_price_for_current_user_shopping_cart(request)
    form = DeliveryForm()
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        order = Order(user=get_current_custom_user(request), cart=get_current_custom_user_shopping_cart(request),
                      total_amount=total_price, order_status='In progress')
        order.save()
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.order = order
            delivery.save()
            cart_items = get_parts_in_order(order)
            for cart_item in cart_items:
                part = cart_item.part
                part.available -= cart_item.quantity
                part.save()
            shoppingCart = get_current_custom_user_shopping_cart(request)
            shoppingCart.user = None
            shoppingCart.save()
            create_new_shopping_cart_for_user(request.user)
            return redirect('successful_order')
    return render(request, 'delivery_info.html', {
        'form': form,
        'total_price': total_price
    })


def successful_order(request):
    return render(request, 'successful_order.html', {})


def calculate_total_price_for_current_user_shopping_cart(request):
    shoppingCart = get_current_custom_user_shopping_cart(request)
    cart_items = CartItem.objects.all().filter(cart=shoppingCart)
    total_price = sum([cartitem.subtotal() for cartitem in cart_items])
    return total_price


def get_current_custom_user(request):
    return CustomUser.objects.all().filter(user=request.user).first()


def get_current_custom_user_shopping_cart(request):
    return ShoppingCart.objects.all().filter(user=get_current_custom_user(request)).first()


def get_current_custom_user_orders(request):
    return Order.objects.all().filter(user=get_current_custom_user(request))


def get_parts_in_order(order):
    cart_items = CartItem.objects.all().filter(cart=order.cart)
    return cart_items


def get_delivery_for_order(order):
    return Delivery.objects.all().filter(order=order).first()


def order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    cart_items = get_parts_in_order(order)
    delivery = get_delivery_for_order(order)
    total_price = sum([cartitem.subtotal() for cartitem in cart_items])
    return render(request, 'order_details.html',
                  {'order': order, 'cart_items': cart_items, 'delivery': delivery, 'total_price': total_price})


def create_new_shopping_cart_for_user(current_user):
    cart = ShoppingCart(user=CustomUser.objects.all().filter(user=current_user).first())
    cart.save()


def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('shopping_cart')


def admin_orders(request):
    return render(request, 'admin_orders.html', {
        'orders': Order.objects.all()
    })


def add_part(request):
    form = PartForm()
    if request.method == 'POST':
        form = PartForm(request.POST, request.FILES)
        if form.is_valid():
            part = form.save(commit=False)
            part.user = get_current_custom_user(request)
            part.save()
            return redirect('parts')
    return render(request, 'add_part.html', {'form': form})


def change_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.order_status = 'Delivered'
    order.save()
    return redirect('admin_orders')
