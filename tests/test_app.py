from models import GroceryList, Product, Recipe


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_product(client, app):
    with app.app_context():
        # Add product
        response = client.post('/products/add', data={'name': 'product_A', 'gluten': '', 'price': ''})
        assert response.status_code == 302
        assert Product.query.count() == 1
        assert Product.query.first().name == 'product_A'
        assert Product.query.first().gluten != ''
        assert Product.query.first().price == 0.0

        # Update product
        product_id = Product.query.first().id
        response = client.post(f'/products/update/{product_id}', data={'name': 'product_A', 'gluten': '', 'price': 1})
        assert response.status_code == 302
        assert Product.query.first().price == 1

        # Delete product
        response = client.post(f'/products/update/{product_id}', data={'delete_product': True})
        assert response.status_code == 302
        assert Product.query.count() == 0


def test_recipe(client, app):
    with app.app_context():
        # Add product
        client.post('/products/add', data={'name': 'product_A', 'gluten': '', 'price': ''})
        product_id = Product.query.first().id

        # Add recipe
        response = client.post('/recipes/add', data={'name': 'recipe_A', 'description': 'recipe_A_description',
                                                     f'quantity_{product_id}': 1})
        assert response.status_code == 302
        assert Recipe.query.count() == 1
        assert Recipe.query.first().name == 'recipe_A'
        assert Recipe.query.first().description == 'recipe_A_description'
        assert Recipe.query.first().products == "{'1': '1'}"

        # Update recipe
        response = client.post('/recipes/update/1', data={'recipe_name': 'recipe_A', 'recipe_description': 'recipe_A_description',
                                                          f'quantity_{product_id}': 2})
        assert response.status_code == 302
        assert Recipe.query.count() == 1
        assert Recipe.query.first().name == 'recipe_A'
        assert Recipe.query.first().description == 'recipe_A_description'
        assert Recipe.query.first().products == "{'1': '2'}"

        # Delete recipe
        response = client.post('/recipes/update/1', data={'delete_recipe': True})
        assert response.status_code == 302
        assert Recipe.query.count() == 0


def test_grocery(client, app):
    """
    This will test the grocery list api calls

    1. Add a product to the product list
    2. Add the product to the grocery list
    3. Create a recipe with a product
    4. Add the recipe to the grocery list, the quantity should sum with the product already in the grocery list and the
       subtotal should calculate accordingly
    5. Adjust the quantity of the grocery list, the subtotal should calculate
    6. Remove the product from the grocery list

    Args:
        client: fixture
        app: fixture

    Returns:

    """
    with app.app_context():
        # Add product
        client.post('/products/add', data={'name': 'product_A', 'gluten': '', 'price': 1})
        product_id = Product.query.first().id

        # Add product to grocery list
        response = client.post(f'/grocery_list/add/product/{product_id}')
        assert response.status_code == 302
        assert GroceryList.query.first().product_id == product_id
        assert GroceryList.query.first().quantity == 1
        assert GroceryList.query.first().subtotal == 1

        # Add recipe
        client.post('/recipes/add', data={'name': 'recipe_A', 'description': 'recipe_A_description',
                                          f'quantity_{product_id}': 1})
        recipe_id = Recipe.query.first().id

        # Add recipe to grocery list
        response = client.post(f'/grocery_list/add/recipe/{recipe_id}')
        assert response.status_code == 302
        assert GroceryList.query.count() == 1
        assert GroceryList.query.first().product_id == product_id
        assert GroceryList.query.first().quantity == 2
        assert GroceryList.query.first().subtotal == 2.0

        # Update grocery list item quantity
        response = client.post(f'/grocery_list/update/quantity/{product_id}', data={'increase': 1})
        assert response.status_code == 302
        assert GroceryList.query.first().quantity == 3
        client.post(f'/grocery_list/update/quantity/{product_id}', data={'decrease': 1})
        assert GroceryList.query.first().quantity == 2

        # Remove product from grocery list
        response = client.post('/grocery_list/remove/product', data={'product_id': product_id})
        assert response.status_code == 302
        assert GroceryList.query.count() == 0
