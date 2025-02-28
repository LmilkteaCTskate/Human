from ollama import Client
import sys
sys.path.append("D:/ASR_LLX_TTS/ASR/Human")
from PyQt5.QtCore import pyqtSignal, QObject

class Talk(QObject):
    # 定义一个信号，用于将模型输出的文本传递给GUI
    model_output_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def Talk_model(self, user_text):
        # 创建客户端并连接到默认地址
        client = Client()
        client = Client(host='http://localhost:11434')
        # 尝试调用模型
        stream = client.chat(
            model='deepseek-r1:1.5b',
            messages=[{'role': 'user', 'content': user_text}],
            stream=True
        )

        is_first_chunk = True

        # 处理流式响应
        for chunk in stream:
            # 获取模型输出的文本
            Model_text = chunk['message']['content']
            #过滤掉<think></think>标签和空白内容
            Model_text = Model_text.strip()
            Model_text = Model_text.replace("\n", "")
            Model_text = Model_text.replace("\r", "")
            Model_text = Model_text.replace(" ", "")
            Model_text = Model_text.replace("\t", "")
            Model_text = Model_text.replace("<sep/>", "")
            Model_text = Model_text.replace("<think>", "")
            Model_text = Model_text.replace("</think>", "")

            
            if is_first_chunk:
                if Model_text:
                  Model_text = f'模型: {Model_text}'
                  is_first_chunk = False
            # 发射信号，将模型输出的文本传递给GUI
            self.model_output_signal.emit(Model_text)