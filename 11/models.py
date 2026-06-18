from sqlalchemy import ForeignKey

from ext import db


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


class Recipe(db.Model, BaseModel):
    __tablename__ = "recipes"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    ingredients = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), default="")


class Review(db.Model, BaseModel):
    __tablename__ = "reviews"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    recipe_id = db.Column(ForeignKey("recipes.id"))
