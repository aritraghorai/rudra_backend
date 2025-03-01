from django.shortcuts import render, redirect
from orders.models import Order
from django.contrib import messages
from django.shortcuts import get_object_or_404


def orders_list(request):
    orders = (
        Order.objects.select_related("user", "shipping_address")
        .prefetch_related(
            "items__variant__product__images", "items__variant__size", "items__design"
        )
        .all()
    )
    return render(
        request,
        "orders/orders_list.html",
        {"orders": orders, "status_choices": Order.STATUS_CHOICES},
    )


def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        order.status = request.POST.get("status")
        order.save()
        messages.success(request, "Order status updated successfully")
    return redirect("orders_list")
