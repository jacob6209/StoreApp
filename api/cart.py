from django.contrib import messages
from django.utils.translation import gettext as _
from storeapp.models import Product

class Cart:
    def __init__(self, request):
        """
        Initialize the cart object
        """
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):
        """
        Add the specified product to the cart
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if replace_current_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)
            if self.cart[product_id]['quantity'] <=0:
                self.remove(product)

        messages.success(self.request, _("Product successfully added to cart"))
        self.save()

    def remove(self, product):
        """
        Remove the specified product from the cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, _("Product successfully removed from cart"))
            self.save()

    def clear(self):
        """
        Remove all items from the cart
        """
        del self.session['cart']
        self.save()

    def save(self):
        """
        Mark the session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and return the product objects
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        """
        Return the total number of items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Return the total price of all items in the cart
        """
        return sum(item['product_obj'].price * item['quantity'] for item in self.cart.values())

    def is_empty(self):
        """
        Check if the cart is empty
        """
        return not bool(self.cart)
