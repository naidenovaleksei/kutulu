from model import KutuluModel
from view.view import View


if __name__ == '__main__':
    model = KutuluModel()
    view = View(model)
    game_must_go_on = True

    while (game_must_go_on):
        if not view.loop():
            break
        game_must_go_on = model.make_turn()
        view.clock.tick(10)
    else:
        model.finish()