"""
AI-Driven Smart Pricing Module for Car Rental Website
This module implements dynamic pricing algorithms to optimize rental rates
based on various factors including demand, seasonality, day of the week,
and special events.
"""

import datetime
import random
import numpy as np
from datetime import timedelta

class SmartPricing:
    def __init__(self):
        # Base pricing factors
        self.weekend_multiplier = 1.25
        self.holiday_multiplier = 1.4
        self.high_demand_multiplier = 1.2
        self.low_demand_multiplier = 0.85
        
        # Seasonal factors (month-based multipliers)
        self.seasonal_factors = {
            1: 0.9,   # January (low season)
            2: 0.9,   # February (low season)
            3: 1.0,   # March
            4: 1.1,   # April
            5: 1.15,  # May
            6: 1.25,  # June (summer high season)
            7: 1.35,  # July (peak summer)
            8: 1.35,  # August (peak summer)
            9: 1.15,  # September
            10: 1.0,  # October
            11: 0.9,  # November
            12: 1.2,  # December (holiday season)
        }
        
        # Common holidays list
        self.holidays = [
            "01-01",  # New Year's
            "07-04",  # Independence Day
            "12-24",  # Christmas Eve
            "12-25",  # Christmas
            "12-31",  # New Year's Eve
            # Add other holidays as needed
        ]
        
    def is_weekend(self, date):
        """Check if the given date falls on a weekend (Saturday or Sunday)"""
        return date.weekday() >= 5  # 5 = Saturday, 6 = Sunday
        
    def is_holiday(self, date):
        """Check if the given date is a holiday"""
        date_string = date.strftime('%m-%d')
        return date_string in self.holidays
        
    def calculate_demand_factor(self, date, car_category):
        """
        Calculate demand factor based on historical data and predictive analytics
        This is a simplified version - a real implementation would use more sophisticated
        ML models trained on historical booking data
        """
        # Base demand by day of week (0=Monday, 6=Sunday)
        day_of_week = date.weekday()
        base_demand = {
            0: 0.7,  # Monday
            1: 0.7,  # Tuesday
            2: 0.8,  # Wednesday
            3: 0.9,  # Thursday
            4: 1.2,  # Friday
            5: 1.3,  # Saturday
            6: 1.0,  # Sunday
        }
        
        # Category-specific demand factors
        category_factors = {
            "Luxury": 1.2,
            "SUV": 1.15,
            "Electric": 1.3,
            "Compact": 0.95,
            "Sedan": 1.0
        }
        
        # Get base demand for the day
        demand = base_demand.get(day_of_week, 1.0)
        
        # Adjust for category
        category_factor = category_factors.get(car_category, 1.0)
        
        # Add some randomness to simulate market fluctuations (±10%)
        randomness = random.uniform(0.9, 1.1)
        
        return demand * category_factor * randomness
    
    def get_dynamic_price(self, base_price, date, car_category):
        """
        Calculate the dynamic price based on all factors
        
        Args:
            base_price (float): The base price of the car rental
            date (datetime): The date for which to calculate the price
            car_category (str): The category of the car
            
        Returns:
            float: The calculated dynamic price
        """
        # Start with the base price
        price = base_price
        
        # Apply seasonal factor
        month = date.month
        season_factor = self.seasonal_factors.get(month, 1.0)
        price *= season_factor
        
        # Apply weekend factor if applicable
        if self.is_weekend(date):
            price *= self.weekend_multiplier
        
        # Apply holiday factor if applicable
        if self.is_holiday(date):
            price *= self.holiday_multiplier
        
        # Apply demand factor
        demand_factor = self.calculate_demand_factor(date, car_category)
        if demand_factor > 1.1:
            price *= self.high_demand_multiplier
        elif demand_factor < 0.9:
            price *= self.low_demand_multiplier
            
        # Round to 2 decimal places
        return round(price, 2)
    
    def generate_price_forecast(self, car, days=14):
        """
        Generate a price forecast for a car for the specified number of days
        
        Args:
            car (dict): The car object containing base price and category
            days (int): Number of days to forecast
            
        Returns:
            list: A list of price predictions for each day
        """
        base_price = car['price_per_day']
        category = car['category']
        today = datetime.datetime.now()
        
        forecast = []
        for i in range(days):
            future_date = today + timedelta(days=i)
            price = self.get_dynamic_price(base_price, future_date, category)
            
            forecast.append({
                "date": future_date.strftime('%Y-%m-%d'),
                "price": price,
                "is_weekend": self.is_weekend(future_date),
                "is_holiday": self.is_holiday(future_date),
                "demand_factor": round(self.calculate_demand_factor(future_date, category), 2)
            })
            
        return forecast
    
    def get_price_adjustments(self, car):
        """
        Get different price adjustments for a car
        
        Args:
            car (dict): The car object containing price and category
            
        Returns:
            dict: Price adjustments for different scenarios
        """
        base_price = car['price_per_day']
        
        return {
            "base_price": base_price,
            "weekend_price": round(base_price * self.weekend_multiplier, 2),
            "holiday_price": round(base_price * self.holiday_multiplier, 2),
            "low_demand_price": round(base_price * self.low_demand_multiplier, 2),
            "high_demand_price": round(base_price * self.high_demand_multiplier, 2)
        }

    def get_optimal_booking_time(self, car_category, target_date, days_range=30):
        """
        Predicts the best time to book a car for the best price
        
        Args:
            car_category (str): The category of car
            target_date (datetime): The target rental date
            days_range (int): How many days to look back from target date
            
        Returns:
            dict: Best booking time and expected savings
        """
        # In a real implementation, this would use ML models trained on historical price data
        # This is a simplified version that returns random but plausible results
        
        days_before = random.randint(7, days_range)
        booking_date = target_date - timedelta(days=days_before)
        expected_savings = random.uniform(5, 15)
        
        return {
            "recommended_booking_date": booking_date.strftime('%Y-%m-%d'),
            "days_before_rental": days_before,
            "expected_savings_percent": round(expected_savings, 1),
            "confidence_score": random.randint(70, 95)
        }

# For testing purposes
if __name__ == "__main__":
    pricer = SmartPricing()
    car = {
        "id": 1,
        "name": "Tesla Model 3",
        "category": "Electric",
        "price_per_day": 120
    }
    
    today = datetime.datetime.now()
    future_date = today + timedelta(days=5)
    
    print(f"Base price: ${car['price_per_day']}")
    print(f"Dynamic price for {future_date.strftime('%Y-%m-%d')}: ${pricer.get_dynamic_price(car['price_per_day'], future_date, car['category'])}")
    
    forecast = pricer.generate_price_forecast(car, 7)
    print("\nPrice forecast for next 7 days:")
    for day in forecast:
        print(f"{day['date']}: ${day['price']} (Demand factor: {day['demand_factor']})")