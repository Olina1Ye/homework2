from app import app, db, User

def update_admin_password():
    with app.app_context():
        # 查找管理员账户
        admin = User.query.filter_by(username='admin').first()
        if admin:
            # 更新密码为 admin123
            admin.password = 'admin123'
            db.session.commit()
            print("管理员密码更新成功！")
            print("用户名: admin")
            print("密码: admin123")
        else:
            print("管理员账户不存在，请先创建管理员账户！")

if __name__ == '__main__':
    update_admin_password() 