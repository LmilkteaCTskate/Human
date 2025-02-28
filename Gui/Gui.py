from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from prompt_toolkit import Application
import threading
sys.path.append("D:/ASR_LLX_TTS/ASR/Human")
from Text.Text import Talk

class UI_Form:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Form")
        MainWindow.resize(1124, 637)
        
        # 对话模型下拉框
        self.comboBox = QtWidgets.QComboBox(MainWindow)
        self.comboBox.setGeometry(QtCore.QRect(60, 440, 161, 41))
        self.comboBox.addItem("")
        
        # ASR下拉框
        self.comboBox_2 = QtWidgets.QComboBox(MainWindow)
        self.comboBox_2.setGeometry(QtCore.QRect(60, 500, 161, 41))
        self.comboBox_2.addItem("")
        
        # TTS下拉框
        self.comboBox_3 = QtWidgets.QComboBox(MainWindow)
        self.comboBox_3.setGeometry(QtCore.QRect(60, 560, 161, 41))
        self.comboBox_3.addItem("")
        
        # 用户输入框
        self.textEdit = QtWidgets.QTextEdit(MainWindow)
        self.textEdit.setGeometry(QtCore.QRect(300, 530, 661, 71))
        
        # 输入框标签
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(310, 480, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        
        # 发送按钮
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(970, 530, 81, 71))
        
        # 对话记录显示
        self.textBrowser = QtWidgets.QTextBrowser(MainWindow)
        self.textBrowser.setGeometry(QtCore.QRect(300, 110, 671, 371))
        self.textBrowser.setWordWrapMode(QtGui.QTextOption.WordWrap)
        
        # 实例化对话功能模块
        self.talk_text = Talk_Text(self)
        self.talk_text.update_signal.connect(self.update_model_output)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "智能对话系统"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Deepseek"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "FunASR"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "pyttsx3"))
        self.label.setText(_translate("MainWindow", "输入框"))
        self.pushButton.setText(_translate("MainWindow", "发送"))
        self.pushButton.clicked.connect(self.talk_text.text_run)

    def update_model_output(self, Model_text):
        # 获取当前内容
        current_text = self.textBrowser.toPlainText()
        # 更新内容
        updated_text = current_text + Model_text
        self.textBrowser.setText(updated_text)
        # 滚动到底部
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())
    # def text_run(self, user_text):
    #     #新线程执行文本对话
    #     user_text = self.textEdit.toPlainText()
    #     self.textBrowser.append(f'用户:{user_text}\n')
    #     # 文本对话结束后，清空输入框
    #     #清空输入框
    #     self.textEdit.clear()
    #     t = threading.Thread(target=self.text_run_thread, args=(user_text,))
    #     t.start()
    # def text_run_thread(self, user_text):
    #     #文本对话
    #     self.text.Talk_model(user_text)




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UI_Form()
        self.ui.setupUi(self)
class Talk_Text(QtCore.QObject):
    update_signal = QtCore.pyqtSignal(str)
    
    def __init__(self, ui_instance):
        super().__init__()
        self.ui = ui_instance
        self.talk_model = Talk()
        
        # 连接模型信号到处理函数
        self.talk_model.model_output_signal.connect(self._handle_model_output)
        
    def text_run(self):
        """触发对话流程"""
        user_text = self.ui.textEdit.toPlainText().strip()
        if not user_text:
            return
        
        # 更新对话框
        self._safe_append_text(f'用户: {user_text}\n')
        self._clear_input()
        
        # 启动处理线程
        threading.Thread(target=self._text_run_thread, args=(user_text,), daemon=True).start()
    
    def _text_run_thread(self, user_text):
        """后台线程执行模型调用"""
        self.talk_model.Talk_model(user_text)
    
    def _handle_model_output(self, text):
        """处理模型输出信号"""
        self.update_signal.emit(text)
    
    def _safe_append_text(self, text):
        """线程安全的文本追加"""
        QtCore.QMetaObject.invokeMethod(
            self.ui.textBrowser,
            "append",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, text)
        )
    
    def _clear_input(self):
        """清空输入框"""
        QtCore.QMetaObject.invokeMethod(
            self.ui.textEdit,
            "clear",
            QtCore.Qt.QueuedConnection
        )

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())