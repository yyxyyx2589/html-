def print_books_pretty(result):
    if not result:
        print("暂无图书信息")
        return

    # 1. 定义表头映射（数据库字段 -> 中文表头）
    headers = {
        'book_id': '图书编号',
        'book_name': '书名',
        'author': '作者',
        'category': '分类',
        'status': '状态'
    }

    # 2. 计算每一列的最佳宽度
    # 初始化宽度为表头的长度
    widths = {key: len(val) for key, val in headers.items()}

    # 遍历数据，如果某行数据比当前记录的宽度长，则更新宽度
    for row in result:
        for key in headers.keys():
            # 将数据转为字符串并计算长度
            val_len = len(str(row.get(key, "")))
            if val_len > widths[key]:
                widths[key] = val_len

    # 3. 增加一点间距（Padding），比如每列多加2个空格
    for key in widths:
        widths[key] += 2

    # 4. 打印表头
    header_line = ""
    for key, title in headers.items():
        # 使用动态计算出的宽度进行格式化
        header_line += f"{title:<{widths[key]}}"
    print(header_line)

    # 5. 打印分隔线 (可选，增加美观度)
    print("-" * sum(widths.values()))

    # 6. 打印数据行
    for row in result:
        row_line = ""
        for key in headers.keys():
            val = row.get(key, "")
            row_line += f"{val:<{widths[key]}}"
        print(row_line)

# --- 模拟数据测试 ---
data = [
    {'book_id': 1, 'book_name': '海', 'author': '老人', 'category': 'C', 'status': '已借出'},
    {'book_id': 3, 'book_name': '红楼梦', 'author': '孙悟空', 'category': 'A', 'status': '可借阅'},
    {'book_id': 101, 'book_name': 'Python高级编程指南', 'author': 'Guido van Rossum', 'category': 'B', 'status': '维修中'}
]

print_books_pretty(data)