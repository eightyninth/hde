from PyQt5 import QtCore, QtGui, QtWidgets
import json

import utils


class VectorTree(QtWidgets.QTreeWidget):
    def __init__(self, json_file, *args, **kw):
        super(VectorTree, self).__init__(*args, **kw)
        # 添加右键目录
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 开放右键策略
        self.customContextMenuRequested.connect(self.rightMenuShow)

        self.json_file = json_file
        self.clicked.connect(self.ADMenushow)

    def ADMenushow(self, idx):
        menu = QtWidgets.QMenu(self)

        menu.addAction(QtWidgets.QAction("添加子节点", menu))
        menu.addAction(QtWidgets.QAction("修改节点", menu))
        menu.addAction(QtWidgets.QAction("删除节点", menu))

        menu.triggered.connect(self.menuSlot)

        menu.exec_(QtGui.QCursor.pos())

    # 添加右键菜单
    def rightMenuShow(self, pos):
        menu = QtWidgets.QMenu(self)

        menu.addAction(QtWidgets.QAction("添加根节点", menu))
        menu.triggered.connect(self.menuSlot)

        menu.exec_(QtGui.QCursor.pos())

    # 菜单功能实现
    def menuSlot(self, act):

        # self: vectorTree -> vectorBox
        parent_vectorBox = self.parent()
        # self: vectorTree -> vectorBox -> Radical_main
        parent_textEdit = parent_vectorBox.parent()

        if act.text() == "添加根节点":
            self.add_root(parent_vectorBox, parent_textEdit)
        if act.text() == "添加子节点":
            self.add_child()
        if act.text() == "删除节点":
            self.delete_node(parent_vectorBox, parent_textEdit)
        if act.text() == "修改节点":
            self.alter_node()

    # 添加对应文字的子节点
    def add_child(self):
        if self.topLevelItemCount() != 0:
            # print("添加子节点")
            item = self.currentItem()

            child = QtWidgets.QTreeWidgetItem(item)
            child.parent().setExpanded(True)

            child.setText(0, self.select_node())
            child.setText(1, str(utils.calculate_impact_value(child)))
            child.setSelected(True)

            # child_parent = []
            # parent = child
            #
            # while parent.parent() is not None:
            #     parent = parent.parent()
            #     child_parent.append(parent)
            #
            # # 从最顶层的根节点开始计算
            # while True:
            #     if len(child_parent) == 0:
            #         break
            #     parent_node = child_parent.pop()
        else:
            QtWidgets.QMessageBox.about(self, "警告", "请添加根节点")

    def alter_node(self):
        if self.topLevelItemCount() != 0:
            # print("修改节点")
            item = self.currentItem()
            item.setText(0, self.select_node())

        else:
            QtWidgets.QMessageBox.about(self, "警告", "请添加根节点")

    # 删除对应文字的节点
    def delete_node(self, parent_vectorBox, parent_textEdit):
        textEdit = parent_textEdit.findChild(QtWidgets.QLineEdit, 'textEdit').text()
        vectorTable = parent_vectorBox.findChild(QtWidgets.QTableWidget, 'vectorTable')

        item = self.currentItem()
        # print("删除节点")

        # 判断此节点有无子节点
        if item.childCount() != 0:
            QtWidgets.QMessageBox.about(self, "警告", "此节点仍有子节点")
        else:
            if item.parent() is None:
                self.takeTopLevelItem(0)
                utils.delete_word_exist(vectorTable, textEdit)
            else:
                item.parent().removeChild(item)

    # 添加对应文字的树根节点
    def add_root(self, parent_vectorBox, parent_textEdit):
        textEdit = parent_textEdit.findChild(QtWidgets.QLineEdit, 'textEdit').text()
        vectorTable = parent_vectorBox.findChild(QtWidgets.QTableWidget, 'vectorTable')
        if textEdit != '':
            if self.topLevelItemCount() == 0:
                if not utils.bool_word_exist(vectorTable, textEdit):
                    # 得到此时即将要拆解的字
                    # print(vectorTable)
                    # tree 添加根节点
                    root_node = QtWidgets.QTreeWidgetItem(self)
                    root_node.setText(0, self.select_node())
                    root_node.setText(1, str(1.0))
                    root_node.setSelected(True)

                    # table 添加目前文字状态(是否编码完成, 是否存储编码)
                    item = [textEdit, str(False), str(False)]
                    rowCount = vectorTable.rowCount()
                    vectorTable.insertRow(rowCount)
                    for i in range(vectorTable.columnCount()):
                        vectorTable.setItem(rowCount, i, QtWidgets.QTableWidgetItem(item[i]))
                else:
                    QtWidgets.QMessageBox.about(self, "警告", "此字符已存在")
            else:
                QtWidgets.QMessageBox.about(self, "警告", "已存在根节点")
        else:
            QtWidgets.QMessageBox.about(self, "警告", "请输入字符")

    def select_node(self):

        radical_json = json.load(open(self.json_file, "rb"))

        items = [k for k in radical_json.keys()]

        font = QtGui.QFont()
        font.setPointSize(30)

        inDlg = QtWidgets.QInputDialog(self)
        inDlg.setFont(font)
        inDlg.setInputMode(0)
        inDlg.setComboBoxItems(items)
        inDlg.setComboBoxEditable(False)
        inDlg.setWindowTitle("设置节点表示")
        inDlg.setLabelText("节点表示")

        if inDlg.exec_():
            item = inDlg.textValue()
        else:
            item = self.select_node()
        return item
