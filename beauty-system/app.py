from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, Product, Review, User, CartItem, Order, OrderItem  # 补充导入所有模型
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.secret_key = 'a_random_secret_key_for_session_123'  # 用于session加密
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beauty.db'  # 数据库文件
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 新增session相关配置
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # 本地开发用

CATEGORY_DATA = [
    {"id": 1, "name": "全部"},
    {"id": 2, "name": "彩妆"},
    {"id": 3, "name": "护肤"},
    {"id": 4, "name": "香水"},
    {"id": 5, "name": "美妆工具"},
    {"id": 6, "name": "男士美妆"},
]
HOT_TAGS = [
    "口红", "粉底液", "洁面", "精华", 
    "控油", "敏感肌", "哑光", "保湿"
]

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beauty.db'  # 使用SQLite数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)
csrf = CSRFProtect(app)

# 配置CSRF豁免
@csrf.exempt
def csrf_exempt():
    pass

# 创建数据库表（首次运行时需要）
with app.app_context():
    db.create_all()
    # 检查是否有商品数据，如果没有则添加一些测试数据
    if not Product.query.first():
        products = [
             # 彩妆类
            Product(name="水光唇釉", price=129.0, image="/static/images/chunyou.jpg", description="水生透橘色，原生气血感", category="彩妆", 
                   brand="Beauty Plus", origin="中国", shelf_life="3年", net_weight="3.5g", 
                   ingredients="水、甘油、聚二甲基硅氧烷、辛酸/癸酸甘油三酯", 
                   usage="取适量涂抹于双唇，打造水润光泽效果"),
            
            Product(name="丝绒哑光口红", price=89.0, image="/static/images/yaguang.jpg", description="持久不脱色，多种色号可选", category="彩妆",
                   brand="Beauty Plus", origin="中国", shelf_life="3年", net_weight="3.8g",
                   ingredients="蓖麻油、蜂蜡、羊毛脂、氧化铁", 
                   usage="直接涂抹于双唇，打造哑光质感妆容"),
            
            Product(name="轻薄粉底液", price=159.0, image="/static/images/fendi.jpg", description="轻薄自然，遮瑕效果好", category="彩妆",
                   brand="Beauty Plus", origin="中国", shelf_life="2年", net_weight="30ml",
                   ingredients="水、甘油、二氧化钛、氧化锌", 
                   usage="取适量点涂于面部，用海绵或手指均匀推开"),
            
            Product(name="十二色眼影盘", price=199.0, image="/static/images/yanying.jpg", description="12色眼影，易上色不飞粉", category="彩妆",
                   brand="Beauty Plus", origin="中国", shelf_life="3年", net_weight="12g",
                   ingredients="滑石粉、云母、氧化铁、二氧化钛", 
                   usage="使用眼影刷蘸取适量眼影，涂抹于眼睑部位"),
            
            Product(name="粉状腮红", price=199.0, image="/static/images/saihong.jpg", description="杏粉色腮红，少女感满满", category="彩妆",
                   brand="Beauty Plus", origin="中国", shelf_life="3年", net_weight="4g",
                   ingredients="滑石粉、云母、氧化铁、二氧化钛", 
                   usage="使用腮红刷蘸取适量，轻扫于颧骨位置"),
            
            # 护肤类
            Product(name="氨基酸洁面乳", price=99.0, image="/static/images/ximiannai.jpg", description="温和清洁，适合敏感肌", category="护肤",
                   brand="Beauty Plus", origin="中国", shelf_life="3年", net_weight="100ml",
                   ingredients="水、椰油酰甘氨酸钠、甘油、透明质酸钠", 
                   usage="取适量于掌心，加水揉搓起泡，轻柔按摩面部后冲洗"),
            
            Product(name="焕活精华液", price=239.0, image="/static/images/jinghua.jpg", description="修护肌肤，提亮肤色", category="护肤",
                   brand="Beauty Plus", origin="中国", shelf_life="2年", net_weight="30ml",
                   ingredients="水、烟酰胺、透明质酸钠、维生素E", 
                   usage="洁面后取2-3滴，轻拍至完全吸收"),
            
            Product(name="保湿补水面膜", price=39.0, image="/static/images/mianmo.jpg", description="单片装，深层补水", category="护肤",
                   brand="Beauty Plus", origin="中国", shelf_life="3年", net_weight="25ml",
                   ingredients="水、甘油、透明质酸钠、芦荟提取物", 
                   usage="洁面后敷于面部15-20分钟，取下后轻拍至吸收"),
            
            Product(name="控油爽肤水", price=89.0, image="/static/images/shui.jpg", description="平衡油脂，收缩毛孔", category="护肤",
                   brand="Beauty Plus", origin="中国", shelf_life="2年", net_weight="150ml",
                   ingredients="水、金缕梅提取物、薄荷提取物、甘油", 
                   usage="洁面后取适量于化妆棉，轻拍于面部"),
            
            Product(name="修护面霜", price=189.0, image="/static/images/minxiuhu.jpg", description="夜间修护，适合干性肌肤", category="护肤",
                   brand="Beauty Plus", origin="中国", shelf_life="2年", net_weight="50g",
                   ingredients="水、甘油、角鲨烷、神经酰胺", 
                   usage="晚间护肤最后一步，取适量均匀涂抹于面部"),
            
            # 香水类
            Product(name="清新花果香水", price=299.0, image="/static/images/dior.jpg", description="前调柑橘，中调玫瑰", category="香水",
                   brand="Beauty Plus", origin="法国", shelf_life="5年", net_weight="50ml",
                   ingredients="酒精、香精、水", 
                   usage="喷洒于手腕、颈部等脉搏处，让香气自然散发"),
            
            Product(name="木质调男士香水", price=349.0, image="/static/images/weilan.jpg", description="檀香基调，持久留香", category="香水",
                   brand="Beauty Plus", origin="法国", shelf_life="5年", net_weight="100ml",
                   ingredients="酒精、香精、檀香精油", 
                   usage="喷洒于手腕、颈部，适合商务场合使用"),
            
            Product(name="淡香水喷雾", price=199.0, image="/static/images/lv.jpg", description="清新淡雅，适合日常使用", category="香水",
                   brand="Beauty Plus", origin="法国", shelf_life="3年", net_weight="30ml",
                   ingredients="酒精、香精、水", 
                   usage="轻喷于衣物或身体，适合日常使用"),
            
            # 美妆工具类
            Product(name="化妆刷套装", price=29.0, image="/static/images/shua.jpg", description="10支装，含腮红刷、眼影刷", category="美妆工具",
                   brand="Beauty Plus", origin="中国", shelf_life="长期", net_weight="套装",
                   ingredients="人造纤维毛、木柄", 
                   usage="根据妆容需要选择合适的刷具，轻柔使用"),
            
            Product(name="粉扑套装", price=39.0, image="/static/images/fenpu.jpg", description="3个装，干湿两用", category="美妆工具",
                   brand="Beauty Plus", origin="中国", shelf_life="长期", net_weight="套装",
                   ingredients="海绵、聚氨酯", 
                   usage="干用可定妆，湿用可上粉底，定期清洗保持卫生"),
            
            # 男士美妆类
            Product(name="男士素颜霜", price=159.0, image="/static/images/suyan.jpg", description="自然提亮，均匀肤色", category="男士美妆",
                   brand="Beauty Plus", origin="中国", shelf_life="2年", net_weight="30ml",
                   ingredients="水、二氧化钛、甘油、透明质酸钠", 
                   usage="洁面后取适量均匀涂抹于面部，打造自然裸妆效果")
        ]
        db.session.add_all(products)
        db.session.commit()

