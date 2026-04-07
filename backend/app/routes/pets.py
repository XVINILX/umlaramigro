from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from app.utils.dependencies import get_current_user
from app.schemas import PetCreate, PetResponse, PetUpdate, PetResponseWithInterests
from app.services import PetService, OrganizationService
from app.repositories import IPetRepository, IOrganizationRepository
from app.repositories.factory import get_pet_repository, get_organization_repository

router = APIRouter(prefix="/pets", tags=["pets"])

@router.post("/", response_model=PetResponse)
async def create_pet(
    pet: PetCreate,
    org_id: int,
    current_user: User = Depends(get_current_user),
    pet_repo: IPetRepository = Depends(get_pet_repository),
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
):
    """Create a new pet for an organization."""
    try:
        org_service = OrganizationService(org_repo)
        pet_service = PetService(pet_repo)
        
        org = await org_service.get_organization_by_id(org_id)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        if org.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to add pets to this organization",
            )

        result = await pet_service.create_pet(pet, org_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.get("/", response_model=list[PetResponse])
async def list_pets(
    pet_repo: IPetRepository = Depends(get_pet_repository),
):
    """List all pets available for adoption."""
    pet_service = PetService(pet_repo)
    return await pet_service.list_pets()

@router.get("/organization/{org_id}", response_model=list[PetResponse])
async def get_organization_pets(
    org_id: int,
    pet_repo: IPetRepository = Depends(get_pet_repository),
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
):
    """Get all pets from an organization."""
    org_service = OrganizationService(org_repo)
    pet_service = PetService(pet_repo)
    
    org = await org_service.get_organization_by_id(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    return await pet_service.get_pets_by_organization(org_id)

@router.get("/{pet_id}", response_model=PetResponseWithInterests)
async def get_pet(
    pet_id: int,
    pet_repo: IPetRepository = Depends(get_pet_repository),
):
    """Get pet by ID."""
    pet_service = PetService(pet_repo)
    pet = await pet_service.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found",
        )
    return pet

@router.put("/{pet_id}", response_model=PetResponse)
async def update_pet(
    pet_id: int,
    pet_update: PetUpdate,
    current_user: User = Depends(get_current_user),
    pet_repo: IPetRepository = Depends(get_pet_repository),
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
):
    """Update pet information."""
    try:
        pet_service = PetService(pet_repo)
        org_service = OrganizationService(org_repo)
        
        pet = await pet_service.get_pet_by_id(pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found",
            )

        org = await org_service.get_organization_by_id(pet.organization_id)
        if org.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this pet",
            )

        result = await pet_service.update_pet(pet_id, pet_update)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("/{pet_id}")
async def delete_pet(
    pet_id: int,
    current_user: User = Depends(get_current_user),
    pet_repo: IPetRepository = Depends(get_pet_repository),
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
):
    """Delete a pet."""
    try:
        pet_service = PetService(pet_repo)
        org_service = OrganizationService(org_repo)
        
        pet = await pet_service.get_pet_by_id(pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found",
            )

        org = await org_service.get_organization_by_id(pet.organization_id)
        if org.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this pet",
            )

        await pet_service.delete_pet(pet_id)
        return {"message": "Pet deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
