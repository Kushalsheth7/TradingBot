from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import logging
from src.client import BinanceClient
from src.utils import logger, load_env_vars, validate_input
from src.market_orders import execute_market_order
from src.limit_orders import execute_limit_order
from src.advanced.stop_limit import execute_stop_limit_order
from src.advanced.oco import execute_oco_order

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Disable Flask's default request logging to keep logs clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Initialize Binance client
try:
    api_key, api_secret, use_testnet = load_env_vars()
    client = BinanceClient(api_key, api_secret, testnet=use_testnet)
except Exception as e:
    logger.error(f"Failed to initialize Binance client: {str(e)}")
    client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/place-order', methods=['POST'])
def place_order():
    if not client:
        return jsonify({
            'success': False,
            'error': 'Binance client not initialized. Check your .env file.'
        }), 500
    
    try:
        data = request.json
        symbol = data.get('symbol')
        side = data.get('side')
        order_type = data.get('type')
        quantity = float(data.get('quantity'))
        price = float(data.get('price')) if data.get('price') else None
        stop_price = float(data.get('stop_price')) if data.get('stop_price') else None
        stop_limit_price = float(data.get('stop_limit_price')) if data.get('stop_limit_price') else None
        
        logger.info(f"[WEB UI] User submitting {order_type} order for {symbol}")
        
        result = None
        
        if order_type == 'MARKET':
            result = execute_market_order(client, symbol, side, quantity)
        elif order_type == 'LIMIT':
            result = execute_limit_order(client, symbol, side, quantity, price)
        elif order_type == 'STOP_LIMIT':
            result = execute_stop_limit_order(client, symbol, side, quantity, price, stop_price)
        elif order_type == 'OCO':
            result = execute_oco_order(client, symbol, side, quantity, price, stop_price, stop_limit_price)
        
        if result:
            return jsonify({
                'success': True,
                'data': result
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Order execution failed. Check logs for details.'
            }), 400
            
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        if os.path.exists('bot.log'):
            with open('bot.log', 'r') as f:
                lines = f.readlines()
                # Return last 50 lines
                return jsonify({
                    'success': True,
                    'logs': lines[-50:]
                })
        else:
            return jsonify({
                'success': True,
                'logs': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
