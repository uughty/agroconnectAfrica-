from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, Http404
from django.urls import reverse
from .models import Product, Category
from .forms import ProductForm
from .utils import user_is_farmer, product_image_url
from django.http import JsonResponse




def product_list(request: HttpRequest) -> HttpResponse:
    category = request.GET.get("category", "").strip()
    q = request.GET.get("q", "").strip()

    products = Product.objects.filter(is_active=True)
    if category in dict(Category.choices):
        products = products.filter(category=category)
    if q:
        products = products.filter(name__icontains=q)

    ctx = {
        "products": products,
        "Category": Category,
        "active_category": category,
        "query": q,
    }
    return render(request, "products/product_list.html", ctx)

def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk, is_active=True)
    ctx = {"product": product, "image_url": product_image_url(product)}
    return render(request, "products/product_detail.html", {"product": product})

# ---------- Farmer Views ----------

@login_required
def my_products(request: HttpRequest) -> HttpResponse:
    if not user_is_farmer(request.user):
        messages.error(request, "Only farmers can access this page.")
        return redirect("product_list")
    products = Product.objects.filter(farmer=request.user)
    return render(request, "products/my_products.html", {"products": products})

@login_required
def add_product(request: HttpRequest) -> HttpResponse:
    if not user_is_farmer(request.user):
        messages.error(request, "Only farmers can add products.")
        return redirect("product_list")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.farmer = request.user
            prod.save()
            messages.success(request, "Product added successfully.")
            return redirect("my_products")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form, "mode": "create"})

@login_required
def edit_product(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    if not user_is_farmer(request.user) or product.farmer != request.user:
        messages.error(request, "You do not have permission to edit this product.")
        return redirect("product_list")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect("my_products")
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"form": form, "mode": "edit", "product": product})

@login_required
def delete_product(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    if not user_is_farmer(request.user) or product.farmer != request.user:
        messages.error(request, "You do not have permission to delete this product.")
        return redirect("product_list")

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect("my_products")

    # Simple confirm screen
    return render(request, "products/confirm_delete.html", {"product": product})

# ---------- Cart (Session Based) ----------

CART_KEY = "cart_items"  # session key, store dict {product_id: qty}

def _get_cart(session):
    return session.get(CART_KEY, {})

def _save_cart(session, cart):
    session[CART_KEY] = cart
    session.modified = True

@login_required
def cart(request: HttpRequest) -> HttpResponse:
    cart = _get_cart(request.session)
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)
    items = []
    total = 0
    for p in products:
        qty = int(cart.get(str(p.id), 0))
        line_total = p.price * qty
        total += line_total
        items.append({"product": p, "qty": qty, "line_total": line_total, "image_url": product_image_url(p)})

    return render(request, "products/cart.html", {"items": items, "total": total})

@login_required
def add_to_cart(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method != "POST":
        raise Http404()

    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart = _get_cart(request.session)
    current = int(cart.get(str(product.id), 0))
    cart[str(product.id)] = current + 1
    _save_cart(request.session, cart)
    messages.success(request, f"Added {product.name} to cart.")
    return redirect("product_list")

@login_required
def remove_from_cart(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method != "POST":
        raise Http404()
    cart = _get_cart(request.session)
    if str(pk) in cart:
        del cart[str(pk)]
        _save_cart(request.session, cart)
        messages.info(request, "Item removed.")
    return redirect("cart")

@login_required
def clear_cart(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        raise Http404()
    _save_cart(request.session, {})
    messages.info(request, "Cart cleared.")
    return redirect("cart")

def product_search(request):
    """Return JSON for live search dropdown"""
    query = request.GET.get("q", "")
    products = Product.objects.filter(name__icontains=query)[:10]  # top 10 matches
    results = [{"id": p.id, "name": p.name} for p in products]
    return JsonResponse(results, safe=False)