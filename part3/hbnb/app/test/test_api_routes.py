# api_integration_test.py

import requests
import time
import json

# ======================================================================
# CONFIGURATION
# ======================================================================
BASE_URL = "http://127.0.0.1:5000/api/v2" # Assurez-vous que le port est correct

# Variables pour stocker les IDs et le token
IDS = {
    'ADMIN_ID': None,
    'USER_ID': None,
    'AMENITY_ID': None,
    'PLACE_ID': None,
    'REVIEW_ID': None,
    'ADMIN_TOKEN': None,
}

# ======================================================================
# FONCTION PRINCIPALE DE TEST
# ======================================================================

def run_api_tests():
    """Exécute une suite de tests d'intégration de bout en bout sur l'API."""
    
    print("--- 🎬 STARTING END-TO-END API TESTS ---")

    # --- 1. SETUP: CREATE AND AUTHENTICATE USERS ---
    print("\n--- 1. SETUP: Users & Authentication ---")

    # A. Création d'un utilisateur admin
    print("\n[1A: POST /users] - Creating Admin User")
    admin_data = {"first_name": "Admin", "last_name": "User", "email": "admin@hbnb.com", "password": "admin_password", "is_admin": True}
    try:
        response = requests.post(f"{BASE_URL}/users", json=admin_data)
        if response.status_code == 201:
            IDS['ADMIN_ID'] = response.json()['id']
            print(f"  ✅ Admin user created. ID: {IDS['ADMIN_ID']}")
        else:
            print(f"  ❌ FAILED TO CREATE ADMIN: {response.status_code} - {response.text}"); return
    except requests.exceptions.ConnectionError:
        print("  ❌ CONNECTION ERROR: Is the Flask server running?"); return

    # B. Création d'un utilisateur normal
    print("\n[1B: POST /users] - Creating Normal User")
    user_data = {"first_name": "Normal", "last_name": "User", "email": "user@hbnb.com", "password": "user_password"}
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    if response.status_code == 201:
        IDS['USER_ID'] = response.json()['id']
        print(f"  ✅ Normal user created. ID: {IDS['USER_ID']}")
    else:
        print(f"  ❌ FAILED TO CREATE USER: {response.status_code} - {response.text}"); return

    # C. Authentification de l'admin pour obtenir un token
    print("\n[1C: POST /auth/login] - Authenticating Admin")
    login_data = {"email": "admin@hbnb.com", "password": "admin_password"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        IDS['ADMIN_TOKEN'] = response.json()['access_token']
        print("  ✅ Admin authenticated, token received.")
    else:
        print(f"  ❌ FAILED TO AUTHENTICATE ADMIN: {response.status_code} - {response.text}"); return

    # Préparer les headers pour les requêtes authentifiées
    auth_headers = {'Authorization': f'Bearer {IDS["ADMIN_TOKEN"]}'}

    # --- 2. CRUD OPERATIONS ---
    print("\n--- 2. CRUD Operations (Amenity, Place, Review) ---")
    
    # A. Création Amenity
    print("\n[2A: POST /amenities]")
    amenity_data = {"name": "Piscine Olympique"}
    response = requests.post(f"{BASE_URL}/amenities", json=amenity_data, headers=auth_headers)
    if response.status_code == 201:
        IDS['AMENITY_ID'] = response.json()['id']
        print(f"  ✅ Amenity created. ID: {IDS['AMENITY_ID']}")
    else:
        print(f"  ❌ FAILED TO CREATE AMENITY: {response.status_code} - {response.text}"); return
        
    # B. Création Place (par l'utilisateur authentifié)
    print("\n[2B: POST /places]")
    place_data = {
        "title": "Villa Paradiso",
        "description": "Un havre de paix.",
        "price": 300.0,
        "owner_id": IDS['ADMIN_ID'], 
        "latitude": 46.3626,       
        "longitude": 6.8045,      
        "amenities": [IDS['AMENITY_ID']]
    }
    response = requests.post(f"{BASE_URL}/places", json=place_data, headers=auth_headers)
    if response.status_code == 201:
        IDS['PLACE_ID'] = response.json()['id']
        print(f"  ✅ Place created. ID: {IDS['PLACE_ID']}")
    else:
        print(f"  ❌ FAILED TO CREATE PLACE: {response.status_code} - {response.text}"); return
        
    # C. Création Review (par l'admin sur le lieu créé)
    # Utilisez la route de collection /reviews car c'est votre endpoint actif.
    print(f"\n[2C: POST /reviews] - Creating Review via Collection Endpoint")
    review_data = {
        "text": "Magnifique endroit!", 
        "rating": 5,
        "place_id": IDS['PLACE_ID'], # ID du lieu dans le payload
        "user_id": IDS['ADMIN_ID']   # ID de l'utilisateur dans le payload (doit être le même que l'authentifié)
    }
    response = requests.post(f"{BASE_URL}/reviews", 
                             json=review_data, 
                             headers=auth_headers)
    
    if response.status_code == 201:
        IDS['REVIEW_ID'] = response.json()['id']
        print(f"  ✅ Review created. ID: {IDS['REVIEW_ID']}")
    else:
        print(f"  ❌ FAILED TO CREATE REVIEW: {response.status_code} - {response.text}"); return

    # --- 3. UPDATE (PUT) OPERATIONS ---
    print("\n--- 3. UPDATE Operations ---")

    print("\n[3A: PUT /places/<id>]")
    # Tente de mettre à jour le lieu créé par l'admin
    response = requests.put(f"{BASE_URL}/places/{IDS['PLACE_ID']}", json={"price": 320.5}, headers=auth_headers)
    if response.status_code == 200 and response.json()['price'] == 320.5:
        print("  ✅ Place price updated successfully.")
    else:
        print(f"  ❌ FAILED TO UPDATE PLACE: {response.status_code} - {response.text}")
        
    # --- 4. DELETE OPERATIONS (Admin required) ---
    print("\n--- 4. DELETE Operations (Admin Rights) ---")

    # A. Suppression de la Review
    print(f"\n[4A: DELETE /reviews/{IDS['REVIEW_ID']}]")
    response = requests.delete(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", headers=auth_headers)
    if response.status_code == 204:
        # Vérifier qu'elle n'existe plus
        check_response = requests.get(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", headers=auth_headers)
        if check_response.status_code == 404:
            print("  ✅ Review deleted successfully (204) and confirmed not found (404).")
        else:
            print("  ❌ DELETE FAILED: Review deleted but still found.")
    else:
        print(f"  ❌ FAILED TO DELETE REVIEW: {response.status_code} - {response.text}")

    # B. Suppression du User (ce qui doit supprimer le Place en cascade)
    # On supprime l'utilisateur normal pour tester, l'admin peut aussi supprimer
    print(f"\n[4B: DELETE /users/{IDS['USER_ID']}]")
    response = requests.delete(f"{BASE_URL}/users/{IDS['USER_ID']}", headers=auth_headers)
    if response.status_code == 204:
        print("  ✅ User deleted successfully (204).")
    else:
        print(f"  ❌ FAILED TO DELETE USER: {response.status_code} - {response.text}")

    # C. Suppression de l'Admin (et vérification de la cascade du lieu)
    print(f"\n[4C: DELETE /users/{IDS['ADMIN_ID']}]")
    response = requests.delete(f"{BASE_URL}/users/{IDS['ADMIN_ID']}", headers=auth_headers)
    if response.status_code == 204:
        print("  ✅ Admin deleted successfully (204).")
        # Vérifier que le lieu (dont l'admin était propriétaire) a aussi été supprimé en cascade
        check_place_response = requests.get(f"{BASE_URL}/places/{IDS['PLACE_ID']}", headers=auth_headers)
        if check_place_response.status_code == 404:
            print("  ✅ Cascade delete confirmed: Associated place is also gone (404).")
        else:
            print(f"  ❌ CASCADE DELETE FAILED: Admin was deleted, but associated place still exists. Status: {check_place_response.status_code}")
    else:
        print(f"  ❌ FAILED TO DELETE ADMIN: {response.status_code} - {response.text}")
        
    print("\n--- 🏁 END OF API TESTS ---")

if __name__ == "__main__":
    run_api_tests()