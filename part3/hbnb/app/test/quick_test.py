import sys
import os
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
            
            # ✅ Test relations avec gestion des AppenderQuery
            print(f"\n🔗 Relations test:")
            
            # User places - utiliser len() directement
            try:
                user_places_count = len(user.places)
                print(f"   User places: {user_places_count}")
            except TypeError:
                # Si c'est une query, utiliser count()
                user_places_count = user.places.count() if hasattr(user.places, 'count') else 0
                print(f"   User places: {user_places_count}")
            
            # Place amenities
            try:
                place_amenities_count = len(place.amenities)
                print(f"   Place amenities: {place_amenities_count}")
            except TypeError:
                place_amenities_count = place.amenities.count() if hasattr(place.amenities, 'count') else 0
                print(f"   Place amenities: {place_amenities_count}")
            
            # ✅ Amenity places - gérer l'AppenderQuery
            try:
                amenity_places_count = len(amenity.places)
                print(f"   Amenity places: {amenity_places_count}")
            except TypeError:
                # Si c'est un AppenderQuery, utiliser count() ou convertir en liste
                if hasattr(amenity.places, 'count'):
                    amenity_places_count = amenity.places.count()
                elif hasattr(amenity.places, 'all'):
                    amenity_places_count = len(amenity.places.all())
                else:
                    amenity_places_count = 0
                print(f"   Amenity places: {amenity_places_count}")
            
            print(f"\n🎯 IDs for API testing:")
            print(f"   User ID: {user.id}")
            print(f"   Place ID: {place.id}")
            print(f"   Amenity ID: {amenity.id}")
            
            # ✅ Test plus détaillé des relations
            print(f"\n🔍 Detailed relations:")
            print(f"   User.places type: {type(user.places)}")
            print(f"   Place.amenities type: {type(place.amenities)}")
            print(f"   Amenity.places type: {type(amenity.places)}")
            
            # Test d'accès aux données
            print(f"\n📋 Data access test:")
            if hasattr(user, 'places'):
                for i, place_obj in enumerate(user.places):
                    print(f"   User place {i+1}: {place_obj.title}")
            
            if hasattr(place, 'amenities'):
                for i, amenity_obj in enumerate(place.amenities):
                    print(f"   Place amenity {i+1}: {amenity_obj.name}")
            
            # Pour amenity.places, gérer différents types
            if hasattr(amenity, 'places'):
                try:
                    places_list = list(amenity.places)  # Convertir en liste
                    for i, place_obj in enumerate(places_list):
                        print(f"   Amenity place {i+1}: {place_obj.title}")
                except:
                    try:
                        places_list = amenity.places.all()  # Si c'est une query
                        for i, place_obj in enumerate(places_list):
                            print(f"   Amenity place {i+1}: {place_obj.title}")
                    except:
                        print("   Could not access amenity places")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root directory")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()