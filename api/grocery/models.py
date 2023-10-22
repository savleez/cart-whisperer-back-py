from django.db import models


class Brand(models.Model):
    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Nombre",
    )

    def __str__(self):
        return self.name


class Store(models.Model):
    class Meta:
        verbose_name = "Tienda"
        verbose_name_plural = "Tiendas"

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Marca",
    )

    def __str__(self):
        return self.name


class StoreLocation(models.Model):
    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locales"

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Nombre",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Dirección",
    )
    store = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Tienda",
    )

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Nombre",
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Nombre",
    )
    brand = models.ForeignKey(
        to=Brand,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Marca",
    )
    variants = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Presentación",
    )
    category = models.ManyToManyField(
        to=ProductCategory,
        verbose_name="Categoría",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    class Meta:
        verbose_name = "Mercado"
        verbose_name_plural = "Mercados"

    details = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Detalles",
    )
    added = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Fecha de creación",
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Fecha de modificación",
    )

    def __str__(self):
        date_added = self.added.strftime("%Y-%m-%d %H:%M")
        return f"{self.id} - {date_added}"


class ShoppingListItem(models.Model):
    class Meta:
        verbose_name = "Producto de mercado"
        verbose_name_plural = "Productos de mercado"

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Producto",
    )
    shopping_list = models.ForeignKey(
        to=ShoppingList,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Lista de mercado",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name="Precio unitario",
    )
    quantity = models.IntegerField(
        blank=False,
        null=False,
        default=1,
        verbose_name="Cantidad",
    )

    @property
    def total_price(self):
        if self.id:
            return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.price}"
