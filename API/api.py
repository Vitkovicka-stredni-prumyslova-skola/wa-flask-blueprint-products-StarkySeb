from flask import Blueprint, render_template
import requests

import json


api_bp = Blueprint('api_bp', __name__,
    template_folder='templates',
    static_folder='static')
URL_API = "https://fakestoreapi.com"

#Načte  seznam produktů z API v JSON formátu a vrátí jej jako pole.
def GetAllProducts():   
    
    request = requests.get(f"{URL_API}/products")
    
    return json.loads(request.text)
def GetAllProductsCategory(category):   
    
    request = requests.get(f"{URL_API}/products")
    
    return json.loads(request.text)

#Načte  seznam produktů z API v JSON formátu a vrátí jej jako pole.
def GetSingleProducts(id):   
    
    request = requests.get(f"{URL_API}/products/" + str(id))
    
    return json.loads(request.text)


 
    

