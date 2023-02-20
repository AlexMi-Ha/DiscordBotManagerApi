# Discord Bot Management API
API to manage all of your Discord Bots<br />
Starting `app.py` starts a web server listening on port `9989`

## Endpoints
Make sure to set the `x-api-key` header to your API Key specified in the `.env` file!

`GET /api/discordbots/`<br/>
Retrieves all running bots in following format:
```
{
  "Id": 0,
  "Name": "string",
  "Description": "string",
  "IsRunning": false
}
```
`POST /api/discordbots/run/{id}`<br/>
Starts the Discord bot with the given ID


`DELETE /api/discordbots/kill/{id}`<br/>
Stops the Discord bot with the given ID

`DELETE /api/discordbots/killall`<br/>
Stops all Discord bots that are currently running

## Setup
Create a `.env` file in the root folder of the project. There you can specify all your secrets.<br />
```
API_TOKEN=SuperSecretApiKeyToAccessThisManagementApi_AddItToEveryHeader
BOT1_TOKEN=DiscordBotToken
...
```
## Build
- Without Docker<br />
`pip3 install requirements.txt`<br />
`python3 app.py`<br />

- With Docker<br/>
Run the `build.sh`
