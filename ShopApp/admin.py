from django.contrib import admin
from .models import *

class ImagesTabularInline(admin.TabularInline):
    model = Images

class TagTabularInline(admin.TabularInline):
    model = Tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTabularInline, TagTabularInline]
    # ImagesTabularInline and TagTabularInline Classes:

# These are inline classes that define how the related models (Images and Tag) should be displayed and edited inline within the parent model's admin page.
# admin.TabularInline is used when you want to display the related models in a tabular format (similar to a table).
# ProductAdmin Class:

# This class defines the configuration for the Product model in the admin interface.
# The inlines attribute specifies which inline classes should be used to manage related models. In this case, it includes ImagesTabularInline and TagTabularInline.
# As a result, when you view or edit a Product in the Django admin, you will see the associated Images and Tag models displayed inline, and you can add/edit them without leaving the Product admin page.

######################ORDER ITEMS##########
class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemTabularInline]


admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
admin.site.register(Tag)
admin.site.register(Contact_us)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
