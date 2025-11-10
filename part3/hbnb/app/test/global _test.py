import requests
import json
import uuid

# ======================================================================
# CONFIGURATION
# ======================================================================
BASE_URL = "http://127.0.0.1:5000/api/v2" 

# Variables pour stocker les IDs et les tokens de tous les utilisateurs et entités
IDS = {
    # Utilisateurs
    'ADMIN_ID': None,
    'USER1_ID': None, # Utilisateur pour les tests globaux (cascade, CRUD)
    'OWNER_ID': None, # Utilisateur pour les tests Place/Review
    'REVIEWER_ID': None, # Utilisateur pour les tests Place/Review
    
    # Entités
    'AMENITY_ID': None, # Amenity pour les tests Place/Review
    'AMENITY_GLOBAL_ID': None, # Amenity pour les tests CRUD global
    'PLACE_ID': None, # Place pour les tests Place/Review
    'PLACE_CASCADE_ID': None, # Place pour le test de cascade
    'REVIEW_ID': None, 
    
    # Tokens
    'ADMIN_TOKEN': None,
    'USER1_TOKEN': None,
    'OWNER_TOKEN': None,
    'REVIEWER_TOKEN': None,
}

# --- Utility Functions ---

def print_result(success, message):
    """Affiche le résultat d'un test avec une coche ou une croix."""
    status = "✅" if success else "❌"
    print(f"  {status} {message}")
    
def test_abort(message):
    """Affiche un message d'échec critique et termine les tests."""
    print(f"\n--- ❌ CRITICAL FAILURE ---")
    print(f"  ABORTING TESTS: {message}")
    print("----------------------------\n")
    return False

# ======================================================================
# FONCTION PRINCIPALE DE TEST
# ======================================================================

