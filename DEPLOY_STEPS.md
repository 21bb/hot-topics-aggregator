# 🚀 Railway 部署详细步骤

## 📋 部署前准备清单

### ✅ 需要准备的东西：
- [ ] GitHub 账号（如果没有，去 https://github.com 注册）
- [ ] Railway 账号（如果没有，去 https://railway.app 注册）
- [ ] Git（检查是否已安装，见下方）

---

## 第一步：检查并安装 Git

### 1.1 检查 Git 是否已安装

打开 PowerShell 或命令提示符，输入：
```bash
git --version
```

**如果显示版本号**（如 `git version 2.xx.x`）：
- ✅ Git 已安装，跳到第二步

**如果显示错误**（如 `'git' is not recognized`）：
- ❌ 需要安装 Git

### 1.2 安装 Git（如果未安装）

**Windows 安装方法：**

1. **下载 Git**
   - 访问：https://git-scm.com/download/win
   - 下载最新版本（会自动下载适合你系统的版本）

2. **安装 Git**
   - 运行下载的安装程序
   - 一路点击 "Next"（使用默认设置即可）
   - 安装完成后重启终端

3. **验证安装**
   ```bash
   git --version
   ```
   应该显示版本号

---

## 第二步：准备 GitHub 仓库

### 2.1 在 GitHub 创建新仓库

1. **登录 GitHub**
   - 访问：https://github.com
   - 如果没有账号，先注册（免费）

2. **创建新仓库**
   - 点击右上角的 "+" 号
   - 选择 "New repository"

3. **填写仓库信息**
   - **Repository name**: `hot-topics-aggregator`（或你喜欢的名字）
   - **Description**: `聚合热榜数据展示平台`（可选）
   - **Visibility**: 选择 **Public**（公开，免费）或 **Private**（私有）
   - ⚠️ **不要**勾选 "Add a README file"（因为我们已经有了）
   - ⚠️ **不要**添加 .gitignore 或 license（我们已经有了）
   - 点击 "Create repository"

4. **复制仓库地址**
   - 创建后会显示仓库页面
   - 复制 HTTPS 地址（类似：`https://github.com/你的用户名/hot-topics-aggregator.git`）
   - 保存这个地址，下一步会用到

---

## 第三步：初始化 Git 并推送代码

### 3.1 打开项目目录

在 PowerShell 中，进入项目目录：
```bash
cd C:\Users\20368\Desktop\projects\hot_topics_aggregator
```

### 3.2 初始化 Git 仓库（如果还没有）

```bash
git init
```

### 3.3 配置 Git（首次使用需要）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

**示例：**
```bash
git config --global user.name "张三"
git config --global user.email "zhangsan@example.com"
```

### 3.4 添加所有文件

```bash
git add .
```

### 3.5 提交代码

```bash
git commit -m "Initial commit: 聚合热榜项目"
```

### 3.6 连接到 GitHub 仓库

**将 `你的用户名` 和 `仓库名` 替换为实际值：**

```bash
git remote add origin https://github.com/你的用户名/hot-topics-aggregator.git
```

**示例：**
```bash
git remote add origin https://github.com/zhangsan/hot-topics-aggregator.git
```

### 3.7 推送到 GitHub

```bash
git branch -M main
git push -u origin main
```

**如果提示输入用户名和密码：**
- 用户名：你的 GitHub 用户名
- 密码：**不是**你的 GitHub 密码，而是 **Personal Access Token**

**如何获取 Personal Access Token：**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token (classic)"
3. 填写 Note（如：Railway部署）
4. 选择过期时间（建议：90 days 或 No expiration）
5. 勾选权限：至少勾选 `repo`（完整仓库权限）
6. 点击 "Generate token"
7. **立即复制 token**（只显示一次！）
8. 使用这个 token 作为密码

### 3.8 验证推送成功

刷新 GitHub 仓库页面，应该能看到所有文件。

