import os
import re
import requests
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()

app = Flask(__name__)

# --- 讀取環境變數 ---
ZABBIX_URL = os.getenv("ZABBIX_URL")
AUTH_TOKEN = os.getenv("ZABBIX_TOKEN")

# ==========================================
# 數據獲取層 (Integration Layer)
# ==========================================
def fetch_raw_zabbix_items(host_id):
    """只負責打 API 拿原始資料，不做任何邏輯處理"""
    payload = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "hostids": host_id,
            "search": { "key_": "ifOperStatus" },
            "output": ["name", "lastvalue", "key_"]
        },
        "id": 1,
        "auth": AUTH_TOKEN
    }
    try:
        response = requests.post(ZABBIX_URL, json=payload, timeout=5)
        response.raise_for_status()
        return response.json().get('result', [])
    except Exception as e:
        print(f"Zabbix Connection Error: {e}")
        return []

# ==========================================
# 數據清洗層 (Service Layer / Normalizer)
# ==========================================
def get_standardized_network_data(host_id):
    """
    負責將原始數據『洗』成我們系統認可的標準格式。
    這就是解耦的核心：未來換掉 Zabbix，只要這份 Function 回傳的格式不變，UI 就不會壞。
    """
    raw_items = fetch_raw_zabbix_items(host_id)
    final_data = {}
    
    for item in raw_items:
        raw_name = item['name']
        
        # 1. 提取備註 (Note)
        note_match = re.search(r'\((.*?)\)', raw_name)
        note = note_match.group(1) if note_match else ""
        
        # 2. 提取 Port 數字 (Logic)
        port_match = re.search(r'(\d+)(?:\s*\(|:|$)', raw_name)
        
        if port_match:
            port_num = port_match.group(1)
            # 限制合理範圍
            if 1 <= int(port_num) <= 52:
                # 定義我們的 Canonical Model (標準資料模型)
                final_data[port_num] = {
                    "status": "Up" if item['lastvalue'] == "1" else "Down",
                    "note": note,
                    "raw_name": raw_name  # 保留原始資訊供 Debug
                }
    
    total_count = max([int(k) for k in final_data.keys()]) if final_data else 0
    
    return {
        "ports_data": final_data,
        "total_count": total_count,
        "source": "Zabbix" # 標註來源，方便未來做多來源整合
    }

# ==========================================
# 路由控制層 (Controller Layer)
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/switch/<host_id>')
def get_switch(host_id):
    # 這裡只管呼叫『清洗層』
    data = get_standardized_network_data(host_id)
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)