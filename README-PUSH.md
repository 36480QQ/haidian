# 提交 PR 指引（更新版）

> 状态：提交包 v0.1.4 已就绪并通过全部本地验证（node --test 28/28、官方 validate_submission.py Result: PASS、review ship as-is、security_review 通过）。
> 本机已确认可直连 GitHub（绕过代理 `http://127.0.0.1:7897` 后连接成功），但 **M-zyx-01 的 fork 尚不存在且无认证凭据**，以下操作需您在登录状态下执行。

## 前置：创建 Personal Access Token（如未配置）

1. 打开 https://github.com/settings/tokens → Generate new token (classic)
2. 勾选 `repo`（含 public_repo）权限
3. 复制 token

## 一键脚本（PowerShell，在 E:\Reasonix 下执行）

```powershell
$env:HTTP_PROXY=""; $env:HTTPS_PROXY=""   # 绕过本机代理（当前代理 127.0.0.1:7897 连不上 GitHub）

# 1) fork 官方仓库（需要浏览器登录态或 gh CLI）
#    浏览器打开 https://github.com/open-city-ai/haidian → Fork → 选账号 M-zyx-01

# 2) 配置凭据（token 方式，首次推送会提示输入用户名+token）
git -C haidian-workspace config credential.helper store

# 3) 推送提交分支
git -C haidian-workspace push -u origin submission/M-zyx-01/ai-symbiotic-belt
#    用户名: M-zyx-01   密码: <Personal Access Token>

# 4) 创建 PR（浏览器）
#    打开 https://github.com/M-zyx-01/haidian/pull/new/submission/M-zyx-01/ai-symbiotic-belt
#    base: open-city-ai/haidian:main  ←  compare: M-zyx-01/haidian:submission/M-zyx-01/ai-symbiotic-belt
#    PR 标题建议: "Submission: 京张智脉 AI共生城市带 (M-zyx-01/ai-symbiotic-belt) v0.1.4"
#    正文模板见 delivery-docs/PR-GUIDE.md
```

## 推送到 GitHub 后的验证

```powershell
# CI 将运行官方 finalize/self_check/preflight；提交后持续监控：
# 在 GitHub PR 页面查看 checks；若有失败，读取日志修复后：
git -C haidian-workspace add -A
git -C haidian-workspace commit -m "fix: <描述>"
git -C haidian-workspace push
```

## 说明

- 提交分支：`submission/M-zyx-01/ai-symbiotic-belt`（commit `04ff7e5`，47 个文件：40 提交包 + 6 scenarios 注册表 + README-PUSH）
- PR 只应包含 `submissions/M-zyx-01/ai-symbiotic-belt/` 路径下的改动
- 推送前可运行 `python delivery-docs/scripts/validate_local_submission.py submissions/M-zyx-01/ai-symbiotic-belt --pr-author M-zyx-01 --repo-root haidian-workspace` 复验（当前 Result: PASS）