# 路由定义
@app.route('/')
def index():
    # 获取筛选参数
    category_id = request.args.get('category')  # 分类ID
    tag = request.args.get('tag')  # 标签
    
    # 基础查询
    query = Product.query
    
    # 分类筛选（CATEGORY_DATA中"全部"的id是1，不筛选）
    if category_id and category_id != '1':
        # 找到对应分类名称
        category_name = next((c['name'] for c in CATEGORY_DATA if str(c['id']) == category_id), None)
        if category_name:
            query = query.filter_by(category=category_name)
    
    # 标签筛选（模糊匹配商品名称或描述）
    if tag:
        query = query.filter(
            (Product.name.like(f'%{tag}%')) | 
            (Product.description.like(f'%{tag}%'))
        )
    
    # 执行查询
    products = query.all()
    
    cart_count = 0
    if 'user_id' in session:
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        cart_count = sum(item.quantity for item in cart_items)
    
    return render_template(
        'index.html', 
        products=products,
        categories=CATEGORY_DATA,
        hot_tags=HOT_TAGS,
        current_category=category_id,
        current_tag=tag,
        cart_count=cart_count  # 添加购物车数量
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Debug: 登录尝试 - 用户名: {username}, 密码: {password}")

        user = User.query.filter_by(username=username).first()
        if user:
            print(f"Debug: 数据库中用户: {user.username}, 密码: {user.password}")
        else:
            print("Debug: 数据库中无此用户")

        if user and user.password == password:  # 明文比较
            session['user_id'] = user.id
            session['username'] = user.username
            print(f"Debug: 登录成功 - session: {dict(session)}")
            return redirect(url_for('index'))
        else:
            print(f"Debug: 登录失败 - 用户不存在或密码错误")
            return "用户名或密码错误，请重试"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return "用户名已存在，请更换"
        
        # 创建新用户
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# 产品详情页路由
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # 获取产品详情
    product = Product.query.get_or_404(product_id)
    
    # 获取产品库存
    stock = product.stock  # 从数据库获取实际库存
    
    # 从数据库查询评论
    reviews = Review.query.filter_by(product_id=product_id).all()
    
    # 计算购物车商品总数
    cart_count = 0
    if 'user_id' in session:
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        cart_count = sum(item.quantity for item in cart_items)
    
    # 找到产品对应的分类ID
    category_id = next((c['id'] for c in CATEGORY_DATA if c['name'] == product.category), 1)
    
    return render_template(
        'product_detail.html',
        product=product,
        stock=stock,
        reviews=reviews,
        categories=CATEGORY_DATA,
        cart_count=cart_count,  # 传递购物车数量到模板
        category_id=category_id  # 传递分类ID
    )

# 购买页面路由
@app.route('/checkout/<int:product_id>/<int:quantity>')
def checkout(product_id, quantity):
    if 'user_id' not in session:
        return redirect(url_for('login', next=url_for('checkout', product_id=product_id, quantity=quantity)))
    
    product = Product.query.get_or_404(product_id)
    total_price = product.price * quantity
    
    return render_template(
        'checkout.html',
        product=product,
        quantity=quantity,
        total_price=total_price
    )

# 处理支付路由
@app.route('/process_payment/<int:product_id>/<int:quantity>', methods=['POST'])
def process_payment(product_id, quantity):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': '请先登录'})
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '请求数据无效'})
        
        # 验证收货信息
        required_fields = ['recipient', 'phone', 'address', 'payment_method']
        if not all(k in data for k in required_fields):
            return jsonify({'status': 'error', 'message': '请填写完整收货信息'})
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'status': 'error', 'message': '商品不存在'})
        
        if product.stock < quantity:
            return jsonify({'status': 'error', 'message': '库存不足'})
        
        # 创建订单
        total_amount = product.price * quantity
        order = Order(
            user_id=session['user_id'],
            total_amount=total_amount,
            status='completed',
            recipient=data['recipient'],
            phone=data['phone'],
            address=data['address'],
            payment_method=data['payment_method']
        )
        db.session.add(order)
        db.session.flush()  # 获取订单ID
        
        # 创建订单项
        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity,
            price=product.price
        )
        db.session.add(order_item)
        
        # 更新库存
        product.stock -= quantity
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '支付成功，订单已提交',
            'redirect_url': url_for('index')
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'支付处理失败: {str(e)}'})

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取当前用户的购物车商品
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    total_price = 0
    # 计算总价并保留商品信息
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            item.product = product
            total_price += product.price * item.quantity
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': '请先登录'})
        
        # 获取数量参数，默认为1
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '请求数据无效'})
        
        quantity = data.get('quantity', 1)
        product_id = data.get('product_id')
        user_id = session['user_id']
        
        print(f"Debug: user_id={user_id}, product_id={product_id}, quantity={quantity}")
        
        if not product_id:
            return jsonify({'status': 'error', 'message': '商品ID无效'})
        
        # 检查商品是否存在
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'status': 'error', 'message': '商品不存在'})
        
        # 检查库存
        if product.stock < quantity:
            return jsonify({'status': 'error', 'message': '库存不足'})
        
        # 检查购物车中是否已有该商品
        cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity  # 已有则增加数量
        else:
            cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        
        db.session.commit()
        
        # 计算购物车总数量
        cart_count = sum(item.quantity for item in CartItem.query.filter_by(user_id=user_id).all())
        
        return jsonify({
            'status': 'success', 
            'message': '已加入购物车',
            'cart_count': cart_count
        })
    except Exception as e:
        print(f"Error in add_to_cart: {str(e)}")
        return jsonify({'status': 'error', 'message': f'服务器错误: {str(e)}'})

