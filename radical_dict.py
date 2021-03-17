from docx import Document
import numpy as np
import json


def radical_json(doc_path="./radical_num.docx", json_path="./radical_classes.json"):
    # 打开部首docx文件
    doc = Document(doc_path)

    # 读取文档中表格信息
    tables = doc.tables
    # print(tables)

    # 查看文档中表格数量
    # print("文档中表格数量: {}.".format(len(tables)))

    # 获取表格的所有单元格
    cells = []
    for table in tables:
        for cell in table._cells:
            cells.append(cell)

    # print(len(cells))

    # 读取单元格内文字
    cells_string = np.array([cell.text for cell in cells]).reshape(-1, 3)
    # print(cells_string)

    # 转换为 3 列, 但只需要前两列, 除去编号行，且按照编号顺序排列部首
    cells_string_list = []

    for string in cells_string:
        if not string[0].isdigit():
            # print(string)
            continue
        else:
            cells_string_list.append([int(string[0]) - 1, string[1]+string[0]])

    cells_string_list.sort()

    # print(len(cells_string_list))

    cells_string_dict = {k: v for v, k in cells_string_list}

    # 准备存入json文件
    with open(json_path, "w") as fw:
        fw.write(json.dumps(cells_string_dict, ensure_ascii=True, indent=4, separators=(',', ':')))

    # print(cells_string_str)


if __name__=="__main__":
    doc_path = "./radical_num.docx"
    json_path = "./radical_classes.json"
    radical_json(doc_path, json_path)
