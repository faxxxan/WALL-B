# DiscordBot Module Documentation

## Overview

The `DiscordBot` module hosts a Discord bot that monitors for @mentions and
answers questions by forwarding them to the `ChatGPT` module (via the
`ai/input` / `ai/response` pubsub topics).

When a user @mentions the bot in a channel or thread the bot will:

1. Collect the recent thread history as context (if the message is already
   inside a thread).
2. Combine the context, the configured system prompt, and the knowledge-source
   URLs into a single query.
3. Publish the query to the `ai/input` topic so that the `ChatGPT` module can
   generate a response.
4. Post the response back to Discord – inside the existing thread if one is
   present, or inside a **new thread** created from the original post otherwise.

## Configuration

Enable the module by editing `config/discordbot.yml`:

```yaml
discordbot:
  enabled: true                               # Set to true to activate
  path: modules.network.discordbot.DiscordBot
  config:
    prompt: >
      You are a helpful assistant for the modular-biped open-source robotics
      project. Answer questions clearly and concisely, referencing the provided
      knowledge sources where relevant. If you are unsure of an answer, say so
      and direct the user to the appropriate knowledge source.
    knowledge_sources:
      - https://github.com/makerforgetech/modular-biped/wiki
      - https://github.com/makerforgetech/modular-biped/discussions
      - https://github.com/makerforgetech/modular-biped
  dependencies:
    python:
      - discord.py
    additional:
      - https://discord.com/developers/applications
```

### Configuration options

| Key | Type | Description |
|-----|------|-------------|
| `prompt` | `str` | System prompt sent to the AI for every question. |
| `knowledge_sources` | `list[str]` | URLs appended to the system prompt as reference sources. |

## Dependencies

After enabling the module, install the required Python package:

```bash
pip install discord.py
```

Or run `./install.sh` if the project installer is configured to read module
dependencies.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_BOT_TOKEN` | **Yes** | Discord bot token obtained from the Developer Portal. |

**Never commit your bot token to source control.**

## Setup

### 1. Create a Discord application and bot

1. Open the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** and give it a name.
3. Navigate to **Bot** → **Add Bot**.
4. Under **Token**, click **Reset Token** and copy the value.
5. Set the token as an environment variable:

   ```bash
   export DISCORD_BOT_TOKEN="your-token-here"
   ```

### 2. Configure bot permissions (intents)

In the Developer Portal under **Bot**:

* Enable **MESSAGE CONTENT INTENT** (required so the bot can read message text).

### 3. Invite the bot to your server

1. Navigate to **OAuth2 → URL Generator**.
2. Select the `bot` scope.
3. Under **Bot Permissions** select at minimum:
   - **Read Messages / View Channels**
   - **Send Messages**
   - **Create Public Threads**
   - **Send Messages in Threads**
4. Copy the generated URL and open it in a browser to invite the bot.

## Pubsub topics

### Topics the module subscribes to

| Topic | Arguments | Description |
|-------|-----------|-------------|
| `ai/response` | `response` (str) | Receives the AI-generated reply and delivers it to Discord. |
| `discord/send` | `channel_id` (int), `message` (str) | Allows other modules to post a message to a specific channel. |
| `system/exit` | – | Gracefully disconnects the bot when the system shuts down. |

### Topics the module publishes to

| Topic | Arguments | Description |
|-------|-----------|-------------|
| `ai/input` | `text` (str) | Sends the assembled question to the `ChatGPT` module. |
| `log/*` | `message` (str) | Standard structured logging (via `BaseModule.log`). |

## Usage examples

### Asking the bot a question

Simply @mention the bot followed by your question in any channel it can see:

```
@YourBot What is the purpose of the modular-biped project?
```

The bot will create a thread (or reply in the existing one) with an
AI-generated answer that references the configured knowledge sources.

### Sending a message from another module

```python
self.publish('discord/send', channel_id=123456789012345678, message='Hello from the robot!')
```

## Integration with the ChatGPT module

The `DiscordBot` module integrates with the `ChatGPT` module through the
standard `ai/input` / `ai/response` pubsub interface:

```
Discord mention → DiscordBot → publish('ai/input', text=...) → ChatGPT
ChatGPT → publish('ai/response', response=...) → DiscordBot → Discord thread
```

Both modules must be **enabled** in their respective YAML config files for
end-to-end functionality.

## Security

* The bot token is read exclusively from the `DISCORD_BOT_TOKEN` environment
  variable (or the optional `token` config key as a fallback). It is never
  logged or published over pubsub.
* Avoid storing the token in the config YAML file if the file is committed to
  source control.

## Conclusion

The `DiscordBot` module provides a simple integration layer between a Discord
server and the modular-biped AI stack. By configuring a system prompt and a
list of knowledge-source URLs, operators can deploy a bot that answers
project-specific questions directly within Discord threads while keeping all
sensitive credentials safely in environment variables.
