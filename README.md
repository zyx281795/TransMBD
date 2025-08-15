# TransMbD 失智監護輔助系統

## 項目簡介

TransMbD（Transformer Mistral 7B based on Dementia）是一個基於大型語言模型的失智症監護輔助系統。該系統旨在利用人工智慧技術輔助醫護人員觀察患者並判定失智症嚴重程度，同時透過對話引導的方式與患者互動，持續收集和分析文本數據以評估症狀變化趨勢。

## 功能特點

- **患者互動介面**：提供簡潔友好的對話介面，支持文本和語音輸入
- **照護人員儀表板**：展示患者狀態評估和失智症嚴重程度預測結果
- **失智症進展預測**：基於患者輸入的文本內容分析失智症症狀變化趨勢
- **引導式對話**：透過智能對話引導患者持續提供有價值的文本信息
- **數據可視化**：將預測結果以直觀的圖表形式展示

## 技術架構

- 前端：HTML, CSS, JavaScript, Bootstrap
- 後端：Django (Python)
- 模型：基於Mistral 7B的大型語言模型
- 數據存儲：SQLite (開發環境)
- 可視化：Plotly, Matplotlib

## 快速開始

### 環境要求

- Python 3.9+
- pip package manager

### 安裝步驟

1. 克隆項目倉庫
   ```bash
   git clone https://github.com/your-username/transmbd-project.git
   cd transmbd-project
   ```

2. 創建虛擬環境並激活
   ```bash
   python -m venv venv
   source venv/bin/activate  # 在Windows上使用: venv\Scripts\activate
   ```

3. 安裝依賴包
   ```bash
   pip install -r requirements.txt
   ```

4. 初始化數據庫
   ```bash
   python manage.py migrate
   ```

5. 創建超級用戶（可選）
   ```bash
   python manage.py createsuperuser
   ```

6. 啟動開發伺服器
   ```bash
   python manage.py runserver
   ```

7. 訪問系統
   - 患者介面: http://127.0.0.1:8000/patient/
   - 照護人員儀表板: http://127.0.0.1:8000/caregiver/
   - 管理介面: http://127.0.0.1:8000/admin/

## 使用示例

### 患者介面

1. 訪問患者介面
2. 通過文本框或語音輸入功能與系統互動
3. 系統會根據輸入內容生成回覆，並引導繼續對話

### 照護人員儀表板

1. 登錄照護人員帳戶
2. 查看患者列表及其預測的失智症嚴重程度
3. 點擊具體患者查看詳細分析報告和歷史對話記錄
4. 導出數據進行進一步分析

## 項目團隊

- 開發者：張詠翔
- 指導教授：陳碩聰
---

Let me know if you need any further adjustments!
