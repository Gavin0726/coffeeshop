import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

## ROUTES
@app.route('/drinks')

def retrieve_drinks():
    
    selection = Drink.query.order_by(Drink.id).all()

    drinks = [drink.short() for drink in selection]

    return jsonify({
        'success': True,
        'drinks': drinks,
    })

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drinks_detail(payload):
    
    selection = Drink.query.order_by(Drink.id).all()

    drinks = [drink.long() for drink in selection]

    return jsonify({
        'success': True,
        'drinks': drinks,
    })

@app.route('/drinks', methods=['POST'])
# @cross_origin()
@requires_auth('post:drinks')
def create_drink(payload):

    body = request.get_json()

    new_title = body.get('title', None)
    recipe_dict = body.get('recipe', None)

    new_recipe = json.dumps(recipe_dict)
    try:
        drink = Drink(
                        title=new_title,
                        recipe=new_recipe,
                        )
        drink.insert()

        selection = Drink.query.filter(Drink.id == drink.id)

        drink = [drink.long() for drink in selection]

        return jsonify({
            'success': True,
            'drinks': drink,
        })

    except BaseException:
        abort(422)

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload,drink_id):
    print(drink_id)
    body = request.get_json()

    update_title = body.get('title', None)
    update_recipe = json.dumps((body.get('recipe', None)))

    try:
        drink = Drink.query.filter(Drink.id == drink_id) \
                .one_or_none()

        if drink is None:
            abort(404)
        print(drink)   
        drink.title = update_title
        drink.recipe = update_recipe
        drink.update()

        selection = Drink.query.filter(Drink.id == drink.id)

        drink = [drink.long() for drink in selection]

        return jsonify({
            'success': True,
            'drinks': drink
        })

    except BaseException:
        abort(400)

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):

        try:
            drink = Drink.query.filter(Drink.id == drink_id) \
                    .one_or_none()

            if drink is None:
                abort(404)

            drink.delete()

            return jsonify({
                'success': True,
                'delete': drink.id
            })

        except BaseException:
            abort(400)

## Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "server error"
    }), 500

@app.errorhandler(AuthError)
def auth_error(ex):
    return jsonify({
    "success": False,
    "error": ex.status_code,
    "message": ex.error['code']
    }),  ex.status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) # specify port=5000