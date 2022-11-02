from email import message
from pydoc import describe
from types import NotImplementedType
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_sqlalchemy import SQLAlchemy
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError






blp = Blueprint("Items", __name__, description = "Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # flask sqlAlchhemy gives us this query method
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id): 
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item has been deleted."}


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            # this will update if existing
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            # this will create from scratch (inluding store ID) if not existing
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


    
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()



    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,item_data):
        # turn data into keyword args with this ** notation
        item=ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the item.")


    
        return item, 201
