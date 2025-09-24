# shop/management/commands/bootstrap.py
from __future__ import annotations
from pathlib import Path
from decimal import Decimal

from django.core.management import BaseCommand, call_command
from django.conf import settings
from django.db import transaction

from shop.models import Category, Item, ItemPhoto

SENTINEL = Path(settings.BASE_DIR) / ".bootstrap_done"


def seed_items(categories: dict[str, Category]) -> list[dict]:
    sergi = categories["sergi"]
    bras = categories["braslety"]
    kolca = categories["kolca"]
    sets = categories["komplekty"]

    data = [
        # name, slug, price, category_slug, (big, s1, s2)
        ("Серьги Двойные", "sergi-dvoinye", "1700.00", "sergi",
         ("items/sergi-dvoinye/big.jpg", "items/sergi-dvoinye/s1.jpg", "items/sergi-dvoinye/s2.jpg")),
        ("Серьги Волна", "sergi-volna", "1500.00", "sergi",
         ("items/sergi-volna/big.jpg", "items/sergi-volna/s1.jpg", "items/sergi-volna/s2.jpg")),
        # ВАЖНО: это — КОЛЬЦА
        ("Кольца с Жемчугом", "kolca-s-zhemchugom", "1000.00", "kolca",
         ("items/kolca-s-zhemchugom/big.jpg", "items/kolca-s-zhemchugom/s1.jpg", "items/kolca-s-zhemchugom/s2.jpg")),
        ("Серьги Листья", "sergi-listya", "1500.00", "sergi",
         ("items/sergi-listya/big.jpg", "items/sergi-listya/s1.jpg", "items/sergi-listya/s2.jpg")),
        ("Серьги с Жемчугом", "sergi-s-zhemchugom", "2000.00", "sergi",
         ("items/sergi-s-zhemchugom/big.jpg", "items/sergi-s-zhemchugom/s1.jpg", "items/sergi-s-zhemchugom/s2.jpg")),
        ("Серьги Кольца", "sergi-kolca", "1200.00", "sergi",
         ("items/sergi-kolca/big.jpg", "items/sergi-kolca/s1.jpg", "items/sergi-kolca/s2.jpg")),
        ("Серьги Асимметрия", "sergi-asimmetriya", "2000.00", "sergi",
         ("items/sergi-asimmetriya/big.jpg", "items/sergi-asimmetriya/s1.jpg", "items/sergi-asimmetriya/s2.jpg")),
        ("Серьги с Сердечками", "sergi-serdechkami", "1500.00", "sergi",
         ("items/sergi-serdechkami/big.jpg", "items/sergi-serdechkami/s1.jpg", "items/sergi-serdechkami/s2.jpg")),
        ("Серьги Тройные", "sergi-troinye", "1700.00", "sergi",
         ("items/sergi-troinye/big.jpg", "items/sergi-troinye/s1.jpg", "items/sergi-troinye/s2.jpg")),
        ("Браслет Цепь", "braslet-cep", "2500.00", "braslety",
         ("items/braslet-cep/big.jpg", "items/braslet-cep/s1.jpg", "items/braslet-cep/s2.jpg")),
        ("Браслет Двойное", "braslet-dvoinoe", "5500.00", "braslety",
         ("items/braslet-dvoinoe/big.jpg", "items/braslet-dvoinoe/s1.jpg", "items/braslet-dvoinoe/s2.jpg")),
        ("Браслет Линия", "braslet-liniya", "4500.00", "braslety",
         ("items/braslet-liniya/big.jpg", "items/braslet-liniya/s1.jpg", "items/braslet-liniya/s2.jpg")),

        # --- Комплекты (папки должны соответствовать slug’ам ниже) ---
        ("Мраморный Комплект", "mramornyj-komplekt", "3500.00", "komplekty",
         ("items/mramornyj-komplekt/big.jpg", "items/mramornyj-komplekt/s1.jpg", "items/mramornyj-komplekt/s2.jpg")),
        ("Золотой Комплект", "zolotoj-komplekt", "3000.00", "komplekty",
         ("items/zolotoj-komplekt/big.jpg", "items/zolotoj-komplekt/s1.jpg", "items/zolotoj-komplekt/s2.jpg")),
        ("Комплект с Мишками", "komplekt-s-mishkami", "4000.00", "komplekty",
         ("items/komplekt-s-mishkami/big.jpg", "items/komplekt-s-mishkami/s1.jpg", "items/komplekt-s-mishkami/s2.jpg")),
        ("Жемчужный Комплект", "zhemchuzhnyj-komplekt", "1700.00", "komplekty",
         ("items/zhemchuzhnyj-komplekt/big.jpg", "items/zhemchuzhnyj-komplekt/s1.jpg",
          "items/zhemchuzhnyj-komplekt/s2.jpg")),
        ("Комплект Колец", "komplekt-kolec", "1200.00", "komplekty",
         ("items/komplekt-kolec/big.jpg", "items/komplekt-kolec/s1.jpg", "items/komplekt-kolec/s2.jpg")),
        ("Жемчужный Комплект 2", "zhemchuzhnyj-komplekt-2", "4000.00", "komplekty",
         ("items/zhemchuzhnyj-komplekt-2/big.jpg", "items/zhemchuzhnyj-komplekt-2/s1.jpg",
          "items/zhemchuzhnyj-komplekt-2/s2.jpg")),
    ]

    # конвертируем в словари для удобства
    as_dicts = []
    for name, slug, price, cat_slug, imgs in data:
        as_dicts.append({
            "name": name,
            "slug": slug,
            "price": Decimal(price),
            "category": {"sergi": sergi, "braslety": bras, "kolca": kolca, "komplekty": sets}[cat_slug],
            "images": imgs,
        })
    return as_dicts


