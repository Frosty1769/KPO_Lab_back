from flask import Blueprint, request
from flask_restx import Api, Resource 
from db_actions.products import (
    add_product, 
    get_all_products, 
    get_product_by_article,
    process_sale,
    delete_product
)

bp = Blueprint("products", __name__)
api = Api(bp, default="products", default_label="Управление товарами")


class ProductAdd(Resource):
    """Добавление товара или увеличение количества (только админ)"""
    def post(self):
        data = request.json
        article = data.get('article')
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity', 0)
        
        return add_product(article, name, price, quantity)


class ProductList(Resource):
    """Получение списка всех товаров"""
    def get(self):
        return get_all_products()


class ProductByArticle(Resource):
    """Получение товара по артикулу"""
    def get(self, article):
        return get_product_by_article(article)


class ProductDelete(Resource):
    """Удаление товара (только админ)"""
    def delete(self, article):
        return delete_product(article)


class Sale(Resource):
    """Обработка продажи товаров"""
    def post(self):
        data = request.json
        items = data.get('items', [])
        
        if not items:
            return {"status": "error", "message": "Список товаров пуст"}
        
        return process_sale(items)


api.add_resource(ProductAdd, "/add")
api.add_resource(ProductList, "/list")
api.add_resource(ProductByArticle, "/article/<string:article>")
api.add_resource(ProductDelete, "/delete/<string:article>")
api.add_resource(Sale, "/sale")
