from typing import List
from fastapi import APIRouter, Depends
from app.organizations.models import Organization
from app.organizations.schemas import OrganizationSchema, SOrgCard
from app.organizations.dao import OrganizationDAO
from app.users.dependescies import get_current_user
from app.exceptions import OrgIsNotFoundException, UserIncorrectRoleException, UserNotAuthException


router = APIRouter(
    prefix="/med_org",
    tags=["Организации"])


@router.get("/med_orgs", response_model=List[OrganizationSchema])
async def get_all_orgs(current_user: dict = Depends(get_current_user)) -> List[Organization]:
    if not current_user:
        raise UserNotAuthException
    
    user = current_user["User"]
    if user['role']['id'] == 2:
        raise UserIncorrectRoleException
    orgs = await OrganizationDAO.find_all()
    return orgs

@router.get("/{organzation_id}", response_model=SOrgCard)
async def get_detail_org(organzation_id: int, current_user: dict = Depends(get_current_user)) -> Organization:
    if not current_user:
       raise UserNotAuthException
    org = await OrganizationDAO.get_org_card(organzation_id)
    if not org:
        raise OrgIsNotFoundException
    return org