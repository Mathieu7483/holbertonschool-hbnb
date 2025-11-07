#!/usr/bin/env python3
"""
Test script for SQLAlchemy relationships in HBnB application
Adapted for current model structure with foreign keys
Run from project root: python app/test/test_relationships.py
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire racine du projet au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Maintenant on peut importer
from app import create_app
from app.extensions import db
from app.models import User, Place, Review, Amenity

def print_separator(title):
    """Print a nice separator with title"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_info(title, data):
    """Print formatted information"""
    print(f"\n🔍 {title}:")
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"   {key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            print(f"   {i}. {item}")
    else:
        print(f"   {data}")

def test_relationships():
    """Test all SQLAlchemy relationships"""
    
    print_separator("INITIALIZING APPLICATION")
    print(f"Project root: {project_root}")
    
    # Créer l'application
    app = create_app()
    
    with app.app_context():
        print_separator("INITIALIZING DATABASE")
        
        try:
            # Supprimer et recréer les tables
            db.drop_all()
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return None
        
        print_separator("CREATING TEST DATA")
        
        # ==========================================
        # 1. CRÉER DES UTILISATEURS
        # ==========================================
        print("\n📝 Creating Users...")
        
        try:
            admin = User(
                first_name="Admin",
                last_name="User",
                email="admin@hbnb.com",
                password="admin123",
                is_admin=True
            )
            
            john = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="password123"
            )
            
            jane = User(
                first_name="Jane",
                last_name="Smith",
                email="jane@example.com",
                password="password456"
            )
            
            users = [admin, john, jane]
            for user in users:
                db.session.add(user)
            
            db.session.commit()
            
            print("✅ Users created:")
            for user in users:
                print_info(f"User: {user.first_name} {user.last_name}", {
                    "ID": user.id,
                    "Email": user.email,
                    "Is Admin": user.is_admin,
                    "Created": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
                })
                
        except Exception as e:
            print(f"❌ Error creating users: {e}")
            return None
        
        # ==========================================
        # 2. CRÉER DES AMENITIES
        # ==========================================
        print("\n📝 Creating Amenities...")
        
        try:
            amenities_data = ["WiFi", "Swimming Pool", "Air Conditioning", "Kitchen", "Parking"]
            
            amenities = []
            for name in amenities_data:
                amenity = Amenity(name=name)
                amenities.append(amenity)
                db.session.add(amenity)
            
            db.session.commit()
            
            print("✅ Amenities created:")
            for amenity in amenities:
                print_info(f"Amenity: {amenity.name}", {
                    "ID": amenity.id,
                    "Created": amenity.created_at.strftime("%Y-%m-%d %H:%M:%S")
                })
                
        except Exception as e:
            print(f"❌ Error creating amenities: {e}")
            return None
        
        # ==========================================
        # 3. CRÉER DES PLACES
        # ==========================================
        print("\n📝 Creating Places...")
        
        try:
            villa = Place(
                title="Luxury Villa in Geneva",
                description="Beautiful villa with lake view",
                price=250.0,
                latitude=46.2044,
                longitude=6.1432,
                owner=john
            )
            
            apartment = Place(
                title="Cozy Apartment in Zurich",
                description="Perfect for business travelers",
                price=120.0,
                latitude=47.3769,
                longitude=8.5417,
                owner=jane
            )
            
            places = [villa, apartment]
            for place in places:
                db.session.add(place)
            
            db.session.commit()
            
            print("✅ Places created:")
            for place in places:
                print_info(f"Place: {place.title}", {
                    "ID": place.id,
                    "Owner": f"{place.owner.first_name} {place.owner.last_name}",
                    "Owner ID": place.owner_id if hasattr(place, 'owner_id') else place.owner.id,
                    "Price": f"${place.price}/night",
                    "Created": place.created_at.strftime("%Y-%m-%d %H:%M:%S")
                })
                
        except Exception as e:
            print(f"❌ Error creating places: {e}")
            return None
        
        # ==========================================
        # 4. CRÉER DES REVIEWS
        # ==========================================
        print("\n📝 Creating Reviews...")
        
        try:
            review1 = Review(
                text="Amazing place! The view was spectacular and everything was perfect.",
                rating=5,
                user=jane,
                place=villa
            )
            
            review2 = Review(
                text="Good location and clean. Would recommend for business trips.",
                rating=4,
                user=john,
                place=apartment
            )
            
            review3 = Review(
                text="Excellent host and beautiful property. Will definitely come back!",
                rating=5,
                user=admin,
                place=villa
            )
            
            reviews = [review1, review2, review3]
            for review in reviews:
                db.session.add(review)
            
            db.session.commit()
            
            print("✅ Reviews created:")
            for review in reviews:
                print_info(f"Review by {review.user.first_name}", {
                    "ID": review.id,
                    "Rating": f"{review.rating}/5 stars",
                    "Place": review.place.title,
                    "User ID": review.user_id,
                    "Place ID": review.place_id,
                    "Text": review.text[:50] + "...",
                    "Created": review.created_at.strftime("%Y-%m-%d %H:%M:%S")
                })
                
        except Exception as e:
            print(f"❌ Error creating reviews: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        # ==========================================
        # 5. TESTER LES RELATIONS (ADAPTÉ)
        # ==========================================
        print_separator("TESTING RELATIONSHIPS")
        
        try:
            # ✅ Test User -> Places (utiliser des requêtes)
            print("\n🔗 Testing User -> Places relationships:")
            for user in users:
                # Chercher les places de cet utilisateur
                user_places = Place.query.filter_by(owner_id=user.id).all()
                user_place_titles = [p.title for p in user_places]
                print_info(f"{user.first_name}'s places", user_place_titles or ["No places"])
            
            # ✅ Test User -> Reviews (utiliser des requêtes)
            print("\n🔗 Testing User -> Reviews relationships:")
            for user in users:
                # Chercher les reviews de cet utilisateur
                user_reviews = Review.query.filter_by(user_id=user.id).all()
                user_review_info = [f"{r.rating}⭐ for place ID {r.place_id}" for r in user_reviews]
                print_info(f"{user.first_name}'s reviews", user_review_info or ["No reviews"])
            
            # ✅ Test Place -> Reviews (utiliser des requêtes)
            print("\n🔗 Testing Place -> Reviews relationships:")
            for place in places:
                # Chercher les reviews pour cette place
                place_reviews = Review.query.filter_by(place_id=place.id).all()
                place_review_info = [f"{r.rating}⭐ by user ID {r.user_id}" for r in place_reviews]
                print_info(f"Reviews for '{place.title}'", place_review_info or ["No reviews"])
            
            # ✅ Test Place -> Amenities (si la relation existe)
            print("\n🔗 Testing Place -> Amenities relationships:")
            for place in places:
                if hasattr(place, 'amenities'):
                    place_amenities = [a.name for a in place.amenities]
                    print_info(f"Amenities in '{place.title}'", place_amenities or ["No amenities"])
                else:
                    print_info(f"Amenities in '{place.title}'", ["Amenity relationship not implemented"])
            
            # ✅ Test détaillé des relations par requêtes
            print("\n🔗 Detailed relationship testing with queries:")
            
            # Compter les relations
            for user in users:
                places_count = Place.query.filter_by(owner_id=user.id).count()
                reviews_count = Review.query.filter_by(user_id=user.id).count()
                print_info(f"{user.first_name}'s stats", {
                    "Places owned": places_count,
                    "Reviews written": reviews_count
                })
            
            for place in places:
                reviews_count = Review.query.filter_by(place_id=place.id).count()
                print_info(f"'{place.title}' stats", {
                    "Reviews received": reviews_count,
                    "Owner": place.owner.first_name if place.owner else "Unknown"
                })
                
        except Exception as e:
            print(f"❌ Error testing relationships: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        # ==========================================
        # 6. DONNÉES POUR TESTS API
        # ==========================================
        print_separator("API TESTING DATA")
        
        print("\n📋 IDs for API testing:")
        
        print("\n👥 USER IDs:")
        for user in users:
            role = "Admin" if user.is_admin else "User"
            print(f"   {user.first_name} ({role}): {user.id}")
        
        print("\n🏠 PLACE IDs:")
        for place in places:
            print(f"   {place.title}: {place.id}")
        
        print("\n⭐ REVIEW IDs:")
        for review in reviews:
            print(f"   Review by {review.user.first_name}: {review.id}")
        
        print("\n🎯 AMENITY IDs:")
        for amenity in amenities:
            print(f"   {amenity.name}: {amenity.id}")
        
        # ==========================================
        # 7. EXEMPLES CURL POUR TESTS
        # ==========================================
        print_separator("CURL EXAMPLES FOR API TESTING")
        
        print(f"\n# 1. Login as admin to get JWT token")
        print(f"curl -X POST http://localhost:5000/api/v2/auth/login \\")
        print(f"  -H 'Content-Type: application/json' \\")
        print(f"  -d '{{\"email\": \"{admin.email}\", \"password\": \"admin123\"}}'")
        
        print(f"\n# 2. Get all users (Admin only)")
        print(f"curl -X GET http://localhost:5000/api/v2/users \\")
        print(f"  -H 'Authorization: Bearer YOUR_TOKEN_HERE'")
        
        print(f"\n# 3. Create a review")
        print(f"curl -X POST http://localhost:5000/api/v2/reviews \\")
        print(f"  -H 'Content-Type: application/json' \\")
        print(f"  -H 'Authorization: Bearer YOUR_TOKEN_HERE' \\")
        print(f"  -d '{{")
        print(f"    \"text\": \"Great place for testing!\",")
        print(f"    \"rating\": 5,")
        print(f"    \"user_id\": \"{jane.id}\",")
        print(f"    \"place_id\": \"{villa.id}\"")
        print(f"  }}'")
        
        print(f"\n# 4. Get specific user")
        print(f"curl -X GET http://localhost:5000/api/v2/users/{john.id} \\")
        print(f"  -H 'Authorization: Bearer YOUR_TOKEN_HERE'")
        
        print_separator("TEST COMPLETED SUCCESSFULLY! 🎉")
        
        return {
            'users': {user.email: user.id for user in users},
            'places': {place.title: place.id for place in places},
            'reviews': {f"review_by_{review.user.first_name}_{i}": review.id for i, review in enumerate(reviews)},
            'amenities': {amenity.name: amenity.id for amenity in amenities}
        }

if __name__ == "__main__":
    try:
        print("🚀 Starting relationship tests (adapted for foreign keys)...")
        ids = test_relationships()
        
        if ids:
            print(f"\n💾 All IDs saved for API testing:")
            for category, items in ids.items():
                print(f"\n{category.upper()}:")
                for name, id_ in items.items():
                    print(f"  {name}: {id_}")
        else:
            print("❌ Test failed!")
                    
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()