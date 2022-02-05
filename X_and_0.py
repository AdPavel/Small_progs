from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import random



Config.set('graphics', 'height', '500')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'resizable', '0')

class GameApp(App):
    # x_count, o_count = 0, 0
    #
    def __init__(self):
        super().__init__()
        self.switch = True
        self.buttons = [[0]*10 for _ in range(10)]
        self.rules_dict = {'vertical': [[], []], 'horizontal': [[], []],
                           'main_diagonal': [[], []], 'secondary_diagonal': [[], []]}


    def comp_turn(self):
        comp_button = self.buttons[random.randint(0, 9)][random.randint(0, 9)]
        while comp_button.disabled:
            comp_button = self.buttons[random.randint(0, 9)][random.randint(0, 9)]
        comp_button.disabled = True
        comp_button.text = '0'
        self.switch = not self.switch
        return comp_button


    def is_fail(self, button, key, idx):
        if button.text == 'X':
            self.rules_dict[key][0].append(idx)
            self.rules_dict[key][1].clear()
        elif button.text == '0':
            self.rules_dict[key][1].append(idx)
            self.rules_dict[key][0].clear()
        elif button.text == '':
            self.rules_dict[key][1].clear()
            self.rules_dict[key][0].clear()
        return (len(self.rules_dict[key][0]) == 5 or len(self.rules_dict[key][1]) == 5, key)


    def rules(self, arg):
        for i in range(len(self.buttons)):
            try:
                y = self.buttons[i].index(arg)
                x = i
                break
            except:
                pass
        for i in range(10):
            for j in range(10):
                if x == i:
                    false, dict_key = self.is_fail(self.buttons[i][j], 'horizontal', (i, j))
                    if false:
                        return (false, dict_key)
                if y == j:
                    false, dict_key = self.is_fail(self.buttons[i][j], 'vertical', (i, j))
                    if false:
                        return (false, dict_key)
                if (y - j) == (x - i):
                    false, dict_key = self.is_fail(self.buttons[i][j], 'secondary_diagonal', (i, j))
                    if false:
                        return (false, dict_key)
                if (i + j) == (x + y):
                    false, dict_key = self.is_fail(self.buttons[i][j], 'main_diagonal', (i, j))
                    if false:
                        return (false, dict_key)
        [[v.clear() for v in val] for val in self.rules_dict.values()]
        return (False, 0)


    def show_fail(self, idx_list):
        self.switch = True
        for i, j in idx_list:
            self.buttons[i][j].color = [0, 1, 0, 1]
        self.restart()
        self.exit_confirmation()
        # popup = Popup(content=Label(text="I am popup"))
        # popup.open()

    def game(self, arg):
        arg.disabled = True
        arg.text = 'X'
        self.switch = not self.switch

        fail, dict_key = self.rules(arg)
        if fail:
            print('U FAIL, begin?:')
            self.show_fail(self.rules_dict[dict_key][0])
        else:
            fail, dict_key = self.rules(self.comp_turn())
            if fail:
                print('COMP FAIL')
                self.show_fail(self.rules_dict[dict_key][1])

    def restart(self, args=True):
        self.switch = True
        for row in self.buttons:
            for button in row:
                if args is bool:
                    button.disabled = args
                else:
                    button.color = [0, 0, 0, 0]
                    button.text = ""
                    button.disabled = False


    def exit_confirmation(self):
        # popup can only have one Widget.  This can be fixed by adding a BoxLayout

        self.box_popup = BoxLayout(orientation='horizontal')

        self.box_popup.add_widget(Label(text="Really exit?"))

        self.box_popup.add_widget(Button(
            text="Yes",
            on_press=self.stop,
            size_hint=(0.215, 0.075)))

        self.box_popup.add_widget(Button(
            text="No",
            # on_press=self.popup_exit.dismiss,
            size_hint=(0.215, 0.075)))

        # self.popup_exit = Popup(title="Exit",
        #                         content=self.box_popup,
        #                         size_hint=(0.4, 0.4),
        #                         auto_dismiss=True)
        #
        # self.popup_exit.open()
        # coordinate = (
        #     (0, 1, 2), (3, 4, 5), (6, 7, 8),  # X
        #     (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Y
        #     (0, 4, 8), (2, 4, 6),  # D
        # )
        #
        # vector = lambda item: [self.buttons[x].text for x in item]
        #
        # color = [0, 1, 0, 1]
        #
        # for item in coordinate:
        #     if vector(item).count('X') == 3 or vector(item).count('O') == 3:
        #         win = True
        #         for i in item:
        #             self.buttons[i].color = color
        #         for button in self.buttons:
        #             button.disabled = True
        #         break

    # def restart(self, arg):
    #     self.switch = True
    #
    #     for button in self.buttons:
    #         button.color = [0, 0, 0, 1]
    #         button.text = ""
    #         button.disabled = False

    def build(self):
        self.title = "Обратные крестики-нолики"
        primary = BoxLayout(orientation="vertical")
        grid = GridLayout(cols=10, spacing=2, padding=5)

        for i in range(10):
            for j in range(10):
                button = Button(
                    # color=[1, 0, 0, 0],
                    font_size=12,
                    disabled=False,
                    on_press=self.game
                )
                self.buttons[i][j] = button
                grid.add_widget(button)

        primary.add_widget(grid)

        primary.add_widget(
            Button(
                text="New Game",
                size_hint=[1, .1],
                on_press=self.restart#(flag=True)
            )
        )

        primary.add_widget(
            Button(
                text="Exit",
                size_hint=[1, .1],
                on_press=self.stop
            )
        )
        return primary


if __name__ == '__main__':
    GameApp().run()