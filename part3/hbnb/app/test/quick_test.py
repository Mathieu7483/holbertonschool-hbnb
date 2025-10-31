"""
Quick relationship test
Run from project root: python app/test/quick_test.py
"""

import sys
import os

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def main():
    try:
        from app import create_app
        from app.extensions import db
        from app.models import User, Place, Review, Amenity
        
        print("✅ Imports successful!")
        print(f"Project root: {project_root}")
        
        app = create_app()
        with app.app_context():
            # Recréer la DB
            db.drop_all()
            db.create_all()
            print("✅ Database created!")
            
            # Test création
            user = User(
                first_name="Test", 
                last_name="User", 
                email="test@example.com", 
                password="test123"
            )
            db.session.add(user)
            db.session.commit()
            print(f"✅ User created with ID: {user.id}")
            
            place = Place(
                title="Test Place",
                description="A test place",
                price=100.0,
                latitude=46.0,
                longitude=6.0,
                owner=user
            )
            db.session.add(place)
            db.session.commit()
            print(f"✅ Place created with ID: {place.id}")
            
            amenity = Amenity(name="Test WiFi")
            db.session.add(amenity)
            db.session.commit()
            
            # Test many-to-many
            place.amenities.append(amenity)
            db.session.commit()
            print(f"✅ Amenity added to place")
            
            # Test relations
            print(f"\n🔗 Relations test:")
            print(f"   User places: {len(user.places)}")
            print(f"   Place amenities: {len(place.amenities)}")
            print(f"   Amenity places: {len(amenity.places)}")
            
            print(f"\n🎯 IDs for API testing:")
            print(f"   User ID: {user.id}")
            print(f"   Place ID: {place.id}")
            print(f"   Amenity ID: {amenity.id}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root directory")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()