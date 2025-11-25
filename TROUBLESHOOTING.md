# Troubleshooting - Xử lý Sự cố

Hướng dẫn xử lý các vấn đề thường gặp khi sử dụng SetHeader.

## 📋 Mục lục

1. [Scripts Issues](#scripts-issues)
2. [Git Hooks Issues](#git-hooks-issues)
3. [CI/CD Issues](#cicd-issues)
4. [IDE Issues](#ide-issues)
5. [Configuration Issues](#configuration-issues)
6. [Performance Issues](#performance-issues)

## Scripts Issues

### ModuleNotFoundError: No module named 'generate_hash'

**Nguyên nhân**: Import error do tên file có dấu gạch ngang.

**Giải pháp**:
- Script đã được sửa để sử dụng `importlib.util`
- Đảm bảo đang chạy từ đúng directory
- Kiểm tra Python version (cần 3.6+)

```bash
# Test import
python -c "import sys; sys.path.insert(0, 'scripts'); import importlib.util; print('OK')"
```

### File not found error

**Nguyên nhân**: Path không đúng hoặc file không tồn tại.

**Giải pháp**:
```bash
# Kiểm tra file có tồn tại
ls path/to/file.py

# Sử dụng absolute path
python scripts/add-header.py /absolute/path/to/file.py

# Hoặc relative path từ project root
python scripts/add-header.py relative/path/to/file.py
```

### Encoding errors trên Windows

**Nguyên nhân**: Windows console không hỗ trợ UTF-8 đầy đủ.

**Giải pháp**:
- Script đã được sửa để tránh ký tự đặc biệt
- Sử dụng `[OK]` thay vì `✓`
- Set console encoding: `chcp 65001` (PowerShell)

### Hash không được generate

**Nguyên nhân**: File rỗng hoặc không đọc được.

**Giải pháp**:
```bash
# Kiểm tra file có nội dung
cat file.py

# Test generate hash
python scripts/generate-hash.py file.py

# Kiểm tra permissions
ls -l file.py
```

### Header không được thêm vào

**Nguyên nhân**: 
- File đã có header
- File không được support
- Binary file

**Giải pháp**:
```bash
# Force replace
python scripts/add-header.py --force file.py

# Kiểm tra file extension có trong config
cat header-config.json | grep -A 5 "file_extensions"

# Kiểm tra file có phải binary không
file file.py
```

## Git Hooks Issues

### Hook không chạy

**Nguyên nhân**: Hook chưa được cài đặt hoặc không có quyền thực thi.

**Giải pháp**:

**Pre-commit Framework:**
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install

# Test hook
pre-commit run --all-files
```

**Native Git Hooks:**
```bash
# Kiểm tra hook có tồn tại
ls -l .git/hooks/pre-commit

# Set executable (Linux/Mac)
chmod +x .git/hooks/pre-commit

# Reinstall
./hooks/install-hooks.sh
```

### Hook chạy nhưng không check files

**Nguyên nhân**: 
- Files không được stage
- Files không match extensions
- Files trong .gitignore

**Giải pháp**:
```bash
# Kiểm tra staged files
git status

# Stage files
git add file.py

# Kiểm tra .gitignore
cat .gitignore

# Test hook manually
.git/hooks/pre-commit
```

### Hook block commit nhưng muốn skip

**Giải pháp**:
```bash
# Skip hook (chỉ khi thực sự cần)
git commit --no-verify -m "message"

# Hoặc fix headers trước
python scripts/add-header.py file.py
git add file.py
git commit -m "message"
```

### Pre-commit framework không tìm thấy Python

**Nguyên nhân**: Python không trong PATH hoặc version sai.

**Giải pháp**:
```bash
# Kiểm tra Python
which python
python --version

# Cấu hình pre-commit sử dụng Python cụ thể
# Sửa .pre-commit-config.yaml
default_language_version:
  python: python3.9
```

## CI/CD Issues

### Pipeline không chạy

**Nguyên nhân**: 
- `.gitlab-ci.yml` không có trong repo
- Branch không trong `only:` section
- GitLab Runner chưa được cấu hình

**Giải pháp**:
```bash
# Kiểm tra file có trong repo
git ls-files | grep gitlab-ci

# Kiểm tra branch
git branch

# Kiểm tra GitLab Runner
# Vào GitLab > Settings > CI/CD > Runners
```

### Job fail với "Module not found"

**Nguyên nhân**: Dependencies chưa được cài đặt.

**Giải pháp**:
```yaml
# Kiểm tra .gitlab-ci.yml có before_script
before_script:
  - pip install -r requirements.txt
```

### Job fail với "File not found"

**Nguyên nhân**: Script paths không đúng.

**Giải pháp**:
```yaml
# Sử dụng absolute paths hoặc đảm bảo working directory đúng
script:
  - cd $CI_PROJECT_DIR
  - python scripts/check-header.py .
```

### Pipeline chạy chậm

**Nguyên nhân**: Không có cache hoặc check quá nhiều files.

**Giải pháp**:
```yaml
# Thêm cache
cache:
  paths:
    - .cache/pip

# Hoặc chỉ check changed files
script:
  - |
    if [ "$CI_MERGE_REQUEST_ID" ]; then
      CHANGED_FILES=$(git diff --name-only origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD)
      python scripts/check-header.py $CHANGED_FILES
    fi
```

## IDE Issues

### VS Code snippets không hiện

**Nguyên nhân**: 
- File snippets không có trong project
- Language mode không đúng
- VS Code chưa reload

**Giải pháp**:
```bash
# Kiểm tra file có tồn tại
ls .vscode/header.code-snippets

# Reload VS Code
# Ctrl+Shift+P > "Reload Window"

# Kiểm tra language mode
# Bottom right corner của VS Code
```

### IntelliJ templates không hoạt động

**Nguyên nhân**: Templates chưa được import hoặc variables sai.

**Giải pháp**:
1. **File** > **Settings** > **Editor** > **File and Code Templates**
2. Kiểm tra templates đã được import
3. Kiểm tra template variables: `${PROJECT_NAME}`, `${YEAR}`, etc.
4. Restart IntelliJ IDEA

### Hash không được generate trong templates

**Nguyên nhân**: Templates/snippets không thể tự động generate hash.

**Giải pháp**:
- Sử dụng script `add-header.py` sau khi tạo file
- Hoặc để trống và update sau
- Sử dụng IDE macro để tự động chạy script

## Configuration Issues

### Config không được load

**Nguyên nhân**: Path không đúng hoặc JSON syntax error.

**Giải pháp**:
```bash
# Kiểm tra JSON syntax
python -m json.tool header-config.json

# Kiểm tra path
python scripts/check-header.py --config header-config.json .
```

### Placeholders không được thay thế

**Nguyên nhân**: Config values chưa được set.

**Giải pháp**:
```json
// Kiểm tra header-config.json
{
  "customer": "Your Customer",  // Không phải "[CUSTOMER]"
  "project_code": "YOUR_CODE"  // Không phải "[PROJECT_CODE]"
}
```

### File extensions không match

**Nguyên nhân**: Extension không có trong config.

**Giải pháp**:
```json
// Thêm vào header-config.json
"file_extensions": {
  "your_language": [".ext1", ".ext2"]
}
```

## Performance Issues

### Check quá chậm với nhiều files

**Nguyên nhân**: Check tất cả files thay vì chỉ changed files.

**Giải pháp**:
```bash
# Chỉ check changed files
git diff --name-only | xargs python scripts/check-header.py

# Hoặc chỉ check staged files
git diff --cached --name-only | xargs python scripts/check-header.py
```

### Migrate quá chậm

**Nguyên nhân**: Quá nhiều files cần migrate.

**Giải pháp**:
```bash
# Migrate từng directory
python scripts/migrate-headers.py src/
python scripts/migrate-headers.py tests/

# Hoặc exclude một số directories
# Sửa script để skip node_modules, venv, etc.
```

## Getting Help

Nếu vấn đề không được giải quyết:

1. **Kiểm tra logs**: Xem error messages chi tiết
2. **Test với file đơn giản**: Tạo file test để reproduce
3. **Kiểm tra versions**: Python, Git, extensions
4. **Xem documentation**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
5. **Liên hệ team**: Cung cấp error messages và steps to reproduce

## Common Error Messages

### "Error: File not found"
- Kiểm tra file path
- Kiểm tra working directory
- Sử dụng absolute path

### "Error: Module not found"
- Cài đặt dependencies: `pip install -r requirements.txt`
- Kiểm tra Python version
- Kiểm tra import paths

### "Error: Permission denied"
- Kiểm tra file permissions
- Set executable: `chmod +x script.py`
- Kiểm tra write permissions

### "Error: Encoding error"
- Set console encoding (Windows): `chcp 65001`
- Kiểm tra file encoding
- Sử dụng UTF-8

---

**Lưu ý**: Luôn backup project trước khi chạy migrate hoặc force operations.