# 更新购物车商品数量
@app.route('/update_cart/<int:item_id>', methods=['POST'])  # 改为POST方法
def update_cart(item_id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': '请先登录'})
    
    data = request.get_json()
    change = data.get('change', 0)  
    if change == 0:
        return jsonify({
            'status': 'error',
            'message': '无效的数量变更'
        })
    
    cart_item = CartItem.query.filter_by(
        id=item_id, 
        user_id=session['user_id']
    ).first()
    
    if not cart_item:
        return jsonify({
            'status': 'error',
            'message': '购物车商品不存在'
        })
    
    # 检查库存
    new_quantity = cart_item.quantity + change
    if new_quantity < 1:
        return jsonify({
            'status': 'error',
            'message': '数量不能小于1'
        })
    
    if new_quantity > cart_item.product.stock:
        return jsonify({
            'status': 'error',
            'message': '库存不足'
        })
    
    cart_item.quantity = new_quantity
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': '数量已更新'
    })

@app.route('/cart_checkout')
def cart_checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    if not cart_items:
        return redirect(url_for('cart'))
    
    total_price = 0
    # 获取商品详情并计算总价
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            item.product = product
            total_price += product.price * item.quantity
    
    return render_template('cart_checkout.html', cart_items=cart_items, total_price=total_price)

