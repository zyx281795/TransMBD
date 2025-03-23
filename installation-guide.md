# TransMbD 失智監護輔助系統安裝指南

本指南詳細說明如何在本地環境中安裝和部署 TransMbD 失智監護輔助系統，以便您可以進行演示和測試。

## 系統要求

- Python 3.9 或更高版本
- 至少 4GB 可用記憶體
- 至少 2GB 可用磁碟空間
- 支援的操作系統：Windows 10/11、macOS 10.15+、Ubuntu 20.04+

## 安裝步驟

### 1. 克隆或下載專案

您可以透過以下方式獲取專案代碼：

```bash
# 使用 Git 克隆（如果您有專案倉庫）
git clone https://github.com/Atypical281795/TransMBD.git
cd TransMBD

# 或者下載並解壓縮專案壓縮包
# 然後進入專案目錄
```

### 2. 使用自動安裝腳本

為了簡化安裝過程，我們提供了自動安裝腳本。根據您的操作系統選擇相應的腳本：

#### Windows 使用者

雙擊運行 `run_demo.bat` 檔案或在命令提示符中運行：

```cmd
run_demo.bat
```

#### macOS/Linux 使用者

在終端中運行：

```bash
chmod +x run_demo.sh  # 賦予腳本執行權限
./run_demo.sh
```

這些腳本將自動執行以下操作：
- 創建 Python 虛擬環境
- 安裝所需依賴
- 設置資料庫
- 創建演示管理員帳戶
- 加載演示數據
- 啟動開發伺服器

當腳本完成後，您可以透過瀏覽器訪問 [http://127.0.0.1:8000](http://127.0.0.1:8000) 來使用系統。

### 3. 手動安裝（如果自動腳本失敗）

如果自動安裝腳本失敗，您可以按照以下步驟手動安裝：

#### 3.1 創建和激活虛擬環境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3.2 安裝依賴

```bash
pip install -r requirements.txt
```

#### 3.3 初始化資料庫

```bash
python manage.py migrate
```

#### 3.4 創建管理員帳戶

```bash
python manage.py createsuperuser
```
按照提示輸入用戶名、電子郵件和密碼。

#### 3.5 啟動開發伺服器

```bash
python manage.py runserver
```

現在您可以透過瀏覽器訪問 [http://127.0.0.1:8000](http://127.0.0.1:8000) 來使用系統。

#### 其他指令1

您可以透過以下命令驗證資料庫表是否已正確創建：
```bash
python manage.py dbshell
```

#### 其他指令2

```bash
python manage.py makemigrations core
```

系統應該會顯示類似於以下內容的輸出：
```
Migrations for 'core':
  core/migrations/0001_initial.py
    - Create model Patient
    - Create model Conversation
    - Create model Message
    - Create model DementiaAssessment
```

## 登錄資訊

如果您使用自動安裝腳本，系統將創建一個默認的管理員帳戶：

- 用戶名：`admin`
- 密碼：`admin`

出於安全考慮，在實際部署中應立即更改此默認密碼。

## 使用說明

安裝完成後，您可以透過以下兩個主要介面使用系統：

1. **患者介面**：[http://127.0.0.1:8000/patient/](http://127.0.0.1:8000/patient/)
   - 提供對話互動功能，支持文本和模擬語音輸入
   - 系統會根據對話內容生成評估結果

2. **照護人員介面**：[http://127.0.0.1:8000/caregiver/](http://127.0.0.1:8000/caregiver/)
   - 需要登錄管理員帳戶
   - 提供患者管理、評估查看和數據分析功能

## 常見問題

1. **依賴項安裝失敗**
   
   如果某些依賴項安裝失敗，請嘗試更新 pip：
   ```bash
   pip install --upgrade pip
   ```
   然後重新嘗試安裝依賴項。

2. **資料庫遷移錯誤**
   
   如果遇到資料庫遷移錯誤，請嘗試刪除資料庫文件（db.sqlite3）並重新運行遷移：
   ```bash
   rm db.sqlite3  # 在 Windows 上使用 del db.sqlite3
   python manage.py migrate
   ```

3. **伺服器啟動失敗**
   
   如果開發伺服器無法啟動，請檢查端口 8000 是否被佔用。您可以透過以下命令使用不同的端口：
   ```bash
   python manage.py runserver 8080
   ```
   然後訪問 [http://127.0.0.1:8080](http://127.0.0.1:8080)。

## 更多幫助

如需進一步的幫助或遇到其他問題，請參閱專案文檔或聯繫我。