// Fetch and display user's amenities in the add_place form

document.addEventListener('DOMContentLoaded', () => {
  const amenitiesInput = document.getElementById('amenities');
  const amenitiesList = document.createElement('ul');
  amenitiesList.id = 'user-amenities-list';
  amenitiesList.style.margin = '10px 0 0 0';
  amenitiesList.style.padding = '0 0 0 20px';
  amenitiesList.style.listStyle = 'disc';

  const amenitiesRow = amenitiesInput && amenitiesInput.parentElement;
  if (amenitiesRow) {
    amenitiesRow.appendChild(amenitiesList);
  }

  // Helper to add amenity to input
  function addAmenityToInput(id) {
    let current = amenitiesInput.value.split(',').map(s => s.trim()).filter(Boolean);
    if (!current.includes(id)) {
      current.push(id);
      amenitiesInput.value = current.join(', ');
    }
  }

  // Use the user's JWT from cookies if available
  // getCookie is already defined in scripts.js, so we avoid duplication if scripts.js is loaded first
  const getCookie = window.getCookie || function(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  };
  const token = getCookie('token');

  fetch('/api/v1/amenities/my_amenities', {
    headers: token ? { 'Authorization': 'Bearer ' + token } : {}
  })
    .then(res => res.json())
    .then(data => {
      amenitiesList.innerHTML = '';
      if (Array.isArray(data) && data.length > 0) {
        data.forEach(a => {
          const li = document.createElement('li');
          li.innerHTML = `<strong>${a.name}</strong> <span style="color:#888;font-size:0.95em">(ID: ${a.id})</span> <button type="button" style="margin-left:8px;padding:2px 8px;font-size:0.95em;cursor:pointer;" data-id="${a.id}">Add</button>`;
          li.querySelector('button').onclick = function() {
            addAmenityToInput(a.id);
          };
          amenitiesList.appendChild(li);
        });
      } else {
        amenitiesList.innerHTML = '<li style="color:#888">No amenities found</li>';
      }
    })
    .catch(() => {
      amenitiesList.innerHTML = '<li style="color:#d72631">Could not load amenities</li>';
    });
});

window.refreshAmenitiesList = function() {
  const amenitiesInput = document.getElementById('amenities');
  const amenitiesList = document.getElementById('user-amenities-list');
  if (!amenitiesInput || !amenitiesList) return;
  // Use global getCookie if available
  const getCookie = window.getCookie || function(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  };
  const token = getCookie('token');
  fetch('/api/v1/amenities/my_amenities', {
    headers: token ? { 'Authorization': 'Bearer ' + token } : {}
  })
    .then(res => res.json())
    .then(data => {
      amenitiesList.innerHTML = '';
      if (Array.isArray(data) && data.length > 0) {
        data.forEach(a => {
          const li = document.createElement('li');
          li.innerHTML = `<strong>${a.name}</strong> <span style="color:#888;font-size:0.95em">(ID: ${a.id})</span> <button type="button" style="margin-left:8px;padding:2px 8px;font-size:0.95em;cursor:pointer;" data-id="${a.id}">Add</button>`;
          li.querySelector('button').onclick = function() {
            let current = amenitiesInput.value.split(',').map(s => s.trim()).filter(Boolean);
            if (!current.includes(a.id)) {
              current.push(a.id);
              amenitiesInput.value = current.join(', ');
            }
          };
          amenitiesList.appendChild(li);
        });
      } else {
        amenitiesList.innerHTML = '<li style="color:#888">No amenities found</li>';
      }
    })
    .catch(() => {
      amenitiesList.innerHTML = '<li style="color:#d72631">Could not load amenities</li>';
    });
};
