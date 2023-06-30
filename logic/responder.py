from PyQt6.QtCore import QRunnable, pyqtSignal, QObject, pyqtSlot

import g4f


class Signals(QObject):
    completed = pyqtSignal(str)


class PsyWorker(QRunnable):
    def __init__(self, text: str, messages: list):
        super(PsyWorker, self).__init__()

        self.text = text
        self.signals = Signals()
        self.messages = messages

    @pyqtSlot()
    def run(self) -> None:
        response = g4f.ChatCompletion.create(
            model='gpt-4',
            messages=self.messages,
            provider=g4f.Provider.DeepAi,
        )
        print(response)
        self.signals.completed.emit(response)
