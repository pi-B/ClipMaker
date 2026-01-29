from PyQt6.QtWidgets import QComboBox
from collections import OrderedDict

def update_combobox_values(list_value : list, comb: QComboBox) -> QComboBox :
    od = OrderedDict(sorted(list_value))
    current_value = comb.currentText()
    comb.clear()
    for cat in od:
        comb.addItem(cat)
    comb.setCurrentText(current_value)
    return comb