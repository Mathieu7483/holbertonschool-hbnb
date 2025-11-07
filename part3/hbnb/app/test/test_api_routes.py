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
    'USER_TOKEN': None, # Token pour l'utilisateur normal
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
    login_data_admin = {"email": "admin@hbnb.com", "password": "admin_password"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data_admin)
    if response.status_code == 200:
        IDS['ADMIN_TOKEN'] = response.json()['access_token']
        print("  ✅ Admin authenticated, token received.")
    else:
        print(f"  ❌ FAILED TO AUTHENTICATE ADMIN: {response.status_code} - {response.text}"); return
        
    # D. Authentification de l'utilisateur normal pour obtenir un token
    print("\n[1D: POST /auth/login] - Authenticating Normal User")
    login_data_user = {"email": "user@hbnb.com", "password": "user_password"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data_user)
    if response.status_code == 200:
        IDS['USER_TOKEN'] = response.json()['access_token']
        print("  ✅ Normal user authenticated, token received.")
    else:
        print(f"  ❌ FAILED TO AUTHENTICATE USER: {response.status_code} - {response.text}"); return

    # Préparer les headers pour les requêtes authentifiées (Admin et User)
    admin_auth_headers = {'Authorization': f'Bearer {IDS["ADMIN_TOKEN"]}'}
    user_auth_headers = {'Authorization': f'Bearer {IDS["USER_TOKEN"]}'}


    # --- 2. CRUD OPERATIONS ---
    print("\n--- 2. CRUD Operations (Amenity, Place, Review) ---")
    
    # A. Création Amenity (par l'Admin)
    print("\n[2A: POST /amenities]")
    amenity_data = {"name": "Piscine Olympique"}
    response = requests.post(f"{BASE_URL}/amenities", json=amenity_data, headers=admin_auth_headers)
    if response.status_code == 201:
        IDS['AMENITY_ID'] = response.json()['id']
        print(f"  ✅ Amenity created. ID: {IDS['AMENITY_ID']}")
    else:
        print(f"  ❌ FAILED TO CREATE AMENITY: {response.status_code} - {response.text}"); return
        
    # B. Création Place (par l'Admin)
    print("\n[2B: POST /places]")
    place_data = {
        "title": "Villa Paradiso",
        "description": "Un havre de paix.",
        "price": 300.0,
        "owner_id": IDS['ADMIN_ID'], # Le lieu appartient à l'Admin
        "latitude": 46.3626,       
        "longitude": 6.8045,       
        "amenities": [IDS['AMENITY_ID']]
    }
    response = requests.post(f"{BASE_URL}/places", json=place_data, headers=admin_auth_headers)
    if response.status_code == 201:
        IDS['PLACE_ID'] = response.json()['id']
        print(f"  ✅ Place created. ID: {IDS['PLACE_ID']}")
    else:
        print(f"  ❌ FAILED TO CREATE PLACE: {response.status_code} - {response.text}"); return
        
    # C. Création Review (par l'utilisateur NORMAL sur le lieu de l'Admin)
    print(f"\n[2C: POST /reviews] - Creating Review via Collection Endpoint")
    review_data = {
        "text": "Magnifique endroit!", 
        "rating": 5,
        "place_id": IDS['PLACE_ID'], 
        "user_id": IDS['USER_ID']   # L'ID de l'utilisateur normal
    }
    # Utiliser le token de l'utilisateur normal
    response = requests.post(f"{BASE_URL}/reviews", 
                             json=review_data, 
                             headers=user_auth_headers)
    
    if response.status_code == 201:
        IDS['REVIEW_ID'] = response.json()['id']
        print(f"  ✅ Review created. ID: {IDS['REVIEW_ID']}")
    else:
        print(f"  ❌ FAILED TO CREATE REVIEW: {response.status_code} - {response.text}"); return

    # --- 3. UPDATE (PUT) OPERATIONS ---
    print("\n--- 3. UPDATE Operations ---")

    print("\n[3A: PUT /places/<id>]")
    # Mise à jour effectuée par l'Admin (l'Admin est le propriétaire)
    response = requests.put(f"{BASE_URL}/places/{IDS['PLACE_ID']}", json={"price": 320.5}, headers=admin_auth_headers)
    if response.status_code == 200 and response.json()['price'] == 320.5:
        print("  ✅ Place price updated successfully.")
    else:
        print(f"  ❌ FAILED TO UPDATE PLACE: {response.status_code} - {response.text}")
        
    # --- 4. DELETE OPERATIONS (Admin required) ---
    print("\n--- 4. DELETE Operations (Admin Rights & Security Check) ---")

    # A. Suppression de la Review
    print(f"\n[4A: DELETE /reviews/{IDS['REVIEW_ID']}]")
    response = requests.delete(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", headers=admin_auth_headers)
    if response.status_code == 204:
        # Vérifier qu'elle n'existe plus
        check_response = requests.get(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", headers=admin_auth_headers)
        if check_response.status_code == 404:
            print("  ✅ Review deleted successfully (204) and confirmed not found (404).")
        else:
            print("  ❌ DELETE FAILED: Review deleted but still found.")
    else:
        print(f"  ❌ FAILED TO DELETE REVIEW: {response.status_code} - {response.text}")

    # B. Suppression du User NORMAL
    # Ceci devrait déclencher la suppression en cascade de la Place si votre ORM est configuré ainsi.
    print(f"\n[4B: DELETE /users/{IDS['USER_ID']}]")
    response = requests.delete(f"{BASE_URL}/users/{IDS['USER_ID']}", headers=admin_auth_headers)
    if response.status_code == 204:
        print("  ✅ Normal User deleted successfully (204).")
    else:
        print(f"  ❌ FAILED TO DELETE NORMAL USER: {response.status_code} - {response.text}")

    # C. TEST DE SÉCURITÉ : Tentative de suppression de l'Admin par lui-même (DOIT ÉCHOUER)
    # Valide la règle métier anti-auto-suppression (403).
    print(f"\n[4C: DELETE /users/{IDS['ADMIN_ID']}] - Testing Self-Deletion (Expected 403)")
    response = requests.delete(f"{BASE_URL}/users/{IDS['ADMIN_ID']}", headers=admin_auth_headers)
    if response.status_code == 403:
        print("  ✅ Security check passed: Admin self-deletion correctly forbidden (403).")
    else:
        print(f"  ❌ SECURITY FAILED: Admin self-deletion should be 403, got {response.status_code} - {response.text}")
        
    # D. CLEANUP FINAL (Suppression de l'Amenity)
    # Note : Le Place associé à l'Admin n'a pas été supprimé par l'Admin (étape 4C) et doit être géré ici
    # Si Place a été supprimé en cascade par la suppression du User (4B), cette étape n'est pas nécessaire.
    # Dans ce script, l'Admin (IDS['ADMIN_ID']) est toujours le propriétaire du Place.
    # Pour garantir le nettoyage, je vais ajouter la vérification de la suppression de la Place.
    
    # Tentative de suppression de la Place qui est liée à l'Admin (pour nettoyer)
    print(f"\n[4D: DELETE /places/{IDS['PLACE_ID']}] - Final Place Cleanup")
    response = requests.delete(f"{BASE_URL}/places/{IDS['PLACE_ID']}", headers=admin_auth_headers)
    if response.status_code == 204:
        print("  ✅ Final cleanup: Place deleted successfully (204).")
    else:
        print(f"  ❌ CLEANUP FAILED: FAILED TO DELETE PLACE: {response.status_code} - {response.text}")

    # Note : L'Admin lui-même (IDS['ADMIN_ID']) reste dans la base, ce qui est correct pour garantir la sécurité.
        
    print("\n--- 🏁 END OF API TESTS ---")

if __name__ == "__main__":
    run_api_tests()