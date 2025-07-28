// ---------- Global Variables ----------
let allPlaces = [];

// ---------- Cookie Helper ----------
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// ---------- Show/hide buttons if logged in ----------
function toggleAuthButtons() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link') || document.getElementById('sidebar-login');
  const registerLink = document.getElementById('register-link') || document.getElementById('sidebar-register');
  const logoutLink = document.getElementById('sidebar-logout');
  const createPlace = document.getElementById('create-place-link');
  const createAmenity = document.getElementById('create-amenity-link');
  const createReview = document.getElementById('create-review-link');

  if (token) {
    if (loginLink) loginLink.classList.add('hidden');
    if (registerLink) registerLink.classList.add('hidden');
    if (logoutLink) logoutLink.classList.remove('hidden');
    if (createPlace) createPlace.classList.remove('hidden');
    if (createAmenity) createAmenity.classList.remove('hidden');
    if (createReview) createReview.classList.remove('hidden');
  } else {
    if (loginLink) loginLink.classList.remove('hidden');
    if (registerLink) registerLink.classList.remove('hidden');
    if (logoutLink) logoutLink.classList.add('hidden');
    if (createPlace) createPlace.classList.add('hidden');
    if (createAmenity) createAmenity.classList.add('hidden');
    if (createReview) createReview.classList.add('hidden');
  }
}

