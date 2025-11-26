# Bật/Tắt Header Check

Hướng dẫn bật/tắt kiểm tra headers trước khi commit.

## Cách sử dụng

### Kiểm tra trạng thái

```bash
python scripts/toggle-header-check.py status
```

### Bật Header Check

```bash
python scripts/toggle-header-check.py enable
```

### Tắt Header Check

```bash
python scripts/toggle-header-check.py disable
```

### Toggle (Bật/Tắt)

```bash
python scripts/toggle-header-check.py toggle
```

## Cơ chế hoạt động

### Cách 1: Flag File (Khuyến nghị)

Khi enable, script sẽ tạo file `.header-check-enabled` trong git root:
- File tồn tại = Header check ENABLED
- File không tồn tại = Header check DISABLED

### Cách 2: Git Config

Script cũng lưu setting vào git config:
```bash
git config header-check.enabled true   # Enable
git config header-check.enabled false  # Disable
git config --unset header-check.enabled  # Remove config
```

## Tích hợp với Pre-commit

### Pre-commit Framework

Hook sẽ tự động check setting trước khi chạy:
- Nếu disabled → Hook skip (exit 0)
- Nếu enabled → Hook chạy bình thường

### Native Git Hooks

Hook script cũng check setting:
- Nếu disabled → Hook exit ngay (exit 0)
- Nếu enabled → Hook chạy check headers

## Use Cases

### Tạm thời tắt check

```bash
# Tắt check
python scripts/toggle-header-check.py disable

# Commit code (không bị block)
git commit -m "WIP: temporary commit"

# Bật lại check
python scripts/toggle-header-check.py enable
```

### Enable cho project mới

```bash
# Setup project
git init
python scripts/toggle-header-check.py enable

# Bây giờ hooks sẽ check headers
```

### Disable cho development

```bash
# Trong quá trình development, có thể tắt tạm thời
python scripts/toggle-header-check.py disable

# Khi sẵn sàng, bật lại
python scripts/toggle-header-check.py enable
```

## Lưu ý

1. **Flag file**: File `.header-check-enabled` nên được add vào `.gitignore` nếu muốn mỗi developer tự quyết định
2. **Git config**: Setting lưu trong `.git/config` (local) hoặc có thể set global
3. **Default**: Mặc định là DISABLED để không block workflow
4. **Team consistency**: Nên thống nhất trong team về việc enable/disable

## Thêm vào .gitignore (Optional)

Nếu muốn mỗi developer tự quyết định:

```gitignore
# Header check flag (optional - mỗi dev tự quyết định)
.header-check-enabled
```

## Git Config Global (Optional)

Có thể set global config cho tất cả repositories:

```bash
# Enable globally
git config --global header-check.enabled true

# Disable globally
git config --global header-check.enabled false
```

## Troubleshooting

### Hook vẫn chạy khi đã disable

1. Kiểm tra flag file:
   ```bash
   ls -la .header-check-enabled
   ```

2. Kiểm tra git config:
   ```bash
   git config --get header-check.enabled
   ```

3. Clean pre-commit cache:
   ```bash
   pre-commit clean
   ```

### Hook không chạy khi đã enable

1. Kiểm tra status:
   ```bash
   python scripts/toggle-header-check.py status
   ```

2. Reinstall hooks:
   ```bash
   pre-commit uninstall
   pre-commit install
   ```

---

**Lưu ý**: Mặc định header check là DISABLED. Cần enable để sử dụng.

