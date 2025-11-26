# SetHeader - File Header Management System

Hệ thống quản lý header chuẩn cho các file code, đảm bảo tất cả file code có header bắt buộc trước khi merge.

## 📋 Tổng quan

SetHeader là một hệ thống tự động để:
- ✅ Thêm header chuẩn vào các file code
- ✅ Kiểm tra header trước khi commit/merge
- ✅ Hỗ trợ 15+ ngôn ngữ lập trình
- ✅ Tích hợp với Git hooks, GitLab CI/CD, và IDE

## 🚀 Quick Start

### 1. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình

Sửa `header-config.json`:
```json
{
  "customer": "Your Customer Name",
  "project_code": "YOUR_PROJECT_CODE",
  "copyright_year": "2025"
}
```

### 3. Thêm Header cho File

```bash
# Thêm header cho một file
python scripts/add-header.py path/to/file.py

# Thêm header cho nhiều file
python scripts/add-header.py file1.py file2.js file3.java
```

### 4. Kiểm tra Headers

```bash
# Kiểm tra tất cả files
python scripts/check-header.py .

# Kiểm tra file cụ thể
python scripts/check-header.py path/to/file.py
```

### 5. Migrate Headers cho File Cũ

```bash
# Interactive mode
python scripts/migrate-headers.py

# Non-interactive mode
python scripts/migrate-headers.py --non-interactive
```

## 📁 Cấu trúc Project

```
SetHeader/
├── templates/              # Header templates cho từng ngôn ngữ
├── scripts/                # Python scripts
│   ├── add-header.py      # Thêm header vào file
│   ├── check-header.py    # Kiểm tra header
│   ├── migrate-headers.py # Migrate headers cho file cũ
│   └── generate-hash.py   # Generate file hash
├── hooks/                  # Git hooks
├── .vscode/                # VS Code configuration
├── .idea/                  # IntelliJ IDEA templates
├── header-config.json      # Cấu hình chung
└── .gitlab-ci.yml          # GitLab CI/CD pipeline
```

## 🌐 Hỗ trợ Ngôn Ngữ

- **Scripting**: Python, Bash, Ruby, Perl
- **Web**: JavaScript, TypeScript, HTML, CSS, XML
- **Enterprise**: Java, C, C++, C#, Go, PHP

Tổng cộng: **15 ngôn ngữ**

## 🔧 Tính năng

### 1. Scripts
- **add-header.py**: Tự động thêm header vào file
- **check-header.py**: Kiểm tra header có tồn tại
- **migrate-headers.py**: Migrate headers cho file cũ

### 2. Git Integration
- **Pre-commit hooks**: Kiểm tra header trước khi commit
- **Pre-commit framework**: Hỗ trợ pre-commit framework
- **Native git hooks**: Hỗ trợ native git hooks

### 3. CI/CD
- **GitLab CI/CD**: Tự động check headers trên merge requests
- **GitHub Actions**: Tự động check headers trên pull requests
- **Block merge**: Không thể merge nếu thiếu header (với cấu hình đúng)

### 4. IDE Integration
- **VS Code**: Snippets và settings
- **IntelliJ IDEA**: File templates

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Hướng dẫn setup đầy đủ
- **[SETUP_PRE_COMMIT.md](SETUP_PRE_COMMIT.md)** - Setup pre-commit hooks
- **[SETUP_GITLAB_CI.md](SETUP_GITLAB_CI.md)** - Setup GitLab CI/CD
- **[SETUP_GITHUB_ACTIONS.md](SETUP_GITHUB_ACTIONS.md)** - Setup GitHub Actions
- **[GITLAB_MERGE_BLOCK_SETUP.md](GITLAB_MERGE_BLOCK_SETUP.md)** - ⚠️ **QUAN TRỌNG**: Cấu hình chặn merge khi thiếu header (GitLab)
- **[SETUP_IDE.md](SETUP_IDE.md)** - Setup IDE integration
- **[SETUP_TOGGLE_CHECK.md](SETUP_TOGGLE_CHECK.md)** - Bật/tắt header check
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Xử lý sự cố

## 🎯 Use Cases

### Thêm Header cho File Mới

```bash
# Tạo file mới
echo "print('Hello')" > new_file.py

# Thêm header
python scripts/add-header.py new_file.py
```

### Kiểm tra Headers trước khi Commit

```bash
# Check headers
python scripts/check-header.py .

# Nếu có file thiếu header, thêm vào
python scripts/add-header.py missing_file.py
```

### Migrate Headers cho Project Cũ

```bash
# Scan và migrate
python scripts/migrate-headers.py

# Hoặc non-interactive
python scripts/migrate-headers.py --non-interactive
```

## 🔒 Format Header

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
# Trace ID: {unique_file_hash}
# ======================================================================================
```

## ⚙️ Configuration

Cấu hình trong `header-config.json`:

```json
{
  "customer": "[CUSTOMER]",
  "project_code": "[PROJECT_CODE]",
  "copyright_year": "2025",
  "hash_algorithm": "sha256",
  "enabled_languages": [...],
  "file_extensions": {...},
  "auto_fix": true,
  "migrate_existing": false
}
```

## 🛠️ Requirements

- Python 3.6+
- Git (cho hooks)
- GitLab Runner (cho CI/CD, optional)

## 📝 License

Proprietary - Developed by Ominext under MSA.

## 🤝 Support

Nếu gặp vấn đề, xem [TROUBLESHOOTING.md](TROUBLESHOOTING.md) hoặc liên hệ team.

## 📚 Quick Links

- [Setup Guide](SETUP_GUIDE.md)
- [Pre-commit Setup](SETUP_PRE_COMMIT.md)
- [GitLab CI Setup](SETUP_GITLAB_CI.md)
- [IDE Setup](SETUP_IDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)

---

**Version**: 1.0.0  
**Last Updated**: 2025

