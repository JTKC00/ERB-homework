# 會議資料整理系統 (Meeting Document Management System)

一個基於 Django 的會議資料管理系統，提供完整的會議記錄、議程管理、附件處理以及資料匯入匯出功能。

## 功能特色

### 🎯 核心功能
- **會議管理**：創建、編輯、查看、刪除會議記錄，支援網頁即時編輯
- **議程管理**：為每個會議添加詳細議程項目，支援網頁即時編輯與拖拉排序
- **附件管理**：上傳和管理會議相關文件（支援 TXT、CSV、PPT、Word、Excel 等）
- **搜索過濾**：根據標題、參加人、日期、地點等條件搜索會議
- **分頁顯示**：每頁顯示 15 筆記錄，支援分頁瀏覽

### 📤 匯出功能
- **ZIP 格式匯出**：將會議資料和所有附件打包下載
- **CSV 格式**：包含完整的會議、議程、附件資訊
- **Word 文件生成**：為單個會議生成完整的 Word 文件包

### 📥 匯入功能
- **ZIP 檔案匯入**：支援完整的資料和附件還原
- **CSV 檔案匯入**：純會議資料匯入
- **智能檔案對應**：自動根據檔名對應附件檔案

### 🌐 多語言支援
- 支援繁體中文、簡體中文、英文
- 可生成不同語言的測試資料

## 系統需求

- Python 3.8+
- Django 4.x
- 相關套件請參考 `requirements.txt`

## 安裝指南

### 1. 克隆專案
```bash
git clone <repository-url>
cd doc_management
```

### 2. 建立虛擬環境
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
```

### 3. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 4. 資料庫設定
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 創建超級用戶
```bash
python manage.py createsuperuser
```

### 6. 啟動開發伺服器
```bash
python manage.py runserver
```

### 7. 快速開始（可選）
```bash
# 生成一些測試資料
python manage.py generate_fake_data --num_meetings 10 --language all

# 訪問系統
# 主頁: http://127.0.0.1:8000/
# 管理後台: http://127.0.0.1:8000/admin/
```

## 使用指南

### 🏠 首頁功能
訪問 `http://127.0.0.1:8000/` 查看：
- 最近會議列表
- 快速匯出/匯入功能
- 管理後台連結

### 📝 會議管理

#### 新增/編輯會議
1. 進入管理後台 `/admin/` 或在會議詳情頁點擊「編輯」按鈕
2. 填寫或修改會議資訊：
   - 標題（最大 200 字元）
   - 日期和時間
   - 地點（最大 100 字元）
   - 參加人員
   - 會議記錄
3. 儲存後即可在列表或詳情頁看到更新內容

#### 查看會議列表
訪問 `/meetings/` 查看所有會議，支援：
- **搜索**：根據標題或參加人搜索
- **過濾**：按日期或地點過濾
- **排序**：按日期或標題排序
- **批量刪除**：選擇多個會議進行刪除

#### 會議詳情
點擊會議標題查看詳細資訊：
- 完整會議資訊
- 議程項目列表
- 附件列表
- 相關操作按鈕

### 📋 議程管理
在管理後台添加議程項目，或於會議詳情頁即時編輯：
1. 選擇「Agenda items」→「Add」或在會議詳情頁點擊「編輯」按鈕
2. 選擇關聯的會議
3. 填寫或修改：
   - 議程標題（最大 200 字元）
   - 詳細描述
   - 負責人（最大 100 字元）
   - 預估時間

#### 議程排序（拖拉調整項次）
- 在會議詳情頁面，議程以表格方式顯示，左側有拖拉手柄（≡）。
- 直接拖拉議程行即可調整順序，系統會自動更新項次（item_number），避免重複與不連續。
- 不可直接編輯項次欄位。
- 可於每一議程行點擊「編輯」按鈕即時修改內容。

### 📎 附件管理

#### 上傳附件
1. 在會議詳情頁面點擊「上傳新附件」
2. 選擇檔案（支援各種格式）
3. 系統自動生成有意義的檔名：`日期_會議標題_原檔名`

#### 下載附件
在會議詳情頁面點擊附件連結即可下載

### 📤 資料匯出

#### ZIP 格式匯出
1. 在首頁點擊「導出會議 (ZIP)」
2. 下載包含以下內容的 ZIP 檔案：
   ```
   meetings_export.zip
   ├── meetings.csv          # 會議資料
   └── attachments/          # 所有附件檔案
       ├── file1.txt
       ├── file2.docx
       └── ...
   ```

#### 單個會議 Word 匯出
在會議詳情頁面點擊「生成 Word 文件」，下載包含：
- 會議記錄文件
- 議程文件  
- 附件列表文件

