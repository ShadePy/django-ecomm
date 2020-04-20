from django import template
from core.models import OrderItem


register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user=user, ordered=False)
        if qs.exists():
            total = 0
            for i in qs:
                total += i.quantity
            return total
    return 0
