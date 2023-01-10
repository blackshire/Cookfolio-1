from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Recipe
from . import db
from sqlalchemy.sql import func

views = Blueprint('views', __name__)  # Allows us to use the views to tell the site where to go


@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    recipe_count = len(current_user.recipes)
    if request.method == 'POST':
        pass
    return render_template('index.html', user=current_user, recipe_count=recipe_count)


@views.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    ingredients = recipe.ingredients.split(',')
    return render_template('recipe.html', user=current_user, recipe=recipe, ingredients=ingredients)


@views.route('/new_recipe', methods=['GET', 'POST'])
@login_required
def new_recipe():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        servings = request.form.get('servings')
        cook_time = request.form.get('cook-time')

        ingredients = ''
        for n, i in enumerate(request.form.getlist('ingredient-number')):
            ingredients += f'{i} {request.form.getlist("ingredient-unit")[n]} {request.form.getlist("ingredient-description")[n]},'

        directions = request.form.get('directions')
        nutrition = request.form.get('nutrition')

        is_public = False
        if request.form.get('public') is not None:
            is_public = True

        last_id = db.session.query(func.max(Recipe.id)).scalar()
        add_recipe = Recipe(id=last_id + 1,
                            name=name,
                            description=description,
                            servings=servings,
                            cook_time=cook_time,
                            ingredients=ingredients[0:len(ingredients) - 1],
                            directions=directions,
                            nutrition=nutrition,
                            is_public=is_public,
                            user_id=current_user.id)

        if Recipe.query.filter(func.lower(Recipe.name).ilike(func.lower(add_recipe.name))).first():
            flash('That recipe already exists', category='error')
            return render_template('new_recipe.html', user=current_user)

        db.session.add(add_recipe)
        db.session.commit()

        flash('Recipe created!', category='success')
        return redirect(url_for('views.index'))
    return render_template('new_recipe.html', user=current_user)


@views.route('/public_recipes', methods=['GET', 'POST'])
@login_required
def public_recipes():
    recipe_list = Recipe.query.filter_by(is_public=True).all()

    return render_template('public_recipes.html', user=current_user, recipe_list=recipe_list)
