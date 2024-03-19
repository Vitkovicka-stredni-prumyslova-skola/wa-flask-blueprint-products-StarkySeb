from flask import Blueprint, render_template, jsonify
from API.api import GetAllProducts, GetSingleProducts, GetAllProductsCategory, GetAllProductsId
from flask import Flask, render_template, request, redirect, url_for
import requests
import base64
from werkzeug.utils import secure_filename
import random
import json
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
    #podminka pro post, pokud nejsou odeslane data z formulare, nacte se webova stranka
    if request.method == 'POST':
        #nacteni produktu z formulare v new-product.html
        product_name = request.form.get('productName')
        product_description = request.form.get('productDescription')
        product_price = request.form.get('productPrice')
        product_category = request.form.get('productCategory')
        #podminka pro vyplneni vsech udaju, pokud neni splnena podminka vyhodi response
        if not all([product_name, product_description, product_price, product_category]):
            return "Please fill in all the form fields."
        #pouziti nahodneho generovani cisel v danem rozmezi pro pocet kusu produktu a pro hodnoceni produktu
        random_int = random.randint(100, 1000)
        random_rate = random.uniform(0.0, 5.0)
        #nacteni obrazu ze static souboru
        image = "static/img/noimage.png"
        #nacitani z formulare pro ulozeni dat do databaze fakeapistore
        product_data = {
            'title': product_name,
            'price': float(product_price),
            'description': product_description,
            'category': product_category,
            'image': image,
            'rating': {'rate':random_rate,'count':random_int}
        }
        #posilani dat do fakeapistore databaze
        fakestore_api_url = "https://fakestoreapi.com/products"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(fakestore_api_url, data=json.dumps(product_data), headers=headers)
        #podminka pro spravne nacteni produktu do databaze
        if response.status_code == 201:
            return "Upload successful"
        else:
            return "Upload failed."
    #nacteni databaze
    MyData = GetAllProducts()
    #nacteni nazvu kategorie z promenne data do promenne categories
    categories = set(product["category"] for product in MyData)
    sortedCategory = sorted(categories)
    categories_count = {}
    for product in MyData:
        category = product["category"]
        categories_count[category] = categories_count.get(category, 0) + 1
    return render_template('products/new-product.html', products=MyData, categories=sortedCategory, pocetProduktu=categories_count)

if __name__ == '__main__':
    app.run(debug=True)















"""
@products_bp.route('/products/add', methods=['GET','POST'])
def uploadProduct():
     if request.method == 'POST':
        # Zpracování formuláře
        product_name = request.form.get('productName')
        product_description = request.form.get('productDescription')
        #product_image = request.files.get('productImage', None)
        product_price = request.form.get('productPrice')
        product_category = request.form.get('productCategory')

        if not all([product_name, product_description, product_price, product_category]):
            return "Please fill in all the form fields."

        fakestore_api_url = "https://fakestoreapi.com/products"
         # Convert binary image data to Base64
        #image_data_base64 = base64.b64encode(product_image.read()).decode('utf-8')
        dataId = GetAllProducts()
        productId = set(product["id"] for product in dataId)
        l = len(productId)
        random_int = random.randint(100, 1000)
        random_rate = random.uniform(0.0, 5.0)
        image = "static/img/noimage.png"

        product_data = {
            'id': l + 1,
            'title': product_name,
            'price': float(product_price),
            'description': product_description,
            'category': product_category,
            'image': image,
            'rating': {'rate':random_rate,'count':random_int}  
        }
        headers = {'Content-Type': 'application/json'}
        # Use requests.post (not request.post)
        response = requests.post(fakestore_api_url, data=json.dumps(product_data), headers=headers )
                # Check the response status and handle accordingly
        if response.status_code == 201:
            # Successful upload, redirect or provide feedback
            return "Upload successful"
        else:
            # Handle the case where the upload failed
            return "Upload failed."

     MyData = GetAllProducts()
     l = len(MyData)
     categories = set(product["category"] for product in MyData)
     sortedCategory = sorted(categories)
     categories_count = {}
     for product in MyData:
        category = product["category"]
        categories_count[category] = categories_count.get(category, 0) + 1
     return render_template('products/new-product.html', products = MyData, categories=sortedCategory, pocetProduktu = categories_count)
"""