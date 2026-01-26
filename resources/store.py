import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blb = Blueprint('store', __name__, description='Operations on store')

@blb.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store with that id does not exist.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found.")

@blb.route('/store')
class StoreList(MethodView):
    def get(self):
        return {"items": list(stores.values())}

    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(400,
                  message="Bad request: Ensure 'name' is included in JSON payload")

        for store in stores.values():
            if (
                    store_data["name"] == store["name"]):
                abort(400, message=f"Store already exits")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store