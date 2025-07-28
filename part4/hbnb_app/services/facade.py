from hbnb_app.persistence.user_repository import UserRepository
from hbnb_app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from hbnb_app.models.user    import User
from hbnb_app.models.amenity import Amenity
from hbnb_app.models.place   import Place
from hbnb_app.models.review  import Review

class HBnBFacade:
    def get_amenities_by_owner(self, owner_id):
        """Return all amenities owned by a specific user (owner_id)"""
        return [a for a in self.amenity_repo.get_all() if str(a.owner_id) == str(owner_id)]
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo   = SQLAlchemyRepository(Place)
        self.review_repo  = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        allowed_fields = ['email', 'password', 'first_name', 'last_name']
        extra_fields = set(user_data.keys()) - set(allowed_fields)

        if extra_fields:
            raise ValueError(f"Invalid fields: {extra_fields}")
        
        filtered_data = {k : user_data[k] for k in allowed_fields if k in user_data}
        user = User(**filtered_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)
    

    def create_amenity(self, amenity_data):
        name = amenity_data.get('name')
        owner_id = amenity_data.get('owner_id')


        import logging
        logging.warning(f"create_amenity called with: {amenity_data}")

        if not name or not owner_id:
            raise ValueError("Amenity must have a name and an owner_id")


        if isinstance(owner_id, dict):
            owner_id = owner_id.get('id')
            logging.warning(f"owner_id extracted from dict: {owner_id}")

        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f'Owner with ID {owner_id} not found')


        for amenity in getattr(owner, 'amenities', []):
            if amenity.name.strip().lower() == name.strip().lower():
                raise ValueError(f"Amenity with name '{name}' already exists for this user")

        amenity = Amenity(name=name, owner=owner, owner_id=owner.id)
        if hasattr(owner, 'amenities'):
            owner.amenities.append(amenity)
        self.amenity_repo.add(amenity)
        logging.warning(f"Amenity created: {amenity}")
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity {amenity_id} not found")
        return amenity
    
    def get_amenity_by_name(self, name):
        name = name.strip().lower()
        for amenity in self.get_all_amenities():
            if amenity.name.strip().lower() == name:
                return amenity
        raise ValueError(f"Amenity with name {name} not found")

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update_from_dict(amenity_data)

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
    
    def delete_amenity(self, amenity_id, current_user):
        amenity = self.get_amenity(amenity_id)
        user_id = current_user.get('id') if isinstance(current_user, dict) else current_user
        is_admin = current_user.get('is_admin', False) if isinstance(current_user, dict) else False
        if str(amenity.owner_id) != str(user_id) and not is_admin:
            raise ValueError("You are not allowed to delete this amenity")
        self.amenity_repo.delete(amenity_id)



    def create_place(self, place_data):
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")
        
        current_user = place_data.get('user')

        amenities = []
        for amenity_input in place_data.get('amenities', []):
            try:
                amenity = self.get_amenity(amenity_input)
            except ValueError:

                amenity = self.get_amenity_by_name(amenity_input)

            if not current_user.get('is_admin', False) and amenity.owner_id != owner.id:
                raise ValueError(f"Amenity '{amenity.name}' does not belong to the user")
            
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
            description=place_data.get('description', '')
        )
        for a in amenities:
            place.add_amenity(a)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        
        if 'owner_id' in place_data:
            raise ValueError("Changing the owner of a place is not allowed")
    
        if 'amenities' in place_data:
            amenities = []
            for amenity_input in place_data['amenities']:
                try:
                    amenity = self.get_amenity(amenity_input)
                except ValueError:
                    amenity = self.get_amenity_by_name(amenity_input)
                amenities.append(amenity)

    
            place_data = dict(place_data)
            place_data['amenities'] = amenities

        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)


    def delete_place(self, place_id):
        self.place_repo.delete(place_id)


    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)


facade = HBnBFacade()

