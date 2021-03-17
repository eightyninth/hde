from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np


def bool_word_exist(table, word):
    rows = table.rowCount()
    bool_exist = False
    for row in range(rows):
        if table.item(row, 0).text() == word:
            bool_exist = True
            break
    return bool_exist

def delete_word_exist(table, word):
    rows = table.rowCount()
    for row in range(rows):
        if table.item(row, 0).text() == word:
            table.removeRow(row)
            break

def word_hde_finish(table, find_word, set_word):
    rows = table.rowCount()
    for row in range(rows):

        if table.item(row, 0).text() == find_word:
            table.item(row, 1).setText(set_word)
            break


def word_save_finish(table, find_word, set_word):
    rows = table.rowCount()
    for row in range(rows):

        if table.item(row, 0).text() == find_word:
            table.item(row, 2).setText(set_word)
            break


alpha = 0.5
beta = -0.001
lambda_ = 0.5  # lambda 是 python 关键字


def calculate_impact_value(parent_node):
    # 记录层次
    level_node = 0
    parent = parent_node
    while parent.parent() is not None:
        parent = parent.parent()
        level_node += 1

    impact_value_1 = alpha ** level_node
    impact_value_2 = 0

    parent = parent_node
    for level in range(level_node):
        if level == 0:
            index = parent.parent().childCount()
        else:
            if parent.parent() is None:
                index = parent.indexOfTopLevelItem(parent) + 1
            else:
                index = parent.parent().indexOfChild(parent) + 1
        impact_value_2 += (alpha ** (level_node - level)) * beta * index
        parent = parent.parent()

    return impact_value_1 + impact_value_2


def calculate_word_hde(radical_json, vector_list):
    # print("hde")
    hde_list = []
    for vector in vector_list:
        hde_list.append([radical_json[vector[0]], float(vector[1])])

    # print(hde_list)

    hde_vector = np.zeros(len(radical_json))
    for hde in hde_list:
        hde_onehot = np.eye(len(radical_json))[hde[0]]
        hde_onehot *= hde[1]
        if hde[0] >= 12:
            hde_vector += hde_onehot
        else:
            hde_vector += hde_onehot * lambda_

    return hde_vector
