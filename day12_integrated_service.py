import pandas as pd  # 🟢 ADD THIS LINE
import os, csv, time
from flask import Flask, jsonify, request
from datetime import datetime
import os, csv, time
from flask import Flask, jsonify, request
from datetime import datetime

# 🟢 FIX 1: Define 'app' at the top level
app = Flask(__name__)

# --- Institutional Config ---
LOG_FILE = 'live_trading_logs.csv'
TRADE_ACTIVE = False  
BUY_PRICE = 0

def record_trade(action, price, confidence, rsi):
    global TRADE_ACTIVE, BUY_PRICE
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Timestamp', 'Action', 'Price', 'Confidence', 'RSI'])
        if not file_exists: writer.writeheader()
        writer.writerow({
            'Timestamp': datetime.now().strftime('%H:%M:%S'),
            'Action': action,
            'Price': f"{price:.2f}",
            'Confidence': f"{confidence:.2f}%",
            'RSI': f"{rsi:.2f}"
        })
    if action == "BUY": 
        TRADE_ACTIVE = True
        BUY_PRICE = price
    elif action == "SELL": 
        TRADE_ACTIVE = False

# 🟢 FIX 2: Initialize log so Dashboard works immediately
def initialize_system():
    global TRADE_ACTIVE, BUY_PRICE
    if os.path.isfile(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        if not df.empty:
            # Check the very last action in the log
            last_action = df.iloc[-1]['Action']
            if last_action == "BUY" or (last_action == "PULSE" and "BUY" in df['Action'].values):
                # If the last real trade was a BUY, we are still active!
                TRADE_ACTIVE = True
                buys = df[df['Action'] == 'BUY']
                BUY_PRICE = float(buys.iloc[-1]['Price'])
                print(f"🔄 [RECOVERY] Detected Active Trade! Entry: ${BUY_PRICE}")

@app.route('/live_signal', methods=['GET'])
def live_signal():
    global TRADE_ACTIVE, BUY_PRICE
    try:
        rsi_1m = float(request.args.get('rsi_1m', 50.0))
        price_now = float(request.args.get('price', 0.0))
        
        # 🟢 Restore your preferred Aggressive Confidence
        if rsi_1m < 55:
            ai_conf = 50.0 + (55 - rsi_1m) * 1.2 
        else:
            ai_conf = 50.0
            
        ai_conf = round(max(0, min(100, ai_conf)), 2)
            
        # --- SIGNAL DECISION LOGIC ---
        signal = "HOLD"  # Default status
        
        # 1. SELL Logic (Exit when RSI is high or Stop-Loss is hit)
# 🟢 SELL LOGIC (Exit for Profit)
        if TRADE_ACTIVE and rsi_1m > 65:
            signal = "SELL"
            record_trade("SELL", price_now, ai_conf, rsi_1m)
            print(f"💰 [PROFIT] Closing trade at ${price_now:,.2f} | RSI: {rsi_1m:.2f}")
        
        # 2. BUY Logic (Enter when Confidence is high and not in a trade)
        elif not TRADE_ACTIVE and ai_conf > 62.0:
            signal = "BUY"
            record_trade("BUY", price_now, ai_conf, rsi_1m)

        # 🟢 DYNAMIC CONSOLE LOG
        # This gives you the exact line you requested
        status_icon = "🟢" if TRADE_ACTIVE else "⚪"
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {status_icon} RSI: {rsi_1m:.2f} | Conf: {ai_conf}% | Signal: {signal} | Price: ${price_now:,.2f}")

        # Keep the Dashboard alive
        record_trade("PULSE", price_now, ai_conf, rsi_1m)

        return jsonify({'status': 'success', 'signal': signal, 'confidence': ai_conf})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
if __name__ == '__main__':
    initialize_system()
    print("🚀 EXPERT BRAIN ONLINE | NO-LAG MODE")
    # 🟢 FIX 4: Ensure app.run is inside the main block
    app.run(port=5000, threaded=True, debug=False)