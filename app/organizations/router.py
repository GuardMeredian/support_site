from typing import List
from fastapi import APIRouter, Depends
from app.EOBD.AKTPAK.models import AKPC_LPU
from app.EOBD.AKTPAK.schemas import SAKPC_LPU
from app.EOBD.AKTPAK.dao import LPUDAO
from app.users.dependescies import get_current_user
from app.exceptions import OrgIsNotFoundException, UserIncorrectRoleException, UserNotAuthException

router = APIRouter(
    prefix="/med_org",
    tags=["Организации"]
)

@router.get("/med_orgs", response_model=List[SAKPC_LPU], name="Получить все организации", description="Получить список всех медицинских организаций")
async def get_all_orgs(current_user: dict = Depends(get_current_user)) -> List[AKPC_LPU]:
    if not current_user:
        raise UserNotAuthException
    
    user = current_user["User"]
    if user['role']['id'] == 2:
        raise UserIncorrectRoleException
    orgs = await LPUDAO.get_orgs()
    return orgs

"""@router.get("/{organzation_id}", response_model=SAKPC_LPU, name="Получить детали организации", description="Получить детальную информацию о медицинской организации по ID")
async def get_detail_org(organzation_id: int, current_user: dict = Depends(get_current_user)) -> Organization:
    if not current_user:
       raise UserNotAuthException
    org = await LPUDAO.get_org_card(organzation_id)
    if not org:
        raise OrgIsNotFoundException
    return org"""