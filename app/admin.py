from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Customer, Product, Cart, OrderPlaced, Order


# ==================== STATUS COLOR MAP ====================
STATUS_COLORS = {
    'Pending':    ('#856404', '#fff3cd'),
    'Accepted':   ('#004085', '#cce5ff'),
    'Packed':     ('#6f42c1', '#e8d8ff'),
    'On The Way': ('#0c5460', '#d1ecf1'),
    'Delivered':  ('#155724', '#d4edda'),
    'Cancel':     ('#721c24', '#f8d7da'),
}


# ==================== CUSTOMER ====================
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display  = ('id', 'get_user', 'name', 'locality', 'city', 'zipcode', 'state')
    list_filter   = ('state', 'city')
    search_fields = ('user__username', 'name', 'city')
    ordering      = ('id',)
    list_per_page = 15

    def get_user(self, obj):
        return format_html('<strong>{}</strong>', obj.user.username if obj.user else '-')
    get_user.short_description = 'User'


# ==================== PRODUCT ====================
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display   = ('id', 'product_thumbnail', 'title', 'brand',
                      'category', 'selling_price', 'discounted_price', 'discount_percent')
    list_filter    = ('brand', 'category')
    search_fields  = ('title', 'brand')
    ordering       = ('id',)
    list_per_page  = 10
    readonly_fields = ('product_preview',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'brand', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('selling_price', 'discounted_price')
        }),
        ('Image', {
            'fields': ('product_image', 'product_preview')
        }),
    )

    def product_thumbnail(self, obj):
        if obj.product_image:
            return format_html(
                '<img src="{}" width="48" height="48" '
                'style="object-fit:cover; border-radius:4px;" />',
                obj.product_image
            )
        return format_html('<span class="no-image">-</span>')  # Safe HTML dash
    product_thumbnail.short_description = 'Image'
    # Or simply: return '-'  # Plain string (Django 6.0 handles it)
    # But safe HTML prevents markup stripping issues

    def product_preview(self, obj):
        if obj.product_image:
            return format_html(
                '<img src="{}" style="max-height:200px; max-width:200px; object-fit:contain;" />',
                obj.product_image
            )
        return '-'
    product_preview.short_description = 'Preview'

    def discount_percent(self, obj):
        try:
            if obj.selling_price and obj.selling_price > 0:
                pct = round((1 - obj.discounted_price / obj.selling_price) * 100)
                color = '#27ae60' if pct > 20 else '#f39c12'
                return format_html(
                    '<span style="color:{};font-weight:600;">{} off</span>',
                    color,
                    f"{pct}%"
                )
        except Exception:
            pass
        return format_html('<span>-</span>')  # Safe HTML dash [web:5]
    discount_percent.short_description = 'Discount'


# ==================== CART ====================
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display  = ('id', 'get_user', 'get_product', 'quantity', 'get_item_total')
    search_fields = ('user__username', 'product__title')
    list_per_page = 15

    def get_user(self, obj):
        return obj.user.username if obj.user else '-'
    get_user.short_description = 'User'

    def get_product(self, obj):
        return obj.product.title if obj.product else '-'
    get_product.short_description = 'Product'

    def get_item_total(self, obj):
        if obj.product:
            total = obj.quantity * obj.product.discounted_price
            return format_html('<strong>Rs. {}</strong>', round(total, 2))
        return '-'
    get_item_total.short_description = 'Item Total'