### 📥 資料匯入

#### ZIP 檔案匯入
1. 點擊「匯入會議 (ZIP/CSV)」
2. 選擇之前匯出的 ZIP 檔案
3. 系統自動：
   - 解析 `meetings.csv`
   - 還原會議資料
   - 重建議程項目
   - 對應附件檔案

#### CSV 檔案匯入
1. 準備符合格式的 CSV 檔案
2. 上傳 CSV 檔案
3. 系統匯入基本會議資料

### 🔧 管理功能

#### 生成測試資料
```bash
# 生成 5 個英文會議
python manage.py generate_fake_data --num_meetings 5 --language en

# 生成 10 個繁體中文會議
python manage.py generate_fake_data --num_meetings 10 --language tw

# 生成 8 個簡體中文會議
python manage.py generate_fake_data --num_meetings 8 --language zh

# 生成 12 個混合語言會議
python manage.py generate_fake_data --num_meetings 12 --language all
```

#### 清除所有會議
在會議列表頁面使用批量刪除功能

## 檔案結構

```
doc_management/
├── manage.py                    # Django 管理指令
├── doc_management/              # 專案設定
│   ├── settings.py             # 設定檔
│   ├── urls.py                 # 主路由
│   └── ...
├── meetings/                    # 會議應用
│   ├── models.py               # 資料模型
│   ├── views.py                # 視圖邏輯
│   ├── urls.py                 # 路由設定
│   ├── admin.py                # 管理後台
│   ├── resources.py            # 匯入匯出資源
│   └── management/commands/
│       └── generate_fake_data.py  # 測試資料生成
├── pages/                       # 頁面應用
├── templates/                   # 模板檔案
├── static/                      # 靜態檔案
├── media/                       # 媒體檔案
└── README.md                    # 說明文件
```

## 資料模型

### Meeting（會議）
- `title`: 會議標題（最大 200 字元）
- `date`: 會議日期
- `start_time/end_time`: 開始/結束時間
- `location`: 會議地點（最大 100 字元）
- `attendees`: 參加人員（文字欄位）
- `minutes`: 會議記錄（文字欄位，可為空）

### AgendaItem（議程項目）
- `meeting`: 關聯會議（外鍵）
- `item_number`: 項目編號
- `item_title`: 議程標題（最大 200 字元）
- `description`: 詳細描述（文字欄位）
- `responsible_person`: 負責人（最大 100 字元）
- `estimated_time`: 預估時間（時間間隔欄位）

### Attachment（附件）
- `meeting`: 關聯會議（外鍵）
- `file`: 檔案（上傳至 attachments/%Y/%m/%d/ 目錄）
- `uploaded_at`: 上傳時間（自動記錄）
- `file_type`: 檔案類型（最大 50 字元，可為空）

## 技術特色

- **智能檔名生成**：附件自動生成有意義的檔名
- **CSV 智能解析**：支援包含逗號的欄位正確解析
- **ZIP 完整匯出**：資料和檔案一次性打包
- **錯誤處理**：完善的異常處理機制
- **響應式設計**：支援各種螢幕尺寸

## 常見問題

### Q: 匯入時出現「檔案過大」錯誤？
A: 檢查 Django 的 `FILE_UPLOAD_MAX_MEMORY_SIZE` 設定，或將大檔案分批處理。

### Q: 附件無法下載？
A: 確認 `MEDIA_URL` 和 `MEDIA_ROOT` 設定正確，且檔案權限允許讀取。

### Q: CSV 匯入時中文亂碼？
A: 確保 CSV 檔案使用 UTF-8 編碼儲存。

### Q: 生成的假資料檔名看不懂？
A: 使用新版本的 `generate_fake_data` 指令，會產生包含日期和會議標題的有意義檔名。

## 版本資訊

- **版本**: 1.0.0
- **更新日期**: 2025年1月
- **開發者**: James Tong
- **框架**: Django 4.x + Python 3.8+
- **主要功能**: 
  - 會議資料 CRUD 操作
  - 智能附件檔名生成
  - ZIP/CSV 完整匯入匯出
  - 多語言假資料生成
  - 響應式網頁設計

## 授權條款

本專案採用 MIT 授權條款。

## 聯絡資訊

如有問題或建議，請聯絡：
- 開發者: James Tong
- 專案: HKCT ERB Django 會議管理系統
- 目的: 個人作業項目

## 特別鳴謝

感謝導師 Mr. Wai Lung Aaron 在本專案學習過程中的悉心指導與支持！

---

**注意**: 本系統為學習專案，建議在正式環境使用前進行充分測試和安全性檢查。建議在生產環境中添加用戶認證、權限管理和資料驗證等安全機制。
