from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from apps.blocks.models import Block, Currency, Provider
from api.schemas import BlockResponse, PaginatedBlockResponse
from api.services.user import get_current_user
from django.contrib.auth import get_user_model


router = APIRouter(prefix="/api/v1/blocks", tags=["blocks"])
User = get_user_model()


@router.get("/", response_model=PaginatedBlockResponse)
def get_blocks(
    limit: int = Query(
        10, ge=1, le=100, description="Number of results to return (1-100)"
    ),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    current_user: User = Depends(get_current_user),  # noqa
):
    qs = Block.objects.select_related("provider", "currency").all()[
        offset : offset + limit
    ]
    results = []
    for block in qs:
        results.append(
            {
                "id": block.id,
                "currency_id": block.currency.id,
                "currency_name": block.currency_name,
                "provider_id": block.provider.id,
                "provider_name": block.provider_name,
                "block_number": block.block_number,
                "created_at": block.created_at.isoformat(),
                "stored_at": block.stored_at.isoformat(),
            }
        )

    return {
        "total": Block.objects.count(),
        "limit": limit,
        "offset": offset,
        "results": results,
    }


@router.get("/{block_id}/", response_model=BlockResponse)
def get_block(
    block_id: int,
    current_user: User = Depends(get_current_user),  # noqa
):
    try:
        return Block.objects.get(id=block_id)
    except Block.DoesNotExist:
        raise HTTPException(status_code=404, detail="Block not found")


@router.get("/search/", response_model=BlockResponse)
def search_blocks(
    currency: Optional[str] = Query(None, description="Currency of the block"),
    number: Optional[int] = Query(None, description="Block number"),
    provider: Optional[str] = Query(None, description="Provider of the block"),
    current_user: User = Depends(get_current_user),  # noqa
):
    if not (currency and number):
        raise HTTPException(
            status_code=400, detail="Currency or block number must be provided"
        )
    # validate currency and provider
    if Currency.objects.filter(name=currency).exists():
        raise HTTPException(status_code=400, detail="Invalid currency")
    if provider and not Provider.objects.filter(name=provider).exists():
        raise HTTPException(status_code=400, detail="Invalid provider")

    filters = {"currency__name": currency, "block_number": number}
    if provider:
        filters["provider__name"] = provider
    return Block.objects.filter(**filters).first()
