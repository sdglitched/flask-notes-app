from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from webapp import db

import json


views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        new_note = Note(note = note, user_id = current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category = 'success')
    return render_template("home.html", user = current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category = 'success')
    return jsonify({})

@views.route('/edit-note/<id>', methods=['GET', 'POST'])
def edit_note(id):
    edited_note = request.form.get('editnote')
    if edited_note:
        Note.query.get(id).note = edited_note
        db.session.commit()
        flash('Note edited!', category = 'success')
        return redirect(url_for('views.home'))
    return render_template("editNote.html", user = current_user, id = id)

