from .controllers import home, user, character, _class, spell, note, spellbook, magic, monster, action, npc


def routes(app):
    '''All Routes / Url
    This app uses an MVC pattern, hence all the url are routed here
    Just import your logics from the controllers package and route
    using the add_url_rule function

    :param app: Flask app instance
    :return: None
    '''

    # Common errors handled already for you. you can add more
    app.register_error_handler(403, home.error_pages)
    app.register_error_handler(404, home.error_pages)
    app.register_error_handler(500, home.error_pages)

    # Add your Url rules here
    # app.add_url_rule('/', view_func=home.index)
    app.add_url_rule('/', view_func=spell.view_all_spells, methods=['GET', 'POST'])

    app.add_url_rule('/register', view_func=user.register, methods=['GET','POST'])
    app.add_url_rule('/login', view_func=user.login, methods=['GET','POST'])
    app.add_url_rule('/logout', view_func=user.logout)

    # app.add_url_rule('/user', view_func=user.view_user, methods=['GET'])
    # app.add_url_rule('/user/edit', view_func=user.edit_user, methods=['GET','POST'])

    app.add_url_rule('/npc', view_func=npc.view_npcs, methods=['GET'])


    app.add_url_rule('/action/edit', view_func=action.edit_action, methods=['GET','POST'])
    app.add_url_rule('/action/delete', view_func=action.delete_action, methods=['GET'])
    app.add_url_rule('/action/create', view_func=action.create_action, methods=['GET','POST'])
    app.add_url_rule('/action', view_func=action.view_action, methods=['GET','POST'])
    app.add_url_rule('/action/res', view_func=action.change_action_res, methods=['POST'])
    app.add_url_rule('/action/reset', view_func=action.reset_action, methods=['POST'])


    app.add_url_rule('/char/create', view_func=character.create_char, methods=['GET','POST'])
    app.add_url_rule('/char/edit', view_func=character.edit_char, methods=['GET','POST'])
    app.add_url_rule('/char/delete', view_func=character.delete_char, methods=['GET'])
    app.add_url_rule('/char', view_func=character.view_char, methods=['GET','POST'])
    app.add_url_rule('/char/slot', view_func=character.change_slot_val, methods=['POST'])
    app.add_url_rule('/char/stats/create', view_func=character.create_stats, methods=['GET', 'POST'])
    app.add_url_rule('/char/stats/edit', view_func=character.edit_stats, methods=['GET', 'POST'])

    app.add_url_rule('/class/create', view_func=_class.create_class, methods=['GET','POST'])
    app.add_url_rule('/class', view_func=_class.view_class, methods=['GET','POST'])
    app.add_url_rule('/class/edit', view_func=_class.edit_class, methods=['GET','POST'])
    app.add_url_rule('/class/delete', view_func=_class.delete_class, methods=['GET'])

    app.add_url_rule('/spell/create', view_func=spell.create_spell, methods=['GET', 'POST'])
    app.add_url_rule('/spell/edit', view_func=spell.edit_spell, methods=['GET', 'POST'])
    app.add_url_rule('/spell/delete', view_func=spell.delete_spell, methods=['GET'])
    app.add_url_rule('/spell', view_func=spell.view_spell, methods=['GET', 'POST'])
    app.add_url_rule('/spell/all', view_func=spell.view_all_spells, methods=['GET', 'POST'])

    app.add_url_rule('/spell/prepare', view_func=spellbook.prepare_spells, methods=['GET', 'POST'])
    app.add_url_rule('/spell/prepare/add', view_func=spellbook.prepare_spell, methods=['POST'])
    app.add_url_rule('/spell/learn', view_func=spellbook.learn_spells, methods=['GET', 'POST'])
    app.add_url_rule('/spell/learn/add', view_func=spellbook.learn_spell, methods=['POST'])
    app.add_url_rule('/spell/learn/class', view_func=spellbook.learn_class_spells, methods=['POST'])

    app.add_url_rule('/notes', view_func=note.view_note, methods=['GET','POST'])
    app.add_url_rule('/notes/create', view_func=note.create_note, methods=['GET','POST'])
    app.add_url_rule('/notes/edit', view_func=note.edit_note, methods=['GET','POST'])
    app.add_url_rule('/notes/delete', view_func=note.delete_note, methods=['GET'])


    app.add_url_rule('/monsters', view_func=monster.view_monster, methods=['GET'])

    app.add_url_rule('/magic/', view_func=magic.view_magic, methods=['GET','POST'])
    app.add_url_rule('/magic/player/delete', view_func=magic.delete_players, methods=['GET','POST'])
    app.add_url_rule('/magic/player/create', view_func=magic.create_player, methods=['GET','POST'])
    app.add_url_rule('/magic/player/activate', view_func=magic.toggle_active_player, methods=['POST'])
    app.add_url_rule('/magic/deck/activate', view_func=magic.toggle_active_deck, methods=['POST'])
    app.add_url_rule('/magic/deck/create', view_func=magic.create_deck, methods=['GET','POST'])
    app.add_url_rule('/magic/deck/delete', view_func=magic.delete_decks, methods=['GET','POST'])




