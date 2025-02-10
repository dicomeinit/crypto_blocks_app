from django.core.management import BaseCommand
from apps.blocks.models import Currency, Provider
import os


class Command(BaseCommand):
    help = "Initialize the system with the default currencies and providers"

    def handle(self, *args, **options):
        if Currency.objects.exists() or Provider.objects.exists():
            self.stdout.write(self.style.SUCCESS("The system is already initialized!"))
            return
        Currency.objects.bulk_create(
            [Currency(name="Bitcoin"), Currency(name="Ethereum")]
        )
        Provider.objects.bulk_create(
            [
                Provider(
                    name="CoinMarketCap",
                    api_key=os.getenv("COINMARKETCAP_API_KEY", "coinmarketcap-api-key"),
                ),
                Provider(name="BlockChair", api_key="blockchair-api-key"),
            ]
        )

        self.stdout.write(self.style.SUCCESS("Initialized successfully!"))
