from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название скидки")
    discount_percentage = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Процент скидки %')

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"{self.name} - {self.discount_percentage}%"


class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=100, decimal_places=2)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Скидка")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} - {self.price}"

    def get_discount_price(self):
        if not self.discount:
            return self.price

        discount_price = (self.discount.discount_percentage * self.price) / 100
        final_price = self.price - discount_price
        return final_price


class Order(models.Model):
    stripe_checkout_session_id = models.CharField(max_length=255, blank=True, editable=False, verbose_name="ID Checkout Session в Stripe")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    order_price = models.DecimalField(max_digits=1000, decimal_places=2, null=True, blank=True, verbose_name='Итого')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} {self.order_price}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    item = models.ForeignKey(Item, on_delete=models.CASCADE,  verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    total_price = models.DecimalField(max_digits=1000, decimal_places=2, verbose_name='Итого', null=True, blank=True)

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def save(self, *args, **kwargs):
        discount_price = (self.item.discount.discount_percentage * self.item.price) / 100
        final_price = self.item.price - discount_price
        self.total_price = self.quantity * final_price

        super(OrderItem, self).save(*args, **kwargs)

        order = self.order
        order.order_price = sum(
            item.total_price for item in order.items.all()
        )
        order.save(update_fields=["order_price"])