// ---------- DOM READY ----------
document.addEventListener('DOMContentLoaded', () => {
  // Custom Theme Button
  const customBtn = document.getElementById('custom-theme-btn');
  if (customBtn) {
    customBtn.onclick = function() {
      showCustomThemeModal();
    };
  }
  // Apply saved theme on load
  applyCustomThemeFromStorage();
// Custom Theme Modal and Logic
function showCustomThemeModal() {
  let modal = document.getElementById('custom-theme-modal');
  if (modal) modal.remove();
  modal = document.createElement('div');
  modal.id = 'custom-theme-modal';
  modal.className = 'custom-theme-modal';
  modal.innerHTML = `
    <div class="custom-theme-content">
      <h2>Pick a Secondary Color</h2>
      <div class="custom-theme-btns">
        <button data-color="red">Red</button>
        <button data-color="blue">Blue</button>
        <button data-color="purple">Purple</button>
      </div>
      <div style="margin-top:1.5em"><button id="close-custom-theme">Close</button></div>
    </div>
  `;
  document.body.appendChild(modal);
  // Highlight current
  const current = localStorage.getItem('custom-secondary') || 'red';
  modal.querySelectorAll('button[data-color]').forEach(btn => {
    if (btn.getAttribute('data-color') === current) btn.classList.add('selected');
    btn.onclick = function() {
      setCustomSecondary(btn.getAttribute('data-color'));
      modal.querySelectorAll('button[data-color]').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      applyCustomThemeFromStorage();
    };
  });
  modal.querySelector('#close-custom-theme').onclick = () => modal.remove();
}

function setCustomSecondary(color) {
  localStorage.setItem('custom-secondary', color);
}

function applyCustomThemeFromStorage() {
  const color = localStorage.getItem('custom-secondary') || 'red';
  let grad;
  let gradLight;
  // Set theme class for CSS variables
  document.body.classList.remove('theme-red', 'theme-blue', 'theme-purple');
  if (color === 'blue') {
    document.body.classList.add('theme-blue');
    gradLight = 'linear-gradient(120deg, #ececf0 0%, #e0e0e6 60%, #4f8cff 100%)';
    grad = 'linear-gradient(135deg, #181a1b 0%, #222 60%, #4f8cff 100%)';
  } else if (color === 'purple') {
    document.body.classList.add('theme-purple');
    gradLight = 'linear-gradient(120deg, #ececf0 0%, #e0e0e6 60%, #a259e6 100%)';
    grad = 'linear-gradient(135deg, #181a1b 0%, #222 60%, #a259e6 100%)';
  } else {
    document.body.classList.add('theme-red');
    gradLight = 'linear-gradient(120deg, #ececf0 0%, #e0e0e6 60%, #d72631 100%)';
    grad = 'linear-gradient(135deg, #181a1b 0%, #222 60%, #d72631 100%)';
  }
  if (document.body.classList.contains('dark-mode')) {
    document.body.style.background = grad;
    document.querySelectorAll('.site-header, .site-footer').forEach(el => {
      el.style.background = grad;
    });
    document.querySelectorAll('.sidebar').forEach(el => {
      el.style.background = '#222';
    });
  } else {
    document.body.style.background = gradLight;
    document.querySelectorAll('.site-header, .site-footer').forEach(el => {
      el.style.background = gradLight;
    });
    document.querySelectorAll('.sidebar').forEach(el => {
      el.style.background = '#fff';
    });
  }
}

// Re-apply theme on dark mode toggle
const origSetupDarkModeBtn = setupDarkModeBtn;
setupDarkModeBtn = function() {
  origSetupDarkModeBtn();
  applyCustomThemeFromStorage();
};
  setupDarkModeBtn();
  // Cambia el texto del botón en modo edición
  if (document.getElementById('place-form')) {
    const params = new URLSearchParams(window.location.search);
    const isEdit = params.get('edit') === '1';
    if (isEdit) {
      const btn = document.getElementById('place-submit-btn');
      if (btn) btn.textContent = 'Update Place';
    }
  }
  toggleAuthButtons();

  // Oculta el botón +Review en la página principal
  if (window.location.pathname.endsWith('/index.html') || window.location.pathname === '/' ) {
    const reviewBtn = document.getElementById('create-review-link');
    if (reviewBtn) reviewBtn.classList.add('hidden');
  }

  const path = window.location.pathname;
  if (path.endsWith('/add_place.html') || path.endsWith('/add_amenity.html')) {
    const homeLink = document.getElementById('home-link');
    if (homeLink) homeLink.style.display = 'inline-block';
  }

  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.onsubmit = function(e) { e.preventDefault(); return false; };
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      try {
        const res = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json; charset=utf-8' },
          body: JSON.stringify({ email, password })
        });
        if (res.ok) {
          const data = await res.json();
          // Defensive: check for access_token
          if (!data.access_token) {
            alert('Login error: No access token received.');
            return;
          }
          document.cookie = `token=${data.access_token}; path=/;`;
          // Log for debugging
          console.log('Login successful, token set:', data.access_token);
          window.location.href = '/index.html';
        } else {
          let errMsg = 'Login failed.';
          try {
            const err = await res.json();
            errMsg = err.message || JSON.stringify(err);
          } catch (e) {
            errMsg = 'HTTP ' + res.status;
          }
          alert('Login error: ' + errMsg);
          console.error('Login error:', errMsg);
        }
      } catch (e) {
        alert('Network error: ' + e);
        console.error('Network error:', e);
      }
    });
  }

  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
      };

      try {
        const res = await fetch('/api/v1/users/', {
          method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
          body: JSON.stringify(data)
        });

        if (res.ok) {
          showToast('Registration successful!');
          setTimeout(() => { window.location.href = '/login.html'; }, 1200);
        } else {
          const err = await res.json();
          showToast(err.message || 'Failed to register.', 4000);
        }
      } catch {
        showToast('Network error', 4000);
      }
    });
  }

  const placeForm = document.getElementById('place-form');
  if (placeForm) {
    // Detect edit mode
    const params = new URLSearchParams(window.location.search);
    const isEdit = params.get('edit') === '1';
    const placeId = params.get('place_id');

    if (isEdit && placeId) {
      // Load place data and fill form
      fetch(`/api/v1/places/${placeId}`)
        .then(res => res.json())
        .then(place => {
          document.getElementById('title').value = place.title || '';
          document.getElementById('description').value = place.description || '';
          document.getElementById('price').value = place.price || '';
          document.getElementById('latitude').value = place.latitude || '';
          document.getElementById('longitude').value = place.longitude || '';
          document.getElementById('amenities').value = (place.amenities || []).map(a => a.id || a.name).join(', ');
          // Cambia el título del formulario
          const h1 = document.querySelector('.site-header h1');
          if (h1) h1.textContent = 'Edit Place';
        })
        .catch(err => {
          alert('Error loading place data');
        });
    }

    placeForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const token = getCookie('token');
      if (!token) return alert('You must be logged in.');

      const data = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        price: parseFloat(document.getElementById('price').value),
        latitude: parseFloat(document.getElementById('latitude').value),
        longitude: parseFloat(document.getElementById('longitude').value),
        amenities: document.getElementById('amenities').value
          .split(',')
          .map(s => s.trim())
          .filter(Boolean)
      };

      let url = '/api/v1/places/';
      let method = 'POST';
      if (isEdit && placeId) {
        url = `/api/v1/places/${placeId}`;
        method = 'PUT';
      }

      const res = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(data)
      });

      if (res.ok) {
        showToast(isEdit ? 'Place updated!' : 'Place created!');
        setTimeout(() => { window.location.href = '/'; }, 1200);
      } else {
        const err = await res.json();
        showToast(`Failed: ${err.message}`, 4000);
      }
    });
  }

  const amenityForm = document.getElementById('amenity-form');
  if (amenityForm) {
    amenityForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const token = getCookie('token');
      const name = document.getElementById('name').value;
      if (!token) {
        alert('You must be logged in');
        return;
      }
      if (!name.trim()) {
        alert('Please enter a name for the amenity.');
        return;
      }
      try {
        const res = await fetch('/api/v1/amenities/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ name })
        });
        if (res.ok) {
          alert('Amenity created!');
          if (window.location.pathname.endsWith('/add_place.html')) {
            if (window.refreshAmenitiesList) window.refreshAmenitiesList();
          }
          setTimeout(() => { window.location.href = '/'; }, 1200);
        } else {
          const err = await res.json();
          alert((err.message || 'Failed to create amenity.') + '\n' + JSON.stringify(err));
          console.error('Amenity creation error:', err);
        }
      } catch (err) {
        alert('Network error: ' + err);
        console.error('Network error:', err);
      }
    });
  }

  const reviewForm = document.getElementById('review-form');
  if (reviewForm && window.location.pathname.endsWith('/place.html')) {
    reviewForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const token = getCookie('token');
      if (!token) return alert('You must be logged in.');

      const place_id = getPlaceIdFromURL(); // keep as string
      const text = document.getElementById('text').value;
      const rating = parseInt(document.getElementById('rating').value);

      if (!place_id || !text || isNaN(rating)) {
        showToast('Please provide valid data.', 4000);
        return;
      }

      const res = await fetch('/api/v1/reviews/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ text, rating, place_id })
      });

      if (res.ok) {
        showToast('Review created!');
        setTimeout(() => { window.location.reload(); }, 1200);
      } else {
        let errMsg = 'Failed';
        try {
          const err = await res.json();
          errMsg = err.message || JSON.stringify(err);
        } catch (e) {
          errMsg = 'Error ' + res.status;
        }
        showToast('Error: ' + errMsg, 4000);
        console.error('Review POST error:', errMsg);
      }
    });
  }

  // Siempre cargar los places en el home
  const priceFilter = document.getElementById('price-filter');
  if (document.getElementById('places-list')) {
    fetchPlaces();
    if (priceFilter) {
      priceFilter.addEventListener('change', () => {
        filterPlaces(priceFilter.value);
      });
    }
  }

  const sidebarLogout = document.getElementById('sidebar-logout');
  if (sidebarLogout) {
    sidebarLogout.addEventListener('click', () => {
      document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
      window.location.href = '/login.html';
    });
  }

  if (document.getElementById('place-details')) {
    fetchPlaceDetails();
    fetchPlaceReviews();
  }
});

