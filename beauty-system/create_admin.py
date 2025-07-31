from app import app, db, User

def create_admin():
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        # 检查是否已存在管理员账户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # 创建管理员账户（使用明文密码，与主应用保持一致）
            admin = User(
                username='admin',
                password='admin123'
            )
            db.session.add(admin)
            db.session.commit()
            print("管理员账户创建成功！")
            print("用户名: admin")
            print("密码: admin123")
        else:
            print("管理员账户已存在！")

if __name__ == '__main__':
    create_admin() 