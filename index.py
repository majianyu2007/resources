import os
import time

def format_size(size):
    # 格式化文件大小为常用单位（B，KB，MB，GB）
    if size < 1024:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024**3:
        return f"{size / (1024**2):.2f} MB"
    else:
        return f"{size / (1024**3):.2f} GB"

def generate_index_html(directory):
    # 获取目录下的文件和子目录
    contents = os.listdir(directory)

    # 排序目录内容，首先显示子目录，然后是文件
    contents.sort(key=lambda item: (not os.path.isdir(os.path.join(directory, item)), item.lower()))

    with open(os.path.join(directory, 'index.html'), 'w', encoding='utf-8') as index_file:
        index_file.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n')
        index_file.write('<html>\n')
        index_file.write(' <head>\n')
        if directory == current_directory:  # 根目录
            index_file.write('  <title>Index of /</title>\n')
        else:
            index_file.write('  <title>Index of /{0}</title>\n'.format(directory.split(os.sep)[-1]))
        index_file.write(' </head>\n')
        index_file.write(' <body>\n')
        if directory == current_directory:  # 根目录
            index_file.write('<h1>Index of /</h1>\n')
        else:
            index_file.write(f'<h1>Index of /{directory.split(os.sep)[-1]}</h1>\n')
        index_file.write('<table><tr><th>Name</th><th>Last modified</th><th>Size</th></tr><tr><th colspan="3"><hr></th></tr>\n')

        for item in contents:
            if item != 'index.py' and item != 'index.html':  # 排除 index.py 和 index.html
                item_path = os.path.join(directory, item)
                item_name = item if os.path.isdir(item_path) else item
                item_modified = time.strftime('%d-%b-%Y %H:%M', time.gmtime(os.path.getmtime(item_path)))
                item_size = format_size(os.path.getsize(item_path)) if os.path.isfile(item_path) else '-'

                if os.path.isdir(item_path):
                    item_name += '/'
                    item_link = item_name
                else:
                    item_link = item

                index_file.write(f'<tr><td><a href="{item_link}">{item_name}</a></td><td align="right">{item_modified}</td><td align="right">{item_size}</td></tr>\n')

        index_file.write('<tr><th colspan="3"><hr></th></tr>\n')
        index_file.write('</table>\n')
        index_file.write('</body></html>\n')

# 获取当前目录
current_directory = os.getcwd()

# 为当前目录生成index.html
generate_index_html(current_directory)

# 遍历当前目录下的所有子目录并生成index.html
for root, dirs, files in os.walk(current_directory):
    for directory in dirs:
        generate_index_html(os.path.join(root, directory))