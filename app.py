from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Mock car database
cars = [
    {
        "id": 1,
        "name": "Tesla Model 3",
        "category": "Electric",
        "price_per_day": 120,
        "image": "static/images/cars/tesla_model3.jpg",
        "seats": 5,
        "transmission": "Automatic",
        "features": ["Autopilot", "360° Camera", "15\" Touchscreen", "Wireless Charging"],
        "rating": 4.8
    },
    {
        "id": 2,
        "name": "Toyota Camry",
        "category": "Sedan",
        "price_per_day": 80,
        "image": "static/images/cars/toyota_camry.jpg",
        "seats": 5,
        "transmission": "Automatic",
        "features": ["Bluetooth", "Backup Camera", "Cruise Control", "USB Ports"],
        "rating": 4.5
    },
    {
        "id": 3,
        "name": "BMW X5",
        "category": "SUV",
        "price_per_day": 200,
        "image": "static/images/cars/bmw_x5.jpg",
        "seats": 7,
        "transmission": "Automatic",
        "features": ["Leather Seats", "Panoramic Roof", "Navigation System", "Premium Sound"],
        "rating": 4.7
    },
    {
        "id": 4,
        "name": "Honda Civic",
        "category": "Compact",
        "price_per_day": 65,
        "image": "static/images/cars/honda_civic.jpg",
        "seats": 5,
        "transmission": "Automatic",
        "features": ["Fuel Efficient", "Apple CarPlay", "Android Auto", "Lane Assist"],
        "rating": 4.4
    },
    {
        "id": 5,
        "name": "Jeep Wrangler",
        "category": "SUV",
        "price_per_day": 150,
        "image": "static/images/cars/jeep_wrangler.jpg",
        "seats": 5,
        "transmission": "Manual",
        "features": ["4x4", "Removable Top", "Off-road Tires", "High Clearance"],
        "rating": 4.6
    },
    {
        "id": 6,
        "name": "Mercedes-Benz S-Class",
        "category": "Luxury",
        "price_per_day": 300,
        "image": "static/images/cars/mercedes_sclass.jpg",
        "seats": 5,
        "transmission": "Automatic",
        "features": ["Massage Seats", "Executive Package", "MBUX System", "Burmester Sound"],
        "rating": 4.9
    }
]

# Mock maintenance predictions
maintenance_predictions = {
    1: {"next_service": "2023-11-15", "predicted_issues": ["Battery health check recommended", "Software update pending"], "reliability_score": 95},
    2: {"next_service": "2023-10-30", "predicted_issues": ["Oil change needed", "Tire rotation recommended"], "reliability_score": 92},
    3: {"next_service": "2023-12-05", "predicted_issues": ["Brake inspection recommended", "Air filter replacement"], "reliability_score": 88},
    4: {"next_service": "2023-11-20", "predicted_issues": ["Transmission fluid check", "Alignment recommended"], "reliability_score": 90},
    5: {"next_service": "2023-10-25", "predicted_issues": ["Suspension check recommended", "Front brakes at 30%"], "reliability_score": 85},
    6: {"next_service": "2023-12-15", "predicted_issues": ["System diagnostics recommended", "Interior sanitization due"], "reliability_score": 93}
}

@app.route('/')
def home():
    featured_cars = random.sample(cars, min(3, len(cars)))
    return render_template('index.html', featured_cars=featured_cars)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/ai_recommendation')
