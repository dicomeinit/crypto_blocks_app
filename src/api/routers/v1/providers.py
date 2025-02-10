from fastapi import APIRouter, Depends
from apps.blocks.models import Provider
from api.schemas import ProviderResponse
from api.services.user import get_current_user
from django.contrib.auth import get_user_model

router = APIRouter(prefix="/api/v1/providers", tags=["providers"])

User = get_user_model()


@router.get("/", response_model=list[ProviderResponse])
def get_providers(current_user: User = Depends(get_current_user)):  # noqa
    return Provider.objects.all()
