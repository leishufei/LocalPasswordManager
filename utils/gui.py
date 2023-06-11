#!usr/bin/env python3
# -*- coding: utf-8 -*-
# @Software : PyCharm
import os
from typing import Union, List, Dict

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from loguru import logger

from . import Database

db = Database()


class DeleteSheetDialog(QDialog):
    def __init__(self, parent=None):
        super(DeleteSheetDialog, self).__init__(parent)

        self.setWindowTitle("删除密码表")
        self.setFixedSize(200, 200)

        self.init_button()

    @staticmethod
    def create_checkbox(parent=None, title="") -> QCheckBox:
        checkbox = QCheckBox(parent=parent)
        checkbox.setText(title)
        return checkbox

    def init_button(self) -> None:
        self.delete_button = QPushButton("删除", self)
        self.delete_button.setFixedSize(60, 20)
        self.delete_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.setFixedSize(60, 20)
        self.cancel_button.clicked.connect(self.reject)

    def init_layout(self, items: List[str]) -> None:
        layout = QVBoxLayout(self)

        checkbox_layout = QVBoxLayout(self)
        self.checkbox_list = []
        for item in items:
            checkbox = self.create_checkbox(parent=self, title=item)
            self.checkbox_list.append(checkbox)
            checkbox_layout.addWidget(checkbox)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(QWidget())
        scroll.widget().setLayout(checkbox_layout)

        layout.addWidget(scroll)

        button_layout = QHBoxLayout(self)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def get_selected_items_checkbox_list(self) -> List[Dict]:
        checkbox_list = []
        for order, checkbox in enumerate(self.checkbox_list, start=1):
            if checkbox.isChecked():
                checkbox_list.append({
                    'order': order,
                    'text': checkbox.text()
                })
        return checkbox_list


class CreateSheetDialog(QDialog):
    def __init__(self, parent=None):
        super(CreateSheetDialog, self).__init__(parent)

        self.setWindowTitle("新增密码表")
        self.setFixedSize(200, 100)

        self.init_input_box()
        self.init_button()
        self.init_layout()

    def init_input_box(self) -> None:
        self.sheet_box = QLineEdit(self)

    def init_button(self) -> None:
        self.save_button = QPushButton("保存", self)
        self.save_button.setFixedSize(60, 20)
        self.save_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.setFixedSize(60, 20)
        self.cancel_button.clicked.connect(self.reject)

    def init_layout(self) -> None:
        layout = QVBoxLayout(self)

        sheet_layout = QHBoxLayout(self)
        sheet_layout.addWidget(QLabel("密码表", self))
        sheet_layout.addWidget(self.sheet_box)
        layout.addLayout(sheet_layout)

        button_layout = QHBoxLayout(self)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)


class ItemDialog(QDialog):
    def __init__(self, parent=None):
        super(ItemDialog, self).__init__(parent)

        self.setWindowTitle("新增密码")
        self.setFixedSize(200, 150)

        self.init_input_box()
        self.init_button()
        self.init_layout()

    def init_input_box(self) -> None:
        self.item_box = QLineEdit(self)
        self.username_box = QLineEdit(self)
        self.password_box = QLineEdit(self)

    def init_button(self) -> None:
        self.save_button = QPushButton("保存", self)
        self.save_button.setFixedSize(60, 20)
        self.save_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.setFixedSize(60, 20)
        self.cancel_button.clicked.connect(self.reject)

    def init_layout(self) -> None:
        layout = QVBoxLayout(self)

        item_layout = QHBoxLayout(self)
        item_layout.addWidget(QLabel("项目", self))
        item_layout.addWidget(self.item_box)
        layout.addLayout(item_layout)

        username_layout = QHBoxLayout(self)
        username_layout.addWidget(QLabel("账号", self))
        username_layout.addWidget(self.username_box)
        layout.addLayout(username_layout)

        password_layout = QHBoxLayout(self)
        password_layout.addWidget(QLabel("密码", self))
        password_layout.addWidget(self.password_box)
        layout.addLayout(password_layout)

        button_layout = QHBoxLayout(self)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)


