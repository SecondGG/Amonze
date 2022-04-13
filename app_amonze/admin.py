from django.contrib import admin
from app_amonze.models import Customer,Item,Transaction,ShippingAddress,TransactionItem

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'user', 'firstname','lastname','date_of_birth','email','address','postcode']

admin.site.register(Customer,CustomerAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_id','item_name','description','price']

admin.site.register(Item,ItemAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'customer', 'date_ordered', 'complete']
    # list_editable = ['return_date','cost']

admin.site.register(Transaction,TransactionAdmin)

class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'transaction', 'quantity']
    # list_editable = ['return_date','cost']

admin.site.register(TransactionItem,TransactionItemAdmin)

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'customer', 'address', 'postcode']
    # list_editable = ['return_date','cost']

admin.site.register(ShippingAddress,ShippingAddressAdmin)