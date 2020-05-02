from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm


class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    paginate_by = 1


class ProductView(DetailView):
    model = Item
    template_name = 'product.html'


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            form = CheckoutForm()
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'form': form,
                'object': order
            }
            return render(self.request, 'checkout-page.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('core:home')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            messages.success(self.request, 'Valid')
            return redirect("core:checkout")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('core:home')


@login_required()
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
            return redirect('core:order-summary')
        else:
            order.items.add(order_item)
            messages.success(request, 'The item was added into the cart')
            return redirect('core:order-summary')

    else:
        date = timezone.now()
        order = Order.objects.create(user=request.user, order_date=date)
        order.items.add(order_item)
        messages.success(request, 'The item was added into the cart')
        return redirect('core:order-summary')


@login_required()
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(
                request, 'Your order was updated, the item was removed')
            return redirect('core:order-summary')
        else:
            messages.warning(request, 'The item is not in the cart')
            return redirect('core:order-summary')

    else:
        messages.warning(request, 'You do not have an active order')
        return redirect('core:order-summary')


@login_required()
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.success(request, 'The quantity is updated')
                return redirect('core:order-summary')
            else:
                order.items.remove(order_item)
                order_item.delete()
                return redirect('core:order-summary')
        else:
            messages.warning(request, 'The item is not in the cart')
            return redirect('core:order-summary')
    else:
        messages.warning(request, 'You do not have an active order')
        return redirect('core:order-summary')
