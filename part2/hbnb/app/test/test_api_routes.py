import requests
import time
import json

# ----------------------------------------------------------------------
# Configuration de l'API
# ----------------------------------------------------------------------
BASE_URL = "http://127.0.0.1:5000/api/v1" # VÉRIFIEZ VOTRE PORT FLASK

# ----------------------------------------------------------------------
# Variables globales pour stocker les IDs créés
# ----------------------------------------------------------------------
IDS = {
    'USER_ID': None,
    'AMENITY_ID': None,
    'PLACE_ID': None,
    'REVIEW_ID': None
}

# ----------------------------------------------------------------------
# Fonction principale d'exécution des tests
# ----------------------------------------------------------------------

def run_full_tests():
    print("--- 🎬 DÉMARRAGE DES TESTS CRUD COMPLETS VIA API ---")
    
    # ---------------------------------
    # 1. PRÉPARATION : CRÉATION DES DÉPENDANCES
    # ---------------------------------

    # A. Création User
    print("\n[1A: POST /users]")
    user_data = {"first_name": "Test", "last_name": "Owner", "email": "owner@hbnb.com"}
    try:
        response = requests.post(f"{BASE_URL}/users", json=user_data)
        if response.status_code == 201:
            IDS['USER_ID'] = response.json()['id']
            print(f"  ✅ User créé. ID: {IDS['USER_ID']}")
        else:
            print(f"  ❌ ÉCHEC CRÉATION USER: {response.status_code} - {response.text}"); return
    except requests.exceptions.ConnectionError:
        print("  ❌ ERREUR DE CONNEXION: Serveur Flask non démarré."); return

    # B. Création Amenity
    print("\n[1B: POST /amenities]")
    amenity_data = {"name": "TestAmenity"}
    response = requests.post(f"{BASE_URL}/amenities", json=amenity_data)
    if response.status_code == 201:
        IDS['AMENITY_ID'] = response.json()['id']
        print(f"  ✅ Amenity créé. ID: {IDS['AMENITY_ID']}")
    else:
        print(f"  ❌ ÉCHEC CRÉATION AMENITY: {response.status_code} - {response.text}"); return

    # C. Création Place (Dépend de l'User)
    print("\n[1C: POST /places]")
    place_data = {
        "title": "Chalet du Lac Léman",
        "description": "Vue magnifique sur le lac, parfait pour le télétravail.",
        "price": 180.50,
        "latitude": 46.3948,
        "longitude": 6.4023,
        # 🎯 CORRECTION MAJEURE: Clé USER_ID au lieu de OWNER_ID et retrait des accolades {}
        "owner_id": IDS['USER_ID'], 
        "amenities": []
    }
    response = requests.post(f"{BASE_URL}/places", json=place_data)
    if response.status_code == 201:
        IDS['PLACE_ID'] = response.json()['id']
        print(f"  ✅ Place créée. ID: {IDS['PLACE_ID']}")
    else:
        print(f"  ❌ ÉCHEC CRÉATION PLACE: {response.status_code} - {response.text}"); return
    # D. Création Review (Dépend de Place et User)
    print("\n[1D: POST /reviews]")
    review_data = {
        "text": "First test review", 
        "rating": 5, 
        "user_id": IDS['USER_ID'], 
        "place_id": IDS['PLACE_ID']
    }
    response = requests.post(f"{BASE_URL}/reviews", json=review_data)
    if response.status_code == 201:
        IDS['REVIEW_ID'] = response.json()['id']
        print(f"  ✅ Review créée. ID: {IDS['REVIEW_ID']}")
    else:
        print(f"  ❌ ÉCHEC CRÉATION REVIEW: {response.status_code} - {response.text}"); return

    # ---------------------------------
    # 2. TESTS D'UPDATE (PUT)
    # ---------------------------------
    
    # E. Update Amenity
    print("\n[2E: PUT /amenities/<id>]")
    old_updated_at = requests.get(f"{BASE_URL}/amenities/{IDS['AMENITY_ID']}").json()['updated_at']
    time.sleep(0.01) # S'assurer que le timestamp change
    response = requests.put(f"{BASE_URL}/amenities/{IDS['AMENITY_ID']}", json={"name": "UpdatedAmenity"})
    if response.status_code == 200 and response.json()['name'] == "UpdatedAmenity" and response.json()['updated_at'] != old_updated_at:
        print("  ✅ SUCCÈS: Amenity mis à jour et updated_at changé.")
    else:
        print(f"  ❌ ÉCHEC UPDATE AMENITY: {response.status_code} - {response.text}")

    # F. Update Place
    print("\n[2F: PUT /places/<id>]")
    old_updated_at = requests.get(f"{BASE_URL}/places/{IDS['PLACE_ID']}").json()['updated_at']
    time.sleep(0.01)
    response = requests.put(f"{BASE_URL}/places/{IDS['PLACE_ID']}", json={"price": 150, "description": "Updated Description"})
    if response.status_code == 200 and response.json()['price'] == 150 and response.json()['updated_at'] != old_updated_at:
        print("  ✅ SUCCÈS: Place mise à jour et updated_at changé.")
    else:
        print(f"  ❌ ÉCHEC UPDATE PLACE: {response.status_code} - {response.text}")

    # G. Update Review
    print("\n[2G: PUT /reviews/<id>]")
    old_updated_at = requests.get(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}").json()['updated_at']
    time.sleep(0.01)
    response = requests.put(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}", json={"rating": 3, "text": "Needs improvement."})
    if response.status_code == 200 and response.json()['rating'] == 3 and response.json()['updated_at'] != old_updated_at:
        print("  ✅ SUCCÈS: Review mise à jour et updated_at changé.")
    else:
        print(f"  ❌ ÉCHEC UPDATE REVIEW: {response.status_code} - {response.text}")


    # ---------------------------------
    # 3. TESTS DE SUPPRESSION (DELETE)
    # ---------------------------------
    
    # H. Delete Review (Doit réussir car nous avons corrigé la Façade)
    print("\n[3H: DELETE /reviews/<id>]")
    response = requests.delete(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}")
    
    if response.status_code == 204:
        # Vérification finale que l'objet a disparu
        check_response = requests.get(f"{BASE_URL}/reviews/{IDS['REVIEW_ID']}")
        if check_response.status_code == 404:
            print("  ✅ SUCCÈS: Review supprimée (Statut 204) et non trouvée après vérification (Statut 404).")
        else:
             print(f"  ❌ ÉCHEC DELETE REVIEW: Suppression OK, mais l'objet est toujours trouvable ({check_response.status_code}).")
    else:
        print(f"  ❌ ÉCHEC DELETE REVIEW: Statut inattendu: {response.status_code} - {response.text}")

   
   
    # ---------------------------------
    # 4. Nettoyage final (Tentative de suppression de l'User)
    # ---------------------------------
    print("\n[4K: VÉRIFICATION DELETE USER (Attendu 405)]")
    response = requests.delete(f"{BASE_URL}/users/{IDS['USER_ID']}")
    if response.status_code == 405:
        print("  ✅ SUCCÈS: DELETE /users non autorisé (Statut 405).")
    else:
        print(f"  ⚠️ ALERTE: DELETE /users devrait être bloqué. Reçu: {response.status_code}")


    print("\n--- 🏁 FIN DES TESTS COMPLETS ---")


if __name__ == "__main__":
    run_full_tests()