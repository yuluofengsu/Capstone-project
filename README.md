# 图书借阅推荐系统配置文档

## 1. 项目简介
本项目是一个基于 **Vue.js** (前端) 和 **Django** (后端) 的图书借阅推荐系统。
- **前端**: Vue 2.x, Ant Design Vue, Vue Router, Vuex, Axios
- **后端**: Django 4.1.4, Django REST Framework
- **数据库**: 默认使用 SQLite (可配置为 MySQL)

## 2. 环境要求
- **Python**: 3.8 或更高版本
- **Node.js**: 14.0 或更高版本 (建议 16.x)
- **NPM**: 6.0 或更高版本

## 3. 后端配置 (Server)

### 3.1 目录结构
后端代码位于 `server/` 目录下。

### 3.2 安装依赖
请确保已安装 Python 环境。
```bash
cd server
pip install -r requirements.txt
```
*注意：如果根目录下没有 requirements.txt，可能需要手动安装以下核心库：*
```bash
pip install django djangorestframework django-cors-headers
```

### 3.3 数据库配置
项目默认使用 **SQLite** 数据库，开箱即用，无需额外配置。

**如果需要使用 MySQL**:
1. 修改 `server/bookproject/settings.py` 文件。
2. 找到 `DATABASES` 配置项，注释掉 SQLite 配置，取消 MySQL 配置的注释。
3. 修改 MySQL 连接信息（NAME, USER, PASSWORD, HOST, PORT）。
4. 确保安装了 mysqlclient 或 pymysql: `pip install mysqlclient`。

### 3.4 运行服务
```bash
# 进入 server 目录
cd server

# 迁移数据库 (如果是首次运行或修改了模型)
python manage.py makemigrations
python manage.py migrate

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```
服务默认运行在 `http://127.0.0.1:8000`。

### 3.5 后台管理账号
如果使用的是默认 SQLite 数据库，通常包含已初始化的管理员账号。
如果需要创建新管理员：
```bash
python manage.py createsuperuser
```

## 4. 前端配置 (Client)

### 4.1 目录结构
前端代码位于 `client/` 目录下。

### 4.2 安装依赖
请确保已安装 Node.js 环境。
```bash
cd client
npm install
```
*注意：如果遇到依赖冲突报错，可以尝试使用 `--legacy-peer-deps` 参数，或检查 Node 版本。*
推荐设置：
```bash
export NODE_OPTIONS=--openssl-legacy-provider
```

### 4.3 配置文件
前端连接后端的 API 地址配置在 `client/src/store/constants.js` 文件中。
```javascript
// client/src/store/constants.js
export const BASE_URL = 'http://127.0.0.1:8000'
```
如果后端端口或地址发生变化，请修改此处的 `BASE_URL`。

### 4.4 运行开发环境
```bash
# 进入 client 目录
cd client

# 启动开发服务
npm run serve
```
启动成功后，访问控制台提示的地址（通常是 `http://localhost:8080`）。

### 4.5 打包构建
```bash
npm run build
```
构建生成的静态文件将位于 `client/dist/` 目录下。

## 5. 常见问题排查

### 5.1 跨域问题 (CORS)
后端已配置 `django-cors-headers` 并在 `settings.py` 中设置了 `CORS_ORIGIN_ALLOW_ALL = True`，默认允许所有跨域请求。如果遇到跨域错误，请检查后端服务是否正常启动。

### 5.2 图片无法显示
如果前端图片无法显示，请检查：
1. 后端 `settings.py` 中的 `MEDIA_URL` 和 `MEDIA_ROOT` 配置。
2. 前端代码中是否正确拼接了 `BASE_URL` (如 `http://127.0.0.1:8000/media/...`)。

### 5.3 登录失败
请检查：
1. 后端数据库中是否存在该用户。
2. 前端 `BASE_URL` 是否指向了正确的后端地址。
3. 浏览器控制台的网络请求 (Network) 是否有报错 (404, 500 等)。
