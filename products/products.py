from flask import Blueprint, render_template
from API.api import GetAllProducts, GetSingleProducts, GetAllProductsCategory
from flask import Flask, render_template, request, redirect, url_for
products_bp = Blueprint('products_bp', __name__,
    template_folder='templates',
    static_folder='static')

@products_bp.route('/products')
def index():
    data = GetAllProducts()
    l = len(data)
    categories = set(product["category"] for product in data)
    sortedCategory = sorted(categories)
    categories_count = {}
    for product in data:
       category = product["category"]
       categories_count[category] = categories_count.get(category, 0) + 1
    return render_template('products/products.html', length =l, products=data, categories=sortedCategory, pocetProduktu = categories_count)

@products_bp.route('/products/<int:id>')
def detailOfProduct(id):
    data = GetSingleProducts(id)
    #nacteni nazvu kategorie z promenne data do promenne categories
    categories = data["category"]
    #nacteni vsech produktu pres metodu GetAllProductsCategory(categories)
    allProducts = GetAllProductsCategory(categories)
    categoryProduct = [product for product in allProducts if product["category"] == categories]
    #omezeni pro nactene produkty
    l = len(categoryProduct)
    if l > 5:
        l = 5
    filtered_products = [product for product in categoryProduct if product["id"] != id]
    fourProducts = filtered_products[:l]
    return render_template('products/detail.html',length = l, id=id, detailOfProduct=data, features=fourProducts)

@products_bp.route('/products/add', methods=['GET','POST'])
def uploadProduct():
     if request.method == 'POST':
        # Zpracování formuláře
        product_name = request.form.get('productName')
        product_description = request.form.get('productDescription')
        product_image = request.files.get('productImage', None)
        product_price = request.form.get('productPrice')
        product_category = request.form.get('productCategory')

        if product_image is None:
            return "No product image provided."

        fakestore_api_url = "https://fakestoreapi.com/products"
        product_data = {
            "title": product_name,
            "description": product_description,
            "image": product_image.read(),
            "price": float(product_price),
            "category": product_category,
        }

        # Use requests.post (not request.post)
        response = requests.post(fakestore_api_url, json=product_data)

        return render_template('products/new-product.html')

     return render_template('products/new-product.html')