"""Сапер Medium"""

import random
import flet as ft


def main(page: ft.Page) -> None:
    # settings for game
    page.title = "Saper"
    page.window_height = 350
    page.window_width = 500
    page.window_center()
    page.update()

    # functions for game
    def boot_game(event: ft.ControlEvent):
        page.clean()
        game._Game__generate_field()
        game.reboot_user_field()
        game.start()
        for i in game.user_field:
            page.add(ft.Row(i))
        page.update()

    def on_clicked(event: ft.ControlEvent):
        x, y = event.control.url
        if game.field[x][y] == 1:
            page.clean()
            page.add(ft.Text("LOSER", size=20))
            page.add(ft.ElevatedButton("Перезапустить игру", on_click=boot_game))
        else:
            event.control.text = str(game.find_bombs(x, y))
            event.control.bgcolor = "green"
            if game.end() == 8:
                page.clean()
                page.add(ft.Text("WINNER", size=20))
                page.add(ft.ElevatedButton("Перезапустить игру", on_click=boot_game))
        page.update()

    def on_long(event: ft.ControlEvent):
        if event.control.bgcolor == "red":
            event.control.text = "X"
            event.control.color = "yellow"
            event.control.bgcolor = "gray"
        else:
            event.control.text = "B"
            event.control.bgcolor = "red"
        if game.end() == 8:
            page.clean()
            page.add(ft.Text("WINNER", size=20))
            page.add(ft.ElevatedButton("Запустить игру", on_click=boot_game))
        page.update()

    class Game:

        def __init__(self, difficulty: int = 0) -> None:
            self.difficulty = difficulty
            self.in_game = False
            self.field = []
            self.user_field = [
                [
                    ft.ElevatedButton(
                        text="X",
                        style=ft.ButtonStyle(
                            shape=ft.BeveledRectangleBorder(),
                            color="yellow",
                            elevation=1,
                        ),
                        url=(j, i),
                        on_click=on_clicked,
                        on_long_press=on_long,
                    )
                    for i in range(7)
                ]
                for j in range(7)
            ]
            self.__generate_field()
            self.start()

        def __generate_field(self):
            self.field = [[0 for _ in range(7)] for _ in range(7)]
            bomb_indices = random.sample(
                range(49), 8
            )  # Выбираем 8 случайных индексов без повторений
            for index in bomb_indices:
                x, y = index // 7, index % 7
                self.field[x][y] = 1  # Устанавливаем бомбу в выбранную клетку

        def find_bombs(self, x: int, y: int) -> list:
            count = 0
            for x1 in range(-1, 2):
                for y2 in range(-1, 2):
                    if x1 == y2 == 0:
                        continue
                    try:
                        if x + x1 >= 0 and y + y2 >= 0:
                            if self.field[x + x1][y + y2] == 1:
                                count += 1
                    except:
                        continue
            return str(count)

        def reboot_user_field(self):
            self.user_field = self.user_field = [
                [
                    ft.ElevatedButton(
                        text="X",
                        style=ft.ButtonStyle(
                            shape=ft.BeveledRectangleBorder(),
                            color="yellow",
                            elevation=1,
                        ),
                        url=(j, i),
                        on_click=on_clicked,
                        on_long_press=on_long,
                    )
                    for i in range(7)
                ]
                for j in range(7)
            ]

        def start(self):
            for i in range(len(self.field)):
                for j in range(len(self.field[i])):
                    if (self.field[i][j] == 0) and (self.find_bombs(i, j) == "0"):
                        self.user_field[i][j].text = "0"
                        self.user_field[i][j].bgcolor = "green"

        def end(self):
            count = 0
            for i in game.user_field:
                for j in i:
                    if j.bgcolor == "red" and game.field[j.url[0]][j.url[1]]:
                        count += 1
            return count

    game = Game(0)
    page.update()

    for i in game.user_field:
        page.add(ft.Row(i))
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
