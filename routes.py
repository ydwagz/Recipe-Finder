from os import makedirs, path

from sqlalchemy import inspect, text
from werkzeug.utils import secure_filename
from ext import app
from flask import abort, flash, redirect, render_template, request, session, url_for
from forms import LoginForm, RecipeForm, RegisterForm
from models import Recipe, Review, User
from ext import db

ADMIN_USERNAMES = {"admin", "luca", "lukas"}


def ensure_database_schema():
    db.create_all()
    recipe_columns = {column["name"] for column in inspect(db.engine).get_columns("recipes")}
    if "details" not in recipe_columns:
        db.session.execute(text("ALTER TABLE recipes ADD COLUMN details TEXT NOT NULL DEFAULT ''"))
    if "user_id" not in recipe_columns:
        db.session.execute(text("ALTER TABLE recipes ADD COLUMN user_id INTEGER"))
    db.session.commit()


def get_current_profile():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return User.query.get(user_id)


def is_recipe_owner_or_admin(recipe):
    current_profile = get_current_profile()
    return bool(current_profile and (current_profile.is_admin or recipe.user_id == current_profile.id))


def require_login():
    if not get_current_profile():
        flash("Please log in first.")
        return redirect(url_for("login"))
    return None


def save_uploaded_image(upload):
    filename = secure_filename(upload.filename)
    if not filename:
        return ""

    image_folder = path.join(app.root_path, "static", "images")
    makedirs(image_folder, exist_ok=True)
    upload.save(path.join(image_folder, filename))
    return filename


@app.context_processor
def inject_current_profile():
    return {"current_profile": get_current_profile()}


def get_ingredients(text):
    return [item.strip().lower() for item in text.replace(",", " ").split() if item.strip()]


@app.route("/")
def home():
    ingredients_text = request.args.get("ingredients", "")
    ingredients = get_ingredients(ingredients_text)
    recipes = Recipe.query.all()
    if ingredients:
        recipes = [
            recipe for recipe in recipes
            if any(ingredient in recipe.ingredients.lower() or ingredient in recipe.title.lower() for ingredient in ingredients)
        ]
    return render_template(
        "index.html",
        recipes=recipes,
        ingredients_text=ingredients_text,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    error = ""
    if form.validate_on_submit():
        username = form.username.data.strip()
        if User.query.filter_by(username=username).first():
            error = "That username is already taken."
            return render_template("register.html", form=form, error=error)

        user_count = User.query.count()
        new_user = User(
            username=username,
            birthdate=form.birthdate.data,
            country=form.country.data,
            is_admin=(user_count == 0 or username.lower() in ADMIN_USERNAMES),
        )
        new_user.set_password(form.password.data)
        img = form.image.data
        if img:
            new_user.image = save_uploaded_image(img)
        new_user.create()
        session["user_id"] = new_user.id
        return redirect("/")
    return render_template("register.html", form=form, error=error)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect

    form = RecipeForm()
    if form.validate_on_submit():
        current_profile = get_current_profile()
        new_recipe = Recipe(
            title=form.title.data,
            ingredients=form.ingredients.data,
            details=form.details.data,
            user_id=current_profile.id,
        )
        img = form.image.data
        if img:
            new_recipe.image = save_uploaded_image(img)
        new_recipe.create()
        return redirect("/")
    return render_template("add_recipe.html", form=form)


@app.route("/update_recipe/<int:recipe_id>", methods=["GET", "POST"])
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if not is_recipe_owner_or_admin(recipe):
        abort(403)

    form = RecipeForm(title=recipe.title, ingredients=recipe.ingredients, details=recipe.details)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.ingredients = form.ingredients.data
        recipe.details = form.details.data
        image = form.image.data
        if image:
            recipe.image = save_uploaded_image(image)

        recipe.save()
        return redirect("/")
    return render_template("add_recipe.html", form=form)


@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if not is_recipe_owner_or_admin(recipe):
        abort(403)

    recipe.delete()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = ""
    if form.validate_on_submit():
        profile = User.query.filter_by(username=form.username.data.strip()).first()
        if profile and profile.check_password(form.password.data):
            session["user_id"] = profile.id
            return redirect("/")
        error = "Username or password is incorrect."
    return render_template("login.html", form=form, error=error)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/recipe/<int:recipe_id>")
def view_recipe_details(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    reviews = Review.query.filter(Review.recipe_id == recipe_id).all()
    return render_template("recipe_details.html", recipe=recipe, reviews=reviews)
