# DISCORDJIYA
# Discord Bot with Chat, Polls, Reminders, and Music Functionality

This project is a Discord bot built using the `discord.py` library and Google Gemini AI. The bot supports various functionalities like responding to user messages, setting reminders, creating polls, summarizing long messages using AI, and managing a music queue system.

## Features

### 1. **Responding to User Messages**
   - The bot listens to user messages in a Discord server and responds to commands with predefined functionalities.

### 2. **Reminders**
   - Users can set reminders with specific time and message. The bot sends a private message to the user when the reminder is due.
   - Reminders can be deleted once they are triggered.

### 3. **Polls**
   - Users can create polls with multiple options. Polls support reactions (e.g., 1️⃣, 2️⃣, etc.) to vote for an option.
   - Users can also delete polls.

### 4. **Summarizing Text**
   - The bot can summarize long texts provided by users by using the Google Gemini API (AI-powered summarization).

### 5. **Music Queue System**
   - Users can add songs to a music queue with the `!play` command.
   - The bot shows the current song queue when users use the `!queue` command.

### 6. **Custom Welcome Messages**
   - The bot automatically sends a welcome message to new members joining the server.

### 7. **Auto-Delete Expired Reminders**
   - The bot automatically deletes expired reminders from the system once the reminder is sent to the user.

## Installation

### Prerequisites
1. **pip** for installing Python packages.
2. **Discord Developer Account**: Create a Discord bot and obtain the bot token.
3. **Google Gemini API Key**: Sign up for Google AI and obtain an API key for Gemini (AI model).

### Steps to Set Up

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
