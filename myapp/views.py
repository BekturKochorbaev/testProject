from django.views.generic import ListView, DetailView
from .models import Order, Item
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import stripe
from decimal import Decimal


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemListView(ListView):
    queryset = Item.objects.all()
    template_name = 'item_list.html'
    context_object_name = 'items'


class OrderListView(ListView):
    queryset = Order.objects.all()
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["STRIPE_PUBLISHABLE_KEY"] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    template_name = 'item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["STRIPE_PUBLISHABLE_KEY"] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class OrderBuyAPIView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        line_items = []

        for order_item in order.items.select_related('item'):
            unit_amount = int(order_item.order.order_price * Decimal('100'))
            line_items.append(
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': order_item.item.name,
                            'description': order_item.item.description,
                        },
                        'unit_amount': unit_amount,
                    },
                    'quantity': order_item.quantity,
                }
            )

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'http://127.0.0.1:8000/success/',
            cancel_url=f'http://127.0.0.1:8000/cancel/',
            metadata={
                'order_id': order.id,
            },
        )

        order.stripe_checkout_session_id = session.id
        order.save(update_fields=['stripe_checkout_session_id'])

        return Response(
            {
                'session_id': session.id,
                'session_url': session.url,
            }
        )


class ItemBuyAPIView(APIView):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        unit_amount = int(item.get_discount_price() * Decimal('100'))

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': unit_amount,
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )

        return Response({'session_id': session.id})
