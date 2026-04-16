✨ 新增功能 (Features)
Zabbix API 整合：透過 JSON-RPC 實時獲取 Switch Port 狀態（Up/Down）。

環境變數解耦：導入 .env 管理機制，分離敏感資訊（URL, Token）與程式碼。

核心數據清洗：實作 get_standardized_network_data 邏輯，利用 Regex 精準解析 Port 備註與編號。

基礎 UI 框架：建立基於 Flask 的 Web 介面，支援地圖畫布的初步顯示。

🛠️ 工程優化 (Engineering)
模組化設計：將 API 調用與資料清洗邏輯分離，降低系統耦合度。

安全性提升：加入 .gitignore 防止私密金鑰洩漏至公共倉庫。
