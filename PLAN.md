# KẾ HOẠCH THIẾT LẬP HEADER CHUNG CHO CÁC FILE CODE

## 1. TỔNG QUAN YÊU CẦU

### 1.1. Mục tiêu
- Thiết lập header chuẩn cho tất cả các file code trong dự án
- Đảm bảo header được tự động thêm vào file mới
- Enforce header bắt buộc trước khi merge code
- Hỗ trợ nhiều ngôn ngữ lập trình

### 1.2. Format Header Mẫu
```
# ======================================================================================
# STRICTLY CONFIDENTIAL | DLP:OMI::STRICT
# ======================================================================================
# OWNERSHIP NOTICE:
# This source code is the proprietary property of [CUSTOMER].
# Developed by Ominext under MSA.
#
# COPYRIGHT (c) 2025 [CUSTOMER]. ALL RIGHTS RESERVED.
#
# WARNING: This file contains trade secrets and confidential information.
# Unauthorized copying or uploading to public networks  is prohibited.
#
# Project: [PROJECT_CODE]
# Trace ID: ${unique_file_hash}
# ======================================================================================
```

### 1.3. Các Thành Phần Cần Thiết
- **Template header** cho từng ngôn ngữ (comment syntax khác nhau)
- **IDE configuration** (VS Code, IntelliJ, etc.)
- **Pre-commit hooks** (kiểm tra local trước khi commit)
- **GitLab CI/CD pipeline** (kiểm tra server-side trước khi merge)
- **Script tự động** thêm header vào file mới
- **Script validation** kiểm tra header có tồn tại

---

## 2. PHÂN TÍCH CHI TIẾT

### 2.1. Các Ngôn Ngữ Cần Hỗ Trợ

**Danh sách ngôn ngữ được xác nhận**:
- **Python**: `# comment`
- **Bash**: `# comment`
- **Ruby**: `# comment`
- **Perl**: `# comment`
- **JavaScript**: `// comment` hoặc `/* comment */`
- **TypeScript**: `// comment` hoặc `/* comment */`
- **Java**: `// comment` hoặc `/* comment */`
- **C**: `// comment` hoặc `/* comment */`
- **C++**: `// comment` hoặc `/* comment */`
- **C#**: `// comment` hoặc `/* comment */`
- **Go**: `// comment` hoặc `/* comment */`
- **PHP**: `// comment` hoặc `/* comment */` hoặc `# comment`
- **HTML**: `<!-- comment -->`
- **CSS**: `/* comment */`
- **XML**: `<!-- comment -->`

**Có thể mở rộng thêm**: SQL, YAML, etc.

#### 2.1.1. Comment Syntax theo Ngôn Ngữ
- **Python, Bash, Ruby, Perl**: `# comment`
- **JavaScript, TypeScript, Java, C, C++, C#, Go**: `// comment` hoặc `/* comment */`
- **PHP**: `// comment` hoặc `/* comment */` hoặc `# comment`
- **HTML, XML**: `<!-- comment -->`
- **CSS**: `/* comment */`

#### 2.1.2. Template Header cho Từng Ngôn Ngữ
Cần tạo template riêng cho mỗi ngôn ngữ với comment syntax phù hợp.

### 2.2. Trace ID - File Hash
- **Yêu cầu**: `${unique_file_hash}` - hash duy nhất cho mỗi file
- **Phương án đã xác nhận**: Sử dụng hash của nội dung file (SHA256)
  - Hash được tính từ content của file
  - Đảm bảo unique cho mỗi file dựa trên nội dung

### 2.3. Placeholders Cần Thay Thế
- `[CUSTOMER]`: Tên khách hàng (từng dự án tự config)
- `[PROJECT_CODE]`: Mã dự án (từng dự án tự config)
- `${unique_file_hash}`: Hash duy nhất của file (tự động generate từ content)

---

## 3. CÁC THÀNH PHẦN CẦN PHÁT TRIỂN

### 3.1. Template Files
**Mục đích**: Lưu trữ template header cho từng ngôn ngữ

**Cấu trúc đề xuất**:
```
templates/
├── python.template
├── bash.template
├── ruby.template
├── perl.template
├── javascript.template
├── typescript.template
├── java.template
├── c.template
├── cpp.template
├── csharp.template
├── go.template
├── php.template
├── html.template
├── css.template
└── xml.template
```

**Nội dung mỗi template**: Header format với comment syntax phù hợp

### 3.2. Configuration Files

#### 3.2.1. `header-config.json`
**Mục đích**: Cấu hình chung cho toàn bộ hệ thống (từng dự án tự config)
```json
{
  "customer": "[CUSTOMER]",
  "project_code": "[PROJECT_CODE]",
  "copyright_year": "2025",
  "hash_algorithm": "sha256",
  "enabled_languages": [
    "python", "bash", "ruby", "perl",
    "javascript", "typescript",
    "java", "c", "cpp", "csharp", "go",
    "php", "html", "css", "xml"
  ],
  "file_extensions": {
    "python": [".py"],
    "bash": [".sh", ".bash"],
    "ruby": [".rb"],
    "perl": [".pl", ".pm"],
    "javascript": [".js", ".jsx"],
    "typescript": [".ts", ".tsx"],
    "java": [".java"],
    "c": [".c", ".h"],
    "cpp": [".cpp", ".cc", ".cxx", ".hpp", ".h"],
    "csharp": [".cs"],
    "go": [".go"],
    "php": [".php"],
    "html": [".html", ".htm"],
    "css": [".css"],
    "xml": [".xml"]
  },
  "auto_fix": true,
  "migrate_existing": false
}
```

**Lưu ý**: 
- `customer` và `project_code` sẽ được config riêng cho từng dự án
- Có thể mở rộng thêm ngôn ngữ khác nếu cần

#### 3.2.2. `.vscode/settings.json`
**Mục đích**: Cấu hình VS Code để tự động thêm header

#### 3.2.3. `.idea/fileTemplates/`
**Mục đích**: Template cho IntelliJ IDEA

### 3.3. Scripts

#### 3.3.1. `scripts/add-header.py`
**Mục đích**: Script tự động thêm header vào file (Python)
- Đọc template phù hợp với extension
- Generate file hash từ content (SHA256)
- Thay thế placeholders ([CUSTOMER], [PROJECT_CODE], hash)
- Insert header vào đầu file (nếu chưa có)
- **Auto-fix**: Tự động thêm header khi thiếu (nếu được enable)

#### 3.3.2. `scripts/check-header.py`
**Mục đích**: Script kiểm tra header có tồn tại (Python)
- Quét tất cả file code trong repo (trừ file trong .gitignore)
- Kiểm tra header có đúng format
- Kiểm tra các placeholder đã được thay thế
- Return exit code 0 (success) hoặc 1 (fail)
- **Exclusions**: Tự động bỏ qua file/folder trong .gitignore

#### 3.3.3. `scripts/generate-hash.py`
**Mục đích**: Generate unique hash cho file (Python)
- Input: file content
- Output: hash string (SHA256)
- Hash được tính từ nội dung file

### 3.4. Pre-commit Hook

#### 3.4.1. `.git/hooks/pre-commit`
**Mục đích**: Kiểm tra header trước khi commit
- Chạy `check-header.py` trên các file staged
- Nếu thiếu header → block commit
- Hiển thị thông báo lỗi rõ ràng
- **Auto-fix option**: Có thể tự động thêm header nếu thiếu (với confirmation)

**Công cụ**: Sử dụng `pre-commit` framework (Python) - mạnh mẽ, nhiều hooks có sẵn

### 3.5. GitLab CI/CD

#### 3.5.1. `.gitlab-ci.yml`
**Mục đích**: Pipeline kiểm tra header trên GitLab
```yaml
stages:
  - validate

check_headers:
  stage: validate
  image: python:3.9
  before_script:
    - pip install -r requirements.txt
  script:
    - python scripts/check-header.py
  only:
    - merge_requests
    - main
    - develop
```

**Kết quả**: 
- Nếu thiếu header → Pipeline fail → Không thể merge
- Hiển thị danh sách file thiếu header trong job log
- Tự động bỏ qua file/folder trong .gitignore

### 3.6. IDE Extensions/Configurations

#### 3.6.1. VS Code
**Phương án được chọn**: Kết hợp extension + snippet
- **Extension**: Sử dụng "File Header" hoặc "Header Comments"
- **Snippet**: Tạo custom snippet trong `.vscode/header.code-snippets`
- **Auto-fix**: Tự động thêm header khi thiếu (có thể config)
- Cấu hình trong `.vscode/settings.json`

#### 3.6.2. IntelliJ IDEA
- Cấu hình File Templates trong Settings
- Tạo template cho từng loại file (Python, Bash, Ruby, Perl, JavaScript, TypeScript, Java, C, C++, C#, Go, PHP, HTML, CSS, XML)
- Tự động insert khi tạo file mới
- Export settings để share với team

---

## 4. QUY TRÌNH TRIỂN KHAI

### 4.1. Phase 1: Setup Templates & Config
1. Tạo thư mục `templates/` với template cho từng ngôn ngữ (Python, Bash, Ruby, Perl, JavaScript, TypeScript, Java, C, C++, C#, Go, PHP, HTML, CSS, XML)
2. Tạo `header-config.json` với cấu hình (placeholders để từng dự án tự config)
3. Tạo script `generate-hash.py` để generate hash từ content (SHA256)
4. Test template với các ngôn ngữ khác nhau

### 4.2. Phase 2: Development Scripts
1. Phát triển `add-header.py`: Script thêm header (với auto-fix)
2. Phát triển `check-header.py`: Script kiểm tra header (bỏ qua .gitignore)
3. Phát triển `migrate-headers.py`: Script migrate header cho file cũ (với user confirmation)
4. Test scripts với các file mẫu
5. Xử lý edge cases (file đã có header, file rỗng, binary files, etc.)

### 4.3. Phase 3: Pre-commit Hook
1. Setup pre-commit framework (Python pre-commit)
2. Tích hợp `check-header.py` vào hook
3. Implement auto-fix option (với confirmation)
4. Test hook với các scenario:
   - File có header → cho phép commit
   - File thiếu header → block commit (hoặc auto-fix nếu enable)
   - File trong .gitignore → bỏ qua
   - File không phải code → bỏ qua

### 4.4. Phase 4: GitLab CI/CD
1. Tạo `.gitlab-ci.yml` với job check headers
2. Cấu hình chạy trên merge requests
3. Test pipeline với MR test
4. Đảm bảo error message rõ ràng

### 4.5. Phase 5: IDE Integration
1. **VS Code**:
   - Cấu hình extension hoặc snippet
   - Tạo hướng dẫn setup cho team
2. **IntelliJ IDEA**:
   - Cấu hình File Templates
   - Export settings để share với team

### 4.6. Phase 6: Documentation & Onboarding
1. Tạo `README.md` với hướng dẫn setup
2. Tạo `SETUP_GUIDE.md` cho từng IDE
3. Tạo `TROUBLESHOOTING.md` cho các vấn đề thường gặp
4. Training cho team về quy trình

---

## 5. CẤU TRÚC THƯ MỤC ĐỀ XUẤT

```
SetHeader/
├── templates/                    # Header templates cho từng ngôn ngữ
│   ├── python.template
│   ├── bash.template
│   ├── ruby.template
│   ├── perl.template
│   ├── javascript.template
│   ├── typescript.template
│   ├── java.template
│   ├── c.template
│   ├── cpp.template
│   ├── csharp.template
│   ├── go.template
│   ├── php.template
│   ├── html.template
│   ├── css.template
│   └── xml.template
│
├── scripts/                      # Các script tự động (Python)
│   ├── add-header.py            # Thêm header vào file (auto-fix)
│   ├── check-header.py          # Kiểm tra header (bỏ qua .gitignore)
│   ├── generate-hash.py         # Generate file hash từ content
│   └── migrate-headers.py       # Migrate header cho file cũ (với confirmation)
│
├── hooks/                        # Git hooks
│   ├── pre-commit               # Pre-commit hook
│   └── install-hooks.sh         # Script cài đặt hooks
│
├── .vscode/                      # VS Code configuration
│   ├── settings.json
│   └── header.code-snippets
│
├── .idea/                        # IntelliJ IDEA templates (optional)
│   └── fileTemplates/
│
├── .gitlab-ci.yml                # GitLab CI/CD pipeline
│
├── header-config.json            # Cấu hình chung
│
├── requirements.txt              # Python dependencies
├── .pre-commit-config.yaml      # Pre-commit framework config
│
├── README.md                     # Hướng dẫn tổng quan
├── SETUP_GUIDE.md                # Hướng dẫn setup chi tiết
└── TROUBLESHOOTING.md            # Xử lý sự cố
```

---

## 6. CÁC VẤN ĐỀ CẦN XỬ LÝ

### 6.1. Edge Cases
- **File đã có header cũ**: Detect và update hoặc skip (tùy config)
- **File rỗng**: Có thể thêm header (tùy config)
- **File binary**: Bỏ qua kiểm tra (detect bằng magic bytes)
- **File generated**: Tự động exclude dựa trên .gitignore
- **File trong .gitignore**: Tự động bỏ qua (theo yêu cầu)
- **File config**: Có thể cần format khác (ví dụ: `.gitignore`, `package.json`)

### 6.2. Performance
- **Large repositories**: Cần optimize script check để không chậm
- **Incremental check**: Chỉ check file thay đổi trong commit/MR
- **Caching**: Cache hash để tránh tính lại

### 6.3. User Experience
- **Error messages**: Phải rõ ràng, chỉ ra file nào thiếu header
- **Auto-fix option**: Tự động thêm header khi thiếu (đã xác nhận - với confirmation)
- **IDE integration**: Phải seamless, không làm phiền developer
- **Migration**: Script migrate file cũ với user confirmation (đã xác nhận)

### 6.4. Maintenance
- **Template updates**: Script migrate để update header cho file cũ (với user confirmation)
- **Version control**: Template và config cần được version control
- **Migration**: Script `migrate-headers.py` để migrate header cho file cũ (với user confirmation)

---

## 7. CÔNG NGHỆ ĐỀ XUẤT

### 7.1. Scripting Language
**Đã xác nhận: Python**
- Pros: Phổ biến, dễ đọc, có sẵn trên nhiều hệ thống
- Cons: Cần Python runtime (thường có sẵn trên Linux/Mac, dễ cài trên Windows)
- Libraries: `hashlib` (SHA256), `pathlib`, `gitignore_parser` (cho .gitignore)

### 7.2. Pre-commit Tools
**Đã xác nhận: pre-commit framework (Python)**
- Mạnh mẽ, nhiều hooks có sẵn
- Dễ setup và maintain
- Hỗ trợ auto-fix
- Tích hợp tốt với Python scripts

### 7.3. Hash Algorithm
- **MD5**: Nhanh nhưng không secure
- **SHA256**: Secure, phổ biến
- **SHA1**: Không nên dùng (deprecated)

**Đề xuất**: SHA256

---

## 8. TESTING STRATEGY

### 8.1. Unit Tests
- Test template rendering cho từng ngôn ngữ
- Test hash generation
- Test placeholder replacement

### 8.2. Integration Tests
- Test add-header với file mới
- Test add-header với file đã có header
- Test check-header với các scenario khác nhau

### 8.3. End-to-End Tests
- Test pre-commit hook với git workflow
- Test GitLab CI với merge request
- Test IDE integration

---

## 9. TIMELINE ƯỚC TÍNH

- **Phase 1-2**: 2-3 ngày (Templates + Scripts)
- **Phase 3**: 1-2 ngày (Pre-commit hook)
- **Phase 4**: 1-2 ngày (GitLab CI/CD)
- **Phase 5**: 2-3 ngày (IDE Integration)
- **Phase 6**: 1-2 ngày (Documentation)

**Tổng cộng**: ~7-12 ngày làm việc

---

## 10. QUYẾT ĐỊNH ĐÃ XÁC NHẬN

✅ **Công nghệ**: Python
✅ **Ngôn ngữ**: Python, Bash, Ruby, Perl, JavaScript, TypeScript, Java, C, C++, C#, Go, PHP, HTML, CSS, XML
✅ **Placeholders**: Từng dự án tự config ([CUSTOMER], [PROJECT_CODE])
✅ **File hash**: Hash của content (SHA256)
✅ **Existing files**: Migrate với user confirmation
✅ **IDE**: VS Code và IntelliJ IDEA (cả hai)
✅ **Auto-fix**: Tự động thêm header khi thiếu
✅ **Exclusions**: Tự động bỏ qua file/folder trong .gitignore

## 11. NEXT STEPS

1. ✅ **Đã xác nhận** tất cả quyết định
2. **Bắt đầu** implement theo phases:
   - Phase 1: Templates & Config
   - Phase 2: Development Scripts
   - Phase 3: Pre-commit Hook
   - Phase 4: GitLab CI/CD
   - Phase 5: IDE Integration
   - Phase 6: Documentation

---

## 12. CHI TIẾT KỸ THUẬT

### 12.1. File Hash Implementation
- **Algorithm**: SHA256
- **Input**: File content (đọc toàn bộ file)
- **Output**: Hex string (64 characters)
- **Usage**: Thay thế `${unique_file_hash}` trong template

### 12.2. .gitignore Parsing
- Sử dụng library `gitignore_parser` hoặc tự implement
- Parse `.gitignore` và các file ignore patterns
- Skip các file/folder match với patterns
- Hỗ trợ nested .gitignore files

### 12.3. Auto-fix Flow
1. Check header có tồn tại
2. Nếu thiếu → Generate header từ template
3. Insert header vào đầu file
4. Log action để user biết

### 12.4. Migration Flow
1. Scan tất cả file code trong repo
2. Detect file thiếu header hoặc header cũ
3. Hiển thị danh sách file cần migrate
4. User confirmation (y/n)
5. Nếu đồng ý → Migrate tất cả file
6. Log kết quả

### 12.5. Template Format
Mỗi template sẽ có format:
```
{comment_start} ======================================================================================
{comment_start} STRICTLY CONFIDENTIAL | DLP:OMI::STRICT
{comment_start} ======================================================================================
{comment_start} OWNERSHIP NOTICE:
{comment_start} This source code is the proprietary property of {CUSTOMER}.
{comment_start} Developed by Ominext under MSA.
{comment_start}
{comment_start} COPYRIGHT (c) {YEAR} {CUSTOMER}. ALL RIGHTS RESERVED.
{comment_start}
{comment_start} WARNING: This file contains trade secrets and confidential information.
{comment_start} Unauthorized copying or uploading to public networks  is prohibited.
{comment_start}
{comment_start} Project: {PROJECT_CODE}
{comment_start} Trace ID: {FILE_HASH}
{comment_start} ======================================================================================
```

Với `{comment_start}` thay đổi theo ngôn ngữ:
- Python, Bash, Ruby, Perl: `#`
- JavaScript, TypeScript, Java, C, C++, C#, Go: `//`
- PHP: `//` hoặc `#`
- HTML/XML: `<!--` (và `-->` ở cuối mỗi dòng hoặc block)
- CSS: `/*` (và `*/` ở cuối mỗi dòng hoặc block)

