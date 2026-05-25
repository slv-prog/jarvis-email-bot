# Jarvis Email Bot

An AI-powered bot that reads your Gmail inbox daily, 
summarises every email using Claude AI, flags urgent 
emails, and delivers a clean digest to Telegram every morning.

## What it does
- Connects to Gmail and fetches last 24 hours of emails
- Uses Claude AI to summarise each email in 2 sentences
- Flags emails that need urgent action
- Delivers formatted digest to Telegram automatically

## Tech stack
- Python
- Claude AI (Anthropic API)
- Gmail API
- Telegram Bot API

## Demo
[Add your Telegram screenshot here]

## Setup
1. Clone this repo
2. Install dependencies: pip install anthropic google-auth google-auth-oauthlib google-api-python-client python-dotenv requests
3. Add your API keys to .env file
4. Run: python jarvis_bot.py
