from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    image = models.ImageField(upload_to="items/", blank=True, null=True)  # запасное базовое фото
    is_available = models.BooleanField(default=True)
    # делаем slug не обязательным, чтобы не падали миграции на существующих строках
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def main_photo(self):
        """
        Главное фото из ItemPhoto(kind='main').
        Если нет — вернём None (в шаблоне упадём на item.image).
        """
        return self.photos.filter(kind="main").order_by("order", "id").first()


class ItemPhoto(models.Model):
    KIND_CHOICES = (("main", "Главное"), ("small", "Маленькое"))
    item = models.ForeignKey(Item, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="items/")
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default="small")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        # get_kind_display — стандартный метод Django для полей с choices
        return f"{self.item.name} — {self.get_kind_display()} ({self.order})"
