from django.db import models

class Products(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('shoe', 'Shoe'),
        ('ball', 'Ball'),
        ('sock', 'Sock'),
        ('accessories', 'Accessories'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(default="")
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='jersey')
    products_solds = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @property
    def is_popular(self):
        return self.products_solds > 25
        
    def increment_solds(self):
        self.products_solds += 1
        self.save()