@app.route('/process_cart_payment', methods=['POST'])
def process_cart_payment():
    try:
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': '请先登录'})
        
        data = request.get_json()
        print(f"Debug: Received payment data: {data}")
        
        # 验证收货信息
        if not data:
            return jsonify({'status': 'error', 'message': '请求数据无效'})
        
        required_fields = ['recipient', 'phone', 'address', 'payment_method']
        if not all(k in data for k in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            return jsonify({'status': 'error', 'message': f'请填写完整收货信息，缺少: {", ".join(missing_fields)}'})
        
        # 获取用户购物车商品
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        if not cart_items:
            return jsonify({'status': 'error', 'message': '购物车为空'})
        
        print(f"Debug: Found {len(cart_items)} items in cart")
        
        # 计算总金额
        total_amount = 0
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if product:
                total_amount += product.price * item.quantity
        
        # 创建订单
        order = Order(
            user_id=session['user_id'],
            total_amount=total_amount,
            status='completed',
            recipient=data['recipient'],
            phone=data['phone'],
            address=data['address'],
            payment_method=data['payment_method']
        )
        db.session.add(order)
        db.session.flush()  # 获取订单ID
        
        # 检查库存并创建订单项
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if not product:
                return jsonify({'status': 'error', 'message': f'商品不存在 (ID: {item.product_id})'})
            
            if product.stock < item.quantity:
                return jsonify({'status': 'error', 'message': f'商品 {product.name} 库存不足 (当前: {product.stock}, 需要: {item.quantity})'})
            
            # 创建订单项
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price
            )
            db.session.add(order_item)
            
            # 更新库存
            product.stock -= item.quantity
        
        # 清空购物车
        for item in cart_items:
            db.session.delete(item)
        
        db.session.commit()
        print("Debug: Payment processed successfully")
        
        return jsonify({
            'status': 'success',
            'message': '支付成功，订单已提交',
            'redirect_url': url_for('index')
        })
        
    except Exception as e:
        print(f"Error in process_cart_payment: {str(e)}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'支付处理失败: {str(e)}'})

# 检查用户登录状态
@app.route('/check_login')
def check_login():
    return jsonify({
        'logged_in': 'user_id' in session
    })

# 后台管理路由
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    # 获取统计数据
    total_products = Product.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    # 获取最近订单
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # 获取热门商品（按销量排序）
    popular_products = db.session.query(
        Product, 
        db.func.sum(OrderItem.quantity).label('sales_count')
    ).join(OrderItem).group_by(Product.id).order_by(
        db.func.sum(OrderItem.quantity).desc()
    ).limit(5).all()
    
    stats = {
        'total_products': total_products,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue
    }
    
    return render_template('admin_dashboard.html', 
                         stats=stats, 
                         recent_orders=recent_orders, 
                         popular_products=popular_products)

@app.route('/admin/products')
def admin_products():
    if 'user_id' not in session or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    products = Product.query.all()
    return render_template('admin_products.html', products=products)

@app.route('/admin/add_product', methods=['POST'])
@csrf.exempt
def admin_add_product():
    print('当前 session:', dict(session))
    if 'user_id' not in session or session.get('username') != 'admin':
        return jsonify({'status': 'error', 'message': '权限不足'})
    
    try:
        data = request.get_json()
        print(f"Debug: 接收到的数据: {data}")
        
        if not data:
            return jsonify({'status': 'error', 'message': '请求数据无效'})
        
        # 验证必需字段
        required_fields = ['name', 'price', 'image', 'category', 'stock']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'status': 'error', 'message': f'字段 {field} 不能为空'})
        
        new_product = Product(
            name=data['name'],
            price=float(data['price']),
            image=data['image'],
            description=data.get('description', ''),
            category=data['category'],
            stock=int(data['stock']),
            brand=data.get('brand', ''),
            origin=data.get('origin', ''),
            shelf_life=data.get('shelf_life', ''),
            net_weight=data.get('net_weight', ''),
            ingredients=data.get('ingredients', ''),
            usage=data.get('usage', '')
        )
        db.session.add(new_product)
        db.session.commit()
        print(f"Debug: 商品添加成功，ID: {new_product.id}")
        return jsonify({'status': 'success', 'message': '商品添加成功'})
    except Exception as e:
        print(f"Debug: 添加商品时出错: {str(e)}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'添加失败: {str(e)}'})

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@csrf.exempt
def admin_delete_product(product_id):
    print('当前 session:', dict(session))
    if 'user_id' not in session or session.get('username') != 'admin':
        return jsonify({'status': 'error', 'message': '权限不足'})
    
    try:
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'status': 'success', 'message': '商品删除成功'})
        else:
            return jsonify({'status': 'error', 'message': '商品不存在'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'删除失败: {str(e)}'})

