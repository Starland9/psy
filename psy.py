import sys

from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *

from logic.responder import PsyWorker


class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def fromDict(self, d: dict):
        self.role = d["role"]
        self.content = d["content"]
        return self

    def toHtml(self):
        if self.role == "user":
            return f"""<div class="chat-bubble">
        <p>{self.content}</p>
      </div>"""
        else:
            return f"""<div class="chat-bubble right">
    <p>{self.content}</p>
  </div>"""

    def toDict(self):
        return {"role": self.role, "content": self.content}

    def __eq__(self, other):
        return self.role == other.role

    def __str__(self):
        return f"{self.role}: {self.content}"


messages: list[Message] = [
    Message(
        "user",
        "Bonjour"
    ),
    Message(
        "assistant",
        "Bonjour je suis ton psy et je vais aider à comprendre et résoudre tes problèmes. "
        "et je donne mes conseil et je te repond sous format html en mode text2html avec un "
        "joli style. comment"
        "puis-je t'aider aujourd'hui ?",
    ),
    Message(
        "user",
        "jai faim",
    ),
    Message(
        "assistant",
        "Je ne repond pas a ce type de question. je suis ton psy juste ton psy",
    ),
    Message(
        "user",
        "ma femme me deteste",
    ),
    Message(
        "assistant",
        "Ceci est un beau sujet de psy",
    )
]


def genHtml(messages_list: list[Message]):
    return """
 <!DOCTYPE html>
<html>
<head>
  <title>Chat Bubble Example</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #000000;
      padding: 20px;
    }
    
    .chat-bubble {
      background-color: #EDEFF1;
      color: #000000;
      border-radius: 20px;
      padding: 10px;
      margin-bottom: 10px;
      max-width: 70%;
    }
    
    .chat-bubble.right {
      background-color: #0084FF;
      color: #FFFFFF;
    }
  </style>
</head>
<body> """ + "\n".join([m.toHtml() for m in messages_list]) + """
</body>
</html>

"""


class ChatBubble(QFrame):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.layout = QVBoxLayout()

        self.setMinimumHeight(30)
        self.setStyleSheet("""
        border: 1px solid transparent;
        border-radius: 10px;
        padding: 1px;
        background-color: #f12345;
        """)

        self.label = QLabel(text)
        self.label.setStyleSheet("""
        font-size: 14px;
        color: white;
        
        """)

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)


class UIMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 600)
        self.setWindowTitle("Mon Psy")
        self.setWindowIcon(QIcon("assets/cerveau.png"))
        self.layout = QVBoxLayout()
        self.thread = QThreadPool()

        self.messages = messages

        self.textBrowser = QTextBrowser()
        self.textBrowser.setPlaceholderText("Raconte moi tout et je te donnerai des conseils")
        self.textBrowser.setStyleSheet("""
        font-size: 16px;
        font-family: monospace;
        border: 1px solid black;
        border-radius: 10px;
        padding: 10px;
        
        """)
        self.textBrowser.setHtml(genHtml(self.messages))
        self.layout.addWidget(self.textBrowser)

        self.textEditSend = QTextEdit()
        self.textEditSend.setMaximumHeight(60)
        self.textEditSend.setPlaceholderText("Raconte moi tout et je te donnerai des conseils")
        self.layout.addWidget(self.textEditSend)

        self.sendButton = QPushButton("Envoyer")
        self.sendButton.clicked.connect(self.analyse)
        self.sendButton.setStyleSheet("""
        border: 1px solid black;
        border-radius: 10px;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
        background-color: #4CAF50;
        color: white
        
        """)
        self.layout.addWidget(self.sendButton)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central.setLayout(self.layout)

    def analyse(self):
        self.messages.append(Message("user", self.textEditSend.toPlainText()))
        self.textBrowser.setHtml(genHtml(self.messages))
        try:

            self.sendButton.setEnabled(False)
            self.sendButton.setText("Analyse en cours...")
            analyseThread = PsyWorker(self.textEditSend.toPlainText(), [m.toDict() for m in self.messages])
            self.thread.start(analyseThread)
            analyseThread.signals.completed.connect(self.analyseComplete)

        except Exception as e:
            print(e)

    def analyseComplete(self, response):
        self.sendButton.setEnabled(True)
        self.sendButton.setText("Envoyer")
        self.messages.append(Message("assistant", response))

        self.textBrowser.setHtml(genHtml(self.messages))

    def close(self) -> bool:
        self.thread.quit()
        self.thread.wait()
        return super().close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UIMainWindow()
    window.show()
    sys.exit(app.exec())
