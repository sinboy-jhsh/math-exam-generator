# 國高中數學科 108 課綱素養命題與自動化產卷技能 (jhsh-math-exam-generator)

本技能 (Skill) 專門用於指導 Google Antigravity 等 AI 代理人進行國高中數學科段考自動化命題，生成符合「新北市立錦和高級中學」試務組規範、**教育部《十二年國民基本教育課程綱要—數學領域（108 課綱）》**與 PISA 數學推論架構的正式**四大獨立檔案**：試題卷、答案卷、答案與詳細解析卷與命題審題檢核表。

---

## ✨ 核心亮點與校方試務組規範全面實作

1. **產出 4 份獨立標準 Word 檔案**：
   - 檔名統一格式：`[學年度][上/下][國/高][年級][科目]段[次][試題/答案卷/答案與詳細解析/命題審題檢核表].docx`（例如：`115上國九數學段三試題.docx`、`115上國九數學段三答案卷.docx`）。
2. **試題卷純粹化排版**：
   - 試題卷上**完全取消填充題作答欄與非選擇題作答區**（學生一律於獨立答案卷作答），全卷徹底刪除「作答欄」、「作答區」贅字。
   - **題號靠左凸排**（`left_indent = 0.28 inch, first_line_indent = -0.28 inch`）。
   - 每題出題範圍小括號靠右對齊且**取消加粗體**（`bold=False`）。
   - 填充題題號比照選擇題使用 `1.`～`10.`（**不使用小括號**）；題幹挖空處使用乾淨底線 `____________`。
3. **獨立單頁 A4 答案卷（比照解析卷格式）**：
   - 卷頭完全比照解析卷格式（粗體加底線抬頭、命題範圍、姓名座號橫線、紅字扣 5 分警語、黑色墨水筆作答扣總分 5 分警語）。
   - 選擇題 2×10 表格、填充題 4×5 表格、非選題 2×2 表格（預留 11～12 行空白手寫高度）。
   - 全卷**剛好 1 整頁 A4 不跨頁**，垂直佔比約 82%～86%，單張收卷省紙有效率。
4. **文繞圖「上及下」與頂點字母白色圓形遮罩 (`bbox`) 防撞字**：
   - 圖形獨立置中一段（寬度 1.55～1.75 吋），與圖名保持適當垂直距離（4pt 間距），絕不擠壓選項。
   - 頂點字母添加白色圓形遮罩：`bbox=dict(boxstyle='circle,pad=0.15', facecolor='white', edgecolor='none')`，徹底防止字母與線條、直角記號交會壓線。
5. **完整內建「教育部 108 數學課綱」與「7～12 年級防超綱紅線系統」**：
   - 涵蓋國中（`數-J`）與高中（`數S-U`）核心素養、學習表現（`n/s/g/a/f/d`）、學習內容（`N/S/G/A/F/D`）與會考 0~3 級分評分規準。
   - 嚴格攔截舊課綱超綱題型（如：7年級絕對值方程、8年級 $f(x)$ 符號、9年級一般式配方法與舊圓冪定理、10年級牛頓一次因式檢驗法）。
6. **Word 原生可編輯數學方程式 (OMML `<m:oMath>`)**：
   - 分式、根式、聯立方程、線段頂標 $\overline{AB}$ 皆為 Word 原生數學物件，點兩下即可直接修改。
7. **SymPy 符號運算 100% 自動驗算防錯機制**：
   - 每題寫入考卷前，強制以 Python `SymPy` 驗算代數解、幾何不等式與畢氏定理，杜絕無解題或矛盾題。
8. **內建腳本工具庫 (`scripts/`)**：
   - 內建 `exam_helpers.py`、`generate_figures.py`、`build_jinhe_115_exam.py` 與 `solutions_data.py`，支援模組化複用與一鍵產卷。

---

## 📦 如何安裝本技能

### 方式 A：全域安裝（推薦，所有專案與新對話皆可隨時調用）

#### 1. 在 Antigravity 對話框貼上一句話自動安裝（最推薦）：
```text
請幫我把這個 GitHub 倉庫安裝成全域 Skill：
https://github.com/geniefu/jhsh-math-exam-generator
並幫我檢查安裝所需的 Python 套件 (python-docx, matplotlib, numpy, sympy)
```

#### 2. 透過 Git 指令一鍵安裝（未來更新只需 `git pull`）：
- **Windows (PowerShell)**:
  ```powershell
  git clone https://github.com/geniefu/jhsh-math-exam-generator.git "$HOME\.gemini\config\skills\jhsh-math-exam-generator"
  ```
- **macOS / Linux**:
  ```bash
  git clone https://github.com/geniefu/jhsh-math-exam-generator.git ~/.gemini/config/skills/jhsh-math-exam-generator
  ```

#### 3. 手動解壓縮安裝：
將 `jhsh-math-exam-generator` 資料夾複製至個人全域設定目錄：
- **Windows**: `C:\Users\<使用者名稱>\.gemini\config\skills\jhsh-math-exam-generator\`
- **macOS / Linux**: `~/.gemini/config/skills/jhsh-math-exam-generator/`

---

## 🚀 快速開始：提詞範例 (Prompt)

安裝完成後，在對話框中輸入：

```text
請使用 jhsh-math-exam-generator 技能為我生成一份數學科段考試卷，規格參數如下：
1、年級與範圍：115學年度第一學期 國中部九年級 第3章 幾何與證明（3-1證明與推理、3-2三角形的外心、內心與重心）。
2、題型與配分：總分 100 分
   - 單選題：10 題，每題 4 分，共 40 分
   - 填充題：10 格，每格 4 分，共 40 分
   - 非選計算證明題：2 題，每題 10 分，共 20 分
3、難易度：難易適中（預估通過率約 65%）
4、格式：輸出成錦和高中排版規範的 4 份 Word (.docx) 檔（試題卷、答案卷、詳細解析卷、命題審題檢核表）。
```

---

## 🛠️ 環境依賴需求 (Dependencies)

```bash
pip install python-docx matplotlib numpy sympy
```