@app.route('/admin/edit_product/<int:product_id>', methods=['POST'])
@csrf.exempt
def admin_edit_product(product_id):
    print('当前 session:', dict(session))
    if 'user_id' not in session or session.get('username') != 'admin':
        return jsonify({'status': 'error', 'message': '权限不足'})
    
    try:
        data = request.get_json()
        print(f"Debug: 编辑商品 {product_id}，接收到的数据: {data}")
        
        if not data:
            return jsonify({'status': 'error', 'message': '请求数据无效'})
        
        product = Product.query.get(product_id)
        if product:
            # 验证必需字段
            required_fields = ['name', 'price', 'image', 'category', 'stock']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'status': 'error', 'message': f'字段 {field} 不能为空'})
            
            product.name = data['name']
            product.price = float(data['price'])
            product.image = data['image']
            product.description = data.get('description', '')
            product.category = data['category']
            product.stock = int(data['stock'])
            # 更新其他字段
            product.brand = data.get('brand', '')
            product.origin = data.get('origin', '')
            product.shelf_life = data.get('shelf_life', '')
            product.net_weight = data.get('net_weight', '')
            product.ingredients = data.get('ingredients', '')
            product.usage = data.get('usage', '')
            
            db.session.commit()
            print(f"Debug: 商品 {product_id} 更新成功")
            return jsonify({'status': 'success', 'message': '商品更新成功'})
        else:
            return jsonify({'status': 'error', 'message': '商品不存在'})
    except Exception as e:
        print(f"Debug: 编辑商品时出错: {str(e)}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'更新失败: {str(e)}'})

@app.route('/admin/get_product/<int:product_id>')
def admin_get_product(product_id):
    if 'user_id' not in session or session.get('username') != 'admin':
        return jsonify({'status': 'error', 'message': '权限不足'})
    
    try:
        product = Product.query.get(product_id)
        if product:
            return jsonify({
                'status': 'success',
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': product.image,
                    'description': product.description,
                    'category': product.category,
                    'stock': product.stock,
                    'brand': product.brand,
                    'origin': product.origin,
                    'shelf_life': product.shelf_life,
                    'net_weight': product.net_weight,
                    'ingredients': product.ingredients,
                    'usage': product.usage
                }
            })
        else:
            return jsonify({'status': 'error', 'message': '商品不存在'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'获取失败: {str(e)}'})

