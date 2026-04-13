from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import localtime
from .models import Customer, Product, Cart, OrderPlaced, Order


# ==================================================
# CUSTOMER ADMIN
# ==================================================
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display    = ['id', 'name', 'user_username', 'user_email', 'city', 'state', 'zipcode']
    list_filter     = ['state', 'city']
    search_fields   = ['name', 'user__username', 'user__email', 'city', 'locality']
    ordering        = ['name']
    readonly_fields = ['user']

    fieldsets = (
        ('User Account',  {'fields': ('user',)}),
        ('Personal Info', {'fields': ('name', 'locality', 'city', 'state', 'zipcode')}),
    )

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'
    user_username.admin_order_field = 'user__username'

    def user_email(self, obj):
        return obj.user.email or '-'
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'


# ==================================================
# PRODUCT ADMIN
# ==================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = [
        'id', 'product_image_preview', 'title', 'brand',
        'category', 'selling_price', 'discounted_price', 'discount_percent'
    ]
    list_filter   = ['category', 'brand']
    search_fields = ['title', 'brand', 'description']
    ordering      = ['category', 'title']
    list_per_page = 20

    fieldsets = (
        ('Product Info', {'fields': ('title', 'brand', 'category', 'description')}),
        ('Pricing',      {'fields': ('selling_price', 'discounted_price')}),
        ('Media',        {'fields': ('product_image',)}),
    )

    def product_image_preview(self, obj):
        if obj.product_image:
            return format_html(
                '<img src="{}" style="height:60px;width:60px;object-fit:contain;'
                'border:1px solid #eee;border-radius:4px;" />',
                obj.product_image.url
            )
        return '-'
    product_image_preview.short_description = 'Image'

    def discount_percent(self, obj):
        if obj.selling_price and obj.selling_price > 0:
            pct   = ((obj.selling_price - obj.discounted_price) / obj.selling_price) * 100
            color = '#27ae60' if pct >= 20 else '#e67e22' if pct >= 10 else '#888'
            return format_html(
                '<span style="color:{};font-weight:600;">{}</span>',
                color, '{:.0f}% off'.format(pct)
            )
        return '-'
    discount_percent.short_description = 'Discount'


# ==================================================
# CART ADMIN
# ==================================================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display  = [
        'id', 'user_username', 'product_title',
        'product_image_preview', 'quantity', 'item_total_display', 'has_payment'
    ]
    list_filter     = ['product__category']
    search_fields   = ['user__username', 'product__title']
    ordering        = ['-id']
    readonly_fields = [
        'user', 'product', 'quantity', 'amount',
        'razor_pay_order_id', 'razor_pay_payment_id', 'razorpay_payment_signature'
    ]
    list_per_page = 25

    def user_username(self, obj):
        return format_html('<strong>{}</strong>', obj.user.username)
    user_username.short_description = 'Customer'
    user_username.admin_order_field = 'user__username'

    def product_title(self, obj):
        return obj.product.title if obj.product else '-'
    product_title.short_description = 'Product'

    def product_image_preview(self, obj):
        if obj.product and obj.product.product_image:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;object-fit:contain;" />',
                obj.product.product_image.url
            )
        return '-'
    product_image_preview.short_description = 'Image'

    def item_total_display(self, obj):
        return format_html(
            '<span>&#8377;{}</span>',
            '{:.2f}'.format(float(obj.item_total))
        )
    item_total_display.short_description = 'Item Total'

    def has_payment(self, obj):
        if obj.razor_pay_payment_id:
            return format_html(
                '<span style="color:#27ae60;font-weight:600;">{}</span>', 'Paid'
            )
        return format_html(
            '<span style="color:#aaa;">{}</span>', 'Pending'
        )
    has_payment.short_description = 'Payment'


# ==================================================
# ORDER PLACED ADMIN
# ==================================================

