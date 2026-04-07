from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from app.utils.dependencies import get_current_user
from app.schemas import InterestFormCreate, InterestFormResponse
from app.services import InterestFormService, PetService, OrganizationService
from app.repositories import (
    IInterestFormRepository,
    IPetRepository,
    IOrganizationRepository,
)
from app.repositories.factory import (
    get_interest_form_repository,
    get_pet_repository,
    get_organization_repository,
)

router = APIRouter(prefix="/interests", tags=["interest forms"])

@router.post("/", response_model=InterestFormResponse)
async def create_interest_form(
    form: InterestFormCreate,
    pet_id: int,
    current_user: User = Depends(get_current_user),
    pet_repo: IPetRepository = Depends(get_pet_repository),
    form_repo: IInterestFormRepository = Depends(get_interest_form_repository),
):
    """Create an interest form for a pet."""
    try:
        pet_service = PetService(pet_repo)
        interest_service = InterestFormService(form_repo)
        
        pet = await pet_service.get_pet_by_id(pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found",
            )

        result = await interest_service.create_interest_form(form, current_user.id, pet_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[InterestFormResponse])
async def list_interest_forms(form_repo: IInterestFormRepository = Depends(get_interest_form_repository)):
    """List all interest forms."""
    interest_service = InterestFormService(form_repo)
    return await interest_service.list_interest_forms()

@router.get("/user/my-interests", response_model=list[InterestFormResponse])
async def my_interest_forms(
    current_user: User = Depends(get_current_user),
    form_repo: IInterestFormRepository = Depends(get_interest_form_repository),
):
    """Get all interest forms submitted by current user."""
    interest_service = InterestFormService(form_repo)
    return await interest_service.get_interest_forms_by_user(current_user.id)

@router.get("/pet/{pet_id}", response_model=list[InterestFormResponse])
async def get_pet_interest_forms(
    pet_id: int,
    current_user: User = Depends(get_current_user),
    pet_repo: IPetRepository = Depends(get_pet_repository),
    org_repo: IOrganizationRepository = Depends(get_organization_repository),
    form_repo: IInterestFormRepository = Depends(get_interest_form_repository),
):
    """Get all interest forms for a specific pet (only for organization owner)."""
    pet_service = PetService(pet_repo)
    org_service = OrganizationService(org_repo)
    interest_service = InterestFormService(form_repo)
    
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
            detail="Not authorized to view interest forms for this pet",
        )

    return await interest_service.get_interest_forms_by_pet(pet_id)

@router.delete("/{interest_id}")
async def delete_interest_form(
    interest_id: int,
    current_user: User = Depends(get_current_user),
    form_repo: IInterestFormRepository = Depends(get_interest_form_repository),
):
    """Delete an interest form."""
    try:
        interest_service = InterestFormService(form_repo)
        interest = await interest_service.get_interest_form_by_id(interest_id)
        if not interest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interest form not found",
            )

        if interest.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this interest form",
            )

        await interest_service.delete_interest_form(interest_id)
        return {"message": "Interest form deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

