# from datetime import datetime, timedelta
#
# import pandas as pd
# from bokeh.charts import TimeSeries
# from bokeh.embed import components
# from bokeh.resources import INLINE

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, AnyOf

import yummly

# default option values
TIMEOUT = 15.0
RETRIES = 2

# Yummly mjboothaus Account: Hackathon Plan - Access granted 24 July 2017
API_ID = 'b4f167ed'
API_KEY = 'f69184af19beb4b76e7b7b1984046581'


# TODO: Look at saving down / caching queries for re-use to avoid using up too many queries
# TODO: Can I use the Beaker library for this? http://beaker.readthedocs.io/en/latest/index.html

# TODO: Need to get templated code into html files

class SearchRecipeForm(FlaskForm):
    # TODO: Improve validation

    search_terms = StringField(u'Recipe search terms:',
                               validators=[DataRequired(), Length(min=2, max=25)],
                               default='Green eggs and ham')

    submit = SubmitField('Submit')


def main():
    return  # TODO: Clarify - is this just a dummy function?


# App configuration

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('splash_screen.html')


@app.route('/search_recipe', methods=['GET', 'POST'])
def searchrecipe():
    form = SearchRecipeForm()
    return render_template('search_recipe.html', form=form)


@app.route('/recipe', methods=['POST'])
def recipe():
    search_terms = request.form.get('search_terms')

    try:

        # Yummly API info - see https://github.com/dgilland/yummly.py

        client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)
        search = client.search(search_terms)

        # params = dict()
        #
        # params['q'] = search_terms
        # params['start'] = 0
        # params['maxResult'] = 10
        # params['requirePicutres'] = True
        # params['allowedIngredient[]'] = ['salt']
        # params['excludedIngredient[]'] = ['']
        # params['maxTotalTimeInSeconds'] = 3600
        # params['facetField[]'] = ['ingredient', 'diet']
        # params['flavor.meaty.min'] = 0.5
        # params['flavor.meaty.max'] = 1
        # params['flavor.sweet.min'] = 0
        # params['flavor.sweet.max'] = 0.5
        # params['nutrition.FAT.min'] = 0
        # params['nutrition.FAT.max'] = 15
        #
        # search = client.search(**params)

        match = search.matches[0]
        recipe = client.recipe(match.id)

    except:
        return render_template('error_recipe.html')

    return render_template('display_recipe.html', recipe_name=recipe.name,
                           recipe_id=recipe.id,
                           recipe_rating=recipe.rating,
                           ingred_list=recipe.ingredientLines)


# print('Total Time:', recipe.totalTime)
# print('Yields:', recipe.yields)
# print('Ingredients:')
# for ingred in recipe.ingredientLines:
#    print(ingred)


if __name__ == '__main__':
    main()
    app.run(port=33507)
