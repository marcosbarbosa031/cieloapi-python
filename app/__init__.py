from flask import Flask, jsonify, request, abort
from config import app_config
from cielo.creditcard import Creditcard

def create_app(config_name):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_object(app_config[config_name])
  app.config.from_pyfile('config.py')

  @app.route('/')
  def index():
    return "Cielo API 3.0"
  
  @app.route('/creditcard', methods=['POST', 'PUT'])
  def creditcard():
    if not request.json:
      return abort(500)
    value = request.json.get('value')
    order_id = request.json.get('order_id')
    name = request.json.get('name')
    cvc = request.json.get('cvc')
    brand = request.json.get('brand')
    expr_date = request.json.get('expr_date')
    card_n = request.json.get('card_n')
    card_holder = request.json.get('card_holder')

    c = Creditcard(value, order_id, name, cvc, brand, expr_date, card_n, card_holder)
    response = c.createTransaction()
    return jsonify(response)

  return app
