import requests
import json
import uuid

# ======================================================================
# CONFIGURATION
# ======================================================================
BASE_URL = "http://127.0.0.1:5000/api/v2" # Assurez-vous que le port est correct

# Variables pour stocker les IDs et les tokens
IDS = {
    'ADMIN_ID': None,
    'USER_ID': None,
    'OWNER_ID': None, # Nouvelle variable pour le créateur de la Place
    'AMENITY_ID': None,
    'PLACE_ID': None,
    'REVIEW_ID': None,
    'ADMIN_TOKEN': None,
    'USER_TOKEN': None,
    'OWNER_TOKEN': None,
}

# --- Utility Functions ---

def print_result(success, message):
    """Affiche le résultat d'un test avec une coche ou une croix."""
    status = "✅" if success else "❌"
    print(f"  {status} {message}")
    
def test_abort(message):
    """Affiche un message d'échec critique et termine les tests."""
    print(f"\n--- ❌ CRITICAL FAILURE ---")
    print(f"  ABORTING TESTS: {message}")
    print("----------------------------\n")
    return False

# ======================================================================
# FONCTION PRINCIPALE DE TEST
# ======================================================================

def run_api_tests():
    """Exécute une suite de tests d'intégration de bout en bout sur l'API."""
    
    print("--- 🎬 STARTING END-TO-END API TESTS ---")

    # --- 1. SETUP: CREATE USERS & AUTHENTICATION ---
    print("\n--- 1. SETUP: Users & Authentication ---")

    # 1A. Création d'un utilisateur Admin
    print("\n[1A: POST /users] - Creating Admin User")
    admin_data = {"first_name": "Admin", "last_name": "God", "email": "admin@hbnb.com", "password": "admin_password", "is_admin": True}
    try:
        response = requests.post(f"{BASE_URL}/users", json=admin_data)
        if response.status_code == 201:
            IDS['ADMIN_ID'] = response.json().get('id')
            print_result(True, f"Admin created. ID: {IDS['ADMIN_ID']}")
            print(f"    -> ADMIN ID generated: {IDS['ADMIN_ID']}")
        else:
            return test_abort(f"FAILED TO CREATE ADMIN: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        return test_abort("CONNECTION ERROR: Is the Flask server running?")

    # 1B. Création d'un utilisateur qui sera le Propriétaire (Owner) de la Place
    print("[1B: POST /users] - Creating Place Owner User")
    owner_data = {"first_name": "Place", "last_name": "Owner", "email": "owner@hbnb.com", "password": "owner_password"}
    response = requests.post(f"{BASE_URL}/users", json=owner_data)
    if response.status_code == 201:
        IDS['OWNER_ID'] = response.json().get('id')
        print_result(True, f"Owner user created. ID: {IDS['OWNER_ID']}")
        print(f"    -> OWNER ID generated: {IDS['OWNER_ID']}")
    else:
        return test_abort(f"FAILED TO CREATE OWNER: {response.status_code} - {response.text}")

    # 1C. Création d'un utilisateur normal (Reviewer)
    print("[1C: POST /users] - Creating Normal User (Reviewer)")
    user_data = {"first_name": "Normal", "last_name": "Reviewer", "email": "user@hbnb.com", "password": "user_password"}
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    if response.status_code == 201:
        IDS['USER_ID'] = response.json().get('id')
        print_result(True, f"Normal user created. ID: {IDS['USER_ID']}")
        print(f"    -> USER ID generated: {IDS['USER_ID']}")
    else:
        return test_abort(f"FAILED TO CREATE USER: {response.status_code} - {response.text}")

    # 1D. Authentification de l'Admin
    print("\n[1D: POST /auth/login] - Authenticating Admin")
    login_data = {"email": "admin@hbnb.com", "password": "admin_password"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        IDS['ADMIN_TOKEN'] = response.json().get('access_token')
        print_result(True, "Admin authenticated, token received.")
        print(f"    -> ADMIN TOKEN received: {IDS['ADMIN_TOKEN'][:25]}...")
    else:
        return test_abort(f"FAILED TO AUTHENTICATE ADMIN: {response.status_code} - {response.text}")
        
    # 1E. Authentification de l'Owner
    print("[1E: POST /auth/login] - Authenticating Owner")
    login_data = {"email": "owner@hbnb.com", "password": "owner_password"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        IDS['OWNER_TOKEN'] = response.json().get('access_token')
        print_result(True, "Owner authenticated, token received.")
        print(f"    -> OWNER TOKEN received: {IDS['OWNER_TOKEN'][:25]}...")
    else:
        return test_abort(f"FAILED TO AUTHENTICATE OWNER: {response.status_code} - {response.text}")

    # 1F. Authentification de l'User (Reviewer)
    print("[1F: POST /auth/login] - Authenticating Reviewer")
    login_data = {"email": "user@hbnb.com", "password": "user_password"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        IDS['USER_TOKEN'] = response.json().get('access_token')
        print_result(True, "Reviewer authenticated, token received.")
        print(f"    -> USER TOKEN received: {IDS['USER_TOKEN'][:25]}...")
    else:
        return test_abort(f"FAILED TO AUTHENTICATE REVIEWER: {response.status_code} - {response.text}")

    # Résumé des IDs et Tokens
    print("\n--- Summary of Generated IDs and Tokens ---")
    print(f"  Admin ID: {IDS['ADMIN_ID']}")
    print(f"  Owner ID: {IDS['OWNER_ID']}")
    print(f"  User ID:  {IDS['USER_ID']}")
    print(f"  Admin Token (truncated): {IDS['ADMIN_TOKEN'][:25]}...")
    print(f"  Owner Token (truncated): {IDS['OWNER_TOKEN'][:25]}...")
    print(f"  User Token (truncated):  {IDS['USER_TOKEN'][:25]}...")
    print("------------------------------------------")


    # Préparer les headers
    admin_headers = {'Authorization': f'Bearer {IDS["ADMIN_TOKEN"]}'}
    owner_headers = {'Authorization': f'Bearer {IDS["OWNER_TOKEN"]}'}
    user_headers = {'Authorization': f'Bearer {IDS["USER_TOKEN"]}'}


    # --- 2. AMENITY & PLACE CREATION ---
    print("\n--- 2. AMENITY & PLACE CREATION ---")
    
    # 2A. Création Amenity (par l'Admin)
    print("\n[2A: POST /amenities] - Admin creates Amenity")
    amenity_data = {"name": "Piscine"}
    response = requests.post(f"{BASE_URL}/amenities", json=amenity_data, headers=admin_headers)
    if response.status_code == 201:
        IDS['AMENITY_ID'] = response.json().get('id')
        print_result(True, f"Amenity created by Admin. ID: {IDS['AMENITY_ID']}")
        print(f"    -> AMENITY ID generated: {IDS['AMENITY_ID']}")
    else:
        return test_abort(f"FAILED TO CREATE AMENITY: {response.status_code} - {response.text}")
        
    # 2B. Modification Amenity (par l'Admin)
    print("[2B: PUT /amenities/<id>] - Admin modifies Amenity")
    response = requests.put(f"{BASE_URL}/amenities/{IDS['AMENITY_ID']}", json={"name": "Piscine Olympique"}, headers=admin_headers)
    if response.status_code == 200 and response.json().get('name') == "Piscine Olympique":
        print_result(True, "Amenity modified successfully by Admin.")
    else:
        print_result(False, f"FAILED to modify Amenity: {response.status_code} - {response.text}")
        
    # 2C. Création Place (par l'Owner)
    print("\n[2C: POST /places] - Owner creates Place")
    place_data = {
        "title": "Owner's Villa",
        "description": "Vue imprenable",
        "price": 300.0,
        "owner_id": IDS['OWNER_ID'], # Le lieu appartient à l'Owner
        "latitude": 46.3626,       
        "longitude": 6.8045,       
        "amenities": [IDS['AMENITY_ID']]
    }
    response = requests.post(f"{BASE_URL}/places", json=place_data, headers=owner_headers)
    if response.status_code == 201:
        IDS['PLACE_ID'] = response.json().get('id')
        print_result(True, f"Place created by Owner. ID: {IDS['PLACE_ID']}")
        print(f"    -> PLACE ID generated: {IDS['PLACE_ID']}")
    else:
        return test_abort(f"FAILED TO CREATE PLACE BY OWNER: {response.status_code} - {response.text}")
        
    # 2D. Création Place (par l'Admin) - Vérification optionnelle
    # Cette étape est moins critique pour les règles métier, mais valide le droit de l'Admin.
    print("[2D: POST /places] - Admin creates second Place")
    admin_place_data = {
        "title": "Admin's Place",
        "description": "Lieu d'admin",
        "price": 100.0,
        "owner_id": IDS['ADMIN_ID'],
        "latitude": 10.0,
        "longitude": 10.0,
        "amenities": []
    }
    response = requests.post(f"{BASE_URL}/places", json=admin_place_data, headers=admin_headers)
    print_result(response.status_code == 201, "Admin successfully created a Place.")


    # --- 3. PLACE UPDATE SECURITY ---
    print("\n--- 3. PLACE UPDATE Security Checks ---")
    
    # 3A. Modification Place par l'Owner (OK)
    print("\n[3A: PUT /places/<id>] - Owner modifies their own Place")
    response = requests.put(f"{BASE_URL}/places/{IDS['PLACE_ID']}", json={"description": "Vue imprenable et jacuzzi"}, headers=owner_headers)
    if response.status_code == 200 and "jacuzzi" in response.json().get('description', ''):
        print_result(True, "Owner successfully updated their own Place.")
    else:
        print_result(False, f"FAILED: Owner should be able to update their Place: {response.status_code} - {response.text}")
        
    # 3B. Modification Place par l'Admin (OK)
    print("[3B: PUT /places/<id>] - Admin modifies Place (Owner's)")
    response = requests.put(f"{BASE_URL}/places/{IDS['PLACE_ID']}", json={"price": 350.0}, headers=admin_headers)
    if response.status_code == 200 and response.json().get('price') == 350.0:
        print_result(True, "Admin successfully updated the Owner's Place.")
    else:
        print_result(False, f"FAILED: Admin should be able to update any Place: {response.status_code} - {response.text}")

    # 3C. Modification Place par un User Tiers (DOIT ÉCHOUER)
    print("[3C: PUT /places/<id>] - User (Reviewer) tries to modify Place (Expected 403/401)")
    response = requests.put(f"{BASE_URL}/places/{IDS['PLACE_ID']}", json={"price": 100.0}, headers=user_headers)
    print_result(response.status_code in [401, 403], f"Security check passed: Third-party User forbidden to update (Got {response.status_code}).")


    # --- 4. REVIEW CREATION SECURITY ---
    print("\n--- 4. REVIEW Creation Security Checks ---")

    # 4A. Création Review par l'User (Reviewer) (OK)
    print("\n[4A: POST /reviews] - Reviewer creates Review (OK)")
    review_data = {
        "text": "Exceptionnel !", 
        "rating": 5,
        "place_id": IDS['PLACE_ID'], 
        "user_id": IDS['USER_ID'] 
    }
    response = requests.post(f"{BASE_URL}/reviews", json=review_data, headers=user_headers)
    if response.status_code == 201:
        IDS['REVIEW_ID'] = response.json().get('id')
        print_result(True, f"Review created by Reviewer. ID: {IDS['REVIEW_ID']}")
        print(f"    -> REVIEW ID generated: {IDS['REVIEW_ID']}")
    else:
        return test_abort(f"FAILED TO CREATE REVIEW BY REVIEWER: {response.status_code} - {response.text}")

    # 4B. User (Reviewer) essaie de poster une 2e Review sur la même Place (DOIT ÉCHOUER 409)
    print("[4B: POST /reviews] - Reviewer tries to create a 2nd Review (Expected 409 Conflict)")
    response = requests.post(f"{BASE_URL}/reviews", json=review_data, headers=user_headers)
    print_result(response.status_code == 409, f"Security check passed: User cannot post multiple reviews (Got {response.status_code}).")

    # 4C. Owner essaie de poster Review sur sa propre Place (DOIT ÉCHOUER 403)
    print("[4C: POST /reviews] - Owner tries to review their own Place (Expected 403 Forbidden)")
    owner_review_data = {
        "text": "Ma place est la meilleure!", 
        "rating": 5,
        "place_id": IDS['PLACE_ID'], 
        "user_id": IDS['OWNER_ID'] # L'Owner essaie de poster
    }
    response = requests.post(f"{BASE_URL}/reviews", json=owner_review_data, headers=owner_headers)
    print_result(response.status_code == 403, f"Security check passed: Owner forbidden to review own Place (Got {response.status_code}).")


    # --- 5. REVIEW UPDATE SECURITY ---
    print("\n--- 5. REVIEW Update Security Checks ---")

    # 5A. Auteur (User/Reviewer) modifie sa propre Review (OK)
    print("\n[5A: PUT /reviews/<id>] - Author modifies their Review")
    response = requests.put(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", json={"text": "Exceptionnel, mais un peu cher."}, headers=user_headers)
    if response.status_code == 200 and "un peu cher" in response.json().get('text', ''):
        print_result(True, "Author successfully updated their Review.")
    else:
        print_result(False, f"FAILED: Author should be able to update their Review: {response.status_code} - {response.text}")

    # 5B. Admin modifie la Review (OK)
    print("[5B: PUT /reviews/<id>] - Admin modifies Review")
    response = requests.put(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", json={"rating": 4}, headers=admin_headers)
    if response.status_code == 200 and response.json().get('rating') == 4:
        print_result(True, "Admin successfully updated the Review.")
    else:
        print_result(False, f"FAILED: Admin should be able to update any Review: {response.status_code} - {response.text}")

    # 5C. Owner essaie de modifier la Review (DOIT ÉCHOUER 403)
    print("[5C: PUT /reviews/<id>] - Owner tries to modify Review (Expected 403 Forbidden)")
    response = requests.put(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", json={"rating": 1}, headers=owner_headers)
    print_result(response.status_code == 403, f"Security check passed: Owner forbidden to modify review (Got {response.status_code}).")


    # --- 6. USER DELETION SECURITY ---
    print("\n--- 6. USER Deletion Security Checks ---")

    # 6A. Admin supprime l'User (Owner) (OK)
    print(f"\n[6A: DELETE /users/{IDS['OWNER_ID']}] - Admin deletes Owner")
    response = requests.delete(f"{BASE_URL}/users/{IDS['OWNER_ID']}", headers=admin_headers)
    if response.status_code == 204:
        print_result(True, "Admin successfully deleted the Owner.")
    else:
        print_result(False, f"FAILED: Admin should be able to delete another user: {response.status_code} - {response.text}")
        
    # 6B. Admin essaie de s'auto-supprimer (DOIT ÉCHOUER 403)
    print(f"[6B: DELETE /users/{IDS['ADMIN_ID']}] - Admin tries to self-delete (Expected 403 Forbidden)")
    response = requests.delete(f"{BASE_URL}/users/{IDS['ADMIN_ID']}", headers=admin_headers)
    print_result(response.status_code == 403, f"Security check passed: Admin self-deletion forbidden (Got {response.status_code}).")
        

    # 7A. Suppression du Reviewer restant (User normal)
    print(f"[7A: DELETE /users/{IDS['USER_ID']}] - Final Reviewer Cleanup")
    response = requests.delete(f"{BASE_URL}/users/{IDS['USER_ID']}", headers=admin_headers)
    if response.status_code == 204:
        print_result(True, "Final cleanup: Reviewer deleted successfully (204).")
    else:
        print_result(False, f"CLEANUP FAILED: FAILED TO DELETE REVIEWER: {response.status_code} - {response.text}")
    
    # 7B. Suppression finale de l'Admin (s'il n'y a plus de données liées)
    print(f"[7B: DELETE /users/{IDS['ADMIN_ID']}] - Final Admin Cleanup")
    response = requests.delete(f"{BASE_URL}/users/{IDS['ADMIN_ID']}", headers=admin_headers)
    if response.status_code == 403:
         print_result(True, "Admin self-deletion check confirmed (403).")
    elif response.status_code == 204:
         print_result(True, "Admin deleted successfully (204).")
    else:
         print_result(False, f"CLEANUP FAILED: Admin deletion failed with {response.status_code} - {response.text}")
        
    print("\n--- 🏁 END OF API TESTS ---")

if __name__ == "__main__":
    run_api_tests()
