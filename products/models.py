from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="კატეგორიის სახელი")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "კატეგორია"
        verbose_name_plural = "კატეგორიები"
        ordering = ['name']


class Product(models.Model):
    # Choices for the new homepage_placement field
    PLACEMENT_CHOICES = [
        ('NONE', 'არ არის ნაჩვენები'),
        ('FEATURED', 'რჩეული პროდუქტი'),
        ('SLIDER', 'სლაიდერი'),
    ]

    name = models.CharField(max_length=200, verbose_name="დასახელება")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ფასი")
    description = models.TextField(verbose_name="აღწერა")
    image = models.ImageField(upload_to='products/', verbose_name="სურათი")
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="კატეგორია")
    popularity = models.PositiveIntegerField(default=0, verbose_name="პოპულარობა")
    date_added = models.DateField(auto_now_add=True, verbose_name="დამატების თარიღი")

    # Replaced is_featured with a choice field
    homepage_placement = models.CharField(
        max_length=10,
        choices=PLACEMENT_CHOICES,
        default='NONE',
        verbose_name="განთავსება მთავარ გვერდზე"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "პროდუქტი"
        verbose_name_plural = "პროდუქტები"
        ordering = ['-popularity']

