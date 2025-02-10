from datetime import datetime

import requests
from core.celery import celery_app
from apps.blocks.models import Currency, Block, Provider


def _get_crypto_latest_block(currency: str) -> tuple[int, datetime]:
    url = f"https://api.blockchair.com/{currency}/blocks?limit=1"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()["data"][0]
    block_date = datetime.fromisoformat(data["time"])
    return data["id"], block_date


@celery_app.task
def fetch_latest_blocks():
    provider = Provider.objects.get(name="BlockChair")
    for currency in Currency.objects.all():
        block_number, block_date = _get_crypto_latest_block(currency.name.lower())
        print(f"Latest {currency.name} block: {block_number} at {block_date}")
        Block.objects.get_or_create(
            currency=currency,
            provider=provider,
            block_number=block_number,
            stored_at=block_date,
        )
