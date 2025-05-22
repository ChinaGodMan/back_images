import requests
import os

TOKEN = os.getenv('SM_MS_TOKEN')
url = "https://sm.ms/api/v2/upload_history"
headers = {
    "Authorization": TOKEN
}
page = 1
all_data = []

while True:
    params = {"page": page}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        all_data.extend(data['data'])
        print(f"第 {page} 页获取到 {len(data['data'])} 条记录")
        total_pages = data.get('TotalPages', 1)
        print(f"总页数: {total_pages}")
        if page >= total_pages:
            break
        page += 1
    else:
        print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
        break


def download_file(url, filename):
    filename = filename.lower()
    filepath = os.path.join("images", filename)
    if os.path.exists(filepath):
        name, ext = os.path.splitext(filename)
        orgin = name
        name, ext = os.path.splitext(url)
        new_filename = name.split('/')[-1]
        new_filename = f"{orgin}_{new_filename}{ext}"
        filepath = os.path.join("images", new_filename)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"文件已保存：{filename}")
    else:
        print(f"下载失败，状态码：{response.status_code}")


print(f"总计获取到 {len(all_data)} 条记录")
c = 0
if not os.path.exists("images"):
    os.makedirs("images")
for item in all_data:
    filename = item['filename']
    url = item['url']
    c = c + 1

    download_file(url, filename)
    print(f"第 {c} 个文件: {filename}, URL: {url} 下载完成")
