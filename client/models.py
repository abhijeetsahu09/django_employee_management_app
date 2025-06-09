from django.db import models

class Client(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('old', 'Old'),
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pending_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    work_completed = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    logo = models.ImageField(upload_to='client_logos/', blank=True, null=True)

    def __str__(self):
        return self.name