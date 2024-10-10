def cart_count(request):
    return {
        'cart_count': request.session.get("cart_count", 0),
    }
