# 清理重复图片脚本
# python imageCleaning.py
import os
import re

def get_referenced_images(md_dir, img_subdir):
    """获取Markdown文件中引用的所有图片路径"""
    referenced_images = set()
    for root, dirs, files in os.walk(md_dir):
        for file in files:
            if file.endswith('.md'):
                md_file_path = os.path.join(root, file)
                with open(md_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 查找图片链接，并假定链接以 '/imgs/' 开头
                    image_links = re.findall(r'!\[.*?\]\(/imgs/(.*?)\)', content)
                    referenced_images.update(image_links)
    return referenced_images

def remove_unused_images(img_dir, referenced_images):
    """移除目录中未被Markdown文件引用的图片"""
    for root, dirs, files in os.walk(img_dir):
        for file in files:
            img_path = os.path.join(root, file)
            # 如果图片路径不在引用的图片集合中，则删除它
            if os.path.relpath(img_path, img_dir) not in referenced_images:
                try:
                    os.remove(img_path)
                    print(f"Removed unused image: {img_path}")
                except OSError as e:
                    print(f"Error removing image: {e.strerror}. {img_path}")

# 设置路径
#md_directory = 'E:\\test\\zfile1' # Markdown文件文件夹路径
#img_directory = 'E:\\test\\imgs'  # 图片所在目录路径

# person_blog_new
md_directory = "E:\\OneDrive - shjd\\github\\person_blog_new\\source\\_posts"
img_directory = "E:\\OneDrive - shjd\\github\\person_blog_new\\source\\imgs"
img_subdir = os.path.relpath(img_directory, md_directory)  # 图片目录相对于Markdown文件目录的路径

# 获取Markdown文件中引用的图片路径
referenced_images = get_referenced_images(md_directory, img_subdir)

# 移除未引用的图片
remove_unused_images(img_directory, referenced_images)