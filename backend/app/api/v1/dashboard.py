from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.services.cache import get_revenue_summary
from app.services.reservations import calculate_monthly_revenue
from app.core.auth import authenticate_request as get_current_user

router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    
    tenant_id = getattr(current_user, "tenant_id", "default_tenant") or "default_tenant"
    
    revenue_data = await get_revenue_summary(property_id, tenant_id)
    
    total_revenue_float = float(revenue_data['total'])
    
    return {
        "property_id": revenue_data['property_id'],
        "total_revenue": total_revenue_float,
        "currency": revenue_data['currency'],
        "reservations_count": revenue_data['count']
    }

@router.get("/dashboard/monthly")
async def get_monthly_revenue(
    property_id: str,
    month: int,
    year: int,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
    if year < 2000 or year > 2100:
        raise HTTPException(status_code=400, detail="Invalid year")
    
    tenant_id = getattr(current_user, "tenant_id", "default_tenant") or "default_tenant"
    
    result = await calculate_monthly_revenue(property_id, tenant_id, month, year)
    
    return {
        "property_id": property_id,
        "month": month,
        "year": year,
        "monthly_revenue": result['total'],
        "reservations_count": result['count']
    }