// ---------- Utility Functions ----------
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id');
}

function fetchPlaces() {
  fetch('/api/v1/places')
    .then(res => {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(data => {
      allPlaces = data;
      displayPlaces(allPlaces);
    })
    .catch(err => {
      console.error('Fetch error:', err);
      const container = document.getElementById('places-list');
      if (container) container.innerHTML = '<p style="color:red;text-align:center">Error loading places. ' + err + '</p>';
    });
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  container.innerHTML = '';

  places.forEach(place => {
    const div = document.createElement('div');
    div.className = 'place-card';
    div.innerHTML = `
      <h3>${place.title}</h3>
      <p>${place.description}</p>
      <p><strong>Price:</strong> $${place.price}</p>
      <a class="details-button" href="place.html?place_id=${place.id}">View Details</a>
    `;
    container.appendChild(div);
  });
}

function filterPlaces(maxPrice) {
  if (maxPrice === 'all') {
    displayPlaces(allPlaces);
  } else {
    const filtered = allPlaces.filter(p => p.price <= parseFloat(maxPrice));
    displayPlaces(filtered);
  }
}

function fetchPlaceDetails() {
  const placeId = getPlaceIdFromURL();
  if (!placeId) return;

  fetch(`/api/v1/places/${placeId}`)
    .then(res => res.json())
    .then(place => {
      // Fill details
      document.getElementById('place-title').textContent = place.title;
      document.getElementById('place-description').textContent = place.description;
      document.getElementById('place-price').textContent = place.price;
      document.getElementById('place-latitude').textContent = place.latitude;
      document.getElementById('place-longitude').textContent = place.longitude;
      // Fix amenities display: show names if amenities are objects
      if (Array.isArray(place.amenities) && place.amenities.length > 0) {
        const names = place.amenities.map(a => (typeof a === 'object' && a !== null && a.name) ? a.name : a);
        document.getElementById('place-amenities').textContent = names.join(', ');
      } else {
        document.getElementById('place-amenities').textContent = '';
      }

      // Show edit/delete buttons if owner or admin
      const token = getCookie('token');
      let isOwnerOrAdmin = false;
      if (token) {
        try {
          // Decode JWT (payload is base64 in 2nd part)
          const payload = JSON.parse(atob(token.split('.')[1]));
          const userId = payload.sub || payload.identity || payload.user_id;
          const isAdmin = payload.is_admin || false;
          if (isAdmin || (userId && userId == place.user_id)) {
            isOwnerOrAdmin = true;
          }
        } catch (e) {
          console.warn('JWT decode error:', e);
        }
      }
      const editBtn = document.getElementById('edit-place-btn');
      const deleteBtn = document.getElementById('delete-place-btn');
      if (isOwnerOrAdmin) {
        if (editBtn) editBtn.classList.remove('hidden');
        if (deleteBtn) deleteBtn.classList.remove('hidden');
        console.log('User is owner or admin, showing edit/delete buttons.');
      } else {
        if (editBtn) editBtn.classList.add('hidden');
        if (deleteBtn) deleteBtn.classList.add('hidden');
        console.log('User is NOT owner/admin. userId:', token ? (function(){try{const p=JSON.parse(atob(token.split('.')[1]));return p.sub||p.identity||p.user_id;}catch(e){return 'JWT error';}})() : 'no token', 'place.user_id:', place.user_id);
      }

      // Add handlers
      if (editBtn) {
        editBtn.onclick = function() {
          window.location.href = `/add_place.html?edit=1&place_id=${place.id}`;
        };
      }
      if (deleteBtn) {
        deleteBtn.onclick = async function() {
          if (!confirm('Are you sure you want to delete this place?')) return;
          const res = await fetch(`/api/v1/places/${place.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          if (res.ok) {
            setTimeout(() => { window.location.href = '/'; }, 1200);
          } else {
            let errMsg = 'Failed';
            try {
              const err = await res.json();
              errMsg = err.message || JSON.stringify(err);
            } catch (e) {
              errMsg = 'Error ' + res.status;
            }
          }
        };
      }
    })
    .catch(err => {
      console.error('Error loading place details:', err);
      document.getElementById('place-details').innerHTML = '<p>Error loading place details.</p>';
    });
}

function fetchPlaceReviews() {
  const placeId = getPlaceIdFromURL();
  if (!placeId) return;

  fetch(`/api/v1/reviews/places/${placeId}/reviews`)
    .then(res => res.json())
    .then(reviews => {
      const reviewsSection = document.getElementById('reviews');
      if (!reviewsSection) return;

      if (reviews.length === 0) {
        reviewsSection.innerHTML += '<p>No reviews yet.</p>';
        return;
      }

      const ul = document.createElement('ul');
      reviews.forEach(review => {
        const li = document.createElement('li');
        let userName = 'Anonymous';
        if (review.user && review.user.first_name) {
          userName = review.user.first_name;
          if (review.user.last_name) {
            userName += ' ' + review.user.last_name;
          }
        }
        // Estrellas para rating
        let stars = '<span class="review-stars">';
        for (let i = 1; i <= 5; i++) {
          stars += i <= review.rating ? '★' : '☆';
        }
        stars += '</span>';
        li.innerHTML = `<strong>${userName}:</strong> ${review.text} ${stars}`;
        ul.appendChild(li);
      });
      reviewsSection.appendChild(ul);
    })
    .catch(err => {
      console.error('Error loading reviews:', err);
      document.getElementById('reviews').innerHTML += '<p>Error loading reviews.</p>';
    });
}

// Dark mode toggle with persistence (works on all pages)
function setupDarkModeBtn() {
  const darkBtn = document.getElementById('toggle-dark');
  if (localStorage.getItem('dark-mode') === '1') {
    document.body.classList.add('dark-mode');
    if (darkBtn) darkBtn.textContent = 'Light Mode';
  } else {
    document.body.classList.remove('dark-mode');
    if (darkBtn) darkBtn.textContent = 'Dark Mode';
  }
  if (darkBtn) {
    darkBtn.onclick = function() {
      document.body.classList.toggle('dark-mode');
      const isDark = document.body.classList.contains('dark-mode');
      darkBtn.textContent = isDark ? 'Light Mode' : 'Dark Mode';
      localStorage.setItem('dark-mode', isDark ? '1' : '0');
    };
  }
}

window.addEventListener('error', function(e) {
  console.error('JavaScript error: ' + e.message);
});
