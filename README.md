# Task Manager Bot

## Introduction
Task Manager Bot is a Telegram bot designed to help users manage their tasks and receive timely reminders. Users can add, view, and remove tasks while also setting reminders with different repetition options (daily, weekly, or monthly).

## Features
- 📌 **Add Tasks**: Users can create tasks with specific times and repetition settings.
- ⏰ **Task Reminders**: The bot sends notifications at the scheduled time.
- 🔁 **Repetition Options**: Tasks can be set to repeat daily, weekly, or monthly.
- 📋 **View Tasks**: Users can list all their scheduled tasks.
- ❌ **Remove Tasks**: Users can delete tasks they no longer need.
- 📞 **Support Contact**: Users can easily reach out for support.

## Commands
- `/start` - Start the bot and display available options.
- `/addtask` - Add a new task with time and repetition settings.
- `/mytasks` - View the list of scheduled tasks.
- `/removetask` - Remove a specific task.
- `/support` - Get support contact information.

## Installation & Setup
1. Clone this repository or download the script.
2. Install dependencies using:
   ```sh
   pip install pyTelegramBotAPI python-dotenv
   ```
3. Create a `.env` file in the same directory and add your bot token and channel ID:
   ```env
   TOKEN=your_telegram_bot_token
   CHANNEL_ID=your_channel_id
   SUPPORT_ID=@your_support_username
   ```
4. Run the bot using:
   ```sh
   python bot.py
   ```

## How It Works
1. The user starts the bot using `/start` and subscribes to the specified Telegram channel.
2. The user can add a task by sending `/addtask`, entering the task details, and specifying a time.
3. The bot asks for a repetition option (once, daily, weekly, or monthly).
4. At the specified time, the bot sends a reminder message to the user.
5. The user can list their tasks using `/mytasks` or remove a task using `/removetask`.

## Threaded Reminder System
The bot runs a background thread that continuously checks the current time and sends reminders when tasks match the scheduled time.


