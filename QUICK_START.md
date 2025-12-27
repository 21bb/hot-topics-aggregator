# 快速部署指南（5分钟上线）

## 🚀 最简单的方法：Railway 部署

### 步骤 1：准备 GitHub 仓库

1. 在 GitHub 创建新仓库
2. 将项目代码推送到 GitHub：

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/hot-topics-aggregator.git
git push -u origin main
```

### 步骤 2：部署到 Railway

1. **访问 Railway**
   - 打开 https://railway.app
   - 使用 GitHub 账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库

3. **自动部署**
   - Railway 会自动检测到 `Procfile` 和 `requirements.txt`
   - 自动构建和部署（约 2-3 分钟）

4. **获取 URL**
   - 部署完成后，Railway 会提供一个 URL
   - 例如：`https://hot-topics-production.up.railway.app`
   - 点击 URL 即可访问你的应用！

### 完成！🎉

你的应用现在已经上线了！

---

## 📝 其他快速部署选项

### Render（类似 Railway）

1. 访问 https://render.com
2. 登录并创建 "Web Service"
3. 连接 GitHub 仓库
4. 配置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. 点击 "Create Web Service"

### Docker 本地测试

如果你想在本地测试 Docker 部署：

```bash
# 构建镜像
docker build -t hot-topics .

# 运行容器
docker run -p 5000:5000 hot-topics

# 访问 http://localhost:5000
```

---

## ⚙️ 环境变量配置（可选）

如果需要配置环境变量（在 Railway 或 Render 中）：

1. 进入项目设置
2. 找到 "Environment Variables" 或 "Environment"
3. 添加以下变量：

```
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

---

## 🔍 验证部署

部署成功后，访问你的 URL，你应该能看到：

- ✅ 页面正常加载
- ✅ 显示热榜数据
- ✅ API 接口正常工作（访问 `/api/hot_topics`）

---

## ❓ 遇到问题？

### 部署失败

1. 检查 `requirements.txt` 是否包含所有依赖
2. 检查 `Procfile` 格式是否正确
3. 查看 Railway/Render 的构建日志

### 应用无法访问

1. 检查端口配置
2. 检查环境变量
3. 查看应用日志

### 数据抓取失败

1. 这是正常的，应用会使用模拟数据
2. 生产环境可能需要配置代理

---

## 🎯 下一步

部署成功后，你可以：

1. **配置自定义域名**
   - Railway: Settings → Domains
   - Render: Settings → Custom Domains

2. **添加监控**
   - 使用 Railway/Render 的内置监控
   - 或集成第三方监控服务

3. **优化性能**
   - 调整 Gunicorn workers
   - 添加缓存策略

---

**祝你部署顺利！** 🚀

