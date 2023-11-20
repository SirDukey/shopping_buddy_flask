import os


from flask import Flask, flash, render_template, request, url_for, redirect
from sqlalchemy import func
from utils import get_product_quantity


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = os.getenv('DEBUG')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.globals.update(get_product_quantity=get_product_quantity)


# Import after app setup to avoid circular import issue
from models import db, GroceryList, Product, Recipe


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products')
def products():
    table = Product.query.all()
    return render_template('products.html', products=table)


@app.route('/products/update/<int:product_id>', methods=['POST'])
def update_product(product_id):
    product = db.get_or_404(Product, product_id)

    if request.form.get('delete_product'):
        db.session.delete(product)
        db.session.commit()
        flash(f'Deleted: {product.name}')
        return redirect(url_for('products'))

    product.name = request.form.get('name')
    product.brand = request.form.get('brand')
    product.store = request.form.get('store')
    product.category = request.form.get('category')
    gluten = request.form.get('gluten')
    if gluten == '':
        product.gluten = False
    else:
        product.gluten = eval(gluten.capitalize())
    product.price = eval(request.form.get('price'))
    product.updated = func.now()
    db.session.commit()
    flash(f'Updated: {product.name}')
    return redirect(url_for('products'))


@app.route('/products/add', methods=['POST'])
def add_product():
    product = Product()
    product.name = request.form.get('name')
    product.brand = request.form.get('brand')
    product.store = request.form.get('store')
    product.category = request.form.get('category')
    gluten = request.form.get('gluten')
    if gluten == '':
        product.gluten = False
    else:
        product.gluten = eval(gluten.capitalize())
    price = request.form.get('price')
    if price == '':
        product.price = 0.0
    else:
        product.price = eval(request.form.get('price'))
    db.session.add(product)
    db.session.commit()
    flash(f'Added: {product.name}')
    return redirect(url_for('products'))


@app.route('/grocery_list')
def grocery_list():
    table = GroceryList.query.all()
    total = 0.0
    for row in table:
        total += row.subtotal
    products_with_quantities = {}
    for row in table:
        product = db.get_or_404(Product, row.product_id)
        products_with_quantities[product.name] = {
            'id': product.id, 'quantity': row.quantity, 'store': product.store, 'price': product.price,
            'subtotal': row.subtotal,
        }
    return render_template('grocery_list.html',
                           products_with_quantities=products_with_quantities, total=total)


@app.route('/grocery_list/update/quantity/<int:product_id>', methods=['POST'])
def update_grocery_list_quantity(product_id):
    product = db.get_or_404(Product, product_id)
    table = db.session.query(GroceryList).filter(GroceryList.product_id == product_id).all()

    decrease = request.form.get('decrease')
    increase = request.form.get('increase')
    for row in table:
        if decrease and row.quantity > 1:
            row.quantity -= 1
        elif increase:
            row.quantity += 1
        row.subtotal = product.price * row.quantity
        db.session.commit()

    return redirect(url_for('grocery_list'))


@app.route('/grocery_list/remove/product', methods=['POST'])
def remove_product_from_grocery_list():
    product_id = request.form.get('product_id')
    product = db.get_or_404(Product, product_id)
    table = db.session.query(GroceryList).filter(GroceryList.product_id == product_id).all()
    product.in_list = False
    for row in table:
        db.session.delete(row)
        db.session.commit()
    return redirect(url_for('grocery_list'))


@app.route('/grocery_list/add/product/<int:product_id>', methods=['POST'])
def add_product_to_grocery_list(product_id, quantity=None):
    product = db.get_or_404(Product, product_id)

    # check if the product is in the grocery list table
    result = db.session.query(GroceryList).filter(GroceryList.product_id == product_id).all()
    if any(result):
        # product is in the table so it should be removed
        product.in_list = False
        for row in result:
            db.session.delete(row)
            db.session.commit()

    else:
        # add a product to the grocery list table
        product.in_list = True
        grocery_item = GroceryList()
        grocery_item.product_id = product_id
        grocery_item.quantity = quantity if quantity else 1
        grocery_item.subtotal = product.price
        db.session.add(grocery_item)
        db.session.commit()
    return redirect(url_for('products'))


@app.route('/grocery_list/add/recipe/<int:recipe_id>', methods=['POST'])
def add_recipe_to_grocery_list(recipe_id):
    recipe = db.get_or_404(Recipe, recipe_id)
    products_quantities = eval(recipe.products)
    products_added = []
    for product_id, quantity in products_quantities.items():
        if quantity == '0':
            continue
        result = db.session.query(GroceryList).filter(GroceryList.product_id == product_id).all()
        if any(result):
            for row in result:
                if row.product_id == int(product_id):
                    row.quantity += int(quantity)
                    db.session.commit()
                    product = db.get_or_404(Product, int(product_id))
                    products_added.append(product.name)

        else:
            product = db.get_or_404(Product, int(product_id))
            product.in_list = True
            grocery_item = GroceryList()
            grocery_item.product_id = product_id
            grocery_item.quantity = quantity if quantity else 1
            grocery_item.subtotal = product.price
            db.session.add(grocery_item)
            products_added.append(product.name)
    db.session.commit()

    flash(f'Added products to grocery list: {products_added}')
    return redirect(url_for('recipes'))


@app.route('/recipes')
def recipes():
    table_recipe = Recipe.query.all()
    table_product = Product.query.all()
    return render_template('recipes.html', recipes=table_recipe, products=table_product)


@app.route('/recipes/add', methods=['POST'])
def add_recipe():
    recipe = Recipe()
    recipe.name = request.form.get('name')
    recipe.description = request.form.get('description')
    quantity_ids = [quantity_id for quantity_id in request.form.keys() if 'quantity' in quantity_id]
    products = {}
    for quantity_id in quantity_ids:
        quantity = request.form.get(quantity_id)
        if quantity != '0':
            products[quantity_id.split('_')[1]] = request.form.get(quantity_id)
    recipe.products = str(products)
    db.session.add(recipe)
    db.session.commit()
    flash(f'Added: {recipe.name}')
    return redirect(url_for('recipes'))


@app.route('/recipes/update/<int:recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipe = db.get_or_404(Recipe, recipe_id)
    if request.form.get('delete_recipe'):
        db.session.delete(recipe)
        db.session.commit()
        flash(f'Deleted: {recipe.name}')
        return redirect(url_for('recipes'))

    recipe.name = request.form.get('recipe_name')
    recipe.description = request.form.get('recipe_description')
    quantity_ids = [quantity_id for quantity_id in request.form.keys() if 'quantity' in quantity_id]
    products = {}
    for quantity_id in quantity_ids:
        products[quantity_id.split('_')[1]] = request.form.get(quantity_id)
    recipe.products = str(products)
    db.session.add(recipe)
    db.session.commit()
    flash(f'Updated: {recipe.name}')
    return redirect(url_for('recipes'))


if __name__ == '__main__':
    with app.app_context():
        # create the db schema if it does not exist
        db.create_all()
    app.run()
