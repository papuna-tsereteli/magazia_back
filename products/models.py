from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField("კატეგორიის სახელი", max_length=100, unique=True)
    created_at = models.DateTimeField("შექმნის თარიღი", default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "კატეგორია"
        verbose_name_plural = "კატეგორიები"


class Product(models.Model):
    class HomepagePlacement(models.TextChoices):
        NONE = 'NONE', 'არ არის ნაჩვენები'
        SLIDER = 'SLIDER', 'სლაიდერი'
        FEATURED = 'FEATURED', 'რჩეული პროდუქტი'

    name = models.CharField("დასახელება", max_length=200)
    description = models.TextField("აღწერა")
    price = models.DecimalField("ფასი", max_digits=10, decimal_places=2)

    # Updated main image field with help text
    image = models.ImageField(
        "პროდუქტის სურათი",
        upload_to='products/',
        help_text="რეკომენდებული ზომა: 800x800 პიქსელი"
    )

    # New dedicated slider image field
    slider_image = models.ImageField(
        "სლაიდერის სურათი",
        upload_to='sliders/',
        blank=True,
        null=True,
        help_text="რეკომენდებული ზომა: 1920x800 პიქსელი"
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="კატეგორია")
    popularity = models.PositiveIntegerField("პოპულარულობა", default=0)
    created_at = models.DateTimeField("შექმნის თარიღი", default=timezone.now)

    homepage_placement = models.CharField(
        "განთავსება მთავარ გვერდზე",
        max_length=10,
        choices=HomepagePlacement.choices,
        default=HomepagePlacement.NONE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "პროდუქტი"
        verbose_name_plural = "პროდუქტები"

