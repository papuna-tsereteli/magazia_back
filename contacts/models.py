from django.db import models
from products.models import Product


class Submission(models.Model):
    # Enum-style choices for the submission type
    SUBMISSION_TYPE_CHOICES = [
        ('PRODUCT', 'პროდუქტის შეძენა'),
        ('CONTACT', 'საკონტაქტო ფორმა'),
    ]

    name = models.CharField(max_length=100, verbose_name="სახელი")
    phone = models.CharField(max_length=50, verbose_name="ტელეფონის ნომერი")
    address = models.CharField(
        max_length=255,
        verbose_name="მისამართი",
        default="მისამართი მითითებული არ არის"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="რაოდენობა")
    comment = models.TextField(blank=True, null=True, verbose_name="კომენტარი")

    submission_type = models.CharField(
        max_length=10,
        choices=SUBMISSION_TYPE_CHOICES,
        verbose_name="ფორმის ტიპი"
    )

    # Link to a product, but make it optional (for the contact form)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="პროდუქტი"
    )

    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="გაგზავნის დრო")

    def __str__(self):
        return f"{self.name} - {self.get_submission_type_display()}"

    class Meta:
        verbose_name = "გაგზავნილი ფორმა"
        verbose_name_plural = "გაგზავნილი ფორმები"
        ordering = ['-submitted_at']