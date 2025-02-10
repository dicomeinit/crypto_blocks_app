from django.contrib import admin
from .models import Currency, Provider, Block


admin.site.register(Currency)
admin.site.register(Provider)
admin.site.register(Block)
