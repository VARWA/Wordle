import random

from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout, QMessageBox

from constants import WORDS, RUS_ALPHABET, LETTER_ON_TRUE_POSITION_COLOR, LETTER_ON_ANOTHER_POSITION_COLOR, \
    LETTER_NO_HAVE_POSITION_COLOR
from current_game_data import CurrentEventData
from letter_model import WordOnTable


class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.__current_data = None
        self.__v1layout = QVBoxLayout()

        self.__restart_game_button = QPushButton("Начать игру заново")
        self.__restart_game_button.setCheckable(True)
        self.__v1layout.addWidget(self.__restart_game_button)
        self.__restart_game_button.clicked.connect(lambda x: self._reset_game(win=False))
        self._new_game()

        self.setLayout(self.__v1layout)

    def _new_game(self):
        self.__answer = self._new_word()
        self.__current_data = CurrentEventData(self.__answer)
        self._init_map()
        self.__v1layout.addLayout(self.__grid)

    def _reset_game(self, win=False):
        restart_window_message = QMessageBox(self)
        if self.__current_data.word_is_unsecreted:
            pre_mess_text = ""
        elif win is True:
            pre_mess_text = f"Ура! Вы отгадали слово {self.__answer} \n"
            self.__current_data.word_is_unsecreted = True
        else:
            pre_mess_text = f"Увы, Вы не отгадали слово {self.__answer} \n"
            self.__current_data.word_is_unsecreted = True

        restart_window_message.setText(pre_mess_text + "Начать игру заново?")
        restart_window_message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        button = restart_window_message.exec()
        if button == QMessageBox.StandardButton.Yes:
            for i in reversed(range(self.__grid.count())):
                widgetToRemove = self.__grid.itemAt(i).widget()
                self.__grid.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
            self._new_game()

    def _init_map(self):
        self.__grid = QGridLayout()
        self.__grid.setSpacing(3)

        for i in range(0, 6):
            for j in range(0, 5):
                self._set_table_element(string=i, column=j)

    def keyPressEvent(self, event):
        if not self.__current_data.game_is_going:
            return None
        if event.key() == 16777219:
            self._remove_letter()
        else:
            pressed_value = event.text()
            checked_value = self._check_letter(pressed_value)
            if checked_value:
                self._add_letter(checked_value)

    @staticmethod
    def _new_word():
        return random.choice(WORDS)

    @staticmethod
    def _check_letter(let):
        if let.isalpha() and let.upper() in RUS_ALPHABET:
            return let.upper()

    def _new_letter(self, string, number_on_string, text):
        self._set_table_element(text=text, string=string, column=number_on_string)

    def _add_letter(self, letter):
        data = self.__current_data
        if data.word_is_unsecreted:
            return
        data.current_word.append(letter)
        self._new_letter(data.count_strings, len(data.current_word) - 1, letter)

        if len(data.current_word) == 5:
            data.last_words.append(data.current_word)
            self._check_word(data.count_strings, data.current_word)
            data.current_word.clear()
            data.count_strings += 1

        if data.count_strings == 6:
            self._reset_game(win=False)
            data.game_is_going = False

    def _remove_letter(self):
        if len(self.__current_data.current_word):
            del self.__current_data.current_word[-1]
            self._set_table_element(string=self.__current_data.count_strings,
                                    column=len(self.__current_data.current_word))

    def _check_word(self, number_of_string, current_word):
        counter = 0
        for i in range(len(current_word)):
            symbol = current_word[i]
            if self.__answer[i] == current_word[i]:
                self._set_table_element(text=symbol, color=LETTER_ON_TRUE_POSITION_COLOR, string=number_of_string,
                                        column=i)
                counter += 1
            elif current_word[i] in self.__answer:
                self._set_table_element(text=symbol, color=LETTER_ON_ANOTHER_POSITION_COLOR, string=number_of_string,
                                        column=i)
            else:
                self._set_table_element(text=symbol, color=LETTER_NO_HAVE_POSITION_COLOR, string=number_of_string,
                                        column=i)
        if counter == 5:
            self.__current_data.game_is_going = False
            self._reset_game(win=True)

    def _set_table_element(self, string, column, text='', color='white'):
        self.__grid.addWidget(WordOnTable(text=text, color=color), string, column)
