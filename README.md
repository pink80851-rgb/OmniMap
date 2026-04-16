# 🌐 OmniMap
**A Real-time Network Observability & Physical Topology Mapping System**

OmniMap 是一個專為企業機房與辦公環境設計的網路觀測平台。它將 Zabbix 的邏輯監控數據，轉化為直觀的實體平面圖映射，旨在將故障排除的 MTTR (平均修復時間) 從分鐘級降低至秒級。

---

## 🚀 核心價值 (The Problem it Solves)
在傳統的 MIS 運作中，網路斷線排查往往受限於「實體佈線黑盒」。當 Zabbix 噴出一個 Port 下線告警時，工程師仍需翻找 Excel 或實體標籤來定位受影響的工位。

**OmniMap 透過以下方式解決此痛點：**
- **實時狀態映射**：自動從 Zabbix API 獲取 Port 狀態，並在平面圖上即時反映。
- **1:N 拓樸支援**：支援單一 Switch Port 映射至多個實體工位（如透過 HUB 串接）。
- **視覺化排雷**：提供拖拉式 UI，讓維運人員能自定義辦公室佈局。

## 🛠️ 技術棧 (Tech Stack)
- **Backend**: Python / Flask (輕量化高效服務)
- **Data Source**: Zabbix API (JSON-RPC)
- **Frontend**: Vanilla JavaScript / CSS Grid / SVG
- **Security**: `.env` 環境變數分離、Regex 數據清洗與標準化

## 📂 專案結構 (Architecture)
```text
OmniMap/
├── app.py              # Flask 主程式 (Controller)
├── data_provider.py    # 數據供應層 (Zabbix Integration)
├── data/
│   └── layout.json     # 實體座標與 1:N 關係儲存
├── templates/
│   └── index.html      # 平面圖畫布
├── static/
│   └── js/             # 拖拉邏輯與 1:N 渲染
└── .env                # 敏感配置 (隱藏)
⚙️ 快速啟動 (Quick Start)
環境配置: 複製 .env.example 並更名為 .env，填入你的 Zabbix URL 與 Token。

安裝依賴: pip install -r requirements.txt

執行: python app.py

📈 未來路線 (Roadmap)
[ ] 支援原生 SNMP 直接抓取 (SNMP Provider)

[ ] 歷史斷線軌跡重播功能

[ ] 結合資產管理系統 (CMDB) 自動匯入備註
