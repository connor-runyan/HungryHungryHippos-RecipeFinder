"""Holds the recipe models for the database."""

from django.db import models
from django.db.models import Q, QuerySet
from django.contrib.auth.models import User
from django.utils import timezone


class Group(models.Model):
    """This represents a food category.

    Each ingredient has a single category. In the web-app, the ingredients are
    categorized by these groups.
    """

    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return self.name


class Ingredient(models.Model):
    """This is an ingredient to recipes.

    Each ingredient may be a part of many recipes and each recipe may have many
    ingredients. The purpose of this class is to provide consistent naming between
    ingredients and easier filtering of recipes by ingredient. Each recipe is a part
    of a group.
    """

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return self.name

    def get_recipes(self):
        """Return a QuerySet of associated Recipes"""
        return self.recipe_set.values()

class IngredientUtils():
    """Class of ingredient helper functions.

    Contains methods to help search for recipes by ingredient
    """

    def __str__(self):
        return "Ingredient Tools"


    def find_recipes(self, ingredients):
        """Returns a QuerySet of Recipes"""

        ing_qs = _make_qs_list(ingredient)
        recipes = _ingredient_intersect(ing_qs)
        return recipes
    
    def _ingredient_intersect(self, ing_qs_list):
        """Returns a QuerySet of Intersection Ingredients

        Given a list of Ingredient QuerySets, this function will
        perform a set intersection, and return a QuerySet containing
        only shared Recipes between the various Ingredients.
        """

        return QuerySet.intersection(*ing_qs_list)

    def _make_qs_list(self, ingredients):
        """Returns a list of QuerySets given a list of ingredient names"""
        qlist = Q()
        # loop over ingredients, making new Q objects and storing
        # them in a QuerySet
        for ing in ingredients:
            qlist |= Q(name=ing)
        db_ings = Ingredient.objects.filter(qlist)
        return db_ings
        



class Appliance(models.Model):
    """This is an appliance that is required to make a recipe.

    A recipe may
    have 0+ appliances. The purpose of this class is to provide consistent
    naming between appliances and easier filtering of recipes by appliance.
    """

    name = models.CharField(max_length=40)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return self.name


class Recipe(models.Model):
    """This holds all the attributes of a recipe.

    The title and summary display when the recipe is shown as a search result.
    The user is the user that submitted the recipe. The time is measured in minutes.
    The image_url points to either an internal or external image location. The
    rating ranges between zero and five. The ingredients and appliances have a
    many-to-many relationship with a recipe.
    """

    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    DIFFICULTY_CHOICES = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('D', 'Difficult')
    )
    difficulty = models.CharField(max_length=1, null=True,
        choices=DIFFICULTY_CHOICES)
    time = models.IntegerField(null=True, blank=True)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    instructions = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    ingredients = models.ManyToManyField(Ingredient,
through='RecipeIngredient')
    appliances = models.ManyToManyField(Appliance)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return self.title

    def get_ingredients(self):
        """Return a queryset of the ingredients in this recipe."""
        return self.ingredients.all()

    def get_appliances(self):
        """Return a queryset of the appliances required by this recipe."""
        return self.appliances.all()


class RecipeIngredient(models.Model):
    """This class is used in the relationship between recipes and ingredients.

    This class adds an amount of an ingredient as well as its unit.
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)
    unit = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return str(self.recipe)


class Comment(models.Model):
    """This holds a comment on a recipe."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return str(self.recipe)
