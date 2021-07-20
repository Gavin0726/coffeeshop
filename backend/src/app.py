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

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')

def retrieve_drinks():
    
    selection = Drink.query.order_by(Drink.id).all()

    drinks = [drink.short() for drink in selection]

    return jsonify({
        'success': True,
        'drinks': drinks,
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drinks_detail(payload):
    
    selection = Drink.query.order_by(Drink.id).all()

    drinks = [drink.long() for drink in selection]

    return jsonify({
        'success': True,
        'drinks': drinks,
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
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

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
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


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
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
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
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

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(ex):
    return jsonify({
    "success": False,
    "error": ex.status_code,
    "message": ex.error['code']
    }),  ex.status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) # specify port=5000