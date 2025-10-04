# Steam Wishlist Discount Tracker

**Author:** Final-year Software Engineering Student  
**Date:** October 2025  
**Tech Stack:** Python, Flask, Requests, dotenv  

---

## Project Overview

The **Steam Wishlist Discount Tracker** is a portfolio project built to strengthen Flask backend development skills, focusing on clean, maintainable code and proper project structure.  

This application fetches your Steam wishlist, retrieves pricing and discount information for each game, and allows filtering by discount percentage. The project is structured to later expose a JSON API for a mobile app frontend.

---

## Features

- Fetch your Steam wishlist using the Steam API.
- Retrieve pricing and discount information for each game.
- Filter games by discount percentages: 10%, 20%, 30%, 40%.
- Display results on an HTML page (Phase 1).
- Expose JSON API endpoints for future mobile app integration (Phase 2 planned).
- Clean, modular Flask project structure with a services layer.

---

## Motivation

- Strengthen Flask backend skills.
- Learn proper project structure and separation of concerns.
- Practice batch API processing and error handling.
- Build a portfolio-ready project that is explainable in interviews.

---

## Project Structure
STEAM_WISHLIST/
├─ services/
│ ├─ init.py
│ └─ steam_service.py # Handles Steam API calls and filtering logic
├─ .env # Stores STEAM_ID and other sensitive info
├─ config.py # Loads environment variables
├─ test_service.py # Unit testing SteamService class
├─ test_steam.py # Initial testing script using raw API calls
├─ requirements.txt # Python dependencies
└─ README.md

**Key Notes:**

- `services/steam_service.py` contains the `SteamService` class with methods:  
  - `get_wishlist_ids()`  
  - `get_game_details(app_id)`  
  - `get_all_games()`  
  - `filter_by_discount(games, min_discount=0)`  

- `config.py` handles environment variables and configuration.  
- `.env` is where you store your Steam ID securely.  

---


