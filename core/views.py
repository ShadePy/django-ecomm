from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView
from django.utils import timezone


class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    paginate_by = 1


class ProductView(DetailView):
    model = Item
    template_name = 'product.html'


class OrderSummaryView(ListView):
    model = Order
    template_name = 'order-summary.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # check if the item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, 'Your order was updated')
            return redirect('core:product', slug=slug)
        else:
            order.items.add(order_item)
            messages.success(request, 'The item was added into the cart')
            return redirect('core:product', slug=slug)

    else:
        date = timezone.now()
        order = Order.objects.create(user=request.user, order_date=date)
        order.items.add(order_item)
        messages.success(request, 'The item was added into the cart')
        return redirect('core:product', slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_item = OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False
    )[0]

    if order_qs.exists():
        order = order_qs[0]
        # check if the item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(order_item)
            messages.info(
                request, 'Your order was updated, the item was removed')
            return redirect('core:product', slug=slug)
        else:
            messages.warning(request, 'The item is not in the cart')
            return redirect('core:product', slug=slug)

    else:
        messages.warning(request, 'You do not have an active order')
        return redirect('core:product', slug=slug)


def checkout_page(request, *args, **kwargs):
    return render(request, 'checkout-page.html')
