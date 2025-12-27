# 项目部署指南

本指南提供多种部署方案，从最简单的平台部署到生产环境部署。

---

## 🚀 方案一：Railway 部署（推荐，最简单）

Railway 是一个现代化的部署平台，支持自动部署，非常适合初学者。

### 步骤 1：准备工作

1. **创建 Railway 账号**
   - 访问 https://railway.app
   - 使用 GitHub 账号登录

2. **准备项目文件**
   - 确保项目已推送到 GitHub
   - 创建必要的配置文件（见下方）

### 步骤 2：创建配置文件

#### 创建 `Procfile`（用于告诉 Railway 如何启动应用）

```procfile
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

#### 更新 `requirements.txt`（添加 Gunicorn）

确保 `requirements.txt` 包含 `gunicorn`（我会帮你创建）

#### 修改 `app.py`（生产环境配置）

需要修改启动配置，使用环境变量获取端口。

### 步骤 3：部署到 Railway

1. **在 Railway 创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的项目仓库

2. **配置环境变量**
   - Railway 会自动检测 Python 项目
   - 无需额外配置（除非需要环境变量）

3. **部署**
   - Railway 会自动构建和部署
   - 部署完成后会提供一个 URL（如：`https://your-app.railway.app`）

### 步骤 4：访问应用

- Railway 会提供一个公开的 URL
- 访问该 URL 即可使用你的应用

### 优点
- ✅ 完全免费（有免费额度）
- ✅ 自动部署（Git push 自动部署）
- ✅ 无需服务器配置
- ✅ 支持自定义域名

### 缺点
- ⚠️ 免费额度有限（每月 $5 免费额度）
- ⚠️ 休眠后首次访问较慢

---

## 🌐 方案二：Render 部署

Render 是另一个简单的部署平台，类似 Railway。

### 步骤 1：创建 Render 账号

- 访问 https://render.com
- 使用 GitHub 账号登录

### 步骤 2：创建 Web Service

1. 点击 "New +" → "Web Service"
2. 连接你的 GitHub 仓库
3. 配置：
   - **Name**: 你的项目名称
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

### 步骤 3：部署

- Render 会自动构建和部署
- 部署完成后会提供一个 URL

### 优点
- ✅ 免费套餐可用
- ✅ 自动部署
- ✅ 简单易用

### 缺点
- ⚠️ 免费套餐在无流量时会休眠
- ⚠️ 休眠后首次访问需要等待

---

## 🖥️ 方案三：云服务器部署（生产环境推荐）

适合需要稳定运行的生产环境。

### 服务器要求

- **操作系统**: Ubuntu 20.04+ 或 CentOS 7+
- **内存**: 至少 1GB
- **Python**: 3.8+
- **推荐**: 阿里云、腾讯云、AWS、DigitalOcean

### 步骤 1：服务器准备

#### 1.1 连接到服务器

```bash
ssh root@your-server-ip
```

#### 1.2 更新系统

```bash
# Ubuntu
apt update && apt upgrade -y

# CentOS
yum update -y
```

#### 1.3 安装 Python 和 pip

```bash
# Ubuntu
apt install python3 python3-pip python3-venv -y

# CentOS
yum install python3 python3-pip -y
```

#### 1.4 安装 Nginx

```bash
# Ubuntu
apt install nginx -y

# CentOS
yum install nginx -y
```

### 步骤 2：部署应用

#### 2.1 创建应用目录

```bash
mkdir -p /var/www/hot_topics
cd /var/www/hot_topics
```

#### 2.2 上传项目文件

可以使用 Git 克隆：

```bash
git clone https://github.com/your-username/hot_topics_aggregator.git .
```

或者使用 `scp` 上传：

```bash
# 在本地执行
scp -r . root@your-server-ip:/var/www/hot_topics/
```

#### 2.3 创建虚拟环境并安装依赖

```bash
cd /var/www/hot_topics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 步骤 3：配置 Gunicorn

#### 3.1 创建 Gunicorn 服务文件

```bash
sudo nano /etc/systemd/system/hot-topics.service
```

添加以下内容：

```ini
[Unit]
Description=Hot Topics Aggregator Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/hot_topics
Environment="PATH=/var/www/hot_topics/venv/bin"
ExecStart=/var/www/hot_topics/venv/bin/gunicorn --workers 3 --bind unix:/var/www/hot_topics/hot_topics.sock app:app

[Install]
WantedBy=multi-user.target
```

#### 3.2 启动服务

```bash
sudo systemctl start hot-topics
sudo systemctl enable hot-topics
sudo systemctl status hot-topics
```

### 步骤 4：配置 Nginx

#### 4.1 创建 Nginx 配置

```bash
sudo nano /etc/nginx/sites-available/hot_topics
```

添加以下内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或 IP

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/hot_topics/hot_topics.sock;
    }

    location /static {
        alias /var/www/hot_topics/static;
    }
}
```

#### 4.2 启用配置

```bash
sudo ln -s /etc/nginx/sites-available/hot_topics /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

### 步骤 5：配置防火墙

```bash
# Ubuntu (UFW)
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable

# CentOS (firewalld)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 步骤 6：配置 SSL（可选，推荐）

使用 Let's Encrypt 免费 SSL 证书：

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 优点
- ✅ 完全控制
- ✅ 性能好
- ✅ 稳定可靠
- ✅ 支持自定义域名和 SSL

### 缺点
- ⚠️ 需要服务器管理知识
- ⚠️ 需要付费购买服务器
- ⚠️ 需要自己维护

---

## 🐳 方案四：Docker 部署

使用 Docker 可以简化部署过程。

### 步骤 1：创建 Dockerfile

在项目根目录创建 `Dockerfile`（我会帮你创建）

### 步骤 2：构建镜像

```bash
docker build -t hot-topics-aggregator .
```

### 步骤 3：运行容器

```bash
docker run -d -p 5000:5000 --name hot-topics hot-topics-aggregator
```

### 步骤 4：使用 Docker Compose（推荐）

创建 `docker-compose.yml`（我会帮你创建）

```bash
docker-compose up -d
```

### 优点
- ✅ 环境一致
- ✅ 易于迁移
- ✅ 隔离性好

### 缺点
- ⚠️ 需要学习 Docker
- ⚠️ 需要 Docker 环境

---

## 📝 部署前检查清单

### 必须修改的配置

1. **关闭调试模式**
   ```python
   app.run(debug=False)  # 生产环境必须为 False
   ```

2. **使用环境变量**
   - 端口号从环境变量获取
   - 敏感信息使用环境变量

3. **配置 CORS**
   - 限制允许的域名
   - 不要使用 `CORS(app)`（允许所有来源）

4. **添加错误处理**
   - 生产环境错误日志
   - 用户友好的错误页面

### 安全建议

1. **使用 HTTPS**
   - 配置 SSL 证书
   - 强制 HTTPS 重定向

2. **限制请求频率**
   - 防止 DDoS 攻击
   - 使用 Nginx 限流

3. **隐藏敏感信息**
   - 不要提交 `.env` 文件
   - 使用环境变量

4. **定期更新依赖**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

---

## 🔧 常见问题

### 1. 应用无法启动

**检查**：
- 端口是否被占用
- 依赖是否安装完整
- 日志文件查看错误信息

### 2. 静态文件无法加载

**解决**：
- 配置 Nginx 静态文件路径
- 或使用 Flask 的 `static_folder`

### 3. 数据抓取失败

**可能原因**：
- 服务器 IP 被目标网站封禁
- 网络连接问题
- 目标网站结构变化

**解决**：
- 使用代理
- 增加请求间隔
- 更新选择器

### 4. 内存占用过高

**优化**：
- 减少缓存数据量
- 优化数据抓取频率
- 使用数据库替代内存缓存

---

## 📊 性能优化建议

1. **使用数据库缓存**
   - Redis 或 SQLite
   - 持久化数据

2. **添加 CDN**
   - 加速静态资源
   - 减少服务器负载

3. **使用缓存头**
   - 浏览器缓存
   - 减少重复请求

4. **优化数据抓取**
   - 异步抓取
   - 批量处理

---

## 🎯 推荐方案

### 初学者
- **Railway** 或 **Render**（最简单，免费）

### 学习部署
- **云服务器 + Nginx + Gunicorn**（学习完整流程）

### 生产环境
- **云服务器 + Docker + Nginx**（稳定可靠）

---

## 📚 相关资源

- [Railway 文档](https://docs.railway.app)
- [Render 文档](https://render.com/docs)
- [Gunicorn 文档](https://gunicorn.org)
- [Nginx 文档](https://nginx.org/en/docs)
- [Docker 文档](https://docs.docker.com)

---

## 💡 下一步

部署成功后，你可以：

1. **配置自定义域名**
2. **添加监控和日志**
3. **设置自动备份**
4. **优化性能**
5. **添加 CI/CD 流程**

祝你部署顺利！🚀

