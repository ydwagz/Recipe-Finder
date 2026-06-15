from os import path

from ext import app
from flask import redirect, render_template, request, session
from forms import LoginForm, RecipeForm, RegisterForm
from models import Recipe, Review

profiles = []


def get_current_profile():
    profile_id = session.get("profile_id")
    if profile_id is None or profile_id >= len(profiles):
        return None
    return profiles[profile_id]


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
        role="admin",
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = {
            "username": form.username.data,
            "password": form.password.data,
            "date": form.birthdate.data,
            "img": "",
        }
        img = form.image.data
        if img:
            directory = path.join(app.root_path, "static", "images", img.filename)
            new_user["img"] = img.filename
            img.save(directory)
        profiles.append(new_user)
        session["profile_id"] = len(profiles) - 1
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        new_recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data)
        img = form.image.data
        if img:
            directory = path.join(app.root_path, "static", "images", img.filename)
            new_recipe.image = img.filename
            img.save(directory)
        new_recipe.create()
        return redirect("/")
    return render_template("add_recipe.html", form=form)


@app.route("/update_recipe/<int:recipe_id>", methods=["GET", "POST"])
def update_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    form = RecipeForm(title=recipe.title, ingredients=recipe.ingredients)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.ingredients = form.ingredients.data
        image = form.image.data
        if image:
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            recipe.image = image.filename

        recipe.save()
        return redirect("/")
    return render_template("add_recipe.html", form=form)


@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    recipe.delete()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = ""
    if form.validate_on_submit():
        for index, profile in enumerate(profiles):
            if profile["username"] == form.username.data and profile["password"] == form.password.data:
                session["profile_id"] = index
                return redirect("/")
        error = "Username or password is incorrect."
    return render_template("login.html", form=form, error=error)


@app.route("/logout")
def logout():
    session.pop("profile_id", None)
    return redirect("/")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/profile/<int:profile_id>")
def profile(profile_id):
    return redirect("/")


@app.route("/recipe/<int:recipe_id>")
def view_recipe_details(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    reviews = Review.query.filter(Review.recipe_id == recipe_id).all()
    return render_template("recipe_details.html", recipe=recipe, reviews=reviews)


@app.route("/category/<category>")
def show_category(category):
    return render_template("category.html", c=category)