# ==================== ORDER PLACED ====================
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display  = (
        'id', 'get_user', 'get_product', 'quantity',
        'get_total_cost', 'payment_method', 'get_paid_badge',
        'get_status_badge', 'change_status_dropdown', 'ordered_date'
    )
    list_filter   = ('status', 'payment_method', 'is_paid', 'ordered_date')
    search_fields = ('user__username', 'product__title', 'razorpay_order_id')
    readonly_fields = (
        'razorpay_signature', 'razorpay_payment_id',
        'razorpay_order_id', 'ordered_date'
    )
    ordering      = ('-ordered_date',)
    list_per_page = 15

    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'customer', 'product', 'quantity', 'ordered_date')
        }),
        ('Status & Payment', {
            'fields': ('status', 'payment_method', 'is_paid')
        }),
        ('Razorpay Details', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature'),
            'classes': ('collapse',),
        }),
    )

    def get_user(self, obj):
        return obj.user.username if obj.user else '-'
    get_user.short_description = 'User'

    def get_product(self, obj):
        return obj.product.title if obj.product else '-'
    get_product.short_description = 'Product'

    def get_total_cost(self, obj):
        if obj.product:
            total = obj.quantity * obj.product.discounted_price
            return format_html('<strong>Rs. {}</strong>', round(total, 2))
        return '-'
    get_total_cost.short_description = 'Total'

    def get_paid_badge(self, obj):
        if obj.is_paid:
            return format_html(
            '<span style="background:#d4edda;color:#155724;padding:3px 10px;'
            'border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            'Paid'  # 👈 Add this arg!
        )
        return format_html(
        '<span style="background:#fff3cd;color:#856404;padding:3px 10px;'
        'border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
        'Unpaid'  # 👈 Add this arg!
    )
    get_paid_badge.short_description = 'Payment'

    def get_status_badge(self, obj):
        text_color, bg_color = STATUS_COLORS.get(obj.status, ('#333', '#eee'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            bg_color, text_color, obj.status
        )
    get_status_badge.short_description = 'Status'

    def change_status_dropdown(self, obj):
        # Build option tags as a plain string — NO format_html here to avoid {} clash
        status_choices = [
            'Pending', 'Accepted', 'Packed', 'On The Way', 'Delivered', 'Cancel'
        ]
        options = ''
        for s in status_choices:
            selected = ' selected' if obj.status == s else ''
            # Use mark_safe carefully — values are hardcoded, not user input
            options += '<option value="{val}"{sel}>{val}</option>'.format(
                val=s, sel=selected
            )

        html = (
            '<select onchange="updateOrderStatus({pk}, this.value)" '
            'style="padding:4px 8px;border:1px solid #ccc;border-radius:4px;font-size:12px;">'
            '{opts}'
            '</select>'
        ).format(pk=obj.pk, opts=options)

        return mark_safe(html)
    change_status_dropdown.short_description = 'Update Status'

    # Custom URL for AJAX status update
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom = [
            path(
                'update-order-status/<int:order_id>/<str:new_status>/',
                self.admin_site.admin_view(self.ajax_update_status),
                name='ajax_update_order_status',
            ),
        ]
        return custom + urls

    def ajax_update_status(self, request, order_id, new_status):
        from django.http import JsonResponse
        allowed = ['Pending', 'Accepted', 'Packed', 'On The Way', 'Delivered', 'Cancel']
        if new_status not in allowed:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
        try:
            order = OrderPlaced.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'success': True})
        except OrderPlaced.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})

    class Media:
        js = ('app/js/admin_status.js',)


# ==================== ORDER ====================
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display  = ('id', 'get_user', 'get_product', 'amount', 'get_paid_badge', 'created_at')
    list_filter   = ('is_paid',)
    search_fields = ('user__username',)
    ordering      = ('-created_at',)
    list_per_page = 15
    readonly_fields = (
        'razorpay_order_id', 'razorpay_payment_id',
        'razorpay_signature', 'created_at'
    )

    def get_user(self, obj):
        return obj.user.username if obj.user else '-'
    get_user.short_description = 'User'

    def get_product(self, obj):
        return obj.product.title if obj.product else '-'
    get_product.short_description = 'Product'

    def get_paid_badge(self, obj):
        if obj.is_paid:
            return format_html(
                '<span style="background:#d4edda;color:#155724;padding:3px 10px;'
                'border-radius:12px;font-size:12px;font-weight:600;">Paid</span>'
            )
        return format_html(
            '<span style="background:#fff3cd;color:#856404;padding:3px 10px;'
            'border-radius:12px;font-size:12px;font-weight:600;">Pending</span>'
        )
    get_paid_badge.short_description = 'Paid'
# ==================================================
# ADMIN SITE CUSTOMIZATION
# ==================================================
admin.site.site_header  = '🛍️ Lucky Store Admin'
admin.site.site_title   = 'Lucky Store'
admin.site.index_title  = 'Welcome to Lucky Store Dashboard'