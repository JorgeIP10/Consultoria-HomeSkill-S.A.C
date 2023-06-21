from .models import ShoppingCart
from datetime import datetime

class ShopCart:
    def __init__(self, request) -> None:
        self.request = request
        self.user = request.user
        try:
            self.cartObject = ShoppingCart.objects.get(user=self.user)
            self.shopcart = self.cartObject.items
        except:
            self.cartObject = ShoppingCart.objects.create(user=self.user, items=[{'products': [], 'status': None}])
            self.shopcart = self.cartObject.items
    
    def add_product(self, product):
        on_shopcart = False
        if self.shopcart[-1]['status']:
            self.shopcart['products'] = [product]
        else:
            if self.shopcart[-1]['products']:
                for article in self.shopcart[-1]['products']:
                    if (product['id'] == article['id']):
                        on_shopcart = True
                        article["quantity"] += 1
                        break
                if not on_shopcart:
                    product["quantity"] = 1
                    self.shopcart[-1]['products'].append(product)
            else:
                product["quantity"] = 1
                self.shopcart[-1]['products'] = [product]
        
        self.save()

    def remove_product_unit(self, product_id):
        for article in self.shopcart[-1]['products']:
            if (product_id == article['id']):
                article["quantity"] -= 1
                break
        
        self.save()
    
    def remove_product(self, product_id):
        for article in self.shopcart[-1]['products']:
            if (product_id == article['id']):
                self.shopcart[-1]['products'].remove(article)
                break
        
        self.save()

    def quantity_products(self):
        total_products = 0
        for article in self.shopcart[-1]['products']:
            total_products += article["quantity"]

        return total_products
    
    def set_purchased(self):
        self.shopcart[-1]['status'] = {}
        self.shopcart[-1]['status']['purchased'] = True
        self.shopcart[-1]['status']['purchase_time'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.shopcart.append({'products': [], 'status': None})
        self.save()

    def save(self):
        self.cartObject.save()
    
    def clear(self):
        self.cartObject.items = [{'products': [], 'status': None}]
        self.cartObject.save()