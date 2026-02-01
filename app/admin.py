from django.contrib import admin
from .models import(
    Customer,
    Product,
    Cart,
    OrderPlaced
)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_name', 'quantity']

    def product_name(self, obj):
        return obj.product.title

    product_name.short_description = "Product"


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']
    search_fields = ("user_username", "product_name", "razorpay_order_id")
    list_filter = ('status', 'ordered_date')
    readonly_fields = ("razorpay_signature", "razorpay_payment_id", "razorpay_order_id")

# Register your models here.
