from app.routes.auth import router as auth_router
from app.routes.organizations import router as organizations_router
from app.routes.pets import router as pets_router
from app.routes.interest_forms import router as interest_forms_router

__all__ = [
    "auth_router",
    "organizations_router",
    "pets_router",
    "interest_forms_router",
]
