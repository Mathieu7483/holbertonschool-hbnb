from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity # Ajouté pour tester les amenities
import datetime

def test_place_creation_and_relationships():
    # Préparation des données temporelles
    now_iso = datetime.datetime.now().isoformat()
    
    # 1. Création de l'Owner (doit fournir TOUS les 7 arguments de User.__init__)
    owner = User(
        id="user-1-owner-id",
        first_name="Alice", 
        last_name="Smith", 
        email="alice.smith@example.com",
        is_admin=False,
        created_at=now_iso,
        updated_at=now_iso
    )
    
    # 2. Création de la Place (ne manque aucun argument)
    # Note : Le BaseModel de Place doit aussi être initialisé dans son __init__
    place = Place(
        title="Cozy Apartment", 
        description="A nice place to stay", 
        price=100, 
        latitude=37.7749, 
        longitude=-122.4194, 
        owner=owner
    )
    
    # 3. Création d'une Review (doit fournir les arguments de Review.__init__)
    # (Nous supposons que Review.__init__ requiert id, created_at, updated_at comme User)
    review = Review(
        id="review-1-id",
        text="Great stay!", 
        rating=5, 
        place=place, 
        user=owner,
        created_at=now_iso,
        updated_at=now_iso
    )
    
    # 4. Création d'une Amenity (doit fournir les arguments de Amenity.__init__)
    # (Nous supposons qu'Amenity.__init__ requiert id, created_at, updated_at, et name)
    amenity = Amenity(
        id="amenity-1-id",
        name="Wifi",
        created_at=now_iso,
        updated_at=now_iso
    )
    
    # Ajout des relations
    place.add_review(review)
    place.add_amenity(amenity)
    
    # 5. Assertions (Tests de vérification)
    
    # Vérification des attributs de base
    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert isinstance(place.owner, User)
    
    # Vérification des relations (Reviews)
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    
    # Vérification des relations (Amenities)
    assert len(place.amenities) == 1
    assert place.amenities[0].name == "Wifi"
    
    print("Place model and relationship tests passed successfully!")

# Exécution du test
test_place_creation_and_relationships()