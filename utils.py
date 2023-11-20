def get_product_quantity(lookup, product_id):
    quantity = eval(lookup).get(str(product_id), '0')
    return int(quantity)
