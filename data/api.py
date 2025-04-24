from fastapi import FastAPI, HTTPException
from datetime import date
from morning_huddle import get_kitchen_insights
from load_data import DinersList
from typing import List, Dict, Optional
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Kitchen Morning Huddle API",
    description="API for accessing kitchen morning huddle information",
    version="1.0.0"
)

class HuddleResponse(BaseModel):
    date: date
    total_reservations: int
    total_guests: int
    total_orders: int
    high_complexity_orders: int
    dietary_requirements: Dict[str, int]
    table_insights: List[Dict]

@app.get("/")
async def root():
    return {"message": "Kitchen Morning Huddle API"}

@app.get("/huddle/{target_date}", response_model=HuddleResponse)
async def get_huddle(target_date: date):
    try:
        # Load data
        diners_list = DinersList.load_from_json("fine-dining-dataset.json")
        
        # Get kitchen insights
        insights = get_kitchen_insights(diners_list, target_date)
        
        # Process insights into response format
        total_guests = 0
        total_orders = 0
        dietary_requirements = {}
        high_complexity_orders = 0
        
        for insight in insights:
            total_guests += insight["party_size"]
            total_orders += len(insight["orders"])
            for diet, count in insight["dietary_requirements"].items():
                dietary_requirements[diet] = dietary_requirements.get(diet, 0) + count
            if insight["complexity"] > 3:
                high_complexity_orders += 1

        response = {
            "date": target_date,
            "total_reservations": len(insights),
            "total_guests": total_guests,
            "total_orders": total_orders,
            "high_complexity_orders": high_complexity_orders,
            "dietary_requirements": dietary_requirements,
            "table_insights": insights
        }
        
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
