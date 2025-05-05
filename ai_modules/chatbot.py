"""
AI-Driven Chatbot Module for Car Rental Website
This module implements an intelligent chatbot that can answer customer questions,
provide rental recommendations, and assist with booking processes.
"""

import re
import random
import datetime
from difflib import get_close_match

class RentalChatbot:
    def __init__(self):
        # Initialize knowledge base with common customer queries and responses
        self.knowledge_base = {
            "greeting": [
                "Hello! How can I help you with your car rental today?",
                "Hi there! Looking to rent a car? I'm here to assist you.",
                "Welcome to AI Car Rentals! How may I help you today?"
            ],
            
            "booking_process": [
                "To make a booking, simply select a car and click on the 'Book Now' button. You'll need to provide your rental dates and driver information.",
                "Booking is easy! Browse our selection, choose a car, select your dates, and follow the checkout process. Need help with a specific step?",
                "Our booking process takes just 3 steps: 1) Select a car 2) Choose dates and location 3) Enter your details and payment information."
            ],
            
            "pricing": [
                "Our prices vary based on the car model, rental duration, and season. You can check out our 'Smart Pricing' page for detailed information.",
                "We use AI-driven dynamic pricing that considers factors like demand, day of the week, and seasonality. The best deals are often found by booking in advance!",
                "Rental rates start from $65/day for economy cars and go up to $300/day for luxury vehicles. We also offer discounts for weekly and monthly rentals."
            ],
            
            "payment_methods": [
                "We accept all major credit cards, PayPal, and Apple Pay. Payment is processed securely at the time of booking.",
                "You can pay using Visa, Mastercard, American Express, Discover, PayPal or Apple Pay. We do not accept cash payments for reservations.",
                "Payment is required at the time of booking and can be made with any major credit card or digital payment method."
            ],
            
            "cancellation_policy": [
                "Cancellations made 48 hours before the pickup time receive a full refund. Late cancellations may incur a fee.",
                "Our flexible cancellation policy allows free cancellation up to 48 hours before your rental. After that, a fee equal to one day's rental applies.",
                "Need to cancel? No problem! Cancel at least 48 hours before pickup for a full refund. Later cancellations are subject to a fee."
            ],
            
            "insurance_options": [
                "We offer various insurance packages starting from $15 per day. Full coverage is recommended for peace of mind.",
                "Insurance options include Basic (covers damages up to $15,000), Premium (covers damages up to $35,000), and Comprehensive (full coverage with no deductible).",
                "All rentals come with standard insurance, but we recommend upgrading to our Premium or Comprehensive coverage for full protection."
            ],
            
            "rental_requirements": [
                "To rent a car, you need to be at least 21 years old, have a valid driver's license, and a credit card in your name.",
                "Requirements include: minimum age of 21 (25 for luxury vehicles), a valid driver's license held for at least 1 year, and a credit card for the security deposit.",
                "You'll need a valid driver's license, credit card, and be at least 21 years old. Additional fees may apply for drivers under 25."
            ],
            
            "pickup_return": [
                "You can pick up and return your rental at any of our locations during business hours (8AM-8PM). After-hours service is available at select locations.",
                "Our main locations offer 24/7 pickup and return. For other locations, please check the specific hours on our Locations page.",
                "Pick up and return is available at the same location, or you can opt for our one-way rental service for an additional fee."
            ],
            
            "car_types": [
                "We offer a variety of car types: Economy, Compact, Sedan, SUV, Luxury, and Electric vehicles to suit every need and budget.",
                "Our fleet includes everything from fuel-efficient compact cars to spacious SUVs and luxury vehicles. We also have a growing selection of electric cars.",
                "Whether you need a small car for city driving or an SUV for a family trip, we have options for every occasion and group size."
            ],
            
            "locations": [
                "We have rental locations in all major cities and airports. You can check our 'Locations' page for specific addresses and contact information.",
                "AI Car Rentals is available in over 50 major cities and 30 airports nationwide. Use our location finder to see our nearest branch.",
                "Find us at most major airports and downtown locations in major metropolitan areas. We offer free shuttle service from airport terminals."
            ],
            
            "additional_services": [
                "We offer additional services like GPS navigation ($5/day), child seats ($7/day), additional drivers ($10/day), and roadside assistance ($7/day).",
                "Enhance your rental with our add-ons: WiFi hotspot, child safety seats, premium insurance, ski racks, and more. Add these during checkout.",
                "Additional services include GPS, child seats, additional drivers, roadside assistance, and our popular full tank option."
            ],
            
            "ai_features": [
                "Our AI features include personalized car recommendations, virtual tours, dynamic pricing, and predictive maintenance for worry-free rentals.",
                "We use AI to enhance your experience through personalized recommendations, optimal pricing, and ensuring all our vehicles are maintained proactively.",
                "Our AI technology helps you find the perfect car based on your needs, gives you the best prices, and ensures all vehicles are in top condition."
            ],
            
            "best_deals": [
                "For the best deals, book in advance, check our weekly specials, or sign up for our loyalty program to earn points and get exclusive discounts.",
                "Save up to 25% by booking at least a week in advance, and look for our off-season specials. Sign up for our newsletter to receive exclusive offers.",
                "Join our rewards program for the best deals! Members get priority upgrades, exclusive discounts, and can earn free rental days."
            ],
            
            "help": [
                "I can help with booking cars, answering questions about our policies, providing information about our fleet, or connecting you with customer service.",
                "Need assistance? I can help with reservations, explain our policies, recommend cars, or provide information about locations and services.",
                "I'm here to help with any questions about our car rental service. What specifically would you like to know about?"
            ]
        }
        
        # Keyword mapping to topics
        self.keyword_mapping = {
            "hello|hi|hey|greetings": "greeting",
            "book|booking|reserve|reservation|rent|renting": "booking_process",
            "price|pricing|cost|rate|fee|charge|how much": "pricing",
            "pay|payment|credit card|debit card|mastercard|visa|amex|paypal": "payment_methods",
            "cancel|cancellation|refund|money back": "cancellation_policy",
            "insurance|coverage|protect|protection": "insurance_options",
            "requirements|qualify|qualification|need to|required|driver's license|driving license|age": "rental_requirements",
            "pickup|return|drop off|dropping off|collect|collecting": "pickup_return",
            "car type|vehicle type|car category|model|luxury|economy|suv|sedan|compact|electric": "car_types",
            "location|branch|airport|city|where": "locations",
            "additional service|extra|add on|addon|gps|child seat|wifi|hotspot": "additional_services",
            "ai|artificial intelligence|smart|intelligent|feature": "ai_features",
            "deal|discount|offer|promo|promotion|coupon|sale|cheap|save|saving|bargain": "best_deals",
            "help|assist|support|guidance": "help"
        }
        
        # Maintain conversation context
        self.context = {
            "last_query": None,
            "last_topic": None,
            "user_preferences": {}
        }
        
    def process_message(self, message):
        """
        Process user message and return appropriate response
        
        Args:
            message (str): User's message
            
        Returns:
            str: Chatbot response
        """
        # Store the message for context
        self.context["last_query"] = message
        message = message.lower().strip()
        
        # Extract any user preferences from the message
        self._extract_preferences(message)
        
        # Check for predefined commands/special cases
        if self._is_exit_command(message):
            return "Thank you for chatting with us! If you have more questions later, feel free to return."
        
        # Find matching topic based on keywords
        topic = self._find_matching_topic(message)
        
        # Store topic for context
        self.context["last_topic"] = topic
        
        # If topic found, return a response from that topic
        if topic:
            return random.choice(self.knowledge_base[topic])
        
        # If no topic matched, provide a default response
        return self._get_default_response()
    
    def _extract_preferences(self, message):
        """Extract user preferences from message to personalize future responses"""
        # Look for car type preferences
        car_types = ["suv", "sedan", "luxury", "compact", "electric"]
        for car_type in car_types:
            if car_type in message:
                self.context["user_preferences"]["car_type"] = car_type
        
        # Look for price sensitivity
        price_terms = ["cheap", "affordable", "budget", "expensive", "luxury", "cost"]
        if any(term in message for term in price_terms):
            if any(term in message for term in ["cheap", "affordable", "budget"]):
                self.context["user_preferences"]["price_sensitivity"] = "budget"
            elif any(term in message for term in ["expensive", "luxury"]):
                self.context["user_preferences"]["price_sensitivity"] = "premium"
        
        # Look for rental duration
        duration_patterns = [
            (r"(\d+)\s*day", "days"),
            (r"(\d+)\s*week", "weeks"),
            (r"(\d+)\s*month", "months")
        ]
        
        for pattern, unit in duration_patterns:
            match = re.search(pattern, message)
            if match:
                self.context["user_preferences"]["duration"] = {
                    "value": int(match.group(1)),
                    "unit": unit
                }
                break
    
    def _is_exit_command(self, message):
        """Check if message is an exit command"""
        exit_commands = ["bye", "goodbye", "exit", "quit", "end", "stop", "that's all", "thank you", "thanks bye"]
        return any(cmd in message for cmd in exit_commands)
    
    def _find_matching_topic(self, message):
        """Find the most relevant topic based on message keywords"""
        for keyword_pattern, topic in self.keyword_mapping.items():
            if re.search(keyword_pattern, message):
                return topic
                
        # If no direct match, try to find close matches in our knowledge base
        all_topics = list(self.knowledge_base.keys())
        words = message.split()
        
        for word in words:
            if len(word) > 3:  #            # Only check longer words for better matches
            matches = get_close_matches(word, all_topics, n=1, cutoff=0.7)
            if matches:
                return matches[0]
        return None
    
    def _get_default_response(self):
        """Provide a default response when no specific topic is matched"""
        default_responses = [
            "I'm not sure I understand. Could you please rephrase your question?",
            "I'd be happy to help with that. Could you provide more details?",
            "I specialize in car rental information. Could you ask me something about our services?",
            "I'm still learning! Could you try asking that in a different way?",
            "I want to make sure I help you correctly. Could you clarify your question?",
            "I'm not certain I caught that. Would you mind asking again?"
        ]
        
        # If we have some context, try to use it
        if self.context["last_topic"]:
            return (f"I'm not sure about that specific question, but I can tell you more about {self.context['last_topic'].replace('_', ' ')}. "
                    "Would that be helpful?")
        
        return random.choice(default_responses)
    
    def get_personalized_recommendation(self):
        """Generate a personalized car recommendation based on user preferences"""
        if not self.context["user_preferences"]:
            return None
            
        pref = self.context["user_preferences"]
        recommendation = []
        
        if "car_type" in pref:
            if pref["car_type"] == "suv":
                recommendation.append("Based on your interest in SUVs, I recommend our 2023 Toyota RAV4 or Honda CR-V.")
            elif pref["car_type"] == "luxury":
                recommendation.append("For luxury, check out our BMW 5 Series or Mercedes E-Class.")
            elif pref["car_type"] == "electric":
                recommendation.append("Our electric vehicle selection includes the Tesla Model 3 and Nissan Leaf.")
            else:
                recommendation.append(f"We have great options in our {pref['car_type']} category.")
        
        if "price_sensitivity" in pref:
            if pref["price_sensitivity"] == "budget":
                recommendation.append("Our economy cars offer the best value starting at just $65/day.")
            else:
                recommendation.append("Our premium collection offers luxury vehicles with all the amenities.")
        
        if "duration" in pref:
            duration = pref["duration"]
            if duration["unit"] == "days" and duration["value"] > 7:
                recommendation.append(f"For your {duration['value']}-day rental, we offer weekly discounts!")
            elif duration["unit"] in ["weeks", "months"]:
                recommendation.append(f"Long-term rentals like yours qualify for our special monthly rates.")
        
        return " ".join(recommendation) if recommendation else None


# Example usage
if __name__ == "__main__":
    chatbot = RentalChatbot()
    print("Chatbot: Welcome to AI Car Rentals! How can I assist you today?")
    print("(Type 'bye' to exit)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['bye', 'exit', 'quit']:
            print("Chatbot: Thank you for using our service. Have a great day!")
            break
        
        response = chatbot.process_message(user_input)
        
        # Check for personalized recommendation
        personalized = chatbot.get_personalized_recommendation()
        if personalized:
            response += " " + personalized
        
        print("Chatbot:", response)