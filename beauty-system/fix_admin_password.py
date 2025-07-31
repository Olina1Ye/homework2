from app import app, db, User

def fix_admin_password():
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if admin:
            # 设置管理员密码
            admin.password = 'admin123'
            db.session.commit()
            print("管理员密码已修复为: admin123")
        else:
            print("管理员用户不存在")

if __name__ == '__main__':
    fix_admin_password() 