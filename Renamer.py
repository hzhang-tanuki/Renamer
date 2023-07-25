from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class RenamerWindow(QtWidgets.QDialog):
    renamer_window = []
    @classmethod
    def show_dialog(cls):
        if not cls.renamer_window:
            cls.renamer_window = RenamerWindow()

        if cls.renamer_window.isHidden():
            cls.renamer_window.show()
        else:
            cls.renamer_window.raise_()
            cls.renamer_window.activateWindow()



    def __init__(self, parent=maya_main_window()):
        super(RenamerWindow, self).__init__(parent)

        self.setWindowTitle('Renamer')
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        # self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.prefix_check_box = QtWidgets.QCheckBox("Prefix")
        self.prefix_lineedit = QtWidgets.QLineEdit()
        self.prefix_lineedit_label = QtWidgets.QLabel("Prefix: ")
        self.prefix_lineedit_label.setVisible(False)
        self.prefix_lineedit.setVisible(False)

        self.suffix_check_box = QtWidgets.QCheckBox("Suffix")
        self.suffix_lineedit = QtWidgets.QLineEdit()
        self.suffix_lineedit_label = QtWidgets.QLabel("Suffix: ")
        self.suffix_lineedit.setVisible(False)
        self.suffix_lineedit_label.setVisible(False)

        self.search_replace_check_box = QtWidgets.QCheckBox("Search & Replace")
        self.search_lineedit = QtWidgets.QLineEdit()
        self.search_lineedit_label = QtWidgets.QLabel("Search: ")
        self.search_lineedit.setVisible(False)
        self.search_lineedit_label.setVisible(False)

        self.replace_lineedit = QtWidgets.QLineEdit()
        self.replace_lineedit_label = QtWidgets.QLabel("Replace: ")
        self.replace_lineedit.setVisible(False)
        self.replace_lineedit_label.setVisible(False)

        self.index_check_box = QtWidgets.QCheckBox("Index")
        self.index_lineedit = QtWidgets.QLineEdit()
        self.index_lineedit_label = QtWidgets.QLabel("Index: ")
        self.index_explaination_lineedit_label = QtWidgets.QLabel("place {} where yiou want the index to be added")

        self.index_lineedit.setVisible(False)
        self.index_lineedit_label.setVisible(False)
        self.index_explaination_lineedit_label.setVisible(False)

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        checkbox_layout = QtWidgets.QGridLayout()

        checkbox_layout.addWidget(self.index_check_box, 0, 0)
        checkbox_layout.addWidget(self.search_replace_check_box, 0, 1)
        checkbox_layout.addWidget(self.prefix_check_box, 1, 0)
        checkbox_layout.addWidget(self.suffix_check_box, 1, 1)

        prefix_layout = QtWidgets.QHBoxLayout()
        prefix_layout.addWidget(self.prefix_lineedit_label)
        prefix_layout.addWidget(self.prefix_lineedit)

        suffix_layout = QtWidgets.QHBoxLayout()
        suffix_layout.addWidget(self.suffix_lineedit_label)
        suffix_layout.addWidget(self.suffix_lineedit)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(self.search_lineedit_label)
        search_layout.addWidget(self.search_lineedit)

        replace_layout = QtWidgets.QHBoxLayout()
        replace_layout.addWidget(self.replace_lineedit_label)
        replace_layout.addWidget(self.replace_lineedit)

        search_replace_layout = QtWidgets.QVBoxLayout()
        spacer_item = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        search_replace_layout.addItem(spacer_item)
        search_replace_layout.addLayout(search_layout)
        search_replace_layout.addLayout(replace_layout)

        index_layout = QtWidgets.QVBoxLayout()
        index_layout.addWidget(self.index_lineedit_label)
        index_layout.addWidget(self.index_explaination_lineedit_label)
        index_layout.addWidget(self.index_lineedit)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(checkbox_layout)
        main_layout.addLayout(index_layout)
        main_layout.addLayout(search_replace_layout)
        main_layout.addLayout(prefix_layout)
        main_layout.addLayout(suffix_layout)
        main_layout.addLayout(btn_layout)

    def create_connections(self):
        self.index_check_box.stateChanged.connect(self.toggle_index_visibility)
        self.search_replace_check_box.stateChanged.connect(self.toggle_search_replace_visibility)
        self.prefix_check_box.stateChanged.connect(self.toggle_prefix_visibility)
        self.suffix_check_box.stateChanged.connect(self.toggle_suffix_visibility)
        self.apply_btn.clicked.connect(self.apply_change)
        self.close_btn.clicked.connect(self.close)

    def undo_chunk_decorator(func):
        def wrapper(*args, **kwargs):
            # Start the undo chunk
            cmds.undoInfo(openChunk=True)
            try:
                # Call the original function
                result = func(*args, **kwargs)
            finally:
                # End the undo chunk
                cmds.undoInfo(closeChunk=True)
            return result
        return wrapper

    def toggle_index_visibility(self, state):
        self.index_lineedit.setVisible(state)
        self.index_lineedit_label.setVisible(state)
        self.index_explaination_lineedit_label.setVisible(state)
        sel_obj = cmds.ls(sl=True)
        if sel_obj:
            sel_obj = cmds.ls(sl=True)[0]
            if state == 2:  # Checked state
                self.search_replace_check_box.setChecked(False)
                self.index_lineedit.setText(sel_obj)

    def toggle_search_replace_visibility(self, state):
        self.search_lineedit.setVisible(state)
        self.search_lineedit_label.setVisible(state)
        self.replace_lineedit.setVisible(state)
        self.replace_lineedit_label.setVisible(state)
        if state == 2:  # Checked state
            self.index_check_box.setChecked(False)

    def toggle_prefix_visibility(self, state):
        self.prefix_lineedit.setVisible(state)
        self.prefix_lineedit_label.setVisible(state)

    def toggle_suffix_visibility(self, state):
        self.suffix_lineedit.setVisible(state)
        self.suffix_lineedit_label.setVisible(state)

    @undo_chunk_decorator
    def apply_change(self):
        sel_objs = cmds.ls(sl=True)

        if self.index_check_box.isChecked():
            index_default_name = self.index_lineedit.text()
            first_part = index_default_name.split("{}")[0]
            second_part = index_default_name.split("{}")[-1]
            temp_list = []
            for obj in sel_objs:
                ind = sel_objs.index(obj) + 1
                formatted_ind = f"{ind:02d}"
                new_name = first_part + str(formatted_ind) + second_part
                renamed_obj = cmds.rename(obj, new_name)
                temp_list.append(renamed_obj)
            sel_objs = temp_list

        if self.prefix_check_box.isChecked():
            prefix = self.prefix_lineedit.text()
            temp_list = []
            for obj in sel_objs:
                obj = obj.split("|")[-1]
                new_name = prefix + obj
                prefixed_obj = cmds.rename(obj, new_name)
                temp_list.append(prefixed_obj)
            sel_objs = temp_list

        if self.suffix_check_box.isChecked():
            suffix = self.suffix_lineedit.text()
            temp_list = []
            for obj in sel_objs:
                obj = obj.split("|")[-1]
                new_name = obj + suffix
                suffixed_obj = cmds.rename(obj, new_name)
                temp_list.append(suffixed_obj)
            sel_objs = temp_list

        if self.search_replace_check_box.isChecked():
            search_word = self.search_lineedit.text()
            replace_word = self.replace_lineedit.text()

            reversed_sel_objs = sel_objs[::-1]
            temp_list = []
            for obj in reversed_sel_objs:
                new_name = obj.split("|")[-1].replace(search_word, replace_word)
                replaced_obj = cmds.rename(obj, new_name)
                temp_list.append(replaced_obj)
            sel_objs = temp_list[::-1]

if __name__ == '__main__':
    try:
        renamer_window.close()
        renamer_window.deleteLater()
    except:
        pass
    renamer_window = RenamerWindow()
    renamer_window.show()

# for controller modifier, use cmds.closeCurve
# for free pivot, separate the function for creating the rig and manipulate the referenced rig