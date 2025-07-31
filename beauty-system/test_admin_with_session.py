#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import re

# 测试配置
BASE_URL = 'http://localhost:5000'

def test_admin_with_session():
    """使用session测试后台功能"""
    print("开始测试后台管理功能...")
    
    session = requests.Session()
    
    # 1. 获取登录页面，提取CSRF令牌
    print("1. 获取登录页面...")
    login_page = session.get(f'{BASE_URL}/login')
    if login_page.status_code != 200:
        print("✗ 无法访问登录页面")
        return
    
    # 提取CSRF令牌
    csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', login_page.text)
    if not csrf_match:
        print("✗ 无法获取CSRF令牌")
        return
    
    csrf_token = csrf_match.group(1)
    print(f"✓ 获取到CSRF令牌: {csrf_token[:20]}...")
    
    # 2. 登录
    print("2. 执行登录...")
    login_data = {
        'username': 'admin',
        'password': 'admin123',
        'csrf_token': csrf_token
    }
    
    login_response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=True)
    print(f"登录响应状态码: {login_response.status_code}")
    
    # 3. 验证登录是否成功
    print("3. 验证登录状态...")
    admin_page = session.get(f'{BASE_URL}/admin/products')
    if admin_page.status_code == 200 and '商品管理' in admin_page.text:
        print("✓ 登录成功，可以访问后台")
    else:
        print("✗ 登录失败，无法访问后台")
        print(f"后台页面内容片段: {admin_page.text[:200]}")
        return
    
    # 4. 测试添加商品
    print("\n4. 测试添加商品...")
    product_data = {
        'name': '测试商品',
        'price': 99.99,
        'image': '/static/images/test.jpg',
        'description': '这是一个测试商品',
        'category': '彩妆',
        'stock': 100,
        'brand': 'Test Brand',
        'origin': '中国',
        'shelf_life': '2年',
        'net_weight': '30ml',
        'ingredients': '测试成分',
        'usage': '测试使用方法'
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    add_response = session.post(
        f'{BASE_URL}/admin/add_product',
        json=product_data,
        headers=headers
    )
    
    print(f"添加商品响应状态码: {add_response.status_code}")
    print(f"添加商品响应内容: {add_response.text}")
    
    if add_response.status_code == 200:
        result = add_response.json()
        if result.get('status') == 'success':
            print("✓ 添加商品成功")
        else:
            print(f"✗ 添加商品失败: {result.get('message')}")
    
    # 5. 测试获取商品
    print("\n5. 测试获取商品...")
    get_response = session.get(f'{BASE_URL}/admin/get_product/2')  # 使用ID为2的商品
    
    print(f"获取商品响应状态码: {get_response.status_code}")
    print(f"获取商品响应内容: {get_response.text}")
    
    if get_response.status_code == 200:
        result = get_response.json()
        if result.get('status') == 'success':
            print("✓ 获取商品成功")
        else:
            print(f"✗ 获取商品失败: {result.get('message')}")
    
    # 6. 测试编辑商品
    print("\n6. 测试编辑商品...")
    edit_data = {
        'name': '修改后的丝绒哑光口红',
        'price': 88.88,
        'image': '/static/images/yaguang.jpg',
        'description': '这是修改后的丝绒哑光口红',
        'category': '彩妆',
        'stock': 150,
        'brand': 'Modified Brand',
        'origin': '中国',
        'shelf_life': '3年',
        'net_weight': '3.8g',
        'ingredients': '修改后的成分',
        'usage': '修改后的使用方法'
    }
    
    edit_response = session.post(
        f'{BASE_URL}/admin/edit_product/2',  # 使用ID为2的商品
        json=edit_data,
        headers=headers
    )
    
    print(f"编辑商品响应状态码: {edit_response.status_code}")
    print(f"编辑商品响应内容: {edit_response.text}")
    
    if edit_response.status_code == 200:
        result = edit_response.json()
        if result.get('status') == 'success':
            print("✓ 编辑商品成功")
        else:
            print(f"✗ 编辑商品失败: {result.get('message')}")
    
    print("\n测试完成")

if __name__ == '__main__':
    test_admin_with_session() 