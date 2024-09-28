import requests
import os
import time
import re
import json

def search_url_in_files(url, directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if url in content:
                        return True
    return False

authorization = os.environ.get('LSKY_AUTHORIZATION')
if not authorization:
    raise ValueError("环境变量 LSKY_AUTHORIZATION 未设置.")
    
base_url = 'http://127.0.0.1:9080/api/v1'

headers = {
    'Authorization': f'Bearer {authorization}',
    'Accept': 'application/json'
}

search_directory = '/Users/colin/Library/Mobile Documents/iCloud~md~obsidian/Documents/ColinVault'

# 定义进度文件的路径
progress_file = 'search_del_progress.json'

# 读取进度
def load_progress():
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {'processed_keys': [], 'current_page': 1}

# 保存进度
def save_progress(processed_keys, current_page):
    with open(progress_file, 'w') as f:
        json.dump({'processed_keys': processed_keys, 'current_page': current_page}, f)

# 加载上次的进度
progress = load_progress()
processed_keys = set(progress['processed_keys'])
current_page = progress['current_page']

while True:
    params = {
        'page': current_page,
        'order': 'newest',
        'permission': 'public'
    }
    
    print(f'请求第 {current_page} 页')
    response = requests.get(f'{base_url}/images', params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        if data['status']:
            if not data['data']['data']:  # 如果没有数据，退出循环
                print("没有更多图片数据，处理完成。")
                break
            
            page_processed = False
            for image in data['data']['data']:
                key = image['key']
                if key in processed_keys:
                    continue  # 跳过已处理的图片
                
                url = image['links']['url']
                
                if not search_url_in_files(url, os.path.expanduser(search_directory)):
                    delete_url = f'{base_url}/images/{key}'
                    delete_response = requests.delete(delete_url, headers=headers)
                    if delete_response.status_code == 200:
                        print(f'成功删除图片，key: {key}')
                        page_processed = True
                    else:
                        print(f'删除图片失败，key: {key}。状态码: {delete_response.status_code}')
                        print(f'响应内容: {delete_response.text}')
                
                processed_keys.add(key)
                #save_progress(list(processed_keys), current_page)  # 保存当前进度
                #time.sleep(1)
            save_progress(list(processed_keys), current_page)
            if not page_processed:
                # 如果这一页没有删除任何图片，移动到下一页
                if current_page < data['data']['last_page']:
                    current_page += 1
                    save_progress(list(processed_keys), current_page)
                else:
                    print("所有页面都已处理完毕，没有需要删除的图片。")
                    break
        else:
            print(f"处理出错: {data['message']}")
            break  # 如果处理出错，退出循环
    else:
        print(f"获取数据失败。状态码: {response.status_code}")
        break  # 如果请求失败，退出循环

print("处理完成。")
