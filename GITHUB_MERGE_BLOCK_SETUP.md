# GitHub Merge Block Setup - Chặn Merge khi thiếu Header

Hướng dẫn cấu hình GitHub để **chặn merge** khi workflow fail (thiếu headers).

## ⚠️ Vấn đề

Mặc dù workflow có thể fail, GitHub vẫn có thể cho phép merge nếu:
- Branch protection rules chưa được setup
- Required status checks chưa được enable
- Repository settings chưa được cấu hình đúng

## ✅ Giải pháp

### Cách 1: Branch Protection Rules (Khuyến nghị)

1. **Vào GitHub Repository Settings**:
   - Vào repository trên GitHub
   - **Settings** > **Branches**

2. **Add branch protection rule**:
   - Click **Add rule** hoặc **Add branch protection rule**
   - **Branch name pattern**: Nhập `main` (hoặc `master`, `develop`)

3. **Cấu hình Protection Rules**:
   - ✅ **Require a pull request before merging**
     - ✅ **Require approvals**: 1 (hoặc số lượng phù hợp)
     - ✅ **Dismiss stale pull request approvals when new commits are pushed**
   
   - ✅ **Require status checks to pass before merging** ⚠️ **QUAN TRỌNG**
     - ✅ **Require branches to be up to date before merging**
     - ✅ **Status checks**: Chọn `Check File Headers` hoặc `check-headers` (tên job trong workflow)
     - ✅ **Require status checks to pass before merging** (nếu có nhiều checks)
   
   - ✅ **Do not allow bypassing the above settings** (khuyến nghị)
   - ✅ **Restrict who can push to matching branches**: Optional
   - ✅ **Require conversation resolution before merging**: Optional

4. **Save changes**

### Cách 2: Organization Settings (Nếu là Organization repo)

1. **Vào Organization Settings**:
   - Vào Organization trên GitHub
   - **Settings** > **Rules** > **Rulesets**

2. **Create ruleset**:
   - Click **New ruleset**
   - **Target branches**: `main`, `master`, `develop`
   - Enable **"Require status checks to pass"**
   - Add status check: `Check File Headers`

3. **Save ruleset**

## 🔍 Kiểm tra Cấu hình

### Test Pull Request

1. **Tạo file không có header**:
   ```bash
   echo "print('test')" > test_no_header.py
   git add test_no_header.py
   git commit -m "Add file without header"
   git push origin feature-branch
   ```

2. **Tạo Pull Request**:
   - Workflow sẽ chạy
   - Job `Check File Headers` sẽ **FAIL**
   - Merge button sẽ bị **DISABLED** hoặc hiển thị warning

3. **Kiểm tra**:
   - Merge button có bị disable không?
   - Có message "Required status check" không?
   - Có thể force merge không? (Nếu có, cần cấu hình thêm)

### Kiểm tra Settings

1. Vào **Settings** > **Branches**
2. Xem branch protection rules đã được tạo chưa
3. Kiểm tra status check `Check File Headers` có trong list không

## 📋 Checklist Cấu hình

- [ ] **Repository Settings** > **Branches**:
  - [ ] ✅ Branch protection rule cho `main`, `master`, `develop`
  - [ ] ✅ "Require status checks to pass before merging" - **ENABLED**
  - [ ] ✅ "Require branches to be up to date before merging" - **ENABLED**
  - [ ] ✅ Status check `Check File Headers` được chọn
  - [ ] ✅ "Do not allow bypassing" - **ENABLED** (khuyến nghị)

- [ ] **`.github/workflows/check-headers.yml`**:
  - [ ] ✅ Workflow file có trong repository
  - [ ] ✅ Job name: `Check File Headers` hoặc `check-headers`
  - [ ] ✅ Workflow chạy trên `pull_request` và `push`

- [ ] **Test**:
  - [ ] ✅ Tạo PR với file thiếu header → Workflow fail
  - [ ] ✅ Merge button bị disable
  - [ ] ✅ Fix headers → Workflow pass → Có thể merge

## 🚨 Troubleshooting

### Workflow fail nhưng vẫn merge được

**Nguyên nhân**: Branch protection rules chưa được cấu hình hoặc chưa enable status checks.

**Giải pháp**:
1. Vào **Settings** > **Branches**
2. Add/Edit branch protection rule
3. Enable **"Require status checks to pass before merging"**
4. Add status check: `Check File Headers`

### Status check không hiện trong list

**Nguyên nhân**: 
- Workflow chưa chạy lần nào
- Job name không đúng

**Giải pháp**:
1. Tạo PR để workflow chạy ít nhất 1 lần
2. Kiểm tra job name trong workflow file
3. Đảm bảo job name match với status check name

### Merge button vẫn enable khi workflow fail

**Nguyên nhân**: 
- Có quyền Admin và có thể bypass
- Branch protection rules chưa đúng

**Giải pháp**:
1. Kiểm tra quyền: Admin có thể bypass (nếu không enable "Do not allow bypassing")
2. Enable **"Do not allow bypassing the above settings"**
3. Kiểm tra status check đã được add vào required checks chưa

### Workflow không chạy trên PR

**Nguyên nhân**: 
- Workflow file không có trong repository
- Branch name không match trong `on:` section
- GitHub Actions bị disable

**Giải pháp**:
1. Kiểm tra `.github/workflows/check-headers.yml` có trong repo
2. Kiểm tra branch name trong workflow file
3. Kiểm tra GitHub Actions enabled trong repository settings

## 📝 Best Practices

1. **Always enable branch protection** cho main branches
2. **Require status checks** để block merge khi fail
3. **Do not allow bypassing** để đảm bảo consistency
4. **Test với PR thực tế** để đảm bảo merge bị block
5. **Document cho team** về requirements

## 🔗 References

- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Required Status Checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)
- [GitHub Actions](https://docs.github.com/en/actions)

## So sánh với GitLab

| Feature | GitHub | GitLab |
|---------|--------|--------|
| Block merge | Branch protection rules | Project settings + Protected branches |
| Status checks | Automatic (từ workflow) | Automatic (từ pipeline) |
| Required checks | Trong branch protection | Trong protected branches |
| Bypass | Có thể disable | Có thể disable |

---

**Lưu ý**: Cấu hình này yêu cầu quyền Admin hoặc có quyền quản lý branch protection. Liên hệ repository admin nếu không có quyền.

