# Discord Bot Management API
API to manage all of your Discord Bots<br />
Starting `app-api.py` starts a web server listening on port `9989`

## Endpoints
Make sure to set the `x-api-key` header to your API Key specified in the `.env` file!

`GET /api/discordbots`<br/>
Retrieves all running bots in following format:
```
{
  "Id": 0,
  "Name": "string",
  "Description": "string",
  "IsRunning": false
}
```
`POST /api/discordbots/{id}`<br/>
Starts the Discord bot with the given ID


`DELETE /api/discordbots/{id}`<br/>
Stops the Discord bot with the given ID

`DELETE /api/discordbots`<br/>
Stops all Discord bots that are currently running

## UI Variant
There is also a UI example supplied in `app-ui.py` it uses an OAuth security token to authenticate the user and serves a simple UI for the interaction with the API.

> The jwt token is read from the `identity-token` cookie.

## Setup (only for no-ui variant)
Create a `.env` file in the root folder of the project. There you can specify all your secrets.<br />
```
API_TOKEN=SuperSecretApiKeyToAccessThisManagementApi_AddItToEveryHeader
BOT1_TOKEN=DiscordBotToken
...
```
Add all your Bot-Scripts to the `/discord/bots/` folder and edit the `/discord/bots.txt` like:
```
<ID>:<NAME>:<DESCRIPTION>:<PATH>
1:Test Bot:Dieser Bot steht zu Testzwecken zur verfügung:./discord/bots/test/testbot.py
2:Test2:Description2:Path2
...
```
You can access the Discord Bot Tokens from the `.env` file via `os.getenv('BOT1_TOKEN')`
## Build
- Without Docker<br />
`pip3 install -r requirements.txt`<br />
`python3 app-api.py`<br />

- With Docker<br/>
Run the `build.sh`
