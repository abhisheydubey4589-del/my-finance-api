
from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/get-stock', methods=['GET'])
def get_stock():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Stock symbol missing"}), 400
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if data.empty:
            return jsonify({"error": "No data found"}), 404
        current_price = data['Close'].iloc[-1]
        return jsonify({
            "symbol": symbol.upper(),
            "price": round(current_price, 2),
            "currency": stock.info.get('currency', 'USD')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
