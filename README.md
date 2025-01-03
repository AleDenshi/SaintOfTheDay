# SaintOfTheDay

Discord bot that posts the Catholic Saint of the day at a specified time.

## Installation

Run the following to install the prerequisites:

```sh
pip install discord python-dotenv pillow
```

To set the Discord token, edit the `.env` file:

```env
DISCORD_TOKEN=2934029340293...
```

## Usage

Upon inviting the bot to your server, run `/addchannel` to add the bot to a specific channel, or `/removechannel` to remove the bot from that channel. By default, the bot will send the Saint of the Day at 13:00 UTC (8:00 AM EST) **although this can be customized using `/settime` (TODO!)**

## Data

This respository contains Creative Commons images of the saints, in addition to a database named `saints.csv` with information on all of the saints. This data may be incomplete as it is still being compiled.
