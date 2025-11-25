# Setup IDE Integration

Hướng dẫn cài đặt và sử dụng header templates trong VS Code và IntelliJ IDEA.

## VS Code Setup

### Cách 1: Sử dụng Snippets (Khuyến nghị)

1. **Snippets đã được tạo sẵn** trong `.vscode/header.code-snippets`

2. **Sử dụng snippets**:
   - Mở file mới hoặc file cần thêm header
   - Gõ prefix: `header-py`, `header-js`, `header-java`, `header-cpp`, `header-html`, `header-css`, `header-php`
   - Chọn snippet từ dropdown
   - Tab qua các placeholders để điền thông tin

3. **Available snippets**:
   - `header-py` - Python files
   - `header-js` - JavaScript/TypeScript files
   - `header-java` - Java files
   - `header-cpp` - C/C++ files
   - `header-html` - HTML files
   - `header-css` - CSS files
   - `header-php` - PHP files

### Cách 2: Sử dụng Extension "File Header"

1. **Cài đặt extension**:
   - Mở VS Code
   - Vào Extensions (Ctrl+Shift+X)
   - Tìm "File Header" hoặc "Header Comments"
   - Cài đặt extension

2. **Cấu hình extension**:
   - Mở Settings (Ctrl+,)
   - Tìm "fileheader"
   - Cấu hình theo hướng dẫn của extension
   - Hoặc sử dụng settings trong `.vscode/settings.json`

3. **Sử dụng**:
   - Extension sẽ tự động thêm header khi tạo file mới
   - Hoặc dùng command: `File Header: Insert Header`

### Cách 3: Sử dụng Task (Tự động thêm header)

1. **Tạo task** trong `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Add Header",
      "type": "shell",
      "command": "python",
      "args": ["scripts/add-header.py", "${file}"],
      "problemMatcher": []
    }
  ]
}
```

2. **Sử dụng**:
   - Mở Command Palette (Ctrl+Shift+P)
   - Chọn "Tasks: Run Task"
   - Chọn "Add Header"

## IntelliJ IDEA Setup

### Cách 1: Import File Templates (Khuyến nghị)

1. **Templates đã được tạo sẵn** trong `.idea/fileTemplates/`

2. **Import templates**:
   - Mở IntelliJ IDEA
   - Vào **File** > **Settings** (Ctrl+Alt+S)
   - Vào **Editor** > **File and Code Templates**
   - Click **Import** button
   - Chọn thư mục `.idea/fileTemplates/` từ project
   - Hoặc copy templates thủ công vào:
     - Windows: `%USERPROFILE%\.IntelliJIdea<version>\config\fileTemplates\`
     - Mac/Linux: `~/.IntelliJIdea<version>/config/fileTemplates/`

3. **Sử dụng**:
   - Tạo file mới: **File** > **New** > **Python File** (hoặc file type khác)
   - Header sẽ tự động được thêm vào

### Cách 2: Tạo Templates Thủ Công

1. **Vào Settings**:
   - **File** > **Settings** > **Editor** > **File and Code Templates**

2. **Tạo template mới**:
   - Click **+** để tạo template mới
   - Đặt tên: "Python Script with Header"
   - Extension: `py`
   - Copy nội dung từ `.idea/fileTemplates/code/Python Script.ft`

3. **Available variables**:
   - `${PROJECT_NAME}` - Tên project
   - `${YEAR}` - Năm hiện tại
   - `${FILE_HASH}` - Hash của file (cần custom)
   - `${PACKAGE_NAME}` - Package name (Java)
   - `${BODY}` - Nội dung file

### Cách 3: Sử dụng Live Templates

1. **Vào Settings**:
   - **File** > **Settings** > **Editor** > **Live Templates**

2. **Tạo template**:
   - Click **+** > **Live Template**
   - Abbreviation: `header-py` (hoặc tên khác)
   - Description: "Insert header for Python"
   - Template text: Copy từ snippet trong `.vscode/header.code-snippets`

3. **Sử dụng**:
   - Gõ `header-py` và nhấn Tab
   - Template sẽ được insert

## Customization

### Thay đổi Placeholders

Các templates sử dụng placeholders:
- `[CUSTOMER]` - Tên khách hàng
- `[PROJECT_CODE]` - Mã dự án
- `${unique_file_hash}` - Hash của file

Để tự động thay thế, bạn có thể:
1. Sử dụng script `add-header.py` sau khi tạo file
2. Cấu hình extension để tự động thay thế
3. Sử dụng macro hoặc script trong IDE

### Thêm Ngôn Ngữ Mới

**VS Code**:
1. Thêm snippet mới vào `.vscode/header.code-snippets`
2. Sử dụng comment syntax phù hợp

**IntelliJ IDEA**:
1. Tạo file template mới trong `.idea/fileTemplates/code/`
2. Sử dụng format: `Language Name.ft`
3. Import vào IntelliJ IDEA

## Best Practices

1. **Sử dụng snippets cho file mới**: Nhanh và linh hoạt
2. **Sử dụng templates cho auto-insert**: Tự động khi tạo file
3. **Kết hợp với scripts**: Sử dụng `add-header.py` để đảm bảo hash đúng
4. **Review trước khi commit**: Kiểm tra header đã đúng chưa

## Troubleshooting

### VS Code snippets không hiện

1. Kiểm tra file `.vscode/header.code-snippets` có trong project
2. Reload VS Code: **Ctrl+Shift+P** > "Reload Window"
3. Kiểm tra language mode đúng (ví dụ: Python cho `header-py`)

### IntelliJ templates không hoạt động

1. Kiểm tra templates đã được import
2. Kiểm tra file extension đúng
3. Restart IntelliJ IDEA
4. Kiểm tra template variables có đúng không

### Hash không được generate

- Snippets/templates không thể tự động generate hash
- Sử dụng script `add-header.py` sau khi tạo file để generate hash đúng
- Hoặc để trống và update sau

## Advanced: Auto-insert với Script

Có thể tạo macro hoặc script để tự động chạy `add-header.py` khi save file:

**VS Code** (với extension "Run on Save"):
```json
{
  "emeraldwalk.runonsave": {
    "commands": [
      {
        "match": "\\.(py|js|java|cpp|php)$",
        "cmd": "python ${workspaceFolder}/scripts/add-header.py ${file}"
      }
    ]
  }
}
```

**IntelliJ IDEA** (với File Watchers):
1. **Settings** > **Tools** > **File Watchers**
2. Tạo watcher mới
3. Program: `python`
4. Arguments: `scripts/add-header.py $FilePath$`
5. Trigger: On file save

---

**Lưu ý**: Templates và snippets chỉ insert header, không generate hash. Để có hash đúng, sử dụng script `add-header.py` sau khi tạo file.

