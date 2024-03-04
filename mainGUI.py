from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from subprocess import Popen


class ImageButton(ButtonBehavior, Image):
    pass


class PyzzleApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Header
        header = Label(text='Pyzzle App', font_size='24sp', size_hint_y=None, height=50)
        layout.add_widget(header)

        # Scrollable buttons
        scroll_view = ScrollView(size_hint=(1, None), height=300)
        buttons_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))

        # Button 1: Maze Solver
        button1 = Button(text='Maze Solver', size_hint_y=None, height=40)
        button1.bind(on_press=lambda x: self.open_script('solver/maze_solver/maze_solver.py'))
        buttons_layout.add_widget(button1)

        # Button 2: Rubik's Cube Solver
        button2 = Button(text="Rubik's Cube Solver", size_hint_y=None, height=40)
        button2.bind(on_press=lambda x: self.open_script('solver/rubik_solver/main.py'))
        buttons_layout.add_widget(button2)

        # Button 3: Sudoku Solver
        button3 = Button(text='Sudoku Solver', size_hint_y=None, height=40)
        button3.bind(on_press=lambda x: self.open_script('solver/sudoku_solver/sudoku_gui.py'))
        buttons_layout.add_widget(button3)

        scroll_view.add_widget(buttons_layout)
        layout.add_widget(scroll_view)

        # Footer
        footer = Label(text='© 2024 JAVALORANT Corporation', font_size='12sp')
        layout.add_widget(footer)

        return layout

    def open_script(self, script_name):
        # Open the specified Python script using subprocess
        Popen(['python', script_name])


if __name__ == '__main__':
    PyzzleApp().run()