@app.route('/admin/orders')
def admin_orders():
    if 'user_id' not in session or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    # 获取所有订单，按创建时间倒序排列
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/users')
def admin_users():
    if 'user_id' not in session or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/categories')
def admin_categories():
    if 'user_id' not in session or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    # 暂时返回空页面
    return render_template('admin_categories.html', categories=[])

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if 'user_id' not in session or session.get('username') != 'admin':
        return jsonify({'status': 'error', 'message': '权限不足'})
    
    try:
        user = User.query.get(user_id)
        if user and user.username != 'admin':
            db.session.delete(user)
            db.session.commit()
            return jsonify({'status': 'success', 'message': '用户删除成功'})
        else:
            return jsonify({'status': 'error', 'message': '用户不存在或不能删除管理员'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'删除失败: {str(e)}'})

@app.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
def admin_update_order_status(order_id):
    if 'user_id' not in session or session.get('username') != 'admin':
        return jsonify({'status': 'error', 'message': '权限不足'})
    
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'status': 'error', 'message': '请求数据无效'})
        
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'status': 'error', 'message': '订单不存在'})
        
        order.status = data['status']
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': '订单状态更新成功'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'更新失败: {str(e)}'})

# 确保在app.py中有以下路由
@app.route('/submit_review/<int:product_id>', methods=['POST'])
def submit_review(product_id):
    """处理商品评论提交"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401  # 未授权状态码
        
        # 获取JSON数据
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({
                'status': 'error',
                'message': '评论内容不能为空'
            }), 400  # 错误请求状态码
        
        content = data['content'].strip()
        if not content:
            return jsonify({
                'status': 'error',
                'message': '评论内容不能为空'
            }), 400
        
        # 检查商品是否存在
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'status': 'error',
                'message': '商品不存在'
            }), 404  # 未找到状态码
        
        # 创建新评论
        new_review = Review(
            product_id=product_id,
            user_id=session['user_id'],
            content=content,
            rating=5  # 可以根据实际需求修改为用户评分
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '评论发表成功'
        }), 200  # 成功状态码
        
    except Exception as e:
        # 捕获所有异常并记录
        db.session.rollback()
        print(f"评论提交错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '服务器错误，评论提交失败'
        }), 500  # 服务器错误状态码

# 从购物车移除商品
@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'user_id' not in session:
        return jsonify({
            'status': 'error',
            'message': '请先登录'
        })
    
    cart_item = CartItem.query.filter_by(
        id=item_id, 
        user_id=session['user_id']
    ).first()
    
    if not cart_item:
        return jsonify({
            'status': 'error',
            'message': '购物车商品不存在'
        })
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': '商品已从购物车移除'
    })

@app.route('/test_browser')
def test_browser():
    return render_template('test_browser.html')

@csrf.exempt
@app.route('/admin/batch_update_products', methods=['POST'])
def batch_update_products():
    if 'user_id' not in session or session.get('username') != 'admin':
        return jsonify({'status': 'error', 'message': '权限不足'})
    try:
        data = request.get_json()
        updates = data.get('updates', [])
        for item in updates:
            product = Product.query.get(item['id'])
            if product:
                product.price = float(item['price'])
                product.stock = int(item['stock'])
        db.session.commit()
        return jsonify({'status': 'success', 'message': '批量保存成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'保存失败: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)