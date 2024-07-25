from datetime import timezone
from django.db import models
from apps.base.models import BaseModel
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Coupon(BaseModel):
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    minimum_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    active = models.BooleanField(default=True)
    # customer_segments = models.ManyToManyField(CustomerSegment, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.get_discount_type_display()}: {self.discount}"

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

    def clean(self):
        if self.valid_from >= self.valid_to:
            raise ValidationError("'Valid from' date must be before 'Valid to' date.")
        
        if self.discount_type == 'percentage' and self.discount > 100:
            raise ValidationError("Percentage discount cannot be greater than 100%.")

    def apply_discount(self, order_total):
        if self.discount_type == 'percentage':
            return order_total * (self.discount / 100)
        else:  # fixed amount
            return min(self.discount, order_total)  # Ensure discount doesn't exceed order total

    def get_discount_display(self):
        if self.discount_type == 'percentage':
            return f"{self.discount}%"
        else:
            return f"${self.discount:.2f}"