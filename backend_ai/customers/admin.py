from django.contrib import admin


from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "external_user", "email", "stripe_customer_id", "created_at"]
    search_fields = ["email", "stripe_customer_id"]
    list_filter = ["created_at"]
    ordering = ["-created_at"]


admin.site.register(Customer, CustomerAdmin)
