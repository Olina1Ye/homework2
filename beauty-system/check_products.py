from app import app, db, Product

def check_products():
    with app.app_context():
        products = Product.query.all()
        print(f"数据库中共有 {len(products)} 个商品:")
        for product in products:
            print(f"ID: {product.id}, 名称: {product.name}, 分类: {product.category}")

if __name__ == '__main__':
    check_products() 