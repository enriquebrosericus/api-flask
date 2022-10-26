import uuid
from flask import Flask, request
from db import items, stores

app = Flask(__name__)




# flask route

# get em all
@app.get("/store")
def get_stores():
    # have to convert to a list here
    return {"stores": list(stores.values())}

#data for 1 store
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message":"Store not found"}, 404




# retrieve a single item
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message":"Item not found"}, 404

        




@app.post("/store")
def create_store():
    store_data = request.get_json()
    # make a uuid or autoincrementer
    store_id = uuid.uuid4().hex

    # passing keyword args to constructor
    store = {**store_data, "id":store_id}
    stores[store_id] = store

    return store, 201



@app.post("/item")
def create_item(name):
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    # assume we have received the expected payload
    item_id = uuid.uuid4().hex
    item = {**item_data, "id":item_id}
    items[item_id] = item
    return item, 201


@app.get("/item")
def get_all_items():
    # have to convert to a list here
    return {"items": list(items.values())}

