
-- Insert admin user (bcrypt hash for 'admin1234' is example, replace if needed)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$wI6Qw6Qw6Qw6Qw6Qw6Qw6uQw6Qw6Qw6Qw6Qw6Qw6Qw6Qw6Qw6Qw6', 1);

-- Insert amenities with UUIDs
INSERT INTO amenities (id, name) VALUES ('b1a7c1e2-1d2b-4e3a-9c4d-5e6f7a8b9c0d', 'WiFi');
INSERT INTO amenities (id, name) VALUES ('c2b8d2f3-2e3c-5f4b-0d1e-6f7a8b9c0d1e', 'Swimming Pool');
INSERT INTO amenities (id, name) VALUES ('d3c9e3f4-3f4d-6g5c-1e2f-7a8b9c0d1e2f', 'Air Conditioning');

-- Optionally, insert a sample place owned by the admin
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES ('e4d0f4g5-4g5e-7h6d-2f3g-8b9c0d1e2f3g', 'Sample Place', 'A nice place to stay', 100.00, 40.7128, -74.0060, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

-- Optionally, link amenities to the sample place
INSERT INTO place_amenity (place_id, amenity_id) VALUES ('e4d0f4g5-4g5e-7h6d-2f3g-8b9c0d1e2f3g', 'b1a7c1e2-1d2b-4e3a-9c4d-5e6f7a8b9c0d');
INSERT INTO place_amenity (place_id, amenity_id) VALUES ('e4d0f4g5-4g5e-7h6d-2f3g-8b9c0d1e2f3g', 'c2b8d2f3-2e3c-5f4b-0d1e-6f7a8b9c0d1e');
INSERT INTO place_amenity (place_id, amenity_id) VALUES ('e4d0f4g5-4g5e-7h6d-2f3g-8b9c0d1e2f3g', 'd3c9e3f4-3f4d-6g5c-1e2f-7a8b9c0d1e2f');

-- Optionally, insert a sample review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES ('f5e1g5h6-5h6f-8i7e-3g4h-9c0d1e2f3g4h', 'Great place!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'e4d0f4g5-4g5e-7h6d-2f3g-8b9c0d1e2f3g');
