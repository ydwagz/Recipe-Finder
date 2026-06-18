from sqlalchemy import ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash

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
    details = db.Column(db.Text(), nullable=False, default="")
    image = db.Column(db.String(), default="")
    user_id = db.Column(ForeignKey("users.id"))

    user = db.relationship("User", back_populates="recipes")


class User(db.Model, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date())
    country = db.Column(db.String(80), default="")
    image = db.Column(db.String(), default="")
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)

    recipes = db.relationship("Recipe", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Review(db.Model, BaseModel):
    __tablename__ = "reviews"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    recipe_id = db.Column(ForeignKey("recipes.id"))
