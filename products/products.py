from flask import Blueprint, render_template
from API.api import GetAllProducts, GetSingleProducts, GetAllProductsCategory
products_bp = Blueprint('products_bp', __name__,
    template_folder='templates',
    static_folder='static')

@products_bp.route('/products')
def index():
    data = GetAllProducts()
    l = len(data)
    categories = set(product["category"] for product in data)
    return render_template('products/products.html', length =l, products=data, categories=categories)

@products_bp.route('/products/<int:id>')
def detailOfProduct(id):
    data = GetSingleProducts(id)
    #nacteni nazvu kategorie z promenne data do promenne categories
    categories = data["category"]
    #nacteni vsech produktu pres metodu GetAllProductsCategory(categories)
    allProducts = GetAllProductsCategory(categories)
    categoryProduct = [product for product in allProducts if product["category"] == categories]
    l = len(categoryProduct)
    if l > 5:
        l = 5
    filtered_products = [product for product in categoryProduct if product["id"] != id]
    fourProducts = filtered_products[:l]
    return render_template('products/detail.html',length = l, id=id, detailOfProduct=data, features=fourProducts)
