# Steam Wishlist Discount Tracker

A Flask-based backend service that fetches your Steam wishlist, retrieves pricing and discount information, and allows filtering by discount percentage.
**Purpose:** Learning Flask, API integration, and backend development  

## What It Does

- Fetches your Steam wishlist using the Steam API
- Retrieves pricing, discount, and free game information for each title
- Filters games based on minimum discount thresholds (10%, 20%, 30%, 40%)
- Displays results on an HTML page (Phase 1)
- Provides JSON data endpoints for future mobile app integration (Phase 2)

## Features

**Wishlist API Integration:**
- Pulls your full Steam wishlist using your Steam ID
- Handles missing price data and free-to-play games gracefully
- Error handling for flaky or unavailable API responses

**Discount Filtering:**
- Filter games by minimum discount
- Returns structured game data: app ID, name, original price, current price, discount, free status

**Batch Processing with Rate Limiting:**
- Sequential API calls with sleep intervals to avoid Steam rate limits
- Tracks failed API requests for debugging and retries

**Web Interface (Phase 1):**
- Simple HTML display of wishlist games
- Ready for expansion into JSON endpoints for mobile apps

## Tech Stack

- **Backend:** Flask (Python)
- **External API:** Steam Web API
- **HTTP Requests:** `requests` library
- **Configuration:** `python-dotenv` for environment variables
- **Utilities:** `time.sleep` for rate-limiting

## Project Structure

