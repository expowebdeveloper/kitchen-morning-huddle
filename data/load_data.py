from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class Review(BaseModel):
    restaurant_name: str
    date: date
    rating: int = Field(..., ge=1, le=5)
    content: str

class Order(BaseModel):
    item: str
    dietary_tags: List[str]
    price: float

class Reservation(BaseModel):
    date: date
    number_of_people: int
    orders: List[Order]

class Email(BaseModel):
    date: date
    subject: str
    combined_thread: str

class Diner(BaseModel):
    name: str
    reviews: Optional[List[Review]] = None
    reservations: Optional[List[Reservation]] = None
    emails: Optional[List[Email]] = None

class DinersList(BaseModel):
    diners: List[Diner]

    @classmethod
    def load_from_json(cls, json_path: str) -> "DinersList":
        import json
        from datetime import datetime

        with open(json_path) as f:
            data = json.load(f)
            
        # Convert date strings to date objects
        for diner in data["diners"]:
            if diner.get("reviews"):
                for review in diner["reviews"]:
                    review["date"] = datetime.strptime(review["date"], "%Y-%m-%d").date()
            
            if diner.get("reservations"):
                for reservation in diner["reservations"]:
                    reservation["date"] = datetime.strptime(reservation["date"], "%Y-%m-%d").date()
            
            if diner.get("emails"):
                for email in diner["emails"]:
                    email["date"] = datetime.strptime(email["date"], "%Y-%m-%d").date()

        return cls(**data)
    
if __name__ == "__main__":
    diners_list = DinersList.load_from_json("fine-dining-dataset.json")    