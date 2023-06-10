from .models import ShoppingCart

class ShopCart:
    def __init__(self, request) -> None:
        self.request = request
        self.user = request.user
        try:
            self.cartObject = ShoppingCart.objects.get(user=self.user)
            self.shopcart = self.cartObject.items
        except:
            self.cartObject = ShoppingCart.objects.create(user=self.user, items=[])
            self.shopcart = self.cartObject.items
    
    def add_product(self, product):
        on_shopcart = False
        if self.shopcart:
            for article in self.shopcart:
                if (product[0]['id'] == article[0]['id']):
                    on_shopcart = True
                    article[0]["quantity"] += 1
                    break
            if not on_shopcart:
                product[0]["quantity"] = 1
                self.shopcart.append(product)
        else:
            product[0]["quantity"] = 1
            self.shopcart.append(product)
        
        self.save()

    def remove_product_unit(self, product_id):
        for article in self.shopcart:
            if (product_id == article[0]['id']):
                article[0]["quantity"] -= 1
                break
        
        self.save()
    
    def remove_product(self, product_id):
        for article in self.shopcart:
            if (product_id == article[0]['id']):
                self.shopcart.remove(article)
                break
        
        self.save()

    def quantity_products(self):
        total_products = 0
        for product in self.shopcart:
            total_products += product[0]["quantity"]

        return total_products

    def save(self):
        self.cartObject.save()
    
    def clear(self):
        self.cartObject.delete()