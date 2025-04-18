# === BACKEND (Flask) ===
# app.py
from flask import request, jsonify, session, redirect, url_for

from functions import find_closest_answer
from load_files import *
from models import *
from language import translate_and_summarize_in_en, translate_en_text_in_multilang


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')

    user = User.query.filter_by(username=username).first()
    if user:
        session['username'] = username
        session['user_id'] = user.id
        
        return jsonify({'success': True, 'redirect': '/chat'})
    else:
        return jsonify({'success': False, 'message': 'Utilisateur non trouvé.'})


@app.route('/logout', methods=['POST'])
def logout():
    session['username'] = None
    session['user_id'] = None

    if 'username' in session:
        del session['username']
    if 'user_id' in session:
        del session['user_id']

    return jsonify({'success': True, 'redirect': '/login', 'message': "Nous n'arrivons pas à vous déconnecter."})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    full_name = data.get('full_name')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'Ce nom d’utilisateur existe déjà.'})

    new_user = User(username=username, full_name=full_name)
    db.session.add(new_user)
    db.session.commit()
    session['username'] = username
    return jsonify({'success': True, 'redirect': '/chat'})


@app.route('/check-auth', methods=['GET'])
def check_auth():
    if session.get('username') and session.get('user_id'):
        return jsonify({'authenticated': True, 'username': session['username']})
    else:
        return jsonify({'authenticated': False})


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in', 'redirect': '/logout', 'authenticated': False}), 401

    translated, summary_text, lang = translate_and_summarize_in_en(question)

    result = find_closest_answer(translated, index, sentences)

    answer = result['question_trouvee']

    answer_in_multilang = translate_en_text_in_multilang(answer, lang)
    
    qa = QA(question=question, answer=answer_in_multilang, user_id=user_id)
    db.session.add(qa)
    db.session.commit()

    return jsonify({'answer': answer_in_multilang})


@app.route('/history', methods=['GET'])
def history():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Not logged in', 'redirect': '/logout', 'authenticated': False}), 401

    qas = QA.query.filter_by(user_id=user_id).all()
    return jsonify([{'question': qa.question, 'answer': qa.answer} for qa in qas])



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
