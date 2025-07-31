from app import app, db, User

def check_admin():
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"管理员用户信息:")
            print(f"ID: {admin.id}")
            print(f"用户名: {admin.username}")
            print(f"密码: {admin.password}")
            print(f"创建时间: {admin.created_at}")
        else:
            print("管理员用户不存在")

if __name__ == '__main__':
    check_admin() 