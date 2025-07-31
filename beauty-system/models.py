from extensions import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # 实际项目中应存储哈希值
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, default=100)  # 添加库存字段
    
    # 规格参数字段
    brand = db.Column(db.String(50), default="Beauty Plus")  # 品牌
    origin = db.Column(db.String(50), default="中国")  # 产地
    shelf_life = db.Column(db.String(20), default="3年")  # 保质期
    net_weight = db.Column(db.String(20))  # 净含量
    ingredients = db.Column(db.Text)  # 成分
    usage = db.Column(db.Text)  # 使用方法

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    # 关联关系，方便查询
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True, cascade='all, delete-orphan'))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 评分
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联用户，方便在模板中获取用户名
    user = db.relationship('User', backref=db.backref('reviews', lazy=True, cascade='all, delete-orphan'))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 收货信息
    recipient = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    
    # 关联关系
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # 购买时的价格
    
    # 关联关系
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True, cascade='all, delete-orphan'))
