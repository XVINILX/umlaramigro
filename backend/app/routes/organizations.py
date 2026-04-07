from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from app.utils.dependencies import get_current_user
from app.schemas import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
    OrganizationResponseWithPets,
)
from app.services import OrganizationService
from app.repositories import IOrganizationRepository
from app.repositories.factory import get_organization_repository

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.post("/", response_model=OrganizationResponse)
async def create_organization(
    org: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
):
    """Create a new organization."""
    try:
        org_service = OrganizationService(org_repo)
        result = await org_service.create_organization(org, current_user.id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[OrganizationResponse])
async def list_organizations(org_repo: IOrganizationRepository = Depends(get_organization_repository)):
    """List all organizations."""
    org_service = OrganizationService(org_repo)
    return await org_service.list_organizations()

@router.get("/my-organizations", response_model=list[OrganizationResponseWithPets])
async def my_organizations(
    current_user: User = Depends(get_current_user),
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
):
    """List organizations owned by current user."""
    org_service = OrganizationService(org_repo)
    return await org_service.get_organizations_by_owner(current_user.id)

@router.get("/{org_id}", response_model=OrganizationResponseWithPets)
async def get_organization(
    org_id: int,
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
):
    """Get organization by ID."""
    org_service = OrganizationService(org_repo)
    org = await org_service.get_organization_by_id(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    return org

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    org_update: OrganizationUpdate,
    current_user: User = Depends(get_current_user),
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
):
    """Update organization."""
    try:
        org_service = OrganizationService(org_repo)
        org = await org_service.get_organization_by_id(org_id)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        if org.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this organization",
            )

        result = await org_service.update_organization(org_id, org_update)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{org_id}")
async def delete_organization(
    org_id: int,
    current_user: User = Depends(get_current_user),
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
):
    """Delete organization."""
    try:
        org_service = OrganizationService(org_repo)
        org = await org_service.get_organization_by_id(org_id)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        if org.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this organization",
            )

        await org_service.delete_organization(org_id)
        return {"message": "Organization deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
