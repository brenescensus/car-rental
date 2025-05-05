"""
AI-Driven Predictive Maintenance Module for Car Rental Website
This module implements predictive maintenance algorithms that analyze vehicle data
to forecast potential maintenance needs and reliability scores.
"""

import datetime
import random
from datetime import timedelta

class PredictiveMaintenance:
    def __init__(self):
        # Common car parts and their average lifespan (in miles)
        self.parts_lifespan = {
            "oil": 5000,
            "tires": 50000,
            "brakes": 40000,
            "battery": 60000,
            "air_filter": 15000,
            "transmission_fluid": 30000,
            "spark_plugs": 60000,
            "timing_belt": 90000,
            "suspension": 70000
        }
        
        # Category-specific reliability factors
        self.reliability_factors = {
            "Luxury": 0.95,    # Luxury cars often have more complex systems that can fail
            "SUV": 0.9,        # SUVs have more wear and tear due to size/weight
            "Electric": 1.1,   # Electric cars have fewer moving parts to break
            "Compact": 1.05,   # Compact cars are usually simpler and reliable
            "Sedan": 1.0       # Baseline
        }
        
    def calculate_reliability_score(self, car_data):
        """
        Calculate a reliability score for a car based on its type, age, and maintenance history
        
        Args:
            car_data (dict): Car information including category, age, mileage, etc.
            
        Returns:
            int: Reliability score (0-100)
        """
        # Start with base score
        base_score = 90
        
        # Adjust for category
        category = car_data.get('category', 'Sedan')
        category_factor = self.reliability_factors.get(category, 1.0)
        
        # Adjust for mileage
        mileage = car_data.get('mileage', 10000)  # Default to 10k if not provided
        mileage_factor = 1.0 - (mileage / 200000)  # Cars with more miles get lower scores
        
        # Adjust for age
        age_years = car_data.get('age_years', 1)  # Default to 1 year if not provided
        age_factor = 1.0 - (age_years / 20.0)  # Older cars get lower scores
        
        # Calculate final score
        score = base_score * category_factor * max(0.5, mileage_factor) * max(0.7, age_factor)
        
        # Add some randomness to simulate real-world variability
        score *= random.uniform(0.95, 1.05)
        
        # Ensure score is within 0-100 range
        return max(0, min(100, round(score)))
        
    def predict_maintenance_issues(self, car_data):
        """
        Predict potential maintenance issues based on car data
        
        Args:
            car_data (dict): Car information including mileage, last service, etc.
            
        Returns:
            list: Predicted maintenance issues
        """
        mileage = car_data.get('mileage', 10000)
        last_service_miles = car_data.get('last_service_miles', 0)
        miles_since_service = mileage - last_service_miles
        
        predicted_issues = []
        
        # Check each part against its lifespan and mileage since last service
        for part, lifespan in self.parts_lifespan.items():
            remaining_life = lifespan - (miles_since_service % lifespan)
            remaining_percent = (remaining_life / lifespan) * 100
            
            # Format part name for display
            part_name = part.replace('_', ' ').title()
            
            # If part is due for service or close to it, add to issues
            if remaining_percent <= 10:
                predicted_issues.append(f"{part_name} replacement needed")
            elif remaining_percent <= 25:
                predicted_issues.append(f"{part_name} at {round(100-remaining_percent)}% wear, replacement soon")
            elif remaining_percent <= 40:
                predicted_issues.append(f"{part_name} check recommended")
        
        # Add some randomness for realism
        if random.random() < 0.3 and len(predicted_issues) < 3:
            random_issues = [
                "Software update pending",
                "Battery health check recommended",
                "Alignment check recommended",
                "Interior sanitization due",
                "Exterior detailing recommended"
            ]
            predicted_issues.append(random.choice(random_issues))
            
        return predicted_issues[:3]  # Return top 3 issues
    
    def calculate_next_service_date(self, car_data):
        """
        Calculate the next recommended service date
        
        Args:
            car_data (dict): Car information
            
        Returns:
            str: Next service date in YYYY-MM-DD format
        """
        today = datetime.datetime.now()
        
        # Base next service on mileage and usage patterns
        mileage = car_data.get('mileage', 10000)
        daily_usage = car_data.get('daily_miles', 30)  # Average miles per day
        
        # Find the part that will need service soonest
        next_service_miles = float('inf')
        for part, lifespan in self.parts_lifespan.items():
            remaining_life = lifespan - (mileage % lifespan)
            next_service_miles = min(next_service_miles, remaining_life)
        
        # Calculate days until next service
        days_until_service = max(1, round(next_service_miles / daily_usage))
        
        # Add some randomness to simulate real-world variability
        days_until_service = int(days_until_service * random.uniform(0.8, 1.2))
        
        # Calculate the next service date
        next_service_date = today + timedelta(days=days_until_service)
        
        return next_service_date.strftime('%Y-%m-%d')
    
    def generate_maintenance_prediction(self, car):
        """
        Generate a complete maintenance prediction for a car
        
        Args:
            car (dict): Car information
            
        Returns:
            dict: Complete maintenance prediction
        """
        # Generate synthetic car data if not provided
        car_data = {
            'id': car.get('id', 0),
            'name': car.get('name', 'Unknown Car'),
            'category': car.get('category', 'Sedan'),
            'mileage': random.randint(5000, 80000),
            'age_years': random.randint(1, 5),
            'last_service_miles': random.randint(0, 5000),
            'daily_miles': random.randint(20, 50)
        }
        
        # Calculate reliability score
        reliability_score = self.calculate_reliability_score(car_data)
        
        # Predict maintenance issues
        predicted_issues = self.predict_maintenance_issues(car_data)
        
        # Calculate next service date
        next_service_date = self.calculate_next_service_date(car_data)
        
        # Return complete prediction
        return {
            "car_id": car_data['id'],
            "reliability_score": reliability_score,
            "next_service": next_service_date,
            "predicted_issues": predicted_issues,
            "estimated_maintenance_cost": self.estimate_maintenance_cost(predicted_issues),
            "health_status": self.get_health_status(reliability_score)
        }
    
    def estimate_maintenance_cost(self, issues):
        """
        Estimate maintenance costs based on predicted issues
        
        Args:
            issues (list): List of predicted maintenance issues
            
        Returns:
            float: Estimated maintenance cost
        """
        # Define average costs for different maintenance types
        costs = {
            "replacement": (200, 800),
            "soon": (150, 600),
            "check": (50, 200),
            "update": (50, 100),
            "sanitization": (80, 150),
            "detailing": (100, 300),
        }
        
        total_cost = 0
        for issue in issues:
            issue_lower = issue.lower()
            
            # Determine cost range based on issue type
            if "replacement" in issue_lower:
                min_cost, max_cost = costs["replacement"]
            elif "soon" in issue_lower:
                min_cost, max_cost = costs["soon"]
            elif "check" in issue_lower:
                min_cost, max_cost = costs["check"]
            elif "update" in issue_lower:
                min_cost, max_cost = costs["update"]
            elif "sanitization" in issue_lower:
                min_cost, max_cost = costs["sanitization"]
            elif "detailing" in issue_lower:
                min_cost, max_cost = costs["detailing"]
            else:
                min_cost, max_cost = (50, 150)  # Default range
                
            # Add random cost within range
            total_cost += random.uniform(min_cost, max_cost)
            
        return round(total_cost, 2)
    
    def get_health_status(self, reliability_score):
        """
        Get a health status label based on reliability score
        
        Args:
            reliability_score (int): Reliability score (0-100)
            
        Returns:
            str: Health status label
        """
        if reliability_score >= 90:
            return "Excellent"
        elif reliability_score >= 80:
            return "Good"
        elif reliability_score >= 70:
            return "Fair"
        elif reliability_score >= 60:
            return "Needs Attention"
        else:
            return "Requires Service"

# For testing purposes
if __name__ == "__main__":
    maintenance = PredictiveMaintenance()
    car = {
        "id": 3,
        "name": "BMW X5",
        "category": "SUV",
        "price_per_day": 200
    }
    
    prediction = maintenance.generate_maintenance_prediction(car)
    print(f"Car: {car['name']}")
    print(f"Reliability Score: {prediction['reliability_score']}")
    print(f"Health Status: {prediction['health_status']}")
    print(f"Next Service: {prediction['next_service']}")
    print(f"Estimated Maintenance Cost: ${prediction['estimated_maintenance_cost']}")
    print("\nPredicted Issues:")
    for issue in prediction['predicted_issues']:
        print(f"- {issue}")