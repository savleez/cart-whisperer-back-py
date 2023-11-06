from django.contrib import admin
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin
from import_export import resources


from api.grocery.models import (
    Brand,
    Store,
    StoreLocation,
    ProductCategory,
    Product,
    ShoppingList,
    ShoppingListItem,
)


# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ("name",)
#     search_fields = ("name",)


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


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "brand", "variants")
#     search_fields = ("name", "brand", "variants")
#     list_filter = ("category",)

#     list_editable = ("name", "brand", "variants")


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


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

    list_display = ("id", "name", "brand", "variants")
    search_fields = ("name", "brand", "variants")
    list_filter = ("category",)

    list_editable = ("name", "brand", "variants")


class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand

    def skip_row(self, instance, original, row, import_validation_errors):
        try:
            existing_instance = Brand.objects.get(name=instance.name)
            return True
        except Brand.DoesNotExist:
            return False


@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    resource_class = BrandResource

    list_display = ("name",)
    search_fields = ("name",)

    def before_import_row(self, row, **kwargs):
        brand_name = row.get("brand")
        if brand_name:
            brand, created = Brand.objects.get_or_create(name=brand_name)
            row["brand"] = brand.pk
