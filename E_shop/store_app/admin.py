from django.contrib import admin

# Register your models here.
from.models import *

class ImageTublerinline(admin.TabularInline):
    model = Images

class TagTublerinline(admin.TabularInline):
    model = Tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageTublerinline,TagTublerinline]


class OrderItemTublerinline(admin.TabularInline):
    model= OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTublerinline]



admin.site.register(Images)
admin.site.register(Tag)

admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Colour)
admin.site.register(Filter_Price)
admin.site.register(Product,ProductAdmin)
admin.site.register(Contact_us)


admin.site.register(Order)
admin.site.register(OrderItem)