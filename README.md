# Event Prize Raffle Bot

Telegram bot for organizing prize raffles at live events and concerts. Allows participants to register by subscribing to channels, then randomly selects a winner.

## Features

- **Participant Registration**: Users must subscribe to required channels to join
- **Automatic Winner Selection**: Random draw from registered participants
- **Admin Panel**: View all participants and select winners
- **Winner Notification**: Automatically notifies the winner

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install aiogram
   ```

3. Configure environment:
   - Create `.env` file according to an example
   - Add your bot token from [@BotFather](https://t.me/BotFather)
   - Set `CHANNEL_IDS` and `ADMIN_IDS` in `.env`

4. Add bot as administrator to channels:
   - Make your bot an administrator in all channels specified in `CHANNEL_IDS`
   - This is required for subscription verification to work properly

5. Run the bot:
   ```bash
   python main.py
   ```

## Usage

- **Participants**: Send `/start` and subscribe to required channels
- **Admins**: Use admin keyboard to view participants or select a random winner

