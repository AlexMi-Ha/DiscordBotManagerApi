# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, jsonify, request, abort, render_template, redirect
from discord.BotApiModel import BotApiModel
import discord.manager as botMan
from dotenv import load_dotenv
import os
import jwt

app = Flask(__name__)
DEBUG_MODE = True

load_dotenv()

def jwt_auth_config():
    alg = 'RS256'
    key = open(os.getenv('JWT_KEY_PATH')).read()
    issuer = os.getenv('JWT_ISSUER')
    audience = os.getenv('JWT_AUDIENCE')
    role = os.getenv('JWT_ROLE')
    return (key, alg, issuer, audience, role)

(KEY, ALGORITHM, ISSUER, AUDIENCE, REQUIRED_ROLE) = jwt_auth_config()

def validate_token(token):
    try:
        decoded = jwt.decode(token, KEY, algorithms=[ALGORITHM], issuer=ISSUER, audience=AUDIENCE)
        has_role = REQUIRED_ROLE in decoded['roles']
        return has_role
    except:
        return False


def authorize(user = False):
    def require_appkey(view_function):
        @wraps(view_function)
        def decorated_function(*args, **kwargs):
            print("auth")
            if request.cookies.get('identity-token') and validate_token(request.cookies.get('identity-token')) or DEBUG_MODE:
                print("Succ")
                return view_function(*args, **kwargs)
            else:
                if user:
                    return redirect(os.getenv('IDENTITY_URL'))
                else:
                    abort(401)
        return decorated_function
    return require_appkey


@app.route('/api/discordbots', methods=['GET'])
@authorize()
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


@app.route('/api/discordbots/runningbots', methods=['DELETE'])
@authorize()
def killall_bots():
    botMan.killall()
    return "Ok", 200

@app.route('/api/discordbots', methods=['POST'])
@authorize()
def add_bot():
    print("lel")
    github = request.form.get('github')
    name = request.form.get('name')
    description = request.form.get('description')
    entry = request.form.get('entry')
    environment = request.form.get('environment')

    botMan.add_bot(github, name, description, entry, environment)
    return "Ok", 200

@app.route('/api/discordbots/<string:id>/pull', methods=['POST'])
@authorize()
def pull_bot(id):
    botMan.pull_bot(id)
    return "Ok", 200

@app.route('/api/discordbots/<string:id>/config', methods=['POST'])
@authorize()
def update_config(id):
    environment = request.form.get('environment')
    botMan.update_env(id, environment)
    return "Ok", 200

@app.route('/api/discordbots/<string:id>/config', methods=['GET'])
@authorize()
def get_config(id):
    return jsonify(botMan.get_env(id))
    

@app.route('/api/discordbots/<string:id>', methods=['DELETE'])
@authorize()
def delete_bot(id):
    botMan.remove_bot(id)
    return "Ok", 200

@app.route('/api/discordbots/runningbots/<string:id>', methods=['DELETE'])
@authorize()
def kill_bot(id):
    botMan.kill(id)
    return "Ok", 200


@app.route('/api/discordbots/runningbots/<string:id>', methods=['POST'])
@authorize()
def run_bot(id):
    botMan.start(id)
    return "Ok", 200


@app.route('/', methods=['GET'])
@authorize(True)
def main_view():
    return render_template('index.html')


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(port=9989)
    botMan.killall()
