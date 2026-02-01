from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced

# -------------------- CUSTOMER --------------------
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'locality', 'city', 'zipcode', 'state')
    list_filter = ('state', 'city')
    search_fields = ('user__username', 'name', 'city')
    ordering = ('id',)
    list_per_page = 10

# -------------------- PRODUCT --------------------
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'category', 'selling_price', 'discounted_price')
    list_filter = ('brand', 'category')
    search_fields = ('title', 'brand')
    ordering = ('id',)
    list_per_page = 10

# -------------------- CART --------------------
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_product', 'quantity')
    search_fields = ('user__username', 'product__title')
    autocomplete_fields = ('user', 'product')
    list_per_page = 10

    def get_product(self, obj):
        return obj.product.title
    get_product.short_description = "Product"

# -------------------- ORDER PLACED --------------------
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'get_product', 'quantity', 'status', 'ordered_date')
    list_editable = ('status',)  # status directly editable
    list_filter = ('status', 'ordered_date')
    search_fields = ('user__username', 'product__title', 'razorpay_order_id')
    readonly_fields = ('razorpay_signature', 'razorpay_payment_id', 'razorpay_order_id')
    autocomplete_fields = ('user', 'product', 'customer')
    ordering = ('-ordered_date',)
    list_per_page = 10

    def get_product(self, obj):
        return obj.product.title
    get_product.short_description = "Product"
