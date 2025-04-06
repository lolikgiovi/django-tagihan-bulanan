from django.contrib import admin

from .models import Bills


class BillsAdmin(admin.ModelAdmin):
    list_display = ("user", "bill_name", "bill_amount", "payment_account")
    list_filter = ("user", "bill_name", "bill_amount", "payment_account")
    search_fields = ("user", "bill_name")


admin.site.register(Bills, BillsAdmin)
