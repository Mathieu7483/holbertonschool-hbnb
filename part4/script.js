// ==================== API CONFIGURATION ====================
const API_BASE_URL = 'http://localhost:5000';
const API_LOGIN_URL = `${API_BASE_URL}/api/v2/auth/login`;
const API_PLACES_URL = `${API_BASE_URL}/api/v2/places/`;
const API_REVIEWS_URL = `${API_BASE_URL}/api/v2/reviews/`;

// Global variable to store all places for filtering
let allPlaces = [];

// ==================== COOKIE & TOKEN MANAGEMENT ====================

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

/**
 * Sets the JWT token in a cookie
 * @param {string} value - The JWT token.
 */
function setToken(value) {
    setCookie('token', value, 3600);
}

/**
 * Retrieves the JWT token from the cookie.
 * @returns {string | null} The token or null.
 */
function getToken() {
    return getCookie('token');
}

/**
 * Removes the JWT token.
 */
function deleteToken() {
    deleteCookie('token');
}

// ==================== API REQUEST ABSTRACTION ====================

/**
 * Abstract function for all Fetch requests.
 * Handles Authorization header, 401 errors, and JSON parsing.
 * @param {string} url - API endpoint URL.
 * @param {string} method - HTTP method (GET, POST, etc.).
 * @param {Object | null} body - Request body object.
 * @param {string | null} token - JWT token for Authorization header.
 * @returns {Promise<Object>} The parsed JSON response data.
 */
async function apiFetch(url, method = 'GET', body = null, token = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method: method,
        headers: headers,
        body: body ? JSON.stringify(body) : null
    };

    const response = await fetch(url, config);

    if (response.status === 401) {
        // Centralized handling for unauthorized access/expired token
        deleteToken();
        if (!window.location.pathname.includes('login')) {
             alert('Your session has expired. Please log in again.');
             window.location.href = 'login.html';
        }
        throw new Error('Unauthorized');
    }
    
    if (!response.ok) {
        // Handle other HTTP errors (4xx, 5xx)
        let errorData = { message: response.statusText };
        try {
            errorData = await response.json();
        } catch {}
        throw new Error(errorData.message || response.statusText);
    }

    return response.json();
}

// ==================== AUTHENTICATION & UI ====================

function checkAuthentication() {
    const token = getToken();
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    if (!token) {
        // User NOT authenticated: show Login, hide Logout
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutButton) logoutButton.style.display = 'none';
    } else {
        // User IS authenticated: hide Login, show Logout
        if (loginLink) loginLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'inline-block'; 
    }
    
    // Determine which data to fetch based on the current page
    const placeId = getPlaceIdFromURL();

    if (document.getElementById('places-list')) {
        fetchPlaces(token); // Fetch places (token can be null for public view)
    } else if (document.getElementById('place-details') && placeId) {
        fetchPlaceDetails(placeId, token); // Fetch details (token can be null for public view)
    }
}

async function loginUser(email, password) {
    return apiFetch(API_LOGIN_URL, 'POST', { email, password });
}

function logoutUser() {
    deleteToken();
    window.location.href = 'index.html';
}

// ==================== URL HELPERS ====================

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    // Checks for 'id' on place.html and 'place_id' on add_review.html
    return params.get('id') || params.get('place_id');
}

// ==================== FETCH PLACES (UNIFIED) ====================

async function fetchPlaces(token = null) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '<p>Loading places...</p>';
    
    try {
        const places = await apiFetch(API_PLACES_URL, 'GET', null, token);
        allPlaces = places;
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);
        placesList.innerHTML = `<p>Failed to load places: ${error.message || 'Network error'}.</p>`;
    }
}

// ==================== DISPLAY PLACES ====================

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

// ==================== FETCH PLACE DETAILS (UNIFIED) ====================

async function fetchPlaceDetails(placeId, token = null) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;
    
    placeDetails.innerHTML = '<p>Loading place details...</p>';
    
    try {
        const place = await apiFetch(`${API_PLACES_URL}${placeId}`, 'GET', null, token);
        displayPlaceDetails(place);
        fetchReviews(placeId, token);
    } catch (error) {
        if (error.message !== 'Unauthorized') {
             console.error('Error fetching place details:', error);
             placeDetails.innerHTML = `<p>Failed to load place details: ${error.message || 'Network error'}.</p>`;
        }
    }
}

// ==================== DISPLAY PLACE DETAILS ====================

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

// ==================== FETCH AND DISPLAY REVIEWS (UNIFIED) ====================

async function fetchReviews(placeId, token) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    reviewsSection.innerHTML = '<h3>Reviews</h3><p>Loading reviews...</p>';

    try {
        const reviewsUrl = `${API_REVIEWS_URL}places/${placeId}/reviews`;
        // Fetch reviews (token is optional)
        const reviews = await apiFetch(reviewsUrl, 'GET', null, token);
        displayReviews(reviews, placeId);
    } catch (error) {
        // If fetch fails (e.g., 404), display the section without reviews
        console.error('Error fetching reviews:', error);
        displayReviews([], placeId);
    }
}

// ==================== DISPLAY REVIEWS ====================

function displayReviews(reviews, placeId) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    // Reset with the blue-styled H3 title
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

async function fetchPlaceNameForReview(placeId, token) {
    try {
        const place = await apiFetch(`${API_PLACES_URL}${placeId}`, 'GET', null, token);
        const pageTitle = document.querySelector('#review-form h2');
        if (pageTitle) {
            pageTitle.textContent = `Add a Review for ${place.title || 'this place'}`;
        }
    } catch (error) {
        console.error('Error fetching place name:', error);
    }
}

// ==================== DOM CONTENT LOADED ====================

document.addEventListener('DOMContentLoaded', () => {
    // Initial check for authentication status and load relevant data
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
                // Use unified login function which leverages apiFetch
                const data = await loginUser(email, password); 
                
                if (data.access_token) {
                    setToken(data.access_token);
                    window.location.href = 'index.html';
                } else {
                    alert('Login successful but no token received.');
                }
            } catch (error) {
                alert(`Login failed: ${error.message || 'Network error'}`);
            }
        });
    }

    // ========== REVIEW FORM (add_review.html) ==========
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const placeId = getPlaceIdFromURL();
        const token = getToken();
        
        if (placeId) {
            const placeIdInput = reviewForm.querySelector('input[name="place_id"]');
            if (placeIdInput) placeIdInput.value = placeId;
            
            if (token) {
                fetchPlaceNameForReview(placeId, token);
            }
        }
        
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
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

            // Attempt to decode user_id from JWT token payload (as done previously)
            let userId = null;
            try {
                const tokenParts = token.split('.');
                const payload = JSON.parse(atob(tokenParts[1]));
                userId = payload.sub || payload.identity;
            } catch (e) {
                console.warn("Could not decode user ID from token payload.");
            }
            
            const reviewData = {
                text: reviewText,
                rating: parseInt(rating),
                user_id: userId,
                place_id: placeId
            };

            try {
                // Use apiFetch to submit the review
                await apiFetch(API_REVIEWS_URL, 'POST', reviewData, token);
                alert('Review added successfully!');
                window.location.href = `place.html?id=${placeId}`;
            } catch (error) {
                alert(`Failed to add review: ${error.message}`);
            }
        });
    }
});