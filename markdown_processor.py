import os
import re
import oss2

# 设置连接到阿里云OSS所需参数
access_key_id = ''
access_key_secret = ''
endpoint = 'http://oss-cn-guangzhou.aliyuncs.com'  # 根据实际情况修改
bucket_name = ''

def upload_to_oss(file_path: str) -> str:
    # 创建Bucket对象并获取上传路径
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    # object_path = 'img/' + os.path.basename(file_path) # 若需要上传至特定文件夹则可以进行修改

    # 将文件上传到OSS中，并返回链接地址
    with open(file_path, 'rb') as f:
        bucket.put_object(object_path, f.read())

    return "https://" + bucket_name + "." + endpoint.replace("http://", "") + "/" + object_path

# 判断是否为图片文件（根据扩展名进行判断）
def is_image_file(file_path: str) -> bool:
    ext = os.path.splitext(file_path)[1].lower()
    return ext in ['.jpg', '.jpeg', '.png', '.gif']

# 处理Markdown文件中的图片链接函数
def process_markdown_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 匹配所有本地图片链接（![](C:/Users/11622/iCloudDrive/iCloud~md~obsidian/Orange_note/临时文件/附件...)）
        pattern = r'!\[\]\((C:/Users/11622/iCloudDrive/iCloud~md~obsidian/Orange_note/临时文件/附件/.+?)\)'
        local_image_links = re.findall(pattern, content)

    for link in local_image_links:
        # 判断是否为图片文件
        if not is_image_file(link):
            continue

        # 获取本地图片路径并读取二进制数据
        image_path = link.replace('/', '\\')

        # 上传图片到云储存库并获取链接地址
        cloud_link = upload_to_oss(image_path)

        # 替换Markdown文件中的本地图片链接为云储存库中的链接地址
        content = content.replace(link, cloud_link)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    # 处理指定目录下所有Markdown文件中的图片链接
    directory = ''  # 根据实际情况修改
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_markdown_file(file_path)