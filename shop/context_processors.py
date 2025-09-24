def cart(request):
    """
    Делает доступным в шаблонах переменную cart_count.
    Корзина хранится в сессии так: {"<item_id>": qty, ...}
    """
    cart = request.session.get("cart", {})
    if isinstance(cart, dict):
        count = sum(int(q) for q in cart.values())
    else:
        count = 0
    return {"cart_count": count}
