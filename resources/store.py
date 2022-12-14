from pydoc import describe
from sqlite3 import IntegrityError
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError



blp = Blueprint("stores", __name__, description = "Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
        #below is kind of a stub
        # raise NotImplementedError("Deleting an item is not implemented")

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store deleted."}




@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # return {"stores": list(stores.values())}
        return StoreModel.query.all()
        # return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
    # turn data into keyword args with this ** notation
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the store.")
 
        return store, 201