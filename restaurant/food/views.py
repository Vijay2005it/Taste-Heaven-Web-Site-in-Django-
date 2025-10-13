from django.shortcuts import render, redirect, get_object_or_404
from .forms import FoodItemForm, LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import ContactMessage, FeedBack, FoodItem, Gallery, Order, GalleryOrder, Payments
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model



# ---------------------- MAIN PAGE ----------------------
def main_page(request):
    food_items = FoodItem.objects.all()
    gallery_images = Gallery.objects.all()
    return render(request, 'food/main.html', {
        'food_items': food_items,
        'gallery_images': gallery_images,
    })


# ---------------------- LOGIN PAGE ----------------------
def login_page(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        role = request.POST.get('user_type')

        if not role:
            messages.error(request, "Please select a role.")
            return render(request, 'food/login.html', {'form': form})

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user:
                if role != user.user_type:
                    messages.error(request, f"You must login as {user.user_type.capitalize()}.")
                    return redirect('food:login')

                login(request, user)

                if role == "admin":
                    return redirect('food:admin_dashboard')
                return redirect('food:main')
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'food/login.html', {'form': form})


# ---------------------- REGISTER PAGE ----------------------
def register_page(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registered Successfully')
            return redirect('food:main')
    else:
        form = RegisterForm()
    return render(request, 'food/register.html', {'form': form})


# ---------------------- ADMIN DASHBOARD ----------------------

@login_required(login_url='food:login')
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        messages.error(request, "Access Denied!")
        return redirect('food:main')

    food_items = FoodItem.objects.all()
    orders = Order.objects.all().select_related('item', 'user')
    gallery_orders = GalleryOrder.objects.all().select_related('gallery_item', 'user')
    contact_messages = ContactMessage.objects.all()
    gallery_images = Gallery.objects.all()
    payments = Payments.objects.all()
    feedbacks = FeedBack.objects.all()


    User = get_user_model()
    total_users = User.objects.count()
    total_food_orders = orders.count()
    total_gallery_orders = gallery_orders.count()

    total_revenue = 0
    for o in orders:
        total_revenue += o.item.price * o.quantity
    for g in gallery_orders:
        total_revenue += g.gallery_item.price * g.quantity

    return render(request, 'food/admin_dashboard.html', {
        'food_items': food_items,
        'orders': orders,
        'gallery_orders': gallery_orders,
        'messages': contact_messages,
        'gallery_images': gallery_images,
        'total_users': total_users,
        'total_food_orders': total_food_orders,
        'total_gallery_orders': total_gallery_orders,
        'total_revenue': total_revenue,
        'payments':payments,
        'feedbacks':feedbacks
    })


@login_required(login_url='food:login')
def mark_gallery_done(request, order_id):
    if request.user.user_type != 'admin':
        messages.error(request, "Access Denied!")
        return redirect('food:main')

    order = get_object_or_404(GalleryOrder, id=order_id)
    order.status = 'Completed'
    order.save()
    messages.success(request, f"Gallery Order #{order.id} marked as completed.")
    return redirect('food:admin_dashboard')



# ---------------------- FOOD MANAGEMENT ----------------------
@login_required(login_url='food:login')
def add_food(request):
    if request.user.user_type != 'admin':
        messages.error(request, "Access Denied!")
        return redirect('food:main')

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item added successfully!")
            return redirect('food:admin_dashboard')
    else:
        form = FoodItemForm()
    return render(request, 'food/add_food.html', {'form': form})


@login_required(login_url='food:login')
def edit_food(request, food_id):
    if not request.user.is_authenticated or request.user.user_type != 'admin':
        messages.error(request, "Access Denied")
        return redirect('food:main')

    food_item = get_object_or_404(FoodItem, id=food_id)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item updated successfully!")
            return redirect('food:admin_dashboard')
    else:
        form = FoodItemForm(instance=food_item)
    return render(request, 'food/edit_food.html', {'form': form, 'food_item': food_item})


@login_required(login_url='food:login')
def delete_food(request, food_id):
    if not request.user.is_authenticated or request.user.user_type != 'admin':
        messages.error(request, "Access Denied")
        return redirect('food:main')
    food_item = get_object_or_404(FoodItem, id=food_id)
    food_item.delete()
    messages.success(request, "Food Item Deleted Successfully")
    return redirect('food:admin_dashboard')


# ---------------------- ORDER ----------------------
@login_required(login_url='food:login')
def order_page(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)

    if request.method == "POST":
        # ensure quantity comes from form
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

        # create a Pending order
        Order.objects.create(user=request.user, item=item, quantity=quantity)
        # redirect to checkout so user can confirm and pay
        return redirect('food:checkout')

    return render(request, 'food/order_page.html', {'item': item})


@login_required(login_url='food:login')
def mark_order_completed(request, order_id):
    # admin action to mark a single order completed
    if not request.user.is_authenticated or request.user.user_type != 'admin':
        messages.error(request, "Access Denied!")
        return redirect('food:main')

    order = get_object_or_404(Order, id=order_id)
    order.status = 'Completed'
    order.save()
    messages.success(request, f"Order #{order.id} marked as completed!")
    return redirect('food:admin_dashboard')


@login_required(login_url='food:login')
def mark_done(request, order_id):
    if request.user.user_type != 'admin':
        messages.error(request, "Access Denied!")
        return redirect('food:main')

    order = get_object_or_404(Order, id=order_id)
    order.status = 'Completed'
    order.save()
    messages.success(request, f"Order #{order.id} marked as completed.")
    return redirect('food:admin_dashboard')



# ---------------------- CONTACT ----------------------
def contact_page(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        messages.success(request, "Your Message was sent Successfully")
        return redirect("food:main")
    return render(request, 'food/contact.html')


# ---------------------- GALLERY ----------------------
@login_required(login_url='food:login')
def add_gallery(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        price_input = request.POST.get('price', '').replace(',', '')

        try:
            price = Decimal(price_input)
            if price > Decimal('999999.99') or price < 0:
                messages.error(request, "Price must be between 0 and 999,999.99.")
                return redirect('food:add_gallery')
        except (InvalidOperation, TypeError):
            messages.error(request, "Invalid price format.")
            return redirect('food:add_gallery')

        if not image or not caption:
            messages.error(request, "Both image and caption are required.")
            return redirect('food:add_gallery')

        Gallery.objects.create(image=image, price=price, caption=caption)
        messages.success(request, "Image Added Successfully")
        return redirect('food:admin_dashboard')

    return render(request, 'food/add_gallery.html')


@login_required(login_url='food:login')
def delete_gallery(request, id):
    gallery_item = get_object_or_404(Gallery, id=id)
    gallery_item.delete()
    messages.success(request, "Image Deleted Successfully")
    return redirect('food:admin_dashboard')


# ---------------------- ABOUT PAGE ----------------------
def about_page(request):
    return render(request, 'food/about_page.html')


# ---------------------- GALLERY ORDER ----------------------
@login_required(login_url='food:login')
def gallery_order_page(request, item_id):
    gallery_item = get_object_or_404(Gallery, id=item_id)

    if request.method == "POST":
        quantity = request.POST.get("quantity")

        # ✅ safe quantity check
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

        # ✅ Create the order entry in database
        order = GalleryOrder.objects.create(
            user=request.user,
            gallery_item=gallery_item,
            quantity=quantity,
            status="Pending"
        )

        order.save()  # ensure save (not strictly needed but safe)

        messages.success(request, "✅ Your gallery order has been placed successfully!")
        return redirect('food:checkout')

    return render(request, 'food/gallery_order.html', {'item': gallery_item})





# ---------------------- CHECKOUT & PAYMENT ----------------------
@login_required(login_url='food:login')
def checkout(request):
    food_orders = Order.objects.filter(user=request.user, status='Pending')
    gallery_orders = GalleryOrder.objects.filter(user=request.user, status='Pending')

    total = sum(o.item.price * o.quantity for o in food_orders) + \
            sum(g.gallery_item.price * g.quantity for g in gallery_orders)

    if not food_orders.exists() and not gallery_orders.exists():
        messages.info(request, "Your cart is empty.")
        return redirect('food:main')

    if request.method == "POST":
        request.session['checkout_total'] = float(total)
        return redirect('food:payment')

    return render(request, 'food/checkout.html', {
        'food_orders': food_orders,
        'gallery_orders': gallery_orders,
        'total': total
    })


@login_required(login_url='food:login')
def payment(request):
    food_orders = Order.objects.filter(user=request.user, status='Pending')
    gallery_orders = GalleryOrder.objects.filter(user=request.user, status='Pending')
    total = request.session.get('checkout_total', 0)

    if not food_orders.exists() and not gallery_orders.exists():
        messages.info(request, "No items to pay for.")
        return redirect('food:main')

    if request.method == "POST":
        data = request.POST

        Payments.objects.create(
            user=request.user,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            address=data.get('address'),
            country=data.get('country'),
            state=data.get('state'),
            pin_code=data.get('pin_code'),
            payment_method=data.get('payment_method'),
            bank_on_card=data.get('name_on_card'),
            card_number=data.get('card_number'),
            expiration_date=data.get('expiration_date'),
            cvv=data.get('cvv'),
            amount=total
        )

        for o in food_orders:
            o.status = 'Completed'
            o.save()

        for g in gallery_orders:
            g.status = 'Completed'
            g.save()

        messages.success(request, "✅ Payment successful! Your order is now complete.")
        return redirect('food:order_success')

    return render(request, 'food/payment.html', {'total': total})


def order_sucess(request): 
    return render(request,'food/order_success.html')

def feedback(request):
    if request.method == "POST":
        message = request.POST.get('message')
        rating = request.POST.get('rating')
        FeedBack.objects.create(user = request.user,message = message ,rating = rating)
        messages.success(request,"Thank You For Your Feed Back ")
        return redirect('food:main')
    feedbacks = FeedBack.objects.filter(user = request.user).order_by('-created_at')
    return render(request,'food/feedback.html',{'feedbacks':feedbacks})