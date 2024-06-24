from model.models import Model
from presenter.main import Presenter
from view.constants import SCREEN_RESOLUTION
from view.main import GeneralView


def main():
    model = Model()
    presenter = Presenter(model)
    view = GeneralView(presenter, model, SCREEN_RESOLUTION)

    while True:
        view.update()
        presenter.handleEvents()


if __name__ == "__main__":
    main()