class MainWindow(QMainWindow):
    QApplication.setStyle("Fusion")

    def __init__(self):
        super(MainWindow, self).__init__()

        self.window_icon_path = "resources/icon/main_window.svg"
        self.search_button_icon_path = "resources/icon/search.svg"
        self.refresh_button_icon_path = "resources/icon/refresh.svg"
        self.create_new_sheet_icon_path = "resources/icon/create_new_sheet.svg"
        self.delete_sheet_icon_path = "resources/icon/delete.svg"

        self.column_count = 3
        self.column_label_list_en = ["item", "username", "password"]
        self.column_label_list_cn = ["项目", "用户名", "密码"]

        # 在渲染table时给这个字典赋值，后面修改值的时候需要用到
        # self.table_recorder[row][column]
        self.table_recorder = {}

        # todo: gui和db中的sheet要重新对应一下，不然删中间的sheet就会出问题
        # self.sheet_recorder[gui_sheet][db_sheet]
        self.sheet_recorder = {}

        self.setup_ui()

    def setup_ui(self) -> None:
        self.setFixedSize(721, 512)
        self.setWindowTitle("Password Manager V1.0")
        self.setWindowIcon(self.create_icon(self.window_icon_path))

        self.init_font()
        self.init_central_widget()
        self.init_main_table()
        self.init_combo_box()
        self.init_label()
        self.init_button()
        self.init_separator()
        self.init_search_box()
        self.init_menu_bar()
        self.init_menu()

    @staticmethod
    def create_icon(icon_path: str, mode=QtGui.QIcon.Mode.Normal, state=QtGui.QIcon.State.Off) -> QIcon:
        icon = QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), mode, state)
        return icon

    def init_font(self) -> None:
        self.font = self.create_font()

    @staticmethod
    def create_font(font_family="微软雅黑", size=10) -> QFont:
        font = QFont()
        font.setFamily(font_family)
        font.setPointSize(size)
        return font

    def init_central_widget(self) -> None:
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

    def init_label(self) -> None:
        self.label = QLabel(parent=self.central_widget)
        self.label.setGeometry(QtCore.QRect(10, 10, 51, 31))
        self.label.setText("密码表")
        self.label.setFont(self.font)

    def init_combo_box(self) -> None:
        self.combo_box = QComboBox(parent=self.central_widget)
        self.combo_box.setGeometry(QtCore.QRect(55, 10, 101, 31))

        sheet_list = self.get_db_sheet_list()
        if len(sheet_list) == 0:
            return

        self.combo_box.addItems(sheet_list)
        self.combo_box.currentIndexChanged.connect(self.fully_render_table)

        self.fully_render_table()

    def create_button(self, rect_list: List[int], icon_path="", parent=None, checkable=False, tip="", bind_func=None) -> Union[QPushButton, None]:
        if len(rect_list) != 4:
            logger.warning(f"Button rect<{rect_list}> is invalid")
            return
        button = QPushButton(parent=parent)
        button.setGeometry(QtCore.QRect(*rect_list))

        if icon_path != "" and os.path.exists(icon_path):
            button.setIcon(self.create_icon(icon_path))

        button.setCheckable(checkable)

        if tip != "":
            button.setToolTip(tip)

        if bind_func and callable(bind_func):
            button.clicked.connect(bind_func)

        return button

    def init_button(self) -> None:
        self.init_create_new_sheet_button()
        self.init_delete_current_sheet()
        self.init_refresh_button()
        self.init_search_button()

    def init_create_new_sheet_button(self) -> None:
        self.create_sheet_button = self.create_button(
            rect_list=[161, 10, 31, 31],
            icon_path=self.create_new_sheet_icon_path,
            parent=self.central_widget,
            checkable=False,
            tip="新增密码表",
            bind_func=self.create_db_sheet
        )

    def init_delete_current_sheet(self) -> None:
        self.delete_sheet_button = self.create_button(
            rect_list=[193, 10, 31, 31],
            icon_path=self.delete_sheet_icon_path,
            parent=self.central_widget,
            checkable=False,
            tip="删除当前密码表",
            bind_func=self.delete_db_sheet
        )

    def init_refresh_button(self) -> None:
        self.refresh_button = self.create_button(
            rect_list=[225, 10, 31, 31],
            icon_path=self.refresh_button_icon_path,
            parent=self.central_widget,
            checkable=False,
            tip="刷新当前密码表",
            bind_func=self.fully_render_table
        )

    def init_search_button(self) -> None:
        self.refresh_button = self.create_button(
            rect_list=[680, 10, 31, 31],
            icon_path=self.search_button_icon_path,
            parent=self.central_widget,
            checkable=False,
            tip="根据关键词检索",
            bind_func=self.search
        )

    def init_separator(self) -> None:
        separator = QFrame(parent=self.central_widget)
        separator.setGeometry(261, 12, 10, 28)
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)

    def init_search_box(self) -> None:
        self.search_box = QLineEdit(parent=self.central_widget)
        self.search_box.setGeometry(QtCore.QRect(276, 10, 399, 31))
        self.search_box.setPlaceholderText("Searching...")

    def init_main_table(self) -> None:
        self.table_widget = QTableWidget(parent=self.central_widget)
        self.table_widget.setGeometry(QtCore.QRect(10, 50, 701, 421))

        # 双击或者按下F2键才能编辑表格
        self.table_widget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)

        self.table_widget.setColumnCount(self.column_count)
        self.table_widget.setHorizontalHeaderLabels(self.column_label_list_cn)

        # 固定列标签，使其不可拖动
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_widget.horizontalHeader().setDefaultSectionSize(160)
        self.table_widget.setColumnWidth(0, 160)
        self.table_widget.setColumnWidth(1, 250)
        self.table_widget.setColumnWidth(2, 250)

        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_widget.verticalHeader().setDefaultSectionSize(30)

        self.table_widget.cellChanged.connect(self.edit_cell)

        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)

    def init_menu_bar(self) -> None:
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 721, 21))
        self.setMenuBar(self.menubar)

    @staticmethod
    def create_menu(actions: List[QAction], parent=None, title="") -> QMenu:
        menu = QMenu(parent=parent)

        if title != "":
            menu.setTitle(title)

        for action in actions:
            menu.addAction(action)

        return menu

    @staticmethod
    def create_action(parent=None, title="", bind_func=None) -> QAction:
        action = QAction(parent=parent)

        if title != "":
            action.setText(title)

        if bind_func and callable(bind_func):
            action.triggered.connect(bind_func)

        return action

    def init_menu(self) -> None:
        # 菜单
        actions = []
        action = self.create_action(parent=self, title="导入密码表")
        actions.append(action)

        action = self.create_action(parent=self, title="导出密码表")
        actions.append(action)

        action = self.create_action(parent=self, title="退出")
        actions.append(action)

        menu_menu = self.create_menu(actions=actions, parent=self.menubar, title="菜单")
        menu_menu.setFixedWidth(100)

        # 关于
        about_menu = self.create_menu(actions=[], parent=self.menubar, title="关于")

        self.menubar.addAction(menu_menu.menuAction())
        self.menubar.addAction(about_menu.menuAction())

    @staticmethod
    def create_message_box(parent=None, icon_type=QMessageBox.Question, message="") -> Union[QMessageBox, None]:
        message_box = QMessageBox(parent=parent)
        if icon_type == QMessageBox.Question:
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.No)
        elif icon_type == QMessageBox.Warning:
            message_box.setStandardButtons(QMessageBox.Yes)
            message_box.setDefaultButton(QMessageBox.Yes)
        else:
            return
        message_box.setIcon(icon_type)
        message_box.setText(message)
        return message_box

    def get_current_sheet(self) -> str:
        index = self.combo_box.currentIndex() + 1
        sheet = self.combo_box.currentText().strip()
        if sheet == "":
            pass
        else:
            sheet = f"{index:02d}_{sheet}"
        logger.info(f"Current sheet: {sheet}")
        return sheet

    @staticmethod
    def get_db_sheet_list() -> List[str]:
        sheet_list = db.query_sheet_list()
        logger.info(f"Fetch db sheet list: {sheet_list}")
        return [each.split("_")[-1] for each in sheet_list]

    def clear_search_box(self) -> None:
        self.search_box.clear()
        logger.info("Cleared search box content")

    def update_table_recorder(self, row: int, column: int, value: str) -> None:
        if self.table_recorder.get(row) is None:
            self.table_recorder[row] = {}
        self.table_recorder[row][column] = value
        logger.info(f"Set table_recorder[{row}][{column}] to {value}")

    def delete_db_rows(self, deleted_items: List[Dict]) -> None:
        sheet = self.get_current_sheet()
        if sheet == "":
            return
        db.delete(sheet, deleted_items)
        logger.info(f"Deleted items of sheet <{sheet}>: {deleted_items}")

    def update_db_row(self, update_item: Dict) -> None:
        sheet = self.get_current_sheet()
        if sheet == "":
            return
        db.update(sheet, update_item)
        logger.info(f"Updated item of sheet <{sheet}>: {update_item}")

    def fully_render_table(self) -> None:
        # 渲染table前需要断开信号，否则会出发其他事件
        self.table_widget.blockSignals(True)

        # 渲染之前先把所有的选中清除，不然会触发itemChanged事件
        self.clear_selection()

        sheet = self.get_current_sheet()
        if sheet == "":
            return

        db_rows = db.query_by_sheet(sheet)
        row_count = len(db_rows)
        self.table_widget.setRowCount(row_count)

        for row, db_row in enumerate(db_rows, start=0):
            values = list(db_row.values())
            for column in range(self.column_count):
                value = values[column]
                item = QTableWidgetItem(value)
                self.table_widget.setItem(row, column, item)
                self.update_table_recorder(row, column, value)

        # 渲染table后重新设置信号
        self.table_widget.blockSignals(False)

    def partially_render_table(self, db_rows: List[Dict]) -> None:
        self.table_widget.blockSignals(True)

        row_count = len(db_rows)
        self.table_widget.setRowCount(row_count)

        for row, db_row in enumerate(db_rows, start=0):
            values = list(db_row.values())
            for column in range(self.column_count):
                value = values[column]
                item = QTableWidgetItem(value)
                self.table_widget.setItem(row, column, item)
                self.update_table_recorder(row, column, value)

        self.table_widget.blockSignals(False)

    def edit_cell(self) -> None:
        item = self.table_widget.currentItem()
        if item is None:
            logger.info("Current item is invalid")
            return

        row = item.row()
        column = item.column()
        value = item.text().strip()

        if self.table_recorder[row][column] == value:
            return

        update_item = {
            "originalItem": {},
            "updatedItem": {}
        }

        for column in range(self.column_count):
            update_item["originalItem"][self.column_label_list_en[column]] = self.table_recorder[row][column]
            update_item["updatedItem"][self.column_label_list_en[column]] = self.table_recorder[row][column]
        update_item["updatedItem"][self.column_label_list_en[column]] = value

        self.update_db_row(update_item)
        self.update_table_recorder(row, column, value)

        # todo: 修改单元格内容后需要确定（按回车键或者点击按钮）后才能更新到数据库
        # 有点难做，shit

    def clear_cell(self, items: List[QTableWidgetItem]) -> None:
        self.show_message_box(message="是否清除？", icon_type=QMessageBox.Question)
        if not self.get_message_box_response():
            return

        for item in items:
            if item is not None:
                item.setText("")

    def clear_selection(self) -> None:
        self.table_widget.clearSelection()
        logger.info("Cleared all selections")

    def get_selected_items(self) -> List[QTableWidgetItem]:
        return self.table_widget.selectedItems()

    def delete_rows(self, items: List[QTableWidgetItem]) -> None:
        self.show_message_box(message="是否删除？", icon_type=QMessageBox.Question)
        if not self.get_message_box_response():
            return

        rows = set()
        for item in items:
            if item is not None:
                row = item.row()
                rows.add(row)

        delete_rows = []
        for row in rows:
            item = {
                "item": self.table_widget.item(row, 0).text(),
                "username": self.table_widget.item(row, 1).text(),
                "password": self.table_widget.item(row, 2).text(),
            }
            delete_rows.append(item)
        self.delete_db_rows(delete_rows)

        # 删除多行需要注意的地方：
        # 1. remove操作要在后面执行，不然就会出现错位的情况
        # 2. 必须加reverse=True，不然也会出现删错位的情况
        for row in sorted(rows, reverse=True):
            self.table_widget.removeRow(row)

    def add_row(self) -> None:
        dialog = ItemDialog(parent=self)
        response = dialog.exec_()
        if response == QDialog.Accepted:
            item = dialog.item_box.text()
            username = dialog.username_box.text()
            password = dialog.password_box.text()
            if item == "" and username == "" and password == "":
                logger.warning("All fields are empty")
                return

            sheet = self.get_current_sheet()
            add_data = {
                "item": item,
                "username": username,
                "password": password
            }
            if not db.insert(sheet, add_data):
                return

            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            values = list(add_data.values())
            for column in range(self.column_count):
                value = values[column]
                item = QTableWidgetItem(value)
                self.table_widget.setItem(row, column, item)
                self.update_table_recorder(row, column, value)

    def show_message_box(self, message: str, icon_type=QMessageBox.Question) -> None:
        # 只有调用exec_函数时才会弹出提示框
        if icon_type not in [QMessageBox.Question, QMessageBox.Warning]:
            return
        self.message_box = self.create_message_box(parent=self, icon_type=icon_type, message=message)

    def get_message_box_response(self) -> bool:
        response = self.message_box.exec_()
        if response == QMessageBox.Yes:
            return True
        else:
            return False

    def search(self) -> None:
        sheet = self.get_current_sheet()
        keyword = self.search_box.text().strip()
        if keyword == "":
            return
        logger.info(f"Search keyword<{keyword}> in the sheet<{sheet}>")
        db_rows = db.query_by_sheet_and_keyword(sheet, keyword)
        self.partially_render_table(db_rows)
        self.clear_search_box()

    def show_context_menu(self, pos: QPoint) -> None:
        selected_items = self.get_selected_items()
        actions = []
        if len(selected_items) == 0:
            action = self.create_action(title="Add Row", bind_func=lambda: self.add_row())
            actions.append(action)
        else:
            action = self.create_action(title="Clear Cell", bind_func=lambda: self.clear_cell(selected_items))
            actions.append(action)

            action = self.create_action(title="Delete Row", bind_func=lambda: self.delete_rows(selected_items))
            actions.append(action)

            action = self.create_action(title="Add Row", bind_func=lambda: self.add_row())
            actions.append(action)

        if len(actions) == 0:
            return

        menu = self.create_menu(actions=actions, parent=self.table_widget)
        cursor_pos = self.table_widget.viewport().mapToGlobal(pos)
        menu.exec_(cursor_pos)

    def is_sheet_exist(self, sheet: str) -> bool:
        sheet_list = self.get_db_sheet_list()
        if sheet in sheet_list:
            return True
        else:
            return False

    def create_db_sheet(self) -> None:
        dialog = CreateSheetDialog(self)
        response = dialog.exec_()
        if response == QDialog.Accepted:
            sheet_list = self.get_db_sheet_list()
            raw_sheet = dialog.sheet_box.text().strip()
            if raw_sheet == "":
                return
            if self.is_sheet_exist(raw_sheet):
                logger.info(f"Target sheet<{raw_sheet}> has already exist")
                return
            sheet = f"{len(sheet_list) + 1:02d}_{raw_sheet}"
            db.create_sheet(sheet)
            self.combo_box.addItem(raw_sheet)

    def delete_db_sheet(self) -> None:
        # 还有点问题
        sheet_list = self.get_db_sheet_list()
        dialog = DeleteSheetDialog(self)
        dialog.init_layout(sheet_list)
        response = dialog.exec_()
        if response == QDialog.Accepted:
            db_sheet_list = []
            selected_checkbox_list = dialog.get_selected_items_checkbox_list()
            for checkbox in selected_checkbox_list:
                self.combo_box.removeItem(checkbox["order"] - 1)
                db_sheet_list.append(f"{checkbox['order']:02d}_{checkbox['text']}")
            if len(db_sheet_list) > 0:
                db.delete_sheet(db_sheet_list)
