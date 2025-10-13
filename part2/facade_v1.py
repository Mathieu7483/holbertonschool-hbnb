#!/usr/bin/python3


from persistance_v1 import in_memory_repository


class HBnB_Facade:
    def __init__(self):
        self.user_repo = in_memory_repository()
        self.place_repo = in_memory_repository()
        self.review_repo = in_memory_repository()
        self.amenity_repo = in_memory_repository()

    def create_user(self, user_data):
        pass

    def get_place(self, place_id):
        pass
