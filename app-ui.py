# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, jsonify, request, abort, render_template
from discord.BotApiModel import BotApiModel
import discord.manager as botMan
from dotenv import load_dotenv
import os
import jwt

app = Flask(__name__)

load_dotenv()


def validate_token(token):
    algorithm = app.config['JWT_ALGORITHM']
    secret = app.config['JWT_PUBLIC_KEY']

    try:
        decoded = jwt.decode(token, secret, algorithms=[algorithm])
        return True
    except:
        return False


def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.cookies.get('identity-token') and validate_token(request.cookies.get('identity-token')):
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


@app.route('/api/discordbots', methods=['GET'])
@require_appkey
def get_bots():
    botModels = []
    for bot in botMan.get_bots():
        model = BotApiModel()
        model.Id = bot.id
        model.Name = bot.name
        model.Description = bot.description
        model.IsRunning = bot.is_running()
        botModels.append(model.serialize())
    return jsonify(botModels)


@app.route('/api/discordbots', methods=['DELETE'])
@require_appkey
def killall_bots():
    botMan.killall()
    return "Ok", 200


@app.route('/api/discordbots/<int:id>', methods=['DELETE'])
@require_appkey
def kill_bot(id):
    botMan.kill(id)
    return "Ok", 200


@app.route('/api/discordbots/<int:id>', methods=['POST'])
@require_appkey
def run_bot(id):
    botMan.start(id)
    return "Ok", 200


@app.route('/', methods=['GET'])
@require_appkey
def main_view():
    return render_template('index.html')


def jwt_auth_config():
    app.config['JWT_ALGORITHM'] = 'RS256'
    app.config['JWT_PUBLIC_KEY'] = open(os.getenv('JWT_KEY_PATH')).read()


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    jwt_auth_config()
    app.run(port=9989)
    botMan.killall()
