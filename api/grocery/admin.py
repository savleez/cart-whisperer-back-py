from django.contrib import admin

from api.grocery.models import (
    Brand,
    Store,
    StoreLocation,
    ProductCategory,
    Product,
    ShoppingList,
    ShoppingListItem,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ("store", "name", "address")
    search_fields = ("store", "name", "address")
    list_filter = ("store",)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "variants")
    search_fields = ("name", "brand", "variants")
    list_filter = ("category",)

    list_editable = ("name", "brand", "variants")


class ShoppingListItemInline(admin.TabularInline):
    model = ShoppingListItem
    extra = 1

    def get_total_price(self, instance):
        return instance.total_price

    get_total_price.short_description = "Precio"

    readonly_fields = ("get_total_price",)  # Campo calculado


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("id", "added", "modified", "details")
    search_fields = ("id", "added", "modified", "details")

    inlines = [ShoppingListItemInline]


@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    def get_total_price(self, obj):
        return obj.total_price

    get_total_price.short_description = "Precio"

    list_display = ("product", "shopping_list", "quantity", "price", "get_total_price")
    search_fields = ("product", "shopping_list", "price")
