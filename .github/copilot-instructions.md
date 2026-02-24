# 图书借阅推荐系统 - AI 编码助手指南

## 项目概览

这是一个**全栈图书借阅推荐系统**，采用前后端分离架构：
- **前端**：Vue 2.x + Ant Design Vue + Vue Router + Vuex (存储层token和用户状态)
- **后端**：Django 4.1.4 + Django REST Framework (RESTful API)
- **数据库**：MySQL (生产环境) / SQLite (开发环境)
- **部署模式**：客户端和服务端独立启动，通过HTTP通信

## 核心架构与数据流

### 前端架构 (`client/`)
```
src/
├── api/              # API层 (分为 admin/ 和 index/ 两套接口)
├── views/            # 页面组件 (路由页面)
├── router/           # 路由配置 (分前台/后台两套路由)
├── store/            # Vuex状态 (user token、admin token独立管理)
├── utils/            # 工具函数 (request.js 是关键的axios拦截器)
├── components/       # 共享组件
└── style/            # 全局样式(LESS)
```

**关键点**：
- 分为**前台(index)和后台(admin)两套独立系统**，共用同一UI库和路由框架
- `store/constants.js` 定义了 `BASE_URL` (后端地址) 和 token key 常量
- 认证通过 `localStorage` 存储 `TOKEN` (前台) 和 `ADMIN_TOKEN` (后台)
- `utils/request.js` 是所有API调用的拦截器，处理token自动附加和403错误处理

### 后端架构 (`server/`)
```
bookproject/          # Django主项目配置
├── settings.py       # 数据库配置(MySQL/SQLite切换)、CORS、中间件
├── urls.py           # 路由总入口 (分myapp/admin/* 和 myapp/index/*)
└── wsgi.py

myapp/                # 业务应用
├── models.py         # ORM模型 (User, Book, Borrow, Comment等)
├── serializers.py    # DRF序列化器
├── permission/       # 权限类
├── auth/             # 认证类 (JWT-like token验证)
├── middlewares/      # 操作日志中间件
├── recommend_books/  # 推荐算法模块
├── spider/           # 豆瓣图书爬虫
└── views/
    ├── admin/        # 后台管理API (books,users,borrows,logs等CRUD)
    └── index/        # 前台用户API (查看书籍、借阅、评论、社区等)
```

**关键点**：
- 所有API返回JSON，路由格式：`/myapp/{admin|index}/{resource}/{action}`
- 认证通过检查请求头中的 `token` 或 `adminToken` header
- 错误时返回 `403` + `{"detail": "AUTH_FAIL_FRONT"}` 或 `"AUTH_FAIL_END"`

## 前后端通信协议

### API请求格式
前端在 `utils/request.js` 的拦截器中自动添加token：
```javascript
config.headers['adminToken'] = storage.get(ADMIN_TOKEN)
config.headers['token'] = storage.get(TOKEN)
```

### 常见API调用模式 (见 `api/index/book.js`)
```javascript
const api = {
  listApi: '/myapp/index/book/list',
  detailApi: '/myapp/index/book/detail',
  // ... 其他端点
}

export const listApi = (data) => axios({ url: api.listApi, method: 'get', params: data })
```

### 错误处理
- `403` + `"AUTH_FAIL_FRONT"` → 前台用户认证失败，触发 `Logout` action 并reload
- `403` + `"AUTH_FAIL_END"` → 后台管理员认证失败，触发 `AdminLogout` action 并reload

## 开发工作流

### 后端启动
```bash
cd server
pip install -r requirements.txt
python manage.py migrate          # 首次需要迁移数据库
python manage.py runserver 0.0.0.0:8000
```

### 前端启动
```bash
cd client
npm install
npm run serve                     # 开发服务 (http://localhost:8080)
npm run build                     # 打包构建 → dist/
```

**注意**：如遇npm依赖冲突，使用 `npm install --legacy-peer-deps` 或设置环保变量。

### 关键配置
- 后端API地址：修改 `client/src/store/constants.js` 中的 `BASE_URL`
- 数据库切换(MySQL/SQLite)：编辑 `server/bookproject/settings.py` 的 `DATABASES`

## 开发约定与模式

### URL路由约定
- **前台路由**：`/myapp/index/{resource}/{action}` (getList, detail, add, remove等)
- **后台路由**：`/myapp/admin/{resource}/{action}` (list, detail, create, update, delete等)
- 文件上传路径：`/upload/{category}/` (ad/, avatar/, banner/, cover/, event/, img/)

### 模型设计约定
- 所有模型使用 `db_table = "b_{resource}"` 命名规范 (前缀 `b_`)
- 主键：`BigAutoField`，支持大型系统扩展
- 时间字段：`auto_now_add=True` (创建时自动设置，后续不变)
- 状态字段：使用 `CHOICES` tuple定义枚举值 (见User model的status、role等)

### Serializer约定
- 使用 `DetailBookSerializer` 和 `UpdateBookSerializer` 分离序列化器以适应不同场景
- `to_representation()` 方法用于动态字段处理 (如豆瓣图片URL代理)
- 支持关联字段：`classification_title = serializers.ReadOnlyField(source='classification.title')`

### 状态管理约定 (Vuex)
- 分离前台(`token`, `username`, `userId`)和后台(`adminToken`, `adminUserName`)状态
- Actions处理异步逻辑 (API调用)，Mutations修改状态
- 使用 `store.dispatch('Logout')` 和 `store.dispatch('AdminLogout')` 分别处理两套认证

### API调用约定
- 所有API通过 `api/{admin|index}/{resource}.js` 文件管理
- 每个文件导出具名函数，便于组件导入和树摇
- 参数通过 `params` (GET) 或 `data` (POST) 传递

## 常见扩展点

### 添加新的管理员功能
1. 在 `server/myapp/models.py` 添加模型
2. 在 `server/myapp/serializers.py` 添加序列化器
3. 在 `server/myapp/views/admin/` 创建视图文件 (list_api, create, update, delete)
4. 在 `server/myapp/urls.py` 注册路由
5. 在 `client/src/api/admin/` 创建API客户端
6. 在 `client/src/views/admin/` 创建表格组件

### 添加前台用户功能
1. 类似上述流程，但视图文件放在 `server/myapp/views/index/`
2. API客户端放在 `client/src/api/index/`
3. 页面放在 `client/src/views/index/`

### 数据库迁移
```bash
cd server
python manage.py makemigrations   # 检测模型变化
python manage.py migrate          # 应用迁移
```

## 调试技巧

- **前端**：Vue DevTools浏览器插件查看Vuex状态，浏览器控制台检查API响应
- **后端**：Django shell (`python manage.py shell`)测试ORM查询，logs via LogMiddleware
- **跨域问题**：已在 `settings.py` 配置 `CORS_ORIGIN_ALLOW_ALL = True`

## 重要文件快速参考

| 文件 | 用途 |
|------|------|
| [client/src/store/constants.js](client/src/store/constants.js) | API基础URL和token key常量 |
| [client/src/utils/request.js](client/src/utils/request.js) | axios拦截器，token自动附加逻辑 |
| [server/bookproject/settings.py](server/bookproject/settings.py) | Django配置(DB, CORS, middleware) |
| [server/myapp/urls.py](server/myapp/urls.py) | 后端路由总映射 |
| [server/myapp/models.py](server/myapp/models.py) | 所有业务模型定义 |
| [client/src/store/modules/user.js](client/src/store/modules/user.js) | 前后台认证状态管理 |
