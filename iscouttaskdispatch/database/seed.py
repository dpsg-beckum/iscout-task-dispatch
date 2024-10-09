from .db import Status, db


def seed_database():
    Status.create_new(1, "Created")
    Status.create_new(2, "Work in Progress")
    Status.create_new(3, "Done")
    Status.create_new(4, "Failed")
