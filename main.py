from model.main import Model
from presenter.main import Presenter
from view.main import View

def main():
    model = Model()
    presenter = Presenter(model)
    view = View(presenter, model)

    while True:
        view.update()
        presenter.handleEvents()

if __name__ == "__main__":
    main()