# Steam Wishlist Discount Tracker

A Flask-based microservice that tracks Steam game discounts on your wishlist. Fetches pricing data from Steam's API and filters games by discount percentage using concurrent processing.

**Purpose:** Learning Flask, multi-API integration, and concurrent backend development

## What It Does

- Fetches your Steam wishlist using your Steam ID
- Retrieves pricing and discount data for each game via concurrent API calls
- Filters games by discount percentage ranges (0%, 1-10%, 11-20%, etc.)
- Reduces fetch time from ~60 seconds (sequential) to ~15 seconds (threaded)
- Web interface for filtering and viewing discounted games (in progress)

## Features

**Multi-API Integration:**
- Steam IWishlistService API for fetching game IDs
- Steam App Details API for pricing and discount information
- Handles free-to-play games, missing price data, and unreleased titles

**Concurrent Processing:**
- ThreadPoolExecutor with configurable workers (default: 10)
- Rate limiting (0.05s delay) to respect Steam's API constraints
- Tracks failed requests for debugging

**Discount Filtering:**
- Filter by exact discount percentage or ranges
- Returns structured data: app_id, name, original_price, current_price, discount_percent, is_free

**Error Handling:**
- Network timeout handling
- JSON parsing error recovery
- Graceful degradation when games can't be fetched

## Tech Stack

- **Backend:** Flask (Python 3.8+)
- **Concurrency:** concurrent.futures.ThreadPoolExecutor
- **External API:** Steam Web API
- **Configuration:** python-dotenv for environment variables

## Technology Stack

**Current (Phase 1):**
- Flask backend with HTML templates (Jinja2)
- Vanilla JavaScript for interactivity
