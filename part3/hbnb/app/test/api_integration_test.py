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
    'OWNER_ID': None,
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

def main_test_suite():
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
        else:
            return test_abort(f"FAILED TO CREATE ADMIN: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        return test_abort("CONNECTION ERROR: Is the Flask server running?")

    # 1B, 1C, 1D, 1E, 1F: (Code d'authentification inchangé pour la concision)
    # 1B. Création d'un utilisateur Owner
    print("[1B: POST /users] - Creating Place Owner User")
    owner_data = {"first_name": "Place", "last_name": "Owner", "email": "owner@hbnb.com", "password": "owner_password"}
    response = requests.post(f"{BASE_URL}/users", json=owner_data)
    if response.status_code == 201:
        IDS['OWNER_ID'] = response.json().get('id')
        print_result(True, f"Owner user created. ID: {IDS['OWNER_ID']}")
    else:
        return test_abort(f"FAILED TO CREATE OWNER: {response.status_code} - {response.text}")

    # 1C. Création d'un utilisateur normal (Reviewer)
    print("[1C: POST /users] - Creating Normal User (Reviewer)")
    user_data = {"first_name": "Normal", "last_name": "Reviewer", "email": "user@hbnb.com", "password": "user_password"}
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    if response.status_code == 201:
        IDS['USER_ID'] = response.json().get('id')
        print_result(True, f"Normal user created. ID: {IDS['USER_ID']}")
    else:
        return test_abort(f"FAILED TO CREATE USER: {response.status_code} - {response.text}")

    # 1D. Authentification de l'Admin
    print("\n[1D: POST /auth/login] - Authenticating Admin")
    login_data = {"email": "admin@hbnb.com", "password": "admin_password"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        IDS['ADMIN_TOKEN'] = response.json().get('access_token')
        print_result(True, "Admin authenticated, token received.")
    else:
        return test_abort(f"FAILED TO AUTHENTICATE ADMIN: {response.status_code} - {response.text}")
        
    # 1E. Authentification de l'Owner
    print("[1E: POST /auth/login] - Authenticating Owner")
    login_data = {"email": "owner@hbnb.com", "password": "owner_password"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        IDS['OWNER_TOKEN'] = response.json().get('access_token')
        print_result(True, "Owner authenticated, token received.")
    else:
        return test_abort(f"FAILED TO AUTHENTICATE OWNER: {response.status_code} - {response.text}")

    # 1F. Authentification de l'User (Reviewer)
    print("[1F: POST /auth/login] - Authenticating Reviewer")
    login_data = {"email": "user@hbnb.com", "password": "user_password"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        IDS['USER_TOKEN'] = response.json().get('access_token')
        print_result(True, "Reviewer authenticated, token received.")
    else:
        return test_abort(f"FAILED TO AUTHENTICATE REVIEWER: {response.status_code} - {response.text}")
        
    # Préparer les headers
    admin_headers = {'Authorization': f'Bearer {IDS["ADMIN_TOKEN"]}'}
    owner_headers = {'Authorization': f'Bearer {IDS["OWNER_TOKEN"]}'}
    user_headers = {'Authorization': f'Bearer {IDS["USER_TOKEN"]}'}
    
    print("------------------------------------------")


    # --- 2. AMENITY & PLACE CREATION + VERIFICATION DE LA RELATION ---
    print("\n--- 2. AMENITY & PLACE CREATION + VERIFICATION DE LA RELATION ---")
    
    # 2A. Création Amenity (par l'Admin)
    print("\n[2A: POST /amenities] - Admin creates Amenity")
    amenity_data = {"name": "Piscine"}
    response = requests.post(f"{BASE_URL}/amenities", json=amenity_data, headers=admin_headers)
    if response.status_code == 201:
        IDS['AMENITY_ID'] = response.json().get('id')
        print_result(True, f"Amenity created by Admin. ID: {IDS['AMENITY_ID']}")
    else:
        return test_abort(f"FAILED TO CREATE AMENITY: {response.status_code} - {response.text}")
        
    # 2B. Création Amenity (ID bidon pour un test d'échec plus tard)
    FAKE_AMENITY_ID = str(uuid.uuid4())
    
    # 2C. Création Place (par l'Owner)
    print("\n[2C: POST /places] - Owner creates Place")
    place_data = {
        "title": "Owner's Villa",
        "description": "Vue imprenable",
        "price": 300.0,
        "owner_id": IDS['OWNER_ID'], # Le lieu appartient à l'Owner
        "latitude": 46.3626,       
        "longitude": 6.8045,       
        "amenities": [IDS['AMENITY_ID']] # Association ici
    }
    response = requests.post(f"{BASE_URL}/places", json=place_data, headers=owner_headers)
    if response.status_code == 201:
        IDS['PLACE_ID'] = response.json().get('id')
        print_result(True, f"Place created by Owner with Amenity ID: {IDS['PLACE_ID']}")
    else:
        return test_abort(f"FAILED TO CREATE PLACE BY OWNER: {response.status_code} - {response.text}")
        
    # 2D. VÉRIFICATION CRITIQUE : GET /places/<id> pour s'assurer que la relation est persistante
    print("[2D: GET /places/<id>] - **CRITICAL CHECK: Verifying Amenity relationship persistence**")
    response = requests.get(f"{BASE_URL}/places/{IDS['PLACE_ID']}", headers=owner_headers)
    
    amenity_ids_in_place = response.json().get('amenities', [])
    
    # On vérifie le statut HTTP et la présence de l'ID de l'Amenity dans la liste
    check_passed = (
        response.status_code == 200 and 
        IDS['AMENITY_ID'] in amenity_ids_in_place
    )
    
    if check_passed:
        print_result(True, "Relationship persistence **CONFIRMED**: Amenity ID found in Place details.")
    else:
        # Échec critique de la persistance, la relation Many-to-Many ne fonctionne pas.
        return test_abort(f"CRITICAL: Amenity ID is **MISSING** from Place details. Got amenities: {amenity_ids_in_place}")
        
    # 2E. TEST D'ÉCHEC : Création Place avec un Amenity ID inexistant (DOIT ÉCHOUER 400)
    print("\n[2E: POST /places] - Test: Creating Place with **FAKE** Amenity ID (Expected 400 Bad Request)")
    bad_place_data = place_data.copy()
    bad_place_data["amenities"] = [FAKE_AMENITY_ID]
    bad_place_data["title"] = "Bad Place"
    
    response = requests.post(f"{BASE_URL}/places", json=bad_place_data, headers=owner_headers)
    print_result(
        response.status_code == 400, 
        f"Validation check passed: Creation with fake Amenity ID forbidden (Got {response.status_code})."
    )
    
    # 2F. Modification Amenity (Admin, inchangé)
    print("[2F: PUT /amenities/<id>] - Admin modifies Amenity")
    response = requests.put(f"{BASE_URL}/amenities/{IDS['AMENITY_ID']}", json={"name": "Piscine Olympique"}, headers=admin_headers)
    if response.status_code == 200 and response.json().get('name') == "Piscine Olympique":
        print_result(True, "Amenity modified successfully by Admin.")
    else:
        print_result(False, f"FAILED to modify Amenity: {response.status_code} - {response.text}")
        
    # 2G. VÉRIFICATION DE LA MODIFICATION (Test de l'impact)
    print("[2G: GET /places/<id>] - Check: Amenity modification does not break the Place relation")
    response = requests.get(f"{BASE_URL}/places/{IDS['PLACE_ID']}", headers=owner_headers)
    
    # La liste d'Amenity doit toujours contenir l'ID, même après modification
    check_passed_after_update = (
        response.status_code == 200 and 
        IDS['AMENITY_ID'] in response.json().get('amenities', [])
    )
    print_result(check_passed_after_update, "Check passed: Place relation maintained after Amenity update.")


    # --- 3. PLACE UPDATE SECURITY (inchangé) ---
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


    # --- 4. REVIEW CREATION SECURITY (inchangé) ---
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


    # --- 5. REVIEW UPDATE SECURITY (inchangé) ---
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


    # --- 6. USER DELETION SECURITY & CLEANUP ---
    print("\n--- 6. USER Deletion Security Checks & Cleanup ---")

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
        
    # 6C. Suppression du Reviewer restant (User normal)
    print(f"[6C: DELETE /users/{IDS['USER_ID']}] - Final Reviewer Cleanup")
    response = requests.delete(f"{BASE_URL}/users/{IDS['USER_ID']}", headers=admin_headers)
    if response.status_code == 204:
        print_result(True, "Final cleanup: Reviewer deleted successfully (204).")
    else:
        print_result(False, f"CLEANUP FAILED: FAILED TO DELETE REVIEWER: {response.status_code} - {response.text}")
    
    # 6D. Suppression finale de l'Admin
    print(f"[6D: DELETE /users/{IDS['ADMIN_ID']}] - Final Admin Cleanup Attempt (Expecting 403 or 204)")
    response = requests.delete(f"{BASE_URL}/users/{IDS['ADMIN_ID']}", headers=admin_headers)
    if response.status_code == 403:
         print_result(True, "Admin self-deletion check confirmed (403).")
    elif response.status_code == 204:
         print_result(True, "Admin deleted successfully (204).")
    else:
         print_result(False, f"CLEANUP FAILED: Admin deletion failed with {response.status_code} - {response.text}")
        
    print("\n--- 🏁 END OF API TESTS ---")

if __name__ == "__main__":
    main_test_suite()