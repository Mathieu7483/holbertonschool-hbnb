// ==================== API CONFIGURATION ====================
const API_BASE_URL = 'http://localhost:5000';
const API_LOGIN_URL = `${API_BASE_URL}/api/v2/auth/login`;
const API_PLACES_URL = `${API_BASE_URL}/api/v2/places/`;
const API_REVIEWS_URL = `${API_BASE_URL}/api/v2/reviews/`;

// Global variable to store all places for filtering
let allPlaces = [];

// ==================== COOKIE HELPER FUNCTIONS ====================

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, maxAge = 3600) {
    document.cookie = `${name}=${value}; path=/; max-age=${maxAge}; SameSite=Lax`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; path=/; max-age=0`;
}

// ==================== TOKEN MANAGEMENT ====================

function setToken(value) {
    setCookie('token', value, 3600);
    localStorage.setItem('token', value);
}

function getToken() {
    const cookieValue = getCookie('token');
    if (cookieValue) return cookieValue;
    return localStorage.getItem('token');
}

function deleteToken() {
    deleteCookie('token');
    localStorage.removeItem('token');
}

// ==================== AUTHENTICATION ====================

function checkAuthentication() {
    const token = getToken();
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    if (!token) {
        // User NOT authenticated
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutButton) logoutButton.style.display = 'none';
        
        // Load places without auth if on index page
        const placesList = document.getElementById('places-list');
        if (placesList) {
            fetchPlacesPublic();
        }
        
        // Load place details without auth if on place page
        const placeDetails = document.getElementById('place-details');
        if (placeDetails) {
            const placeId = getPlaceIdFromURL();
            if (placeId) {
                fetchPlaceDetailsPublic(placeId);
            }
        }
    } else {
        // User IS authenticated
        if (loginLink) loginLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'inline-block';
        
        // Fetch places if on index page
        const placesList = document.getElementById('places-list');
        if (placesList) {
            fetchPlaces(token);
        }
        
        // Fetch place details if on place page
        const placeDetails = document.getElementById('place-details');
        if (placeDetails) {
            const placeId = getPlaceIdFromURL();
            if (placeId) {
                fetchPlaceDetails(token, placeId);
            }
        }
    }
}

async function loginUser(email, password) {
    const response = await fetch(API_LOGIN_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    return response;
}

function logoutUser() {
    deleteToken();
    window.location.href = 'index.html';
}

// ==================== URL HELPERS ====================

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// ==================== FETCH PLACES ====================

async function fetchPlacesPublic() {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '<p>Loading places...</p>';
    
    try {
        const response = await fetch(API_PLACES_URL, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            allPlaces = places;
            displayPlaces(places);
        } else {
            placesList.innerHTML = '<p>Failed to load places.</p>';
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        placesList.innerHTML = '<p>Network error.</p>';
    }
}

async function fetchPlaces(token) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '<p>Loading places...</p>';
    
    try {
        const response = await fetch(API_PLACES_URL, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const places = await response.json();
            allPlaces = places;
            displayPlaces(places);
        } else if (response.status === 401) {
            deleteToken();
            window.location.href = 'login.html';
        } else {
            placesList.innerHTML = '<p>Failed to load places.</p>';
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        placesList.innerHTML = '<p>Network error.</p>';
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('article');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price || 0;

        placeCard.innerHTML = `
            <h2>${place.title || 'Unnamed Place'}</h2>
            <div class="place-price">Price: $${place.price || 0}/night</div>
            <div class="place-location">Lat: ${place.latitude || 'N/A'}, Long: ${place.longitude || 'N/A'}</div>
            <p class="place-description">${place.description || 'No description available.'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}

// ==================== CLIENT-SIDE FILTER ====================

function filterPlacesByPrice(maxPrice) {
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const price = parseFloat(card.dataset.price) || 0;
        
        if (maxPrice === 'all') {
            card.style.display = 'block';
        } else {
            const priceLimit = parseFloat(maxPrice);
            card.style.display = price <= priceLimit ? 'block' : 'none';
        }
    });
}

// ==================== FETCH PLACE DETAILS ====================

async function fetchPlaceDetailsPublic(placeId) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;
    
    placeDetails.innerHTML = '<p>Loading place details...</p>';
    
    try {
        const response = await fetch(`${API_PLACES_URL}${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            fetchReviews(placeId, null);
        } else if (response.status === 404) {
            placeDetails.innerHTML = '<p>Place not found.</p>';
        } else {
            placeDetails.innerHTML = '<p>Failed to load place details.</p>';
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        placeDetails.innerHTML = '<p>Network error.</p>';
    }
}

async function fetchPlaceDetails(token, placeId) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;
    
    placeDetails.innerHTML = '<p>Loading place details...</p>';
    
    try {
        const response = await fetch(`${API_PLACES_URL}${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            fetchReviews(placeId, token);
        } else if (response.status === 401) {
            deleteToken();
            window.location.href = 'login.html';
        } else if (response.status === 404) {
            placeDetails.innerHTML = '<p>Place not found.</p>';
        } else {
            placeDetails.innerHTML = '<p>Failed to load place details.</p>';
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        placeDetails.innerHTML = '<p>Network error.</p>';
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    const detailsHTML = `
        <h2>${place.title || 'Unnamed Place'}</h2>
        <div class="place-info">
            <p><strong>Host:</strong> ${place.owner?.first_name || ''} ${place.owner?.last_name || 'Unknown'}</p>
            <p><strong>Price:</strong> $${place.price || 0}/night</p>
            <p><strong>Location:</strong> Lat ${place.latitude || 'N/A'}, Long ${place.longitude || 'N/A'}</p>
        </div>
        
        <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>

        <h3>Amenities</h3>
        <ul>
            ${place.amenities && place.amenities.length > 0 
                ? place.amenities.map(amenity => `<li>${amenity.name || amenity}</li>`).join('') 
                : '<li>No amenities listed.</li>'}
        </ul>
    `;

    placeDetails.innerHTML = detailsHTML;
}

// ==================== FETCH AND DISPLAY REVIEWS ====================

async function fetchReviews(placeId, token) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    reviewsSection.innerHTML = '<h3>Reviews</h3><p>Loading reviews...</p>';

    try {
        // Use the correct endpoint from your API: /api/v2/reviews/places/{place_id}/reviews
        const reviewsUrl = `${API_REVIEWS_URL}places/${placeId}/reviews`;
        
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(reviewsUrl, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews, placeId);
        } else {
            // If endpoint fails, show empty reviews
            displayReviews([], placeId);
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        // Always show the section even on error
        displayReviews([], placeId);
    }
}

function displayReviews(reviews, placeId) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    reviewsSection.innerHTML = '<h3>Reviews</h3>';

    if (!reviews || reviews.length === 0) {
        reviewsSection.innerHTML += '<p>No reviews yet. Be the first to review!</p>';
    } else {
        reviews.forEach(review => {
            const reviewCard = document.createElement('article');
            reviewCard.className = 'review-card';
            
            reviewCard.innerHTML = `
                <h4>${review.user?.first_name || 'Anonymous'}</h4>
                <p><strong>Rating:</strong> ${review.rating || 'N/A'}/5</p>
                <p>${review.text || 'No comment provided.'}</p>
            `;
            
            reviewsSection.appendChild(reviewCard);
        });
    }

    // Add "Add Review" button if user is authenticated
    const token = getToken();
    if (token && placeId) {
        const addReviewButton = document.createElement('a');
        addReviewButton.href = `add_review.html?place_id=${placeId}`;
        addReviewButton.className = 'add-review-button';
        addReviewButton.textContent = 'Add Review';
        reviewsSection.appendChild(addReviewButton);
    }
}

// ==================== FETCH PLACE NAME FOR REVIEW PAGE ====================

async function fetchPlaceNameForReview(token, placeId) {
    try {
        const response = await fetch(`${API_PLACES_URL}${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const place = await response.json();
            const pageTitle = document.querySelector('#review-form h2');
            if (pageTitle) {
                pageTitle.textContent = `Add a Review for ${place.title || 'this place'}`;
            }
        }
    } catch (error) {
        console.error('Error fetching place name:', error);
    }
}

// ==================== DOM CONTENT LOADED ====================

document.addEventListener('DOMContentLoaded', () => {
    
    // Check authentication on page load
    checkAuthentication();

    // ========== LOGOUT BUTTON ==========
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', (e) => {
            e.preventDefault();
            logoutUser();
        });
    }

    // ========== PRICE FILTER ==========
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            filterPlacesByPrice(event.target.value);
        });
    }

    // ========== LOGIN FORM ==========
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            if (!email || !password) {
                alert('Please enter both email and password.');
                return;
            }

            try {
                const response = await loginUser(email, password);

                if (response.ok) {
                    const data = await response.json();
                    
                    if (data.access_token) {
                        setToken(data.access_token);
                        window.location.href = 'index.html';
                    } else {
                        alert('Login successful but no token received.');
                    }
                } else {
                    let errorMessage = 'Login failed. ';
                    
                    if (response.status === 401) {
                        errorMessage += 'Invalid email or password.';
                    } else if (response.status >= 500) {
                        errorMessage += 'Server error. Please try again later.';
                    } else {
                        try {
                            const errorData = await response.json();
                            errorMessage += errorData.message || response.statusText;
                        } catch {
                            errorMessage += response.statusText;
                        }
                    }
                    
                    alert(errorMessage);
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('Network error. Please check your connection and try again.');
            }
        });
    }

    // ========== REVIEW FORM (add_review.html) ==========
    const reviewForm = document.getElementById('review-form');
    if (reviewForm && window.location.pathname.includes('add_review')) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('place_id');
        
        const placeIdInput = reviewForm.querySelector('input[name="place_id"]');
        if (placeIdInput && placeId) {
            placeIdInput.value = placeId;
        }
        
        const token = getToken();
        if (token && placeId) {
            fetchPlaceNameForReview(token, placeId);
        }
        
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const token = getToken();
            if (!token) {
                alert('You must be logged in to add a review.');
                window.location.href = 'login.html';
                return;
            }
            
            const reviewText = document.getElementById('review').value.trim();
            const rating = document.getElementById('rating').value;
            
            if (!reviewText || !rating) {
                alert('Please fill in all fields.');
                return;
            }
            
            // Get user_id from JWT token (decode it or get from API)
            // For simplicity, we'll let the backend handle it based on the token
            try {
                // Parse JWT to get user_id (simple base64 decode of payload)
                const tokenParts = token.split('.');
                const payload = JSON.parse(atob(tokenParts[1]));
                const userId = payload.sub || payload.identity;
                
                const response = await fetch(API_REVIEWS_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        text: reviewText,
                        rating: parseInt(rating),
                        user_id: userId,
                        place_id: placeId
                    })
                });
                
                if (response.ok) {
                    alert('Review added successfully!');
                    window.location.href = `place.html?id=${placeId}`;
                } else {
                    const errorData = await response.json();
                    alert(`Failed to add review: ${errorData.message || response.statusText}`);
                }
            } catch (error) {
                console.error('Error adding review:', error);
                alert('Network error. Please check your connection and try again.');
            }
        });
    }
});