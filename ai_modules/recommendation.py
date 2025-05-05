"""
Car Recommendation AI Module

This module provides AI-driven car recommendations based on user preferences.
It analyzes user input, historical user data (when available), and car characteristics
to provide personalized vehicle recommendations.
"""

import numpy as np
from datetime import datetime
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CarRecommendationEngine:
    """AI engine for generating personalized car recommendations."""
    
    def __init__(self, car_data):
        """
        Initialize the recommendation engine with available car data.
        
        Args:
            car_data (list): List of car dictionaries containing vehicle information
        """
        self.car_data = car_data
        self.feature_weights = {
            'category_match': 0.35,
            'price_match': 0.25,
            'seats_match': 0.20,
            'transmission_match': 0.10,
            'rating': 0.10
        }
        logger.info("Recommendation engine initialized with %d vehicles", len(car_data))
    
    def get_recommendations(self, preferences, user_history=None, limit=3):
        """
        Generate personalized car recommendations based on user preferences.
        
        Args:
            preferences (dict): User preferences (category, price range, seats, etc.)
            user_history (list, optional): User's rental history for improved recommendations
            limit (int): Maximum number of recommendations to return
            
        Returns:
            dict: Recommendations with explanation
        """
        try:
            logger.info("Generating recommendations for preferences: %s", preferences)
            
            # Calculate match scores for each car
            scored_cars = []
            for car in self.car_data:
                score = self._calculate_match_score(car, preferences, user_history)
                scored_cars.append({
                    "car": car,
                    "match_score": min(score * 100, 100)  # Convert to percentage with max of 100
                })
            
            # Sort by match score (descending)
            scored_cars.sort(key=lambda x: x['match_score'], reverse=True)
            
            # Create personalized explanation
            explanation = self._generate_explanation(preferences, scored_cars[:limit])
            
            return {
                "recommendations": scored_cars[:limit],
                "explanation": explanation
            }
            
        except Exception as e:
            logger.error("Error generating recommendations: %s", str(e))
            return {
                "recommendations": [],
                "explanation": "We couldn't process your preferences. Please try again."
            }
    
    def _calculate_match_score(self, car, preferences, user_history=None):
        """
        Calculate match score between a car and user preferences.
        
        Args:
            car (dict): Car information
            preferences (dict): User preferences
            user_history (list, optional): User's rental history
            
        Returns:
            float: Match score (0-1)
        """
        score = 0
        
        # Category match
        if preferences.get('category') and preferences['category'] == car['category']:
            score += self.feature_weights['category_match']
        
        # Price match (within budget)
        try:
            max_price = float(preferences.get('max_price', 1000))
            if car['price_per_day'] <= max_price:
                # Higher score for prices well below max (better value)
                price_ratio = 1 - (car['price_per_day'] / max_price)
                value_bonus = price_ratio * 0.5  # Up to 50% bonus for good value
                score += self.feature_weights['price_match'] * (1 + value_bonus)
            else:
                # Penalize for being over budget
                score -= self.feature_weights['price_match']
        except (ValueError, TypeError):
            # If max_price is not valid, skip this criterion
            pass
        
        # Seats match
        try:
            seats_needed = int(preferences.get('seats', 0))
            if seats_needed > 0:
                if car['seats'] >= seats_needed:
                    # Perfect if exact match or just 1-2 more seats
                    if car['seats'] <= seats_needed + 2:
                        score += self.feature_weights['seats_match']
                    else:
                        # Slightly lower score for much bigger cars than needed
                        score += self.feature_weights['seats_match'] * 0.8
                else:
                    # Car doesn't have enough seats
                    score -= self.feature_weights['seats_match']
        except (ValueError, TypeError):
            pass
        
        # Transmission preference
        if preferences.get('transmission') and preferences['transmission'] == car['transmission']:
            score += self.feature_weights['transmission_match']
        
        # Rating factor (high rated cars get a boost)
        if 'rating' in car:
            rating_normalized = car['rating'] / 5.0  # Assuming 5-star rating system
            score += self.feature_weights['rating'] * rating_normalized
        
        # If we have user history, incorporate that data
        if user_history:
            history_bonus = self._calculate_history_bonus(car, user_history)
            score += history_bonus
        
        return max(0, score)  # Ensure score is not negative
    
    def _calculate_history_bonus(self, car, user_history):
        """
        Calculate bonus score based on user's rental history.
        
        Args:
            car (dict): Car information
            user_history (list): User's rental history
            
        Returns:
            float: History bonus score
        """
        bonus = 0
        
        # Check if user has rented similar category before
        category_rentals = [rental for rental in user_history 
                          if rental.get('category') == car['category']]
        if category_rentals:
            # User has rented this category before
            bonus += 0.05
            
            # Check ratings they gave for this category
            category_ratings = [rental.get('rating', 0) for rental in category_rentals 
                              if 'rating' in rental]
            if category_ratings:
                avg_rating = sum(category_ratings) / len(category_ratings)
                if avg_rating >= 4:  # They liked this category
                    bonus += 0.05
        
        # Check if user has rented this specific car before
        car_rentals = [rental for rental in user_history 
                     if rental.get('car_id') == car['id']]
        if car_rentals:
            # User has rented this specific car before
            car_ratings = [rental.get('rating', 0) for rental in car_rentals 
                         if 'rating' in rental]
            if car_ratings:
                avg_car_rating = sum(car_ratings) / len(car_ratings)
                if avg_car_rating >= 4:  # They liked this car
                    bonus += 0.10
                elif avg_car_rating < 3:  # They didn't like this car
                    bonus -= 0.15
        
        return bonus
    
    def _generate_explanation(self, preferences, recommendations):
        """
        Generate a personalized explanation for the recommendations.
        
        Args:
            preferences (dict): User preferences
            recommendations (list): List of recommended cars with scores
            
        Returns:
            str: Personalized explanation
        """
        if not recommendations:
            return "No matches found for your preferences."
        
        # Build explanation based on key matching factors
        factors = []
        
        if preferences.get('category'):
            category_matches = [r for r in recommendations 
                             if r['car']['category'] == preferences['category']]
            if category_matches:
                factors.append(f"category ({preferences['category']})")
        
        if preferences.get('max_price'):
            budget_matches = [r for r in recommendations 
                           if r['car']['price_per_day'] <= float(preferences.get('max_price', 0))]
            if budget_matches:
                factors.append(f"budget (under ${preferences['max_price']}/day)")
        
        if preferences.get('seats'):
            seat_matches = [r for r in recommendations 
                         if r['car']['seats'] >= int(preferences.get('seats', 0))]
            if seat_matches:
                factors.append(f"seating capacity ({preferences['seats']}+ seats)")
        
        if preferences.get('transmission'):
            transmission_matches = [r for r in recommendations 
                                 if r['car']['transmission'] == preferences['transmission']]
            if transmission_matches:
                factors.append(f"transmission type ({preferences['transmission']})")
        
        # Create the explanation text
        if factors:
            explanation = "These cars were matched based on your preferences for " 
            if len(factors) == 1:
                explanation += factors[0] + "."
            elif len(factors) == 2:
                explanation += factors[0] + " and " + factors[1] + "."
            else:
                explanation += ", ".join(factors[:-1]) + ", and " + factors[-1] + "."
                
            # Add top car highlight if there's a standout option
            top_car = recommendations[0]
            if top_car['match_score'] >= 90:
                explanation += f" The {top_car['car']['name']} is an excellent match with a {int(top_car['match_score'])}% compatibility score."
                
            return explanation
        else:
            return "These cars best match your overall preferences."


# For testing purposes
if __name__ == "__main__":
    # Sample car data
    sample_cars = [
        {
            "id": 1,
            "name": "Tesla Model 3",
            "category": "Electric",
            "price_per_day": 120,
            "seats": 5,
            "transmission": "Automatic",
            "rating": 4.8
        },
        {
            "id": 2,
            "name": "Toyota Camry",
            "category": "Sedan",
            "price_per_day": 80,
            "seats": 5,
            "transmission": "Automatic",
            "rating": 4.5
        }
    ]
    
    # Sample user preferences
    sample_preferences = {
        "category": "Electric",
        "max_price": "150",
        "seats": "4"
    }
    
    # Initialize and test the recommendation engine
    engine = CarRecommendationEngine(sample_cars)
    results = engine.get_recommendations(sample_preferences)
    
    print(json.dumps(results, indent=2))