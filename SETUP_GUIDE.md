# Setup Guide - Hướng dẫn Setup Đầy Đủ

Hướng dẫn chi tiết để setup SetHeader cho project của bạn.

## 📋 Mục lục

1. [Yêu cầu](#yêu-cầu)
2. [Cài đặt](#cài-đặt)
3. [Cấu hình](#cấu-hình)
4. [Sử dụng Scripts](#sử-dụng-scripts)
5. [Setup Git Hooks](#setup-git-hooks)
6. [Setup GitLab CI/CD](#setup-gitlab-cicd)
7. [Setup IDE](#setup-ide)
8. [Best Practices](#best-practices)

## Yêu cầu

### Hệ thống
- Python 3.6 hoặc cao hơn
- Git (cho hooks)
- GitLab Runner (cho CI/CD, optional)

### Dependencies
- `gitignore-parser>=0.1.0`
- `pre-commit>=3.0.0` (optional, cho pre-commit framework)

## Cài đặt

### Bước 1: Clone hoặc Copy Project

```bash
# Nếu là git repository
git clone <repository-url>
cd SetHeader

# Hoặc copy toàn bộ thư mục vào project của bạn
```

### Bước 1.5: Kiểm tra Git Repository (Nếu dùng Pre-commit)

**Quan trọng**: Pre-commit framework yêu cầu git repository.

```bash
# Kiểm tra có phải git repository không
git status

# Nếu chưa phải, init git repository
git init
```

### Bước 2: Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Kiểm tra Cài đặt

```bash
# Test script
python scripts/check-header.py --help
python scripts/add-header.py --help
```

## Cấu hình

### 1. Cấu hình header-config.json

Sửa file `header-config.json`:

```json
{
  "customer": "Your Customer Name",
  "project_code": "YOUR_PROJECT_CODE",
  "copyright_year": "2025",
  "hash_algorithm": "sha256",
  "enabled_languages": [
    "python", "javascript", "java", "cpp", "php"
  ],
  "file_extensions": {
    "python": [".py"],
    "javascript": [".js", ".jsx"],
    "java": [".java"],
    "cpp": [".cpp", ".hpp"],
    "php": [".php"]
  },
  "auto_fix": true,
  "migrate_existing": false
}
```

**Lưu ý**:
- `customer`: Tên khách hàng (sẽ thay thế `[CUSTOMER]` trong header)
- `project_code`: Mã dự án (sẽ thay thế `[PROJECT_CODE]` trong header)
- `copyright_year`: Năm copyright
- `enabled_languages`: Danh sách ngôn ngữ được enable
- `file_extensions`: Mapping extensions với ngôn ngữ

### 2. Customize Templates (Optional)

Nếu cần thay đổi format header, sửa các file trong `templates/`:
- `templates/python.template`
- `templates/javascript.template`
- etc.

## Sử dụng Scripts

### 1. Thêm Header cho File

```bash
# Thêm header cho một file
python scripts/add-header.py path/to/file.py

# Thêm header cho nhiều file
python scripts/add-header.py file1.py file2.js file3.java

# Force replace header cũ
python scripts/add-header.py --force file.py

# Sử dụng config file khác
python scripts/add-header.py --config custom-config.json file.py
```

### 2. Kiểm tra Headers

```bash
# Kiểm tra tất cả files trong directory
python scripts/check-header.py .

# Kiểm tra file cụ thể
python scripts/check-header.py path/to/file.py

# Kiểm tra nhiều paths
python scripts/check-header.py dir1/ dir2/ file.py

# Non-recursive
python scripts/check-header.py --no-recursive .

# Sử dụng config file khác
python scripts/check-header.py --config custom-config.json .
```

### 3. Migrate Headers cho File Cũ

```bash
# Interactive mode (mặc định)
python scripts/migrate-headers.py

# Migrate specific directory
python scripts/migrate-headers.py path/to/directory

# Non-interactive mode
python scripts/migrate-headers.py --non-interactive

# Force replace existing headers
python scripts/migrate-headers.py --force

# Non-recursive
python scripts/migrate-headers.py --no-recursive .
```

## Setup Git Hooks

### Option 1: Pre-commit Framework (Khuyến nghị)

Xem chi tiết: [SETUP_PRE_COMMIT.md](SETUP_PRE_COMMIT.md)

```bash
# Cài đặt pre-commit
pip install pre-commit

# Cài đặt hooks
pre-commit install

# Test
pre-commit run --all-files
```

### Option 2: Native Git Hooks

**Windows:**
```powershell
.\hooks\install-hooks.ps1
```

**Linux/Mac:**
```bash
chmod +x hooks/install-hooks.sh
./hooks/install-hooks.sh
```

## Setup CI/CD

### GitLab CI/CD

Xem chi tiết: [SETUP_GITLAB_CI.md](SETUP_GITLAB_CI.md)

**Quick Setup**:
1. Đảm bảo `.gitlab-ci.yml` có trong repository
2. GitLab Runner đã được cấu hình
3. Pipeline sẽ tự động chạy khi:
   - Tạo Merge Request
   - Push vào `main`, `master`, `develop`

**Block Merge**: Xem [GITLAB_MERGE_BLOCK_SETUP.md](GITLAB_MERGE_BLOCK_SETUP.md)

### GitHub Actions

Xem chi tiết: [SETUP_GITHUB_ACTIONS.md](SETUP_GITHUB_ACTIONS.md)

**Quick Setup**:
1. Đảm bảo `.github/workflows/check-headers.yml` có trong repository
2. GitHub Actions tự động enabled (mặc định)
3. Workflow sẽ tự động chạy khi:
   - Tạo Pull Request vào `main`, `master`, `develop`
   - Push vào `main`, `master`, `develop`

**Block Merge**: 
- Vào **Settings** > **Branches**
- Add branch protection rule
- Enable **"Require status checks to pass before merging"**
- Add status check: `Check File Headers`

### Test Local

```bash
# Sử dụng Docker
docker run --rm -v $(pwd):/workspace -w /workspace python:3.9 bash -c "pip install -r requirements.txt && python scripts/check-header.py ."
```

## Setup IDE

### VS Code

Xem chi tiết: [SETUP_IDE.md](SETUP_IDE.md)

**Sử dụng Snippets:**
1. Mở file mới
2. Gõ `header-py`, `header-js`, etc.
3. Chọn snippet từ dropdown

**Sử dụng Extension:**
1. Cài đặt "File Header" extension
2. Extension tự động thêm header khi tạo file mới

### IntelliJ IDEA

Xem chi tiết: [SETUP_IDE.md](SETUP_IDE.md)

**Import Templates:**
1. **File** > **Settings** > **Editor** > **File and Code Templates**
2. Click **Import** và chọn `.idea/fileTemplates/`
3. Templates sẽ tự động thêm header khi tạo file mới

## Best Practices

### 1. Workflow Khuyến nghị

```
1. Tạo file mới trong IDE
   ↓
2. Sử dụng snippet/template để thêm header
   ↓
3. Viết code
   ↓
4. Chạy add-header.py để generate hash đúng
   ↓
5. Commit code
   ↓
6. Pre-commit hook kiểm tra header
   ↓
7. Push và tạo MR
   ↓
8. GitLab CI kiểm tra header
   ↓
9. Merge nếu pass
```

### 2. Migrate Project Cũ

```bash
# 1. Backup project
git checkout -b backup-branch

# 2. Scan files cần migrate
python scripts/migrate-headers.py --non-interactive

# 3. Review changes
git diff

# 4. Commit nếu OK
git add .
git commit -m "Add headers to all files"
```

### 3. Check Headers thường xuyên

```bash
# Thêm vào package.json scripts (nếu có)
"scripts": {
  "check-headers": "python scripts/check-header.py ."
}

# Hoặc tạo alias
alias check-headers="python scripts/check-header.py ."
```

### 4. Auto-fix trong Workflow

Có thể setup auto-fix trong:
- Pre-commit hooks (với confirmation)
- GitLab CI (không khuyến nghị)
- IDE save actions

## Troubleshooting

Xem chi tiết: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Common Issues

1. **Script không tìm thấy file**: Kiểm tra path và working directory
2. **Import errors**: Đảm bảo dependencies đã được cài đặt
3. **Hook không chạy**: Kiểm tra permissions và installation
4. **CI/CD fail**: Kiểm tra GitLab Runner và Python version

## Next Steps

1. ✅ Cấu hình `header-config.json`
2. ✅ Test scripts với file mẫu
3. ✅ Setup git hooks
4. ✅ Setup CI/CD (nếu dùng GitLab)
5. ✅ Setup IDE integration
6. ✅ Migrate headers cho file cũ (nếu cần)
7. ✅ Train team về workflow

## Tài liệu Tham khảo

- [README.md](README.md) - Tổng quan
- [SETUP_PRE_COMMIT.md](SETUP_PRE_COMMIT.md) - Pre-commit hooks
- [SETUP_GITLAB_CI.md](SETUP_GITLAB_CI.md) - GitLab CI/CD
- [SETUP_IDE.md](SETUP_IDE.md) - IDE integration
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Xử lý sự cố

---

**Lưu ý**: Đảm bảo tất cả team members đã setup và hiểu workflow trước khi bắt đầu enforce headers.

