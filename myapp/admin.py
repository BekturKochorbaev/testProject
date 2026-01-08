from django.contrib import admin
from .models import Item, Discount, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('total_price',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percentage')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'order_price', 'is_paid', 'created_at')
    readonly_fields = ('order_price',)

