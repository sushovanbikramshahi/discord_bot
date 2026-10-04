
A Discord bot made with Python and discord.py.

## Commands

Prefix: `!`

| Command | What it does | Example |
|---------|--------------|---------|
| `!assign @user @role` | Gives a role to a member | `!assign @Ram @moderator` |
| `!remove @user @role` | Removes a role from a member | `!remove @Ram @moderator` |
| `!poll question` | Creates a poll with 👍 / 👎 buttons | `!poll Do you like pizza?` |
| `!imp message` | joins voice and alerts people of the imp message | `!imp I need the papers now.` |
|`!kick @user @reason` | kicks the member with reason given by administator | `!kick @ram @spamming` |
|`!ban @user @reason` | ban the member with reason given by administator | `!ban @ram @spamming` |
|`!warn @user @reason` | warn the member with reason and bans if maximum warning is reached | `!warn@ram @spamming` |
|`!warncount @user ` | Shows the warn count of the user | `!warncount @ram ` |
|`!resetcount @user`  | Resets the warn count of the user | `!resetwarn @ram ` |
|`!current_weather`  | Shows the current weather | `!current weather ` |





## Automatic features

- Welcomes new members when they join with a nice template
- Deletes messages with banned words and warns the sender

## How to run it

1. Install the requirements: `pip install -r requirements.txt`
2. Create a `.env` file with your bot token: `DISCORD_KEY=your_token_here`
3. Run the bot: `python main.py`