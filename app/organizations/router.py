from typing import List
from fastapi import APIRouter, HTTPException
from app.organizations.models import Organization
from app.organizations.schemas import OrganizationSchema, SOrgCard
from app.organizations.dao import OrganizationDAO


router = APIRouter(
    prefix="/med_org",
    tags=["Организации"])


@router.get("/med_orgs", response_model=List[OrganizationSchema])
async def get_all_tickets() -> List[Organization]:
    orgs = await OrganizationDAO.get_orgs()
    return orgs

@router.get("/{organzation_id}", response_model=SOrgCard)
async def get_detail_ticket(organzation_id: int) -> Organization:
    ticket = await OrganizationDAO.get_org_card(organzation_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Орагнизация не найдена")
    return ticket