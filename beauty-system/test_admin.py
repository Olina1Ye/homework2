#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

# 测试配置
BASE_URL = 'http://localhost:5000'

def test_add_product_direct():
    """直接测试添加商品API"""
    print("直接测试添加商品API...")
    
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
    
    response = requests.post(
        f'{BASE_URL}/admin/add_product',
        json=product_data,
        headers=headers
    )
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            print("✓ 添加商品API正常")
            return True
        else:
            print(f"✗ 添加商品API返回错误: {result.get('message')}")
            return False
    else:
        print(f"✗ 添加商品API请求失败: {response.status_code}")
        return False

def test_get_product_direct():
    """直接测试获取商品API"""
    print("\n直接测试获取商品API...")
    
    response = requests.get(f'{BASE_URL}/admin/get_product/1')
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            print("✓ 获取商品API正常")
            return True
        else:
            print(f"✗ 获取商品API返回错误: {result.get('message')}")
            return False
    else:
        print(f"✗ 获取商品API请求失败: {response.status_code}")
        return False

def test_edit_product_direct():
    """直接测试编辑商品API"""
    print("\n直接测试编辑商品API...")
    
    edit_data = {
        'name': '修改后的测试商品',
        'price': 88.88,
        'image': '/static/images/test.jpg',
        'description': '这是修改后的测试商品',
        'category': '护肤',
        'stock': 150,
        'brand': 'Modified Brand',
        'origin': '中国',
        'shelf_life': '3年',
        'net_weight': '50ml',
        'ingredients': '修改后的成分',
        'usage': '修改后的使用方法'
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f'{BASE_URL}/admin/edit_product/1',
        json=edit_data,
        headers=headers
    )
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            print("✓ 编辑商品API正常")
            return True
        else:
            print(f"✗ 编辑商品API返回错误: {result.get('message')}")
            return False
    else:
        print(f"✗ 编辑商品API请求失败: {response.status_code}")
        return False

def main():
    print("开始直接测试后台API功能...")
    
    # 测试获取商品
    test_get_product_direct()
    
    # 测试添加商品
    test_add_product_direct()
    
    # 测试编辑商品
    test_edit_product_direct()
    
    print("\n直接API测试完成")

if __name__ == '__main__':
    main() 