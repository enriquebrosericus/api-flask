from flask import Flask, request

app = Flask(__name__)

# stores = [
#     {
#         "name": "My Store",
#         "items": [
#             {
#             "name": "Chair",
#             "price": 15.99
#             }
#         ]
#     }
# ]

stores = {}
item = {
    1: {
        "name":"Chair",
        "price":17.99
    },
    2: {
        "name":"Table",
        "price":180.50
    }
}


# flask route

# get em all
@app.get("/store")
def get_stores():
    return {"stores": stores}

#data for 1 store
@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
        return {"message":"Store not found"}, 404

# items in a particular store
@app.get("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        print(store["name"])
        if store["name"] == name:
            return {"items": store["items"]}
        return {"message":"Store not found"}, 404

        




@app.post("/store")
def create_stores():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201



@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item
    return {"message": "Store not found"}, 404

