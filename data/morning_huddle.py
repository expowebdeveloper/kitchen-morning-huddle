from datetime import date
from load_data import DinersList
from typing import List, Dict
from collections import defaultdict

def analyze_order_patterns(orders: List[Dict]) -> Dict:
    """Analyze order patterns for kitchen planning"""
    patterns = {
        "total_items": len(orders),
        "dietary_requirements": defaultdict(int),
        "estimated_prep_time": 0,  # in minutes
        "complexity_score": 0      # 1-5 scale
    }
    
    # Analyze each order
    for order in orders:
        # Track dietary requirements
        for tag in order.dietary_tags:
            patterns["dietary_requirements"][tag] += 1
            
        # Estimate prep time and complexity
        # More dietary tags = more complexity
        complexity = 1 + len(order.dietary_tags) * 0.5
        patterns["complexity_score"] = min(5, patterns["complexity_score"] + complexity)
        
        # Basic prep time estimate (could be refined with actual menu data)
        patterns["estimated_prep_time"] += 15 * (1 + len(order.dietary_tags) * 0.2)
    
    return patterns

def get_kitchen_insights(diners_list: DinersList, target_date: date = None) -> Dict:
    """Get insights focused on kitchen operations"""
    if target_date is None:
        target_date = date.today()

    insights = []
    
    for diner in diners_list.diners:
        if not diner.reservations:
            continue
            
        for reservation in diner.reservations:
            if reservation.date == target_date:
                # Analyze orders for this reservation
                order_patterns = analyze_order_patterns(reservation.orders)
                
                insight = {
                    "name": diner.name,
                    "party_size": reservation.number_of_people,
                    "orders": reservation.orders,
                    "dietary_requirements": order_patterns["dietary_requirements"],
                    "prep_time": order_patterns["estimated_prep_time"],
                    "complexity": order_patterns["complexity_score"],
                    "kitchen_notes": []
                }
                
                # Add kitchen-specific notes
                if order_patterns["complexity_score"] > 3:
                    insight["kitchen_notes"].append("Complex order - requires extra attention")
                if len(order_patterns["dietary_requirements"]) > 0:
                    insight["kitchen_notes"].append("Multiple dietary restrictions - verify ingredients")
                
                insights.append(insight)
    
    return insights


# if __name__ == "__main__":
#     # Load data
#     diners_list = DinersList.load_from_json("fine-dining-dataset.json")
    
#     # For testing purposes, let's use a specific date
#     test_date = date(2024, 5, 20)
    
#     # Get kitchen insights for the day
#     daily_insights = get_kitchen_insights(diners_list, test_date)