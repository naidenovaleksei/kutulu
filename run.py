from model import KutuluModel
from view.view import View


if __name__ == '__main__':
    model = KutuluModel()
    view = View(model)

    while (True):
        if not view.loop():
            break
        model.make_turn()
        view.clock.tick(1)
    else:
        model.finish()