def ai_recommendation():
    return render_template('ai_recommendation.html', cars=cars)

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    # Get user preferences from form
    preferences = request.form.to_dict()
    
    # Simple AI recommendation algorithm (in a real scenario this would be more sophisticated)
    recommended_cars = []
    for car in cars:
        score = 0
        # Match category preference
        if preferences.get('category') == car['category']:
            score += 3
        
        # Match price range
        try:
            max_price = int(preferences.get('max_price', 1000))
            if car['price_per_day'] <= max_price:
                score += 2
            else:
                score -= 3  # Penalize for being over budget
        except ValueError:
            pass
            
        # Match seats preference
        try:
            seats_needed = int(preferences.get('seats', 0))
            if car['seats'] >= seats_needed:
                score += 1
        except ValueError:
            pass
            
        # Additional feature matching could be added here
        
        if score > 0:
            recommended_cars.append({
                "car": car,
                "match_score": min(score * 20, 100)  # Convert to percentage with max of 100%
            })
    
    # Sort by match score
    recommended_cars.sort(key=lambda x: x['match_score'], reverse=True)
    
    return jsonify({
        "recommendations": recommended_cars[:3],  # Return top 3 matches
        "explanation": "These cars were matched based on your preferences for category, budget, and seating capacity."
    })

@app.route('/virtual_tour')
def virtual_tour():
    return render_template('virtual_tour.html')

@app.route('/smart_pricing')
def smart_pricing():
    # Dynamic pricing based on day of week, demand, etc.
    price_adjustments = {}
    for car in cars:
        base_price = car['price_per_day']
        weekend_price = round(base_price * 1.25, 2)  # 25% more expensive on weekends
        holiday_price = round(base_price * 1.4, 2)  # 40% more expensive on holidays
        low_demand_price = round(base_price * 0.85, 2)  # 15% discount during low demand
        
        price_adjustments[car['id']] = {
            "base_price": base_price,
            "weekend_price": weekend_price,
            "holiday_price": holiday_price,
            "low_demand_price": low_demand_price
        }
    
    # Generate some future dates for price prediction demo
    today = datetime.now()
    future_dates = []
    for i in range(14):
        future_date = today + timedelta(days=i)
        is_weekend = future_date.weekday() >= 5  # 5 = Saturday, 6 = Sunday
        
        # Simulate some holiday dates
        is_holiday = future_date.strftime('%m-%d') in ['07-04', '12-25', '12-31', '01-01']
        
        # Simulate demand based on day of week
        demand_factor = random.uniform(0.8, 1.2)
        if is_weekend:
            demand_factor *= 1.1
        if is_holiday:
            demand_factor *= 1.3
            
        future_dates.append({
            "date": future_date.strftime('%Y-%m-%d'),
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
            "demand_factor": round(demand_factor, 2)
        })
    
    return render_template('smart_pricing.html', cars=cars, price_adjustments=price_adjustments, future_dates=future_dates)

@app.route('/predictive_maintenance')
def predictive_maintenance():
    return render_template('predictive_maintenance.html', cars=cars, predictions=maintenance_predictions)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    
    if query:
        for car in cars:
            if (query in car['name'].lower() or 
                query in car['category'].lower() or 
                any(query in feature.lower() for feature in car['features'])):
                results.append(car)
    
    return render_template('search_results.html', results=results, query=query)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message', '').lower()
    
    # Simple AI chatbot responses
    responses = {
        "hello": "Hello! How can I help you with your car rental today?",
        "hi": "Hi there! Looking to rent a car? I'm here to assist you.",
        "booking": "To make a booking, simply select a car and click on the 'Book Now' button. You'll need to provide your rental dates and driver information.",
        "price": "Our prices vary based on the car model, rental duration, and season. You can check out our 'Smart Pricing' page for detailed information.",
        "payment": "We accept all major credit cards, PayPal, and Apple Pay. Payment is processed securely at the time of booking.",
        "cancel": "Cancellations made 48 hours before the pickup time receive a full refund. Late cancellations may incur a fee.",
        "insurance": "We offer various insurance packages starting from $15 per day. Full coverage is recommended for peace of mind.",
        "requirements": "To rent a car, you need to be at least 21 years old, have a valid driver's license, and a credit card in your name."
    }
    
    # Check for keyword matches
    for keyword, response in responses.items():
        if keyword in user_message:
            return jsonify({"response": response})
    
    # Default response
    return jsonify({
        "response": "I'm not sure I understand your question. Would you like to know about our cars, pricing, or booking process?"
    })

if __name__ == '__main__':
    app.run(debug=True)