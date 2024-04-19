# 导出目录结构树
# python dir_tree.py "E:\OneDrive - shjd\github\person_blog_new" 2
import os
import sys

def list_file(start_path, max_level=5):
    '''
    start_path: 需要导出文件目录树的绝对路径, 例如: /home/soma
    max_level: 限制需要统计的文件级数, 例如: 5, 即超过5级（5个文件夹）的文件就不再进行统计
    '''
    f_txt = open('./dir_tree.txt', 'w')
    for root, subdirs, files in sorted(os.walk(start_path)):
        # 对os.walk的输出进行排序可以得到跟文件夹目录一样的排序，否则会乱序
        # root, subdirs, files分别是父路径，子目录列表，子文件列表
        subdirs = sorted(subdirs)
        files = sorted(files)
        level = root.replace(start_path, '').count(os.sep)
        dir_indent = '|   ' * level + '|--'
        file_indent = '|   ' * (level + 1) + '|--'

        if level:
            f_txt.write('{}{}'.format(dir_indent, os.path.basename(root)))
            f_txt.write('\n')
        else:
            f_txt.write('{}{}'.format('|--', start_path))
            f_txt.write('\n')
        if level < max_level:
            for f in files:
                f_txt.write('{}{}'.format(file_indent, f))
                f_txt.write('\n')
    f_txt.close()

path = sys.argv[1]
max_level = int(sys.argv[2])

list_file(path, max_level)
