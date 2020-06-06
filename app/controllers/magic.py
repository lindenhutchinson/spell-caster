from flask import render_template, flash, redirect, url_for, request, session
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, logout_user

from werkzeug.datastructures import MultiDict

from app.models.m_player import MPlayer
from app.models.deck import Deck

from app.db.db import db

from app.forms import DeckForm, MPlayerForm, RandomForm, PickDeckForm, PickMPlayerForm

from app.utils.model_helpers import *
import random


def toggle_active_player():
    player_id = request.json['id']
    player = get_model(MPlayer, player_id)
    act = player.is_active
    update_model(player, {'is_active': not player.is_active})
    return "player is not active" if act else "player is active"


def toggle_active_deck():
    deck_id = request.json['id']
    deck = get_model(Deck, deck_id)
    act = deck.is_active
    update_model(deck, {'is_active': not deck.is_active})
    return "deck is not active" if act else "deck is active"


def create_deck():
    form = DeckForm()

    # insert the created note into the database after the user has submitted the form
    if form.is_submitted():
        insert_form(Deck, form)
        flash("Created a deck!")
        return redirect(url_for('create_deck'))

    return render_template('form.html', form=form, title="Create Deck")


def delete_players():
    form = PickMPlayerForm()

    form.player_id.choices = get_select_choices(MPlayer, 'name')

    if form.is_submitted():
        flash("Deleted player!")
        p = get_model(MPlayer, form.player_id.data)
        delete_model(p)
        return redirect(url_for('delete_players')) if get_default(MPlayer) else redirect(url_for('view_magic'))

    return render_template("form.html", form=form, title="Delete Players")


def delete_decks():
    form = PickDeckForm()
    form.deck_id.choices = get_select_choices(Deck, 'name')

    if form.is_submitted():
        flash("Deleted deck!")
        d = get_model(Deck, form.deck_id.data)
        delete_model(d)
        return redirect(url_for('delete_decks')) if get_default(Deck) else redirect(url_for('view_magic'))

    return render_template("form.html", form=form, title="Delete Decks")


def create_player():
    form = MPlayerForm()

    if form.is_submitted():
        insert_form(MPlayer, form)
        flash("Created a player!")
        return redirect(url_for('create_player'))

    return render_template('form.html', form=form, title="Create Player")


def view_magic():
    decks = get_all_models(Deck)
    players = get_all_models(MPlayer)
    active_players = [p.id for p in players if p.is_active]
    active_decks = [d.id for d in decks if d.is_active]

    form = RandomForm()
    chosen_players = []
    chosen_decks = []
    playing = {}

    if form.is_submitted():
        chosen_players = [p for p in players if p.is_active]
        chosen_decks = [d for d in decks if d.is_active]
        # random.shuffle(chosen_players)
        random.shuffle(chosen_decks)
        if len(chosen_decks) < len(chosen_players):
            flash("You don't have enough decks for that number of players!")
        elif len(chosen_players) == 0:
            flash("You're going to need some players to do that!")
        else:
            for p in chosen_players:
                d = random.choice(chosen_decks)
                chosen_decks.remove(d)
                playing.update({p.name:d.name})


    return render_template('magic.html', form=form, playing=playing, active_players=active_players,active_decks=active_decks, decks=decks, players=players, title="Magic")
    
