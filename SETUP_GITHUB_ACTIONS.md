# Setup GitHub Actions - Check Headers

Hướng dẫn cài đặt và sử dụng GitHub Actions để kiểm tra headers tự động trên Pull Requests.

## Tổng quan

GitHub Actions workflow sẽ tự động kiểm tra headers cho tất cả code files khi:
- Tạo Pull Request vào `main`, `master`, hoặc `develop`
- Push vào `main`, `master`, hoặc `develop`

Nếu có file thiếu header, workflow sẽ fail và **block merge** (nếu cấu hình branch protection).

## Cấu hình

### File Workflows

Có 2 workflow files:

1. **`.github/workflows/check-headers.yml`** - Check tất cả files
   - Chạy trên PR và push vào main branches
   - Check toàn bộ repository
   - Phù hợp cho repositories nhỏ/trung bình

2. **`.github/workflows/check-headers-changed-files.yml`** - Check chỉ changed files
   - Chỉ chạy trên PR
   - Chỉ check files thay đổi trong PR
   - Hiệu quả hơn cho repositories lớn

### Chọn Workflow

**Sử dụng `check-headers.yml` nếu**:
- Repository nhỏ/trung bình (< 1000 files)
- Muốn check toàn bộ codebase
- Đơn giản, dễ maintain

**Sử dụng `check-headers-changed-files.yml` nếu**:
- Repository lớn (> 1000 files)
- Chỉ cần check files thay đổi
- Muốn workflow chạy nhanh hơn

## Yêu cầu

### GitHub Repository

- Repository phải có GitHub Actions enabled (mặc định enabled)
- Không cần cấu hình thêm

### Dependencies

Workflow sẽ tự động cài đặt dependencies từ `requirements.txt`:
- `gitignore-parser>=0.1.0`
- `pre-commit>=3.0.0` (optional)

## Sử dụng

### Tự động chạy

Workflow sẽ tự động chạy khi:
- Tạo Pull Request vào `main`, `master`, hoặc `develop`
- Push vào `main`, `master`, hoặc `develop`

### Xem kết quả

1. Vào GitHub repository
2. Click vào tab **Actions**
3. Xem workflow run
4. Nếu fail, xem logs để biết file nào thiếu header

### Fix lỗi

Nếu workflow fail vì thiếu header:

```bash
# 1. Check files thiếu header
python scripts/check-header.py .

# 2. Thêm header cho file cụ thể
python scripts/add-header.py path/to/file.py

# 3. Hoặc migrate tất cả files
python scripts/migrate-headers.py --non-interactive

# 4. Commit và push lại
git add .
git commit -m "Add headers to files"
git push
```

## Block Merge khi thiếu Header

### Cách 1: Branch Protection Rules (Khuyến nghị)

1. **Vào Repository Settings**:
   - Vào GitHub repository
   - **Settings** > **Branches**

2. **Add branch protection rule**:
   - Click **Add rule**
   - **Branch name pattern**: `main` (hoặc `master`, `develop`)
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Status checks**: Chọn `Check File Headers` (tên job)
   - ✅ **Do not allow bypassing the above settings** (khuyến nghị)

3. **Save changes**

### Cách 2: Required Status Checks

1. **Settings** > **Branches** > **Branch protection rules**
2. Edit rule cho `main`/`master`/`develop`
3. Enable **"Require status checks to pass before merging"**
4. Add status check: `Check File Headers` hoặc `check-headers`

## Customization

### Thay đổi Python version

Sửa trong workflow file:
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.10'  # Thay đổi version
```

### Thêm branches

Sửa trong `on:` section:
```yaml
on:
  pull_request:
    branches:
      - main
      - release/*  # Thêm pattern
```

### Sử dụng config file khác

```yaml
- name: Check file headers
  run: |
    python scripts/check-header.py --config custom-config.json .
```

### Chỉ check trên PR

```yaml
on:
  pull_request:
    branches:
      - main
      - master
      - develop
  # Remove push: section
```

## Testing Locally

### Test với act (GitHub Actions local runner)

```bash
# Cài đặt act
# Windows: choco install act-cli
# Mac: brew install act
# Linux: https://github.com/nektos/act

# Test workflow
act pull_request
```

### Test script trực tiếp

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy check
python scripts/check-header.py .
```

## Troubleshooting

### Workflow không chạy

1. Kiểm tra workflow file có trong `.github/workflows/`
2. Kiểm tra branch name trong `on:` section
3. Kiểm tra GitHub Actions enabled trong repository settings

### Job fail với "Module not found"

1. Kiểm tra `requirements.txt` có đầy đủ dependencies
2. Kiểm tra `Install dependencies` step có chạy
3. Kiểm tra Python version compatibility

### Job fail với "File not found"

1. Kiểm tra script paths đúng
2. Kiểm tra working directory
3. Kiểm tra file có trong repository

### Merge vẫn được phép khi workflow fail

**Nguyên nhân**: Branch protection rules chưa được cấu hình.

**Giải pháp**:
1. Vào **Settings** > **Branches**
2. Add/Edit branch protection rule
3. Enable **"Require status checks to pass before merging"**
4. Add status check: `Check File Headers`

## Best Practices

1. **Enable branch protection**: Đảm bảo merge bị block khi workflow fail
2. **Use changed-files workflow**: Cho repositories lớn để tăng tốc độ
3. **Test locally**: Test workflow changes local trước khi push
4. **Monitor workflow runs**: Xem logs để hiểu tại sao workflow fail
5. **Keep dependencies updated**: Cập nhật `requirements.txt` thường xuyên

## Comparison: GitHub vs GitLab

| Feature | GitHub Actions | GitLab CI/CD |
|---------|---------------|--------------|
| Workflow file | `.github/workflows/*.yml` | `.gitlab-ci.yml` |
| Trigger | `pull_request`, `push` | `merge_requests`, `push` |
| Block merge | Branch protection rules | Project settings + Protected branches |
| Status checks | Automatic | Automatic |
| Comments on PR | Via github-script | Via GitLab API |

## Advanced Configuration

### Matrix Strategy (Multiple Python versions)

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

### Caching dependencies

```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### Conditional execution

```yaml
- name: Check headers
  if: github.event.pull_request.draft == false
  run: python scripts/check-header.py .
```

---

**Lưu ý**: Để chặn merge khi workflow fail, **bắt buộc** phải cấu hình Branch Protection Rules trong GitHub repository settings.

