from django.db import models
from Ebookify.enums import ORDER_STATUS
import uuid


class Order(models.Model):
    order_Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_wrt_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(
        max_length=50, null=False, choices=ORDER_STATUS, default=ORDER_STATUS[0][0]
    )
    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now_add=True)
