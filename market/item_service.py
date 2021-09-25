from market.models import Item
from market import db
from random import getrandbits

def check_exist(item):
    return Item.query.filter_by(name=item.name).first()

def check_barcode_exist(barcode):
    return Item.query.filter_by(barcode=barcode).first()

def add_item(item):
    new_item = Item(name=item.name.data, barcode=item.barcode.data, description=item.description.data, price=int(item.price.data))
    db.session.add(new_item)
    db.session.commit()

def generate_barcode():
    barcode = str(getrandbits(40))
    while check_barcode_exist(barcode):
        barcode = str(getrandbits(40))
    return barcode
