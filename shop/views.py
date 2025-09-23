from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Item, Category
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

def items_list(request):
    items = Item.objects.all()

    category = request.GET.get("category")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")
    material = request.GET.get("material")

    if category:
        items = items.filter(category__slug=category)
    if price_min:
        items = items.filter(price__gte=price_min)
    if price_max:
        items = items.filter(price__lte=price_max)
    if material:
        items = items.filter(material__iexact=material)

    return render(request, "shop/items_list.html", {"items": items})

def add_item(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST.get("description", "")
        price = request.POST["price"]
        category_id = request.POST["category"]
        image = request.FILES["image"]

        category = Category.objects.get(id=category_id)

        Item.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image,
        )
        return redirect("items_list")

    categories = Category.objects.all()
    return render(request, "shop/add_item.html", {"categories": categories})


def items_json(request):
    items = Item.objects.all().select_related("category")
    data = [
        {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": str(item.price),
            "category": item.category.name,
            "image_url": item.image.url if item.image else None,
        }
        for item in items
    ]
    return JsonResponse(data, safe=False)

def add_to_cart(request, item_id):
    cart = request.session.get("cart", {})
    quantity = int(request.POST.get("quantity", 1))
    if str(item_id) in cart:
        cart[str(item_id)] += quantity
    else:
        cart[str(item_id)] = quantity
    request.session["cart"] = cart
    return redirect("cart_detail")

def cart_detail(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0
    for item_id, qty in cart.items():
        item = Item.objects.get(id=item_id)
        items.append({"item": item, "quantity": qty, "subtotal": item.price*qty})
        total += item.price*qty
    return render(request, "shop/cart.html", {"items": items, "total": total})