class Command(BaseCommand):
    help = "Migrate DB and seed initial data once (idempotent)."

    def handle(self, *args, **options):
        # 1) миграции (на любой БД)
        self.stdout.write(self.style.WARNING("→ Running migrate ..."))
        call_command("migrate", interactive=False)

        # 2) если уже делали — выходим
        if SENTINEL.exists():
            self.stdout.write(self.style.SUCCESS("✓ Bootstrap already done — skipping."))
            return

        # 3) сидинг и правки путей
        with transaction.atomic():
            self._seed_all()

        # 4) создаём «флажок», чтобы больше не выполнять
        try:
            SENTINEL.write_text("done\n", encoding="utf-8")
        except Exception:
            # если файловая система read-only — просто молча продолжим
            pass

        self.stdout.write(self.style.SUCCESS("✓ Bootstrap finished."))

    # ---------- helpers ----------
    def _seed_all(self):
        # категории
        cats = {
            "sergi": Category.objects.get_or_create(name="Серьги", slug="sergi")[0],
            "braslety": Category.objects.get_or_create(name="Браслеты", slug="braslety")[0],
            "kolca": Category.objects.get_or_create(name="Кольца", slug="kolca")[0],
            "komplekty": Category.objects.get_or_create(name="Комплекты", slug="komplekty")[0],
        }

        items = seed_items(cats)

        created_or_updated = 0
        for row in items:
            name, slug, price, cat = row["name"], row["slug"], row["price"], row["category"]
            big, s1, s2 = row["images"]

            item, _created = Item.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "price": price, "category": cat, "image": big, "is_available": True},
            )
            # обновим поля каждый раз — идемпотентно
            item.name = name
            item.price = price
            item.category = cat
            item.image = big
            item.is_available = True
            item.save()

            # фото перезапишем под заданный порядок (идемпотентно)
            ItemPhoto.objects.filter(item=item).delete()
            ItemPhoto.objects.create(item=item, image=big, kind="main", order=0)
            ItemPhoto.objects.create(item=item, image=s1, kind="small", order=1)
            ItemPhoto.objects.create(item=item, image=s2, kind="small", order=2)

            created_or_updated += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Seeded items: {created_or_updated}"))