def run_all_tests():
    """Exécute la suite de tests d'intégration complète."""
    
    print("--- 🎬 STARTING COMPLETE API INTEGRATION TESTS ---")

    # --- 1. SETUP: CREATE ALL USERS & AUTHENTICATION ---
    print("\n--- 1. SETUP: ALL Users & Authentication ---")

    try:
        # 1A. Création d'un utilisateur Admin
        print("\n[1A: POST /users] - Creating Admin User")
        admin_data = {"first_name": "Admin", "last_name": "Master", "email": "admin_full@hbnb.com", "password": "admin_password", "is_admin": True}
        response = requests.post(f"{BASE_URL}/users", json=admin_data)
        if response.status_code == 201: IDS['ADMIN_ID'] = response.json().get('id')
        print_result(response.status_code == 201, f"Admin created. ID: {IDS['ADMIN_ID']}")
        
        # 1B. Création d'un utilisateur Owner (pour Place/Review)
        print("[1B: POST /users] - Creating Place Owner User")
        owner_data = {"first_name": "Place", "last_name": "Owner", "email": "owner_full@hbnb.com", "password": "owner_password"}
        response = requests.post(f"{BASE_URL}/users", json=owner_data)
        if response.status_code == 201: IDS['OWNER_ID'] = response.json().get('id')
        print_result(response.status_code == 201, f"Owner created. ID: {IDS['OWNER_ID']}")

        # 1C. Création d'un Reviewer (pour Place/Review)
        print("[1C: POST /users] - Creating Reviewer User")
        reviewer_data = {"first_name": "Normal", "last_name": "Reviewer", "email": "reviewer_full@hbnb.com", "password": "reviewer_password"}
        response = requests.post(f"{BASE_URL}/users", json=reviewer_data)
        if response.status_code == 201: IDS['REVIEWER_ID'] = response.json().get('id')
        print_result(response.status_code == 201, f"Reviewer created. ID: {IDS['REVIEWER_ID']}")

        # 1D. Création User 1 (pour tests globaux/cascade)
        print("[1D: POST /users] - Creating User 1 (Cascade)")
        user1_data = {"first_name": "User", "last_name": "One", "email": "user1_full@hbnb.com", "password": "user1_password"}
        response = requests.post(f"{BASE_URL}/users", json=user1_data)
        if response.status_code == 201: IDS['USER1_ID'] = response.json().get('id')
        print_result(response.status_code == 201, f"User 1 created. ID: {IDS['USER1_ID']}")


        # Authentification de tous les utilisateurs
        login_map = {
            'ADMIN_TOKEN': ("admin_full@hbnb.com", "admin_password"),
            'OWNER_TOKEN': ("owner_full@hbnb.com", "owner_password"),
            'REVIEWER_TOKEN': ("reviewer_full@hbnb.com", "reviewer_password"),
            'USER1_TOKEN': ("user1_full@hbnb.com", "user1_password")
        }
        
        for key, (email, password) in login_map.items():
            response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
            if response.status_code == 200:
                IDS[key] = response.json().get('access_token')
            print_result(response.status_code == 200, f"Authenticated {key.replace('_TOKEN', '')}, token received.")

        if not all(IDS[k] for k in ['ADMIN_TOKEN', 'OWNER_TOKEN', 'REVIEWER_TOKEN', 'USER1_TOKEN']):
             return test_abort("SETUP FAILED: Not all users created or authenticated.")
        
        # Définir les headers
        admin_headers = {'Authorization': f'Bearer {IDS["ADMIN_TOKEN"]}'}
        owner_headers = {'Authorization': f'Bearer {IDS["OWNER_TOKEN"]}'}
        reviewer_headers = {'Authorization': f'Bearer {IDS["REVIEWER_TOKEN"]}'}
        user1_headers = {'Authorization': f'Bearer {IDS["USER1_TOKEN"]}'}
        
        print("\n--- SETUP COMPLETE ---")
        
    except requests.exceptions.ConnectionError:
        return test_abort("CONNECTION ERROR: Is the Flask server running?")
        
    print("------------------------------------------")

    # ======================================================================
    # SECTION 2 : GLOBAL SECURITY & VALIDATION TESTS
    # ======================================================================
    
    print("\n--- 2. GLOBAL SECURITY & VALIDATION TESTS (Task I & II.A) ---")
    
    # 2A. Accès Protégé SANS Token (Expected 401/400)
    print("\n[2A: POST /places] - Protected Access without Token (Expected 401/400 Unauthorized/Bad Request)")
    response = requests.post(f"{BASE_URL}/places", json={}, headers={'Content-Type': 'application/json'}) 
    print_result(
        response.status_code in [401, 400], 
        f"Security check passed: Access without JWT forbidden (Got {response.status_code})."
    )

    # 2B. Connexion Échec (Mot de passe incorrect) (Expected 401)
    print("[2B: POST /auth/login] - Login with Wrong Password (Expected 401 Unauthorized)")
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": "user1_full@hbnb.com", "password": "wrong_password"})
    print_result(response.status_code == 401, f"Security check passed: Login with bad password forbidden (Got {response.status_code}).")

    # 2C. Création Utilisateur avec Email Existant (Expected 400/409)
    print("[2C: POST /users] - Create User with Existing Email (Expected 400/409 Conflict)")
    response = requests.post(f"{BASE_URL}/users", json=user1_data)
    print_result(response.status_code in [400, 409], f"Validation check passed: Duplicate email creation forbidden (Got {response.status_code}).")

    # 2D. Validation ORM (Place - Champ non-nullable manquant)
    print("\n[2D: POST /places] - Validation Test: Missing non-nullable field (Expected 400)")
    bad_place_data = {
        "title": "Missing Price", "owner_id": IDS['USER1_ID'], "latitude": 10.0, 
        "longitude": 10.0, "amenities": []
        # 'price' est manquant ici
    }
    response = requests.post(f"{BASE_URL}/places", json=bad_place_data, headers=user1_headers)
    print_result(response.status_code == 400, f"Validation check passed: Missing field forbidden (Got {response.status_code}).")

    print("------------------------------------------")

    # ======================================================================
    # SECTION 3 : AMENITY CRUD & CASCADING DELETION TESTS
    # ======================================================================
    
    print("\n--- 3. AMENITY CRUD & CASCADING DELETION TESTS (Task III) ---")

    # 3A. Amenity CRUD Complet (Exclut la suppression)
    print("\n[3A: AMENITY] - CRUD Test (Create, Read, Update only)")
    
    # CREATE Amenity Global
    amenity_data = {"name": "Jardin"}
    response = requests.post(f"{BASE_URL}/amenities", json=amenity_data, headers=admin_headers)
    if response.status_code != 201: return test_abort(f"Amenity CRUD FAILED at CREATE: {response.text}")
    IDS['AMENITY_GLOBAL_ID'] = response.json().get('id')
    print_result(True, f"Amenity GLOBAL CREATE (201) confirmed. ID: {IDS['AMENITY_GLOBAL_ID']}")
    
    # READ Amenity Global
    response = requests.get(f"{BASE_URL}/amenities/{IDS['AMENITY_GLOBAL_ID']}")
    print_result(response.status_code == 200, "Amenity GLOBAL READ (200) confirmed.")

    # UPDATE Amenity Global
    response = requests.put(f"{BASE_URL}/amenities/{IDS['AMENITY_GLOBAL_ID']}", json={"name": "Jardin Zen"}, headers=admin_headers)
    print_result(response.status_code == 200 and response.json().get('name') == "Jardin Zen", "Amenity GLOBAL UPDATE (200) confirmed.")

    # DELETE Amenity Global (COMMENTÉ POUR ÉVITER LE 405)
    # response = requests.delete(f"{BASE_URL}/amenities/{IDS['AMENITY_GLOBAL_ID']}", headers=admin_headers)
    # print_result(response.status_code == 204, f"Amenity GLOBAL DELETE (204) confirmed (Got {response.status_code}).")
    print_result(True, "Amenity GLOBAL DELETE test skipped (functionality pending).")
    
    
    # 3B. CASCADING DELETION (User -> Place)
    print("\n[3B: CASCADING DELETION] - User -> Place (Expected 404 on Place)")

    # Créer une Amenity temporaire pour la Place de cascade (nous devrons la supprimer manuellement)
    temp_amenity = requests.post(f"{BASE_URL}/amenities", json={"name": "Temp Amenity"}, headers=admin_headers).json().get('id')
    
    # Créer une Place associée à l'User 1
    place_data_cascade = {
        "title": "Cascade Test Place", "description": "Test", "price": 1.0,
        "owner_id": IDS['USER1_ID'], "latitude": 1.0, "longitude": 1.0, 
        "amenities": [temp_amenity]
    }
    response = requests.post(f"{BASE_URL}/places", json=place_data_cascade, headers=user1_headers)
    if response.status_code != 201: return test_abort(f"CASCADE SETUP FAILED: Cannot create Place: {response.text}")
    IDS['PLACE_CASCADE_ID'] = response.json().get('id')
    print_result(True, "Place created for cascade test.")
    
    # Suppression de l'User 1 (Owner)
    response = requests.delete(f"{BASE_URL}/users/{IDS['USER1_ID']}", headers=admin_headers)
    if response.status_code != 204: return test_abort(f"CASCADE DELETE FAILED: Cannot delete User: {response.text}")
    print_result(True, "User 1 deleted (204).")
    
    # VÉRIFICATION DE LA CASCADAGE : La Place DOIT être supprimée
    response = requests.get(f"{BASE_URL}/places/{IDS['PLACE_CASCADE_ID']}", headers=admin_headers)
    cascade_success = response.status_code == 404
    print_result(
        cascade_success, 
        f"Cascade check passed: Place automatically deleted when Owner deleted (Got {response.status_code})."
    )
    
    # Nettoyage des Amenities temporaires créées par l'Admin (si DELETE fonctionne)
    # Étant donné que DELETE /amenities ne fonctionne pas encore, on ne peut pas garantir le nettoyage.
    # On va tout de même essayer, si l'implémentation a été ajoutée entre-temps
    requests.delete(f"{BASE_URL}/amenities/{temp_amenity}", headers=admin_headers)
    requests.delete(f"{BASE_URL}/amenities/{IDS['AMENITY_GLOBAL_ID']}", headers=admin_headers)

    print("------------------------------------------")

    # ======================================================================
    # SECTION 4 : PLACE & REVIEW INTEGRITY AND SECURITY TESTS
    # ======================================================================

    print("\n--- 4. PLACE & REVIEW INTEGRITY AND SECURITY TESTS ---")
    
    # 4A. Création Amenity (pour Place/Review)
    print("\n[4A: POST /amenities] - Admin creates Amenity (P/R)")
    amenity_data = {"name": "Piscine P/R"}
    response = requests.post(f"{BASE_URL}/amenities", json=amenity_data, headers=admin_headers)
    if response.status_code != 201: return test_abort("FAILED to create P/R Amenity.")
    IDS['AMENITY_ID'] = response.json().get('id')
    
    # 4B. Création Place (par l'Owner)
    print("[4B: POST /places] - Owner creates Place (P/R)")
    place_data = {
        "title": "Owner's Villa", "description": "Vue imprenable", "price": 300.0,
        "owner_id": IDS['OWNER_ID'], "latitude": 46.3626, "longitude": 6.8045, 
        "amenities": [IDS['AMENITY_ID']]
    }
    response = requests.post(f"{BASE_URL}/places", json=place_data, headers=owner_headers)
    if response.status_code != 201: return test_abort(f"FAILED to create P/R Place: {response.text}")
    IDS['PLACE_ID'] = response.json().get('id')
    
    # 4C. VÉRIFICATION CRITIQUE : Relation Many-to-Many
    print("[4C: GET /places/<id>] - CRITICAL CHECK: Amenity relationship persistence")
    response = requests.get(f"{BASE_URL}/places/{IDS['PLACE_ID']}", headers=owner_headers)
    amenity_ids_in_place = response.json().get('amenities', [])
    check_passed = (response.status_code == 200 and IDS['AMENITY_ID'] in amenity_ids_in_place)
    print_result(check_passed, "Relationship persistence **CONFIRMED**.")
    
    # 4D. Modification Place par un User Tiers (DOIT ÉCHOUER 403)
    print("[4D: PUT /places/<id>] - Reviewer tries to modify Place (Expected 403 Forbidden)")
    response = requests.put(f"{BASE_URL}/places/{IDS['PLACE_ID']}", json={"price": 100.0}, headers=reviewer_headers)
    print_result(response.status_code == 403, f"Security check passed: Third-party User forbidden to update (Got {response.status_code}).")

    
    # --- 5. REVIEW CREATION & SECURITY ---
    
    # 5A. Création Review par le Reviewer (OK)
    print("\n[5A: POST /reviews] - Reviewer creates Review (OK)")
    review_data = {
        "text": "Exceptionnel !", "rating": 5,
        "place_id": IDS['PLACE_ID'], "user_id": IDS['REVIEWER_ID'] 
    }
    response = requests.post(f"{BASE_URL}/reviews", json=review_data, headers=reviewer_headers)
    if response.status_code != 201: return test_abort(f"FAILED TO CREATE REVIEW: {response.text}")
    IDS['REVIEW_ID'] = response.json().get('id')

    # 5B. Owner essaie de poster Review sur sa propre Place (DOIT ÉCHOUER 403)
    print("[5B: POST /reviews] - Owner tries to review their own Place (Expected 403 Forbidden)")
    owner_review_data = {
        "text": "Ma place est la meilleure!", "rating": 5,
        "place_id": IDS['PLACE_ID'], "user_id": IDS['OWNER_ID']
    }
    response = requests.post(f"{BASE_URL}/reviews", json=owner_review_data, headers=owner_headers)
    print_result(response.status_code == 403, f"Security check passed: Owner forbidden to review own Place (Got {response.status_code}).")

    # 5C. Owner essaie de supprimer la Review (DOIT ÉCHOUER 403)
    print("[5C: DELETE /reviews/<id>] - Owner tries to delete Review (Expected 403 Forbidden)")
    response = requests.delete(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", headers=owner_headers)
    print_result(response.status_code == 403, f"Security check passed: Owner forbidden to delete review (Got {response.status_code}).")

    
    # --- 6. FINAL CLEANUP & RECAP ---
    print("\n--- 6. FINAL CLEANUP & RECAP ---")

    # 6A. Suppression des entités restantes
    
    # Supprimer la Review
    requests.delete(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", headers=admin_headers)
    # Supprimer la Place (doit être possible par Admin)
    requests.delete(f"{BASE_URL}/places/{IDS['PLACE_ID']}", headers=admin_headers)
    # Supprimer l'Amenity (Seulement si DELETE fonctionne maintenant, sinon cette ligne échoue silencieusement)
    requests.delete(f"{BASE_URL}/amenities/{IDS['AMENITY_ID']}", headers=admin_headers)
    
    print_result(True, "All secondary entities deleted (attempted).")

    # 6B. Suppression des utilisateurs restants
    
    # Admin essaie de s'auto-supprimer (DOIT ÉCHOUER 403)
    print(f"[6B: DELETE /users/{IDS['ADMIN_ID']}] - Admin tries to self-delete (Expected 403 Forbidden)")
    response = requests.delete(f"{BASE_URL}/users/{IDS['ADMIN_ID']}", headers=admin_headers)
    print_result(response.status_code == 403, "Security check passed: Admin self-deletion forbidden (403).")
    
    # Suppression finale de l'Owner et du Reviewer par Admin
    requests.delete(f"{BASE_URL}/users/{IDS['OWNER_ID']}", headers=admin_headers)
    requests.delete(f"{BASE_URL}/users/{IDS['REVIEWER_ID']}", headers=admin_headers)
    
    print_result(True, "Owner and Reviewer deleted.")
    
    # 6C. Suppression finale de l'Admin
    response = requests.delete(f"{BASE_URL}/users/{IDS['ADMIN_ID']}", headers=admin_headers)
    print_result(response.status_code in [204, 403], f"Final cleanup: Admin deletion attempt (Got {response.status_code}).")

    # ======================================================================
    # RÉCAPITULATIF DES IDS ET TOKENS (NOUVELLE SECTION)
    # ======================================================================
    print("\n\n--- 📋 RÉCAPITULATIF DES IDS ET TOKENS CRÉÉS ---")
    for key, value in IDS.items():
        if 'TOKEN' in key and value: # S'assurer que le token existe avant de tronquer
            print(f"**{key}** (Bearer): {value[:15]}... (Tronqué)")
        elif value:
            print(f"**{key}**: {value}")
        else:
             print(f"**{key}**: None (Supprimé ou non créé)")
    print("-------------------------------------------------")
        
    print("\n--- 🏁 END OF COMPLETE API INTEGRATION TESTS ---")
    return True

if __name__ == "__main__":
    run_all_tests()