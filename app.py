from flask import Flask, jsonify
from discord.BotApiModel import BotApiModel
import discord.manager as botMan

app = Flask(__name__)


@app.route('/api/discordbots', methods=['GET'])
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


@app.route('/api/discordbots/killall', methods=['DELETE'])
def killall_bots():
    botMan.kill()
    return "Ok", 200


@app.route('/api/discordbots/kill/<int:id>', methods=['DELETE'])
def kill_bot(id):
    botMan.kill(id)
    return "Ok", 200


@app.route('/api/discordbots/run/<int:id>', methods=['POST'])
def run_bot(id):
    botMan.start(id)
    return "Ok", 200


if __name__ == "__main__":
    app.run(port=9989)
