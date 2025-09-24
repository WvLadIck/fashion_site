from decimal import Decimal

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from .models import Category, Item

from django.views.decorators.http import require_POST
from django.http import JsonResponse
def about(request):
    return render(request, "about.html")
@require_POST
def delete_from_cart(request, slug: str) -> JsonResponse:
    item = get_object_or_404(Item, slug=slug, is_available=True)
    cart = _get_cart(request)
    key = str(item.id)
    if key in cart:
        del cart[key]
        request.session.modified = True
    return JsonResponse({"ok": True, "count": _cart_count(cart)})

# ----------------------- helpers -----------------------
@require_POST
def update_cart(request: HttpRequest, item_id: int) -> HttpResponse:
    item = get_object_or_404(Item, id=item_id, is_available=True)
    try:
        qty = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty = 1

    cart = _get_cart(request)
    key = str(item.id)

    if qty <= 0:
        cart.pop(key, None)
    else:
        cart[key] = qty

    request.session.modified = True
    return redirect("cart_detail")

def home(request):
    return render(request, "home.html")
def _get_cart(request: HttpRequest) -> dict:
    """
    Корзина в сессии: ключ — str(item.id), значение — qty (int).
    """
    cart = request.session.setdefault("cart", {})
    return cart

def _cart_count(cart: dict) -> int:
    return sum(int(q) for q in cart.values())

# ----------------------- catalog -----------------------

from decimal import Decimal, InvalidOperation

def items_list(request: HttpRequest) -> HttpResponse:
    qs = (Item.objects.filter(is_available=True)
          .select_related("category").prefetch_related("photos"))

    # категория
    cat_slug = request.GET.get("cat") or ""
    current_category = None
    if cat_slug:
        qs = qs.filter(category__slug=cat_slug)
        current_category = Category.objects.filter(slug=cat_slug).first()

    # цены
    price_min = request.GET.get("price_min") or ""
    price_max = request.GET.get("price_max") or ""
    try:
        if price_min != "":
            qs = qs.filter(price__gte=Decimal(price_min))
        if price_max != "":
            qs = qs.filter(price__lte=Decimal(price_max))
    except InvalidOperation:
        pass  # тихо игнорим кривые числа

    # сортировка: price_asc | price_desc | name_asc (по желанию)
    order = request.GET.get("order") or ""
    if order == "price_asc":
        qs = qs.order_by("price")
    elif order == "price_desc":
        qs = qs.order_by("-price")
    elif order == "name_asc":
        qs = qs.order_by("name")
    else:
        qs = qs.order_by("id")  # дефолт

    categories = Category.objects.all().order_by("name")
    selected = {
        "price_min": price_min,
        "price_max": price_max,
        "order": order,
    }
    ctx = {"items": qs, "categories": categories,
           "current_category": current_category, "selected": selected}
    return render(request, "items_list.html", ctx)


# ----------------------- cart -----------------------

@require_POST
def add_to_cart(request, slug: str):
    item = get_object_or_404(Item, slug=slug, is_available=True)
    try:
        qty_add = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty_add = 1
    qty_add = max(1, qty_add)

    cart = _get_cart(request)
    key = str(item.id)
    cart[key] = int(cart.get(key, 0)) + qty_add
    request.session.modified = True
    return JsonResponse({"ok": True, "count": _cart_count(cart), "qty": cart[key]})

@require_POST
def remove_from_cart(request: HttpRequest, slug: str) -> JsonResponse:
    item = get_object_or_404(Item, slug=slug, is_available=True)
    cart = _get_cart(request)
    key = str(item.id)
    if key in cart:
        cart[key] = int(cart[key]) - 1
        if cart[key] <= 0:
            del cart[key]
        request.session.modified = True
    return JsonResponse({"ok": True, "count": _cart_count(cart), "qty": cart.get(key, 0)})

def cart_clear(request: HttpRequest) -> HttpResponse:
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("cart_detail")

def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = request.session.get("cart", {})
    ids = [int(k) for k in cart.keys()]
    items = Item.objects.filter(id__in=ids).select_related("category").prefetch_related("photos")

    lines = []
    total = Decimal("0.00")
    for item in items:
        qty = int(cart.get(str(item.id), 0))
        subtotal = item.price * qty
        total += subtotal
        lines.append({"item": item, "qty": qty, "subtotal": subtotal})

    ctx = {"items": lines, "total": total}
    return render(request, "cart.html", ctx)

from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Item

def checkout(request):
    """
    Страница оформления: берём позиции из сессии (как в cart_detail)
    и показываем список + итог.
    Если корзина пуста — отправим обратно в корзину.
    """
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("cart_detail")

    ids = [int(k) for k in cart.keys()]
    items = Item.objects.filter(id__in=ids).select_related("category")

    lines = []
    total = Decimal("0.00")
    for item in items:
        qty = int(cart.get(str(item.id), 0))
        subtotal = item.price * qty
        total += subtotal
        lines.append({"item": item, "qty": qty, "subtotal": subtotal})

    ctx = {"items": lines, "total": total}
    return render(request, "checkout.html", ctx)