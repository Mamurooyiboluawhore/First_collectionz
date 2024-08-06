from django.db import models

# Create your models here.
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    user =  models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'payment'
