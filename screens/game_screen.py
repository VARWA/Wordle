import random

from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout, QMessageBox

from constants import WORDS, RUS_ALPHABET
from current_game_data import CurrentEventData
from letter_model import WordOnTable


class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.v1layout = QVBoxLayout()

        self.restart_game_button = QPushButton("Начать игру заново")
        self.restart_game_button.setCheckable(True)
        self.v1layout.addWidget(self.restart_game_button)
        self.restart_game_button.clicked.connect(lambda x: self.reset_game(win=False))
        self.new_game()

        self.setLayout(self.v1layout)

    def new_game(self):
        self.current_data = CurrentEventData(self.new_word())
        self.init_map()
        self.v1layout.addLayout(self.grid)

    def reset_game(self, win=False):
        restart_window_message = QMessageBox(self)
        print(win)
        if self.current_data.word_is_unsecreted:
            pre_mess_text = ""
        elif win is True:
            pre_mess_text = f"Ура! Вы отгадали слово {self.answer} \n"
            self.current_data.word_is_unsecreted = True
        else:
            pre_mess_text = f"Увы, Вы не отгадали слово {self.answer} \n"
            self.current_data.word_is_unsecreted = True

        restart_window_message.setText(pre_mess_text + "Начать игру заново?")
        restart_window_message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        button = restart_window_message.exec()
        if button == QMessageBox.StandardButton.Yes:
            for i in reversed(range(self.grid.count())):
                widgetToRemove = self.grid.itemAt(i).widget()
                self.grid.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
            self.new_game()

    def init_map(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(3)

        for i in range(0, 6):
            for j in range(0, 5):
                self.set_table_element(string=i, column=j)

    def keyPressEvent(self, event):
        if not self.current_data.game_is_going:
            return None
        if event.key() == 16777219:
            self.remove_letter()
        else:
            pressed_value = event.text()
            checked_value = self.check_letter(pressed_value)
            if checked_value:
                self.add_letter(checked_value)

    def new_word(self):
        self.answer = random.choice(WORDS)
        return self.answer

    def check_letter(self, let):
        if let.isalpha() and let.upper() in RUS_ALPHABET:
            return let.upper()

    def new_letter(self, string, number_on_string, text):
        self.set_table_element(text=text, string=string, column=number_on_string)

    def add_letter(self, letter):
        data = self.current_data
        if data.word_is_unsecreted:
            return
        data.current_word.append(letter)
        self.new_letter(data.count_strings, len(data.current_word) - 1, letter)

        if len(data.current_word) == 5:
            data.last_words.append(data.current_word)
            self.check_word(data.count_strings, data.current_word)
            data.current_word.clear()
            data.count_strings += 1

        if data.count_strings == 6:
            self.reset_game(win=False)
            data.game_is_going = False

    def remove_letter(self):
        if len(self.current_data.current_word):
            del self.current_data.current_word[-1]
            self.set_table_element(string=self.current_data.count_strings, column=len(self.current_data.current_word))

    def check_word(self, number_of_string, current_word):
        counter = 0
        for i in range(len(current_word)):
            symbol = current_word[i]
            if self.answer[i] == current_word[i]:
                self.set_table_element(text=symbol, color='rgb(40,181,22)', string=number_of_string, column=i)
                counter += 1
            elif current_word[i] in self.answer:
                self.set_table_element(text=symbol, color='rgb(242,233,28)', string=number_of_string, column=i)
            else:
                self.set_table_element(text=symbol, color='lightgrey', string=number_of_string, column=i)
        if counter == 5:
            self.current_data.game_is_going = False
            self.reset_game(win=True)

    def set_table_element(self, string, column, text='', color='white'):
        self.grid.addWidget(WordOnTable(text=text, color=color), string, column)
