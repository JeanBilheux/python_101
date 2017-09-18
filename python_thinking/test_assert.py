def apply_discount(product, discount):

    price = int(product['price'] * (1.0 - discount))
    assert 0 <= price <= product['price'] , "wrong discount!"
    return price

if __name__ == '__main__':

    shoes = {'name': 'Fancy Shoes', 'price': 14900}
    print(apply_discount(shoes, 0.25))
    print(apply_discount(shoes, 2))


## command to run it

#/Users/j35/anaconda/envs/py35/bin/python -O /Users/j35/git/notebooks/python_101/python_thinking/test_assert.py
#11175
#-14900

#Process finished with exit code 0