---

## 第四步：部署到 Railway

### 4.1 登录 Railway

1. 访问：https://railway.app
2. 点击 "Login" 或 "Start a New Project"
3. 选择 "Login with GitHub"
4. 授权 Railway 访问你的 GitHub

### 4.2 创建新项目

1. 登录后，点击 **"New Project"**（或 "+ New"）
2. 选择 **"Deploy from GitHub repo"**
3. 如果第一次使用，可能需要授权 Railway 访问 GitHub
4. 在仓库列表中找到你的 `hot-topics-aggregator` 仓库
5. 点击仓库名称

### 4.3 自动部署

Railway 会自动：
- ✅ 检测到 `Procfile` 和 `requirements.txt`
- ✅ 识别为 Python 项目
- ✅ 开始构建和部署（约 2-5 分钟）

**你可以看到：**
- 构建日志（Building...）
- 安装依赖（Installing dependencies...）
- 启动应用（Starting...）

### 4.4 获取部署 URL

部署完成后：

1. 点击项目卡片
2. 找到 **"Settings"** 标签
3. 在 **"Domains"** 部分，你会看到一个 URL
   - 类似：`https://hot-topics-production.up.railway.app`
4. 点击这个 URL 即可访问你的应用！

### 4.5 配置环境变量（可选）

如果需要配置环境变量：

1. 在项目页面，点击 **"Variables"** 标签
2. 点击 **"New Variable"**
3. 添加变量：
   - **Key**: `FLASK_ENV`
   - **Value**: `production`
4. 点击 **"Add"**

**常用环境变量：**
- `FLASK_ENV=production`（生产环境）
- `FLASK_DEBUG=False`（关闭调试）

---

## 第五步：验证部署

### 5.1 访问应用

打开 Railway 提供的 URL，你应该看到：
- ✅ 页面正常加载
- ✅ 显示"聚合热榜"标题
- ✅ 显示热榜数据（或"暂无数据"提示）
- ✅ 刷新按钮可以点击

### 5.2 测试 API

访问：`https://你的URL.railway.app/api/hot_topics`

应该返回 JSON 数据：
```json
{
  "data": [...],
  "last_update": "2025-01-XX XX:XX:XX"
}
```

---

## 🎉 部署完成！

### 你现在拥有：
- ✅ 一个在线的 Web 应用
- ✅ 可以分享的公开链接
- ✅ 自动部署（每次 push 到 GitHub 会自动更新）

### 后续操作：

#### 1. 更新代码后自动部署
```bash
git add .
git commit -m "更新说明"
git push
```
Railway 会自动检测并重新部署！

#### 2. 查看部署日志
- Railway 项目页面 → "Deployments" 标签
- 可以看到每次部署的日志

#### 3. 配置自定义域名（可选）
- Railway 项目 → Settings → Domains
- 添加你的域名

---

## ❓ 常见问题

### Q1: 部署失败怎么办？

**检查：**
1. 查看 Railway 的构建日志（Build Logs）
2. 检查 `requirements.txt` 是否包含所有依赖
3. 检查 `Procfile` 格式是否正确
4. 确保代码没有语法错误

### Q2: 应用无法访问？

**检查：**
1. 部署是否完成（查看 Deployments）
2. 应用是否正在运行（查看 Metrics）
3. 检查日志（View Logs）

### Q3: 数据抓取失败？

**这是正常的：**
- 应用会使用模拟数据
- 生产环境可能需要配置代理
- 不影响基本功能展示

### Q4: 如何停止部署？

**在 Railway：**
- 项目页面 → Settings → Delete Project
- 或暂停服务（某些计划支持）

---

## 📞 需要帮助？

如果遇到问题：
1. 查看 Railway 的构建日志
2. 检查 GitHub 仓库是否正确推送
3. 查看 `DEPLOYMENT.md` 获取更多信息

---

**祝你部署顺利！** 🚀

