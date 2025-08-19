from django.templatetags.static import static
from .models import Category, Product

CATEGORY_FALLBACKS = {
    Category.LIVESTOCK: "products/images/livestock.jpg",
    Category.CROPS: "products/images/crops.jpg",
    Category.FRUITS: "products/images/fruits.jpg",
    Category.VEGETABLES: "products/images/vegetables.jpg",
    Category.GRAINS: "products/images/grains.jpg",
}

DEFAULT_FALLBACK = "products/images/default.jpg"

def user_is_farmer(user) -> bool:
    # Works if you have a boolean field OR a group named "Farmer"
    if not user.is_authenticated:
        return False
    if hasattr(user, "is_farmer"):
        return bool(getattr(user, "is_farmer"))
    return user.groups.filter(name__iexact="Farmer").exists()

def product_image_url(product: Product) -> str:
    if product.has_image:
        return product.image.url
    # Fallback per category
    return static(CATEGORY_FALLBACKS.get(product.category, DEFAULT_FALLBACK))