class OrderStatusFilter(admin.SimpleListFilter):
    title          = 'Order Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('Pending',    'Pending'),
            ('Accepted',   'Accepted'),
            ('Packed',     'Packed'),
            ('On The Way', 'On The Way'),
            ('Delivered',  'Delivered'),
            ('Cancel',     'Cancelled'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class PaymentMethodFilter(admin.SimpleListFilter):
    title          = 'Payment Method'
    parameter_name = 'payment_method'

    def lookups(self, request, model_admin):
        return [
            ('COD',      'Cash on Delivery'),
            ('Razorpay', 'Razorpay (Online)'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(payment_method=self.value())
        return queryset


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'product_thumbnail', 'product_name',
        'quantity', 'total_cost_display', 'payment_method',
        'payment_status_badge', 'order_status_badge',
        'ordered_date_formatted', 'change_status_links',
    ]
    list_filter     = [OrderStatusFilter, PaymentMethodFilter, 'is_paid', 'ordered_date']
    search_fields   = [
        'user__username', 'user__email', 'customer__name',
        'product__title', 'razorpay_order_id', 'razorpay_payment_id'
    ]
    ordering        = ['-ordered_date']
    list_per_page   = 20
    date_hierarchy  = 'ordered_date'
    readonly_fields = [
        'user', 'customer', 'product', 'quantity', 'ordered_date',
        'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature',
        'is_paid', 'payment_method',
    ]

    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'customer', 'product', 'quantity', 'ordered_date')
        }),
        ('Order Status', {
            'fields': ('status',),
            'description': 'Change the status here — the customer sees this on their Orders page.'
        }),
        ('Payment Details', {
            'fields': (
                'payment_method', 'is_paid',
                'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature'
            ),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_accepted', 'mark_packed', 'mark_on_the_way', 'mark_delivered', 'mark_cancelled']

    # ── Display helpers ──

    def customer_name(self, obj):
        name  = obj.customer.name if obj.customer else obj.user.username
        email = obj.user.email or ''
        return format_html(
            '<div style="line-height:1.5;">'
            '<strong style="font-size:13px;">{}</strong><br>'
            '<span style="color:#888;font-size:11px;">{}</span>'
            '</div>',
            name, email
        )
    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'customer__name'

    def product_thumbnail(self, obj):
        if obj.product and obj.product.product_image:
            return format_html(
                '<img src="{}" style="height:55px;width:55px;object-fit:contain;'
                'border:1px solid #eee;border-radius:4px;" />',
                obj.product.product_image.url
            )
        return '-'
    product_thumbnail.short_description = 'Image'

    def product_name(self, obj):
        if obj.product:
            return format_html(
                '<div style="max-width:160px;line-height:1.5;">'
                '<span style="font-size:13px;font-weight:500;">{}</span><br>'
                '<span style="color:#aaa;font-size:11px;">{}</span>'
                '</div>',
                obj.product.title,
                obj.product.get_category_display()
            )
        return '-'
    product_name.short_description = 'Product'

    def total_cost_display(self, obj):
        return format_html(
            '<strong>&#8377;{}</strong>',
            '{:.2f}'.format(float(obj.total_cost))
        )
    total_cost_display.short_description = 'Total'

    def payment_status_badge(self, obj):
        if obj.is_paid:
            return format_html(
                '<span style="background:#d4edda;color:#155724;padding:3px 10px;'
                'border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
                'Paid'
            )
        return format_html(
            '<span style="background:#fff3cd;color:#856404;padding:3px 10px;'
            'border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
            'Pending'
        )
    payment_status_badge.short_description = 'Payment'

    def order_status_badge(self, obj):
        colors = {
            'Pending':    ('#fff3cd', '#856404'),
            'Accepted':   ('#cce5ff', '#004085'),
            'Packed':     ('#d1ecf1', '#0c5460'),
            'On The Way': ('#e2d9f3', '#4a235a'),
            'Delivered':  ('#d4edda', '#155724'),
            'Cancel':     ('#f8d7da', '#721c24'),
        }
        bg, fg = colors.get(obj.status, ('#eee', '#333'))
        return format_html(
            '<span style="background:{};color:{};padding:4px 12px;'
            'border-radius:12px;font-size:11px;font-weight:600;white-space:nowrap;">{}</span>',
            bg, fg, obj.status
        )
    order_status_badge.short_description = 'Status'

    def ordered_date_formatted(self, obj):
        dt = localtime(obj.ordered_date)
        return format_html(
            '<span style="font-size:12px;color:#555;">{}</span>',
            dt.strftime('%d %b %Y, %I:%M %p')
        )
    ordered_date_formatted.short_description = 'Ordered On'

    def change_status_links(self, obj):
        next_steps = {
            'Pending':    ('Accepted',   '#007bff', 'Accept'),
            'Accepted':   ('Packed',     '#17a2b8', 'Pack'),
            'Packed':     ('On The Way', '#6f42c1', 'Ship'),
            'On The Way': ('Delivered',  '#28a745', 'Deliver'),
        }
        if obj.status in next_steps:
            _next, color, label = next_steps[obj.status]
            return format_html(
                '<a href="/admin/app/orderplaced/{}/change/" '
                'style="background:{};color:#fff;padding:4px 10px;border-radius:4px;'
                'font-size:11px;font-weight:600;text-decoration:none;white-space:nowrap;">'
                '{}</a>',
                obj.id, color, '-> ' + label
            )
        if obj.status == 'Delivered':
            return format_html(
                '<span style="color:#28a745;font-size:12px;font-weight:600;">{}</span>',
                'Done'
            )
        if obj.status == 'Cancel':
            return format_html(
                '<span style="color:#dc3545;font-size:12px;">{}</span>',
                'Cancelled'
            )
        return '-'
    change_status_links.short_description = 'Next Step'

    # ── Bulk actions ──

    def mark_accepted(self, request, queryset):
        n = queryset.filter(status='Pending').update(status='Accepted')
        self.message_user(request, '{} order(s) marked as Accepted.'.format(n))
    mark_accepted.short_description = 'Mark selected as Accepted'

    def mark_packed(self, request, queryset):
        n = queryset.filter(status='Accepted').update(status='Packed')
        self.message_user(request, '{} order(s) marked as Packed.'.format(n))
    mark_packed.short_description = 'Mark selected as Packed'

    def mark_on_the_way(self, request, queryset):
        n = queryset.filter(status='Packed').update(status='On The Way')
        self.message_user(request, '{} order(s) marked as On The Way.'.format(n))
    mark_on_the_way.short_description = 'Mark selected as On The Way'

    def mark_delivered(self, request, queryset):
        n = queryset.update(status='Delivered', is_paid=True)
        self.message_user(request, '{} order(s) marked as Delivered.'.format(n))
    mark_delivered.short_description = 'Mark selected as Delivered'

    def mark_cancelled(self, request, queryset):
        n = queryset.update(status='Cancel')
        self.message_user(request, '{} order(s) marked as Cancelled.'.format(n))
    mark_cancelled.short_description = 'Mark selected as Cancelled'


# ==================================================
# ORDER (Razorpay) ADMIN
# ==================================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = [
        'id', 'user_username', 'product_title',
        'amount_display', 'payment_status', 'razorpay_order_id', 'created_at_formatted'
    ]
    list_filter     = ['is_paid', 'created_at']
    search_fields   = ['user__username', 'razorpay_order_id', 'razorpay_payment_id', 'product__title']
    ordering        = ['-created_at']
    readonly_fields = [
        'user', 'product', 'amount', 'razorpay_order_id',
        'razorpay_payment_id', 'razorpay_signature', 'created_at'
    ]
    list_per_page = 25

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Customer'

    def product_title(self, obj):
        return obj.product.title if obj.product else '-'
    product_title.short_description = 'Product'

    def amount_display(self, obj):
        return format_html(
            '<strong>&#8377;{}</strong>',
            '{:.2f}'.format(float(obj.amount))
        )
    amount_display.short_description = 'Amount'

    def payment_status(self, obj):
        if obj.is_paid:
            return format_html(
                '<span style="background:#d4edda;color:#155724;padding:3px 10px;'
                'border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
                'Paid'
            )
        return format_html(
            '<span style="background:#f8d7da;color:#721c24;padding:3px 10px;'
            'border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
            'Unpaid'
        )
    payment_status.short_description = 'Status'

    def created_at_formatted(self, obj):
        dt = localtime(obj.created_at)
        return dt.strftime('%d %b %Y, %I:%M %p')
    created_at_formatted.short_description = 'Created At'

# ==================================================
# ADMIN SITE CUSTOMIZATION
# ==================================================
admin.site.site_header  = '🛍️ Lucky Store Admin'
admin.site.site_title   = 'Lucky Store'
admin.site.index_title  = 'Welcome to Lucky Store Dashboard'