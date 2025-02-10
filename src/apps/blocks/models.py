from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Block(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    block_number = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    stored_at = models.DateTimeField()

    def __str__(self):
        return f"{self.currency.name} - {self.block_number}"

    class Meta:
        unique_together = ("currency", "block_number")

    @property
    def currency_name(self):
        return self.currency.name

    @property
    def provider_name(self):
        return self.provider.name