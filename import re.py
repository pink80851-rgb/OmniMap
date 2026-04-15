import re

def extract_port_number(item_name):
    # 1. 先排除掉我們不要的虛擬埠
    if any(x in item_name.lower() for x in ["ch", "null", "vlan"]):
        return None

    # 2. 核心正則：支援 Interface 1, Interface g1, Interface g1(FAE)
    match = re.search(r"Interface\s*g?(\d+)", item_name, re.IGNORECASE)
    
    if match:
        return match.group(1)
    return None

# --- 👇 請加上這段測試代碼 ---
# 我們把剛才 Log 裡看到的幾種格式丟進去測試
test_data = [
    "Interface 1(): Operational status",
    "Interface g1(): Operational status",
    "Interface g1(FAE Room): Operational status",
    "Interface ch1(): Operational status"
]

print("--- 測試開始 ---")
for text in test_data:
    result = extract_port_number(text)
    print(f"原始資料: {text}")
    print(f"抓取結果: {result}")
    print("-" * 20)