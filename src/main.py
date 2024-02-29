from .cube.cube import Cube
from .cube.gui import Gui

if __name__ == "__main__":
    cube = Cube(2)
    gui = Gui(cube)
    gui.run()
