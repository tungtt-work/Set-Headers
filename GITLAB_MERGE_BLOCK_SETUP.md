# GitLab Merge Block Setup - Chặn Merge khi thiếu Header

Hướng dẫn cấu hình GitLab để **chặn merge** khi pipeline fail (thiếu headers).

## ⚠️ Vấn đề

Mặc dù pipeline có `allow_failure: false`, GitLab vẫn có thể cho phép merge nếu:
- Project settings chưa được cấu hình đúng
- Branch protection rules chưa được setup
- Merge request settings chưa enforce pipeline

## ✅ Giải pháp

### Cách 1: GitLab Project Settings (Khuyến nghị)

1. **Vào GitLab Project Settings**:
   - Vào project trên GitLab
   - **Settings** > **Merge requests**

2. **Cấu hình Merge request settings**:
   - ✅ **Enable "Pipelines must succeed"**
   - ✅ **Enable "All discussions must be resolved"** (optional)
   - ✅ **Enable "All status checks must pass"** (nếu có)

3. **Save changes**

### Cách 2: Branch Protection Rules

1. **Vào Settings** > **Repository** > **Protected branches**

2. **Protect branches** (`main`, `master`, `develop`):
   - ✅ **Allowed to merge**: Chọn "Maintainers" hoặc "Developers + Maintainers"
   - ✅ **Allowed to push**: Chọn "Maintainers" (hoặc Developers nếu cần)
   - ✅ **Require approval**: Optional
   - ✅ **Allowed to force push**: Disable
   - ✅ **Allowed to delete**: Disable

3. **Merge checks**:
   - ✅ **Allowed to merge**: "Allowed to merge"
   - ✅ **Require pipeline to pass**: **ENABLE THIS** ⚠️
   - ✅ **Require status checks to pass**: Optional

4. **Save changes**

### Cách 3: Merge Request Approval Rules (GitLab Premium/Ultimate)

Nếu có GitLab Premium/Ultimate:

1. **Settings** > **Merge request approvals**
2. Tạo approval rule:
   - **Name**: "Header Check Required"
   - **Approvals required**: 0 (vì pipeline sẽ check)
   - **Eligible approvers**: All members
   - **Require pipeline to pass**: ✅ **ENABLE**

### Cách 4: GitLab CI/CD Variables

Có thể thêm variable để enforce:

1. **Settings** > **CI/CD** > **Variables**
2. Thêm variable:
   - **Key**: `REQUIRE_HEADER_CHECK`
   - **Value**: `true`
   - **Protected**: ✅
   - **Masked**: ❌

3. Update `.gitlab-ci.yml`:
```yaml
check_headers:
  script:
    - |
      if [ "$REQUIRE_HEADER_CHECK" == "true" ]; then
        python scripts/check-header.py .
      else
        echo "Header check is optional"
      fi
```

## 🔍 Kiểm tra Cấu hình

### Test Merge Request

1. **Tạo file không có header**:
   ```bash
   echo "print('test')" > test_no_header.py
   git add test_no_header.py
   git commit -m "Add file without header"
   git push origin feature-branch
   ```

2. **Tạo Merge Request**:
   - Pipeline sẽ chạy
   - Job `check_headers` sẽ **FAIL**
   - Merge button sẽ bị **DISABLED** hoặc hiển thị warning

3. **Kiểm tra**:
   - Merge button có bị disable không?
   - Có message "Pipeline must pass" không?
   - Có thể force merge không? (Nếu có, cần cấu hình thêm)

### Kiểm tra Settings

```bash
# Kiểm tra protected branches (nếu có quyền)
# Vào GitLab UI: Settings > Repository > Protected branches
```

## 📋 Checklist Cấu hình

- [ ] **Project Settings** > **Merge requests**:
  - [ ] ✅ "Pipelines must succeed" - **ENABLED**
  - [ ] ✅ "All discussions must be resolved" - Optional
  - [ ] ✅ "All status checks must pass" - Optional

- [ ] **Repository Settings** > **Protected branches**:
  - [ ] ✅ Branches `main`, `master`, `develop` được protect
  - [ ] ✅ "Require pipeline to pass" - **ENABLED**
  - [ ] ✅ "Allowed to force push" - **DISABLED**

- [ ] **`.gitlab-ci.yml`**:
  - [ ] ✅ `allow_failure: false` cho job `check_headers`
  - [ ] ✅ Job chạy trên `merge_requests`

- [ ] **Test**:
  - [ ] ✅ Tạo MR với file thiếu header → Pipeline fail
  - [ ] ✅ Merge button bị disable
  - [ ] ✅ Fix headers → Pipeline pass → Có thể merge

## 🚨 Troubleshooting

### Pipeline fail nhưng vẫn merge được

**Nguyên nhân**: Project settings chưa enforce pipeline.

**Giải pháp**:
1. Vào **Settings** > **Merge requests**
2. Enable **"Pipelines must succeed"**
3. Save và test lại

### Protected branches không hoạt động

**Nguyên nhân**: 
- Chưa protect branches
- Settings không đúng

**Giải pháp**:
1. Vào **Settings** > **Repository** > **Protected branches**
2. Protect branches `main`, `master`, `develop`
3. Enable **"Require pipeline to pass"**

### Merge button vẫn enable khi pipeline fail

**Nguyên nhân**: 
- Có quyền Maintainer/Admin và có thể bypass
- Settings chưa đúng

**Giải pháp**:
1. Kiểm tra quyền: Maintainer/Admin có thể bypass
2. Cấu hình **"Allowed to merge"** chỉ cho Maintainers
3. Enable **"Require pipeline to pass"** trong protected branches

### Pipeline không chạy trên MR

**Nguyên nhân**: 
- `.gitlab-ci.yml` không có `merge_requests` trong `only:`
- GitLab Runner chưa được cấu hình

**Giải pháp**:
1. Kiểm tra `.gitlab-ci.yml` có `only: - merge_requests`
2. Kiểm tra GitLab Runner đã được setup
3. Xem pipeline logs trong GitLab

## 📝 Best Practices

1. **Always enable "Pipelines must succeed"** trong project settings
2. **Protect main branches** với "Require pipeline to pass"
3. **Test với MR thực tế** để đảm bảo merge bị block
4. **Document cho team** về requirements
5. **Review settings định kỳ** để đảm bảo vẫn enforce

## 🔗 References

- [GitLab Merge Request Settings](https://docs.gitlab.com/ee/user/project/merge_requests/settings/)
- [Protected Branches](https://docs.gitlab.com/ee/user/project/protected_branches/)
- [Merge Request Approval Rules](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)

---

**Lưu ý**: Cấu hình này yêu cầu quyền Maintainer hoặc Owner. Liên hệ GitLab admin nếu không có quyền.

