from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.organizations.models import Organization
from app.organizations.schemas import OrganizationSchema, SOrgCard
from app.organizations.dao import OrganizationDAO
from app.users.dependescies import get_current_user
from app.exceptions import OrgIsNotFoundException, UserIncorrectRoleException, UserNotAuthException

router = APIRouter(
    prefix="/med_org",
    tags=["Организации"]
)

@router.get("/med_orgs", response_model=List[OrganizationSchema], name="Получить все организации", description="Получить список всех медицинских организаций")
async def get_all_orgs(current_user: dict = Depends(get_current_user)) -> List[Organization]:
    if not current_user:
        raise UserNotAuthException
    
    user = current_user["User"]
    if user['role']['id'] == 2:
        raise UserIncorrectRoleException
    orgs = await OrganizationDAO.get_orgs()
    return orgs

@router.get("/{lpucode}", response_model=SOrgCard, name="Получить детали организации", description="Получить детальную информацию о медицинской организации по ID")
async def get_detail_org(lpucode: int, current_user: dict = Depends(get_current_user)) -> OrganizationSchema:
    if not current_user:
        raise UserNotAuthException
    user_role = current_user["User"]['role']['id']
    if user_role == 2:
        
        user_lpucode = current_user["User"]["organization"]["lpucode"]
        if lpucode != user_lpucode:
            # Перенаправляем пользователя на страницу с его собственным lpucode
            return RedirectResponse(url=f"/med_org/{user_lpucode}")
    org = await OrganizationDAO.get_org_card(lpucode)
    if not org:
        raise OrgIsNotFoundException
    return org