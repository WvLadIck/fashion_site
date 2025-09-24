from django.contrib import admin
from .models import Category, Item, ItemPhoto

class ItemPhotoInline(admin.TabularInline):
    model = ItemPhoto
    extra = 1

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ItemPhotoInline]

admin.site.register(Category)
