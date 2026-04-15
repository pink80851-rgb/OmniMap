import requests
import json
import re

# --- 配置區 ---
ZABBIX_URL = "http://192.168.1.101/zabbix/api_jsonrpc.php"
AUTH_TOKEN = "a676b9e0cdb150cf26a4f8d0fa5bce63f18b6db2f14d020b2d396ba589b2cb53"

def get_cleaned_switch_data(host_id):
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
        response = requests.post(ZABBIX_URL, json=payload)
        items = response.json().get('result', [])
        
        final_data = {}
        for item in items:
            raw_name = item['name']
            # Regex 說明: 找 g 後面的數字，並選取括號內的所有內容
            # 例如: "Interface g17(2C-02)" -> 17, 2C-02
            match = re.search(r'g(\d+)(?:\((.*?)\))?', raw_name)
            
            if match:
                port_num = match.group(1)   # 17
                note = match.group(2) if match.group(2) else "" # 2C-02
                
                final_data[port_num] = {
                    "status": "Up" if item['lastvalue'] == "1" else "Down",
                    "note": note,
                    "full_name": raw_name.split(':')[0]
                }
        
        return final_data

    except Exception as e:
        return {"error": str(e)}

# --- 執行測試 ---
target_host = "10708"
result = get_cleaned_switch_data(target_host)

# 印出漂亮的結果供前端參考
print(f"--- Host {target_host} 清洗後的資料 ---")
print(json.dumps(result, indent=4, ensure_ascii=False))