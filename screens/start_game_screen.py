from PyQt6.QtWidgets import QWidget, QPushButton, QFormLayout


class StartGameScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout()

        self.start_game_button = QPushButton("Начать игру")
        self.start_game_button.setCheckable(True)
        self.layout.addRow(self.start_game_button)

        self.setLayout(self.layout)
