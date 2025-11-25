# Setup Pre-commit Hooks

Hướng dẫn cài đặt và sử dụng pre-commit hooks để kiểm tra headers tự động.

## Cách 1: Sử dụng Pre-commit Framework (Khuyến nghị)

### Bước 0: Kiểm tra Git Repository

**Quan trọng**: Pre-commit framework yêu cầu git repository.

```bash
# Kiểm tra có phải git repository không
git status

# Nếu chưa phải, init git repository
git init
```

### Bước 1: Cài đặt pre-commit

```bash
# Cài đặt pre-commit
pip install pre-commit

# Hoặc từ requirements.txt
pip install -r requirements.txt
```

### Bước 2: Cài đặt hooks

```bash
# Cài đặt hooks vào .git/hooks/
pre-commit install
```

### Bước 3: Test

```bash
# Test hook (chạy trên tất cả files)
pre-commit run --all-files

# Test hook trên staged files (như khi commit)
pre-commit run
```

### Sử dụng

Khi bạn commit code, hook sẽ tự động chạy và kiểm tra headers:

```bash
git add file.py
git commit -m "Add new feature"
# Hook sẽ tự động chạy và kiểm tra file.py
```

Nếu file thiếu header, commit sẽ bị chặn và hiển thị lỗi.

## Cách 2: Sử dụng Native Git Hooks

### Windows (PowerShell)

```powershell
.\hooks\install-hooks.ps1
```

### Linux/Mac (Bash)

```bash
chmod +x hooks/install-hooks.sh
./hooks/install-hooks.sh
```

### Sử dụng

Hook sẽ tự động chạy khi bạn commit:

```bash
git add file.py
git commit -m "Add new feature"
# Hook sẽ tự động chạy
```

## Cấu hình

### Enable Auto-fix (Tự động thêm header)

Nếu muốn tự động thêm header khi thiếu, sửa `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: check-headers
        # ... existing config ...
      
      # Uncomment để enable auto-fix
      - id: auto-fix-headers
        name: Auto-fix missing headers
        entry: python scripts/add-header.py
        language: system
        types: [file]
        pass_filenames: true
        stages: [pre-commit]
```

**Lưu ý**: Auto-fix sẽ tự động thêm header, có thể không phù hợp với mọi workflow.

### Bỏ qua hook cho một commit

```bash
# Skip hooks
git commit --no-verify -m "message"
```

**Cảnh báo**: Chỉ dùng khi thực sự cần thiết!

## Troubleshooting

### Hook không chạy

1. Kiểm tra hooks đã được cài đặt:
   ```bash
   ls .git/hooks/pre-commit
   ```

2. Kiểm tra quyền thực thi (Linux/Mac):
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

### Hook chạy nhưng không check files

- Kiểm tra file có được stage không: `git status`
- Kiểm tra file extension có trong config không
- Kiểm tra file có trong .gitignore không (sẽ bị skip)

### Pre-commit framework không tìm thấy Python

- Đảm bảo Python đã được cài đặt và trong PATH
- Có thể chỉ định Python path trong `.pre-commit-config.yaml`

## Update Hooks

```bash
# Update pre-commit hooks
pre-commit autoupdate

# Reinstall hooks
pre-commit uninstall
pre-commit install
```

## Uninstall

```bash
# Uninstall pre-commit hooks
pre-commit uninstall

# Hoặc xóa thủ công
rm .git/hooks/pre-commit
```

