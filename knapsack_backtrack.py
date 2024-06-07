from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem,
                             QTreeWidget, QTreeWidgetItem, QVBoxLayout,
                             QWidget)


#dữ liệu đầu vào: values (giá trị của vật thứ i), weights(khối lượng của vật thứ i)
#max_weight: khối lượng lớn nhất của túi, 
#domains: là 1 list với domain[i] là mảng từ 1 -> c với c là số lượng của vật i
def backtracking(values, weights, max_weight, domains, item_0):
    total_items = len(values)
    max_val = 0
    best_weight = 0
    best_set = None

    current_option = [0] * total_items

    all_sets = []
    all_values = []
    all_weights = []

    def backtrack(i, current_value, current_weight, parent):
        nonlocal max_val, best_set, best_weight
        #nếu khối lượng hiện tại vượt quả max_weight thì quay lui
        if current_weight > max_weight:
            #giao diện
            parent.setBackground(0,QtGui.QBrush(QtGui.QColor("#EF6F6C")))
            s = set_ui(parent.text(0), "Weight exceed capacity, BACKTRACK!", weights, current_weight)
            parent.setText(0, s)
            return
        #sau khi chọn xong giá trị của total_items
        if i == total_items:
            #giao diện
            parent.setBackground(0,QtGui.QBrush(QtGui.QColor("#7FB685")))

            s = set_ui(parent.text(0), "Valid set!", weights, current_weight)
            parent.setText(0, s)

            #tìm kiếm giải pháp tốt nhất
            if current_value > max_val:
                max_val = current_value
                best_set = current_option[:]
                best_weight = current_weight
            #lưu lại tất cả các giải pháp
            all_sets.append(current_option[:])
            all_values.append(current_value)
            all_weights.append(current_weight)
        else:
            #xét các giái trị mà vật thứ i có (tưởng ứng lần lượt lấy 0, 1, 2, ... c vật i)
            for x in domains[i]:
                #gắn giá trị
                current_option[i] = x
                
                #giao diện
                string = " ".join([str(x) for x in current_option[:i + 1]])
                if x > 0:
                    st = f'Consider Item {i + 1} : ' + string + f' : adding {x} to the knapsack'
                else:
                    st = f'Consider Item {i + 1} : ' + string + f' : not adding to the knapsack'
                child = QTreeWidgetItem(parent)
                child.setText(0, st)

                #xét tiếp vật thể thứ i + 1
                backtrack(i + 1, current_value +
                    values[i]*x, current_weight + weights[i]*x, child)
                #nhánh cận
                if current_weight + weights[i]*x > max_weight:
                    break

    backtrack(0,0,0,item_0)
    return max_val, best_set, best_weight, all_sets, all_values, all_weights

def set_ui(text, results, weights, current_weight):
    #text = consider 4 : 0 1 0 0
    s1 = text.split(" : ") #s1 = ['Co', '0100]
    s2 = s1[1].split(" ") #s2 = ['0','1',...]
            
    s3 = text+ \
            "\n    weight = " + "+".join([str(int(s2[i])* weights[i]) for i in range(len(s2))]) + \
             f' = {current_weight}'\
             + f'\n \t {results}' 
    return s3