# Beauty System - 美妆电商系统

一个基于Flask框架开发的美妆电商网站，提供完整的在线购物体验，包括商品浏览、购物车管理、订单处理和后台管理功能。

## 🎯 项目特性

### 用户功能
- **用户注册/登录**: 支持用户账户管理
- **商品浏览**: 按分类筛选商品，支持标签搜索
- **商品详情**: 查看商品详细信息、规格参数、用户评论
- **购物车管理**: 添加商品、修改数量、删除商品
- **订单处理**: 支持直接购买和购物车批量购买
- **商品评论**: 用户可以对商品发表评论

### 管理员功能
- **数据统计**: 商品总数、用户总数、订单总数、总收入统计
- **商品管理**: 添加、编辑、删除商品，批量更新
- **订单管理**: 查看所有订单，更新订单状态
- **用户管理**: 查看用户列表，删除用户
- **分类管理**: 商品分类管理

### 技术特性
- **响应式设计**: 适配不同设备屏幕
- **实时库存**: 库存实时更新，防止超卖
- **安全支付**: 支持多种支付方式
- **数据持久化**: SQLite数据库存储
- **会话管理**: 安全的用户会话管理

## 🛠️ 技术栈

- **后端框架**: Flask
- **数据库**: SQLite + SQLAlchemy ORM
- **前端**: HTML5 + CSS3 + JavaScript
- **模板引擎**: Jinja2
- **安全**: CSRF保护

## 📦 安装说明

### 环境要求
- Python 3.7+
- pip

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd beauty-system
```

2. **安装依赖**
```bash
pip install flask flask-sqlalchemy flask-wtf
```

3. **运行应用**
```bash
python app.py
```

4. **访问应用**
打开浏览器访问 `http://localhost:5000`

## 🚀 使用指南

### 用户操作

1. **注册/登录**
   - 访问首页，点击"登录"按钮
   - 新用户点击"注册"创建账户
   - 登录后可以享受完整购物功能

2. **浏览商品**
   - 首页显示所有商品
   - 使用分类筛选（全部、彩妆、护肤、香水、美妆工具、男士美妆）
   - 点击热门标签快速搜索

3. **购买商品**
   - 点击商品进入详情页
   - 查看商品规格、成分、使用方法
   - 选择数量，点击"加入购物车"或"立即购买"

4. **购物车管理**
   - 点击购物车图标查看购物车
   - 修改商品数量或删除商品
   - 点击"结算"完成购买

5. **订单处理**
   - 填写收货信息（收货人、电话、地址）
   - 选择支付方式
   - 确认订单信息并支付

### 管理员操作

1. **管理员登录**
   - 使用管理员账户登录（用户名: admin；密码：admin123）
   - 访问 `/admin/dashboard` 进入管理后台

2. **数据概览**
   - 查看商品、用户、订单统计数据
   - 查看最近订单和热门商品

3. **商品管理**
   - 添加新商品，设置价格、库存、分类等
   - 编辑现有商品信息
   - 删除不需要的商品
   - 批量更新商品价格和库存

4. **订单管理**
   - 查看所有订单列表
   - 更新订单状态（待处理、已完成、已取消）

5. **用户管理**
   - 查看用户列表
   - 删除用户账户（不能删除管理员）

## 📁 项目结构

```
beauty-system/
├── app.py                 # 主应用文件
├── models.py             # 数据模型定义
├── extensions.py         # Flask扩展配置
├── static/              # 静态资源
│   └── images/         # 商品图片
├── templates/           # HTML模板
│   ├── index.html      # 首页
│   ├── login.html      # 登录页
│   ├── register.html   # 注册页
│   ├── product_detail.html  # 商品详情页
│   ├── cart.html       # 购物车页面
│   ├── checkout.html   # 结算页面
│   └── admin_*.html    # 管理后台页面
├── instance/           # 数据库文件
│   └── beauty.db      # SQLite数据库
└── README.md          # 项目说明文档
```

## 🗄️ 数据库模型

### User（用户）
- id: 用户ID
- username: 用户名
- password: 密码
- created_at: 创建时间

### Product（商品）
- id: 商品ID
- name: 商品名称
- price: 价格
- image: 商品图片
- description: 商品描述
- category: 商品分类
- stock: 库存数量
- brand: 品牌
- origin: 产地
- shelf_life: 保质期
- net_weight: 净含量
- ingredients: 成分
- usage: 使用方法

### CartItem（购物车项）
- id: 购物车项ID
- user_id: 用户ID
- product_id: 商品ID
- quantity: 数量

### Order（订单）
- id: 订单ID
- user_id: 用户ID
- total_amount: 总金额
- status: 订单状态
- created_at: 创建时间
- recipient: 收货人
- phone: 联系电话
- address: 收货地址
- payment_method: 支付方式

### OrderItem（订单项）
- id: 订单项ID
- order_id: 订单ID
- product_id: 商品ID
- quantity: 数量
- price: 购买时价格

### Review（评论）
- id: 评论ID
- product_id: 商品ID
- user_id: 用户ID
- content: 评论内容
- rating: 评分
- created_at: 创建时间

## 🔧 配置说明

### 数据库配置
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beauty.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

### 会话配置
```python
app.secret_key = 'a_random_secret_key_for_session_123'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

## 🛡️ 安全特性

- **CSRF保护**: 防止跨站请求伪造攻击
- **会话安全**: 安全的会话管理
- **输入验证**: 表单数据验证
- **SQL注入防护**: 使用ORM防止SQL注入

## 🚀 部署说明

### 开发环境
```bash
python app.py
```

### 生产环境
建议使用Gunicorn或uWSGI部署：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 更新日志

### v1.0.0
- 初始版本发布
- 完整的电商功能
- 管理员后台
- 用户评论系统

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

**注意**: 这是一个演示项目，生产环境使用前请确保：
- 修改默认密钥
- 配置安全的数据库
- 启用HTTPS
- 添加更多安全措施 
