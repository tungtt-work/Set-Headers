# Setup GitLab CI/CD

Hướng dẫn cài đặt và sử dụng GitLab CI/CD pipeline để kiểm tra headers tự động.

## Tổng quan

GitLab CI/CD pipeline sẽ tự động kiểm tra headers cho tất cả code files khi:
- Tạo Merge Request
- Push vào branches: `main`, `master`, `develop`

Nếu có file thiếu header, pipeline sẽ fail và không thể merge.

## Cấu hình

### File `.gitlab-ci.yml`

Pipeline được cấu hình trong `.gitlab-ci.yml` với các job:

1. **check_headers**: Job chính chạy trên MR và main branches
   - Sử dụng Python 3.9 image
   - Cài đặt dependencies từ `requirements.txt`
   - Chạy `check-header.py` để kiểm tra headers
   - Fail nếu có file thiếu header

2. **check_headers_all**: Job optional chạy trên các branches khác
   - Có thể chạy manual
   - Allow failure để không block development

## Yêu cầu

### GitLab Runner

Đảm bảo GitLab Runner đã được cài đặt và cấu hình với:
- Docker executor
- Python 3.9 image available

### Dependencies

Pipeline sẽ tự động cài đặt dependencies từ `requirements.txt`:
- `gitignore-parser>=0.1.0`
- `pre-commit>=3.0.0` (optional)

## Sử dụng

### Tự động chạy

Pipeline sẽ tự động chạy khi:
- Tạo Merge Request
- Push vào `main`, `master`, hoặc `develop`

### Xem kết quả

1. Vào GitLab project
2. Click vào **CI/CD** > **Pipelines**
3. Xem job `check_headers`
4. Nếu fail, xem logs để biết file nào thiếu header

### Fix lỗi

Nếu pipeline fail vì thiếu header:

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

## Customization

### Thay đổi Python version

Sửa trong `.gitlab-ci.yml`:
```yaml
image: python:3.10  # Thay đổi version
```

### Thêm branches

Thêm vào `only:` section:
```yaml
only:
  - merge_requests
  - main
  - master
  - develop
  - release/*  # Thêm pattern mới
```

### Thay đổi config file

Nếu sử dụng config file khác:
```yaml
script:
  - python scripts/check-header.py --config custom-config.json .
```

### Enable auto-fix (Không khuyến nghị)

Có thể thêm job để tự động fix headers, nhưng không khuyến nghị vì:
- Có thể thay đổi code không mong muốn
- Khó review changes

Nếu muốn enable:
```yaml
auto_fix_headers:
  stage: validate
  image: python:3.9
  before_script:
    - pip install -r requirements.txt
  script:
    - python scripts/add-header.py $(git diff --name-only origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD | grep -E '\.(py|js|java)$')
  only:
    - merge_requests
  allow_failure: true
```

## Testing Locally

### Sử dụng Docker

```bash
# Chạy giống như GitLab CI
docker run --rm -v $(pwd):/workspace -w /workspace python:3.9 bash -c "pip install -r requirements.txt && python scripts/check-header.py ."
```

### Sử dụng gitlab-ci-local

```bash
# Cài đặt gitlab-ci-local
npm install -g gitlab-ci-local

# Chạy pipeline local
gitlab-ci-local check_headers
```

### Test script trực tiếp

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy check
python scripts/check-header.py .
```

## Troubleshooting

### Pipeline không chạy

1. Kiểm tra GitLab Runner đã được cấu hình
2. Kiểm tra `.gitlab-ci.yml` có trong repo
3. Kiểm tra branch có trong `only:` section

### Job fail với "Module not found"

1. Kiểm tra `requirements.txt` có đầy đủ dependencies
2. Kiểm tra `before_script` có cài đặt dependencies
3. Kiểm tra Python version compatibility

### Job fail với "File not found"

1. Kiểm tra script paths đúng
2. Kiểm tra working directory
3. Kiểm tra file có trong repo

### Performance issues

1. Sử dụng cache cho pip packages
2. Chỉ check changed files (nếu cần optimize)
3. Sử dụng `allow_failure: true` cho optional checks

## Best Practices

1. **Luôn check headers trước khi push**: Chạy `check-header.py` local trước khi commit
2. **Sử dụng pre-commit hooks**: Kết hợp với pre-commit hooks để check sớm
3. **Review pipeline logs**: Xem logs để hiểu tại sao pipeline fail
4. **Keep dependencies updated**: Cập nhật `requirements.txt` thường xuyên
5. **Test locally**: Test pipeline changes local trước khi push

## Advanced Configuration

### Check only changed files

Có thể optimize bằng cách chỉ check files thay đổi:

```yaml
script:
  - |
    if [ "$CI_MERGE_REQUEST_ID" ]; then
      CHANGED_FILES=$(git diff --name-only origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD | grep -E '\.(py|js|java|cpp|php)$' || true)
      if [ -n "$CHANGED_FILES" ]; then
        python scripts/check-header.py $CHANGED_FILES
      fi
    else
      python scripts/check-header.py .
    fi
```

### Parallel execution

Có thể chạy check song song cho nhiều file types:

```yaml
check_headers_python:
  script:
    - python scripts/check-header.py --filter python .
  parallel:
    matrix:
      - FILTER: [python, javascript, java]
```

---

**Lưu ý**: Pipeline này đảm bảo tất cả code files có headers trước khi merge, giúp maintain code quality và compliance.

