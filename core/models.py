from django.db import models
from django.conf import settings
from django.urls import reverse

category_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sportwear'),
    ('O', 'Outwear')
)

Label_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    item_name = models.CharField(max_length=17)
    category = models.CharField(
        choices=category_CHOICES, max_length=2, default='S')
    label = models.CharField(choices=Label_CHOICES, max_length=1, default='P')
    price = models.FloatField()
    slug = models.SlugField()
    discount_price = models.FloatField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'slug': self.slug})

    def __str__(self):
        return self.item_name


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
