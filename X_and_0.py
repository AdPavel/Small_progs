from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import random

Config.set('graphics', 'height', '550')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'resizable', '0')


class GameApp(App):
    def __init__(self):
        super().__init__()
        self.switch = True
        self.buttons = [[0]*10 for _ in range(10)]
        self.rules_dict = {'vertical': [[], []], 'horizontal': [[], []],
                           'main_diagonal': [[], []], 'secondary_diagonal': [[], []]}

    def game(self, arg) -> None:
        """
        Распределяет очередность хода, ход игрока
        :param arg: class of button
        :return: None
        """
        arg.disabled = True
        arg.text = 'X'
        self.switch = not self.switch

        fail, dict_key = self.rules(arg)
        if fail:
            self.show_fail(self.rules_dict[dict_key][0], 'SkyNet')
        else:
            fail, dict_key = self.rules(self.comp_turn())
            if fail:
                self.show_fail(self.rules_dict[dict_key][1], 'YOU')
        return None

    def comp_turn(self):
        """
        Ход компа, случайно генерирует идекс кнопки
        :return: класс Кнопки
        """
        comp_button = self.buttons[random.randint(0, 9)][random.randint(0, 9)]
        while comp_button.disabled:
            comp_button = self.buttons[random.randint(0, 9)][random.randint(0, 9)]
        comp_button.disabled = True
        comp_button.text = '0'
        self.switch = not self.switch
        return comp_button

    def rules(self, arg) -> tuple:
        """
        Описывает правила
        :param arg: класс Кнопки, определяет идекс в массиве кнопок
        :return: кортеж Проигрыш, Ключ словаря (false, dict_key)
        """
        for i in range(len(self.buttons)):
            try:
                y = self.buttons[i].index(arg)
                x = i
                break
            except: pass
        for i in range(10):
            for j in range(10):
                if x == i:
                    fail, dict_key = self.is_fail(self.buttons[i][j], 'horizontal', (i, j))
                    if fail:
                        return fail, dict_key
                if y == j:
                    fail, dict_key = self.is_fail(self.buttons[i][j], 'vertical', (i, j))
                    if fail:
                        return fail, dict_key
                if (y - j) == (x - i):
                    fail, dict_key = self.is_fail(self.buttons[i][j], 'secondary_diagonal', (i, j))
                    if fail:
                        return fail, dict_key
                if (i + j) == (x + y):
                    fail, dict_key = self.is_fail(self.buttons[i][j], 'main_diagonal', (i, j))
                    if fail:
                        return fail, dict_key
        [[v.clear() for v in val] for val in self.rules_dict.values()]
        return False, 0

    def is_fail(self, button, key: str, idx: tuple) -> tuple:
        """
        Определяет проигрышную комбиацию
        :param button: класс Кнопка
        :param key: ключ для словаря с индексами отмеченных кнопок
        :param idx: игдексы отмеченных кнопок
        :return: кортеж Проигрыш, Ключ Словаря (fail, key)
        """
        if button.text == 'X':
            self.rules_dict[key][0].append(idx)
            self.rules_dict[key][1].clear()
        elif button.text == '0':
            self.rules_dict[key][1].append(idx)
            self.rules_dict[key][0].clear()
        elif button.text == '':
            self.rules_dict[key][1].clear()
            self.rules_dict[key][0].clear()
        return len(self.rules_dict[key][0]) == 5 or len(self.rules_dict[key][1]) == 5, key

    def show_fail(self, idx_list: tuple, winner: str) -> None:
        """
        Отмечает проигрышную комбинацию
        :param idx_list: список кортежей индекса кнопок
        :param winner: строка кто победитель
        :return: None
        """
        self.switch = True
        for i, j in idx_list:
            self.buttons[i][j].color = [0, 1, 0, 1]
        self.restart()
        self.window_continue(winner)
        return None

    def restart(self, args=True) -> None:
        """
        Сбрасывает все отметки в первоначальное состояние или отключает кнопки для show_fail()
        :param args: класс кнопки или bool
        :return: None
        """
        self.switch = True
        for row in self.buttons:
            for button in row:
                if args is True:
                    button.disabled = args
                else:
                    button.color = [0, 0, 0, 0]
                    button.text = ""
                    button.disabled = False
        return None

    def window_continue(self, winner: str) -> None:
        """
        Всплывающее окно после окончания партии
        :param winner: строка кто победитель
        :return: None
        """
        layout = GridLayout(rows=4, padding=5)
        popup_winner = Label(text=f'{winner} WIN!')
        popup_label = Label(text='Begin New Game?')
        new_game_button = Button(text='Yes',
                                 on_press=self.restart)
        close_button = Button(text='No',
                              on_press=self.stop)
        layout.add_widget(popup_winner)
        layout.add_widget(popup_label)
        layout.add_widget(new_game_button)
        layout.add_widget(close_button)

        popup = Popup(title='GAME OVER',
                      content=layout,
                      size_hint=(None, None), size=(200, 200))
        popup.open()
        new_game_button.bind(on_press=popup.dismiss)
        return None

    def build(self):
        self.title = 'Reverse tic-tac-toe'
        primary = BoxLayout(orientation='vertical')
        layout_grid = GridLayout(cols=10, spacing=2, padding=5)

        for i in range(10):
            for j in range(10):
                button = Button(font_size=12,
                                disabled=False,
                                on_press=self.game)
                self.buttons[i][j] = button
                layout_grid.add_widget(button)

        layout_buttons = GridLayout(cols=2, size_hint=(1, None), size=(200, 50))
        layout_buttons.add_widget(Button(text='New Game',
                                         on_press=self.restart))

        layout_buttons.add_widget(Button(text='Exit',
                                         on_press=self.stop))

        primary.add_widget(layout_grid)
        primary.add_widget(layout_buttons)

        return primary


if __name__ == '__main__':
    GameApp().run()
