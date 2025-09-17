from django.db import models

CATEGORY_CHOICES = [
    ('jersey', 'Jersey'),
    ('merch', 'Merchandise'),
    ('ticket', 'Ticket'),
]

class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(default="")
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='jersey')
    products_solds = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def is_popular(self):
        return self.products_solds > 25

    def purchase(self, quantity=1):
        if self.stock >= quantity:
            self.stock -= quantity
            self.products_solds += quantity
            self.save()
            return True
        return False
