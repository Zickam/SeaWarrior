import os

from model.models import Model
from presenter.main import Presenter
from view.main import GeneralView

from view.constants import SCREEN_RESOLUTION

def main():
    model = Model()
    presenter = Presenter(model)
    view = GeneralView(presenter, model, SCREEN_RESOLUTION)

    while True:
        view.update()
        presenter.handleEvents()


if __name__ == "__main__":
    current_dir = os.getcwd()
    print(current_dir)
    main()