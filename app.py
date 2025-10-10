from flask import Flask, render_template, request
from services.steam_service import SteamService
from config import Config

app = Flask(__name__)
steam_service = SteamService(Config.STEAM_ID, country_code="ZA")

games_cache = None

def get_cached_games():
    global games_cache
    if games_cache is None:
        print("Fetching games from steam api")
        games_cache = steam_service.get_all_games()
    return games_cache

@app.route('/')
def index():
    games = get_cached_games()
    return render_template('index.html', total_games = len(games))

@app.route('/wishlist')
def wishlist():
    min_discount = int(request.args.get('min_discount', 0))
    max_discount = int(request.args.get('max_discount', 100))

    games = get_cached_games()

    filtered_games = steam_service.filter_by_discount_range(games, min_discount, max_discount)

    filtered_games = sorted(filtered_games, key=lambda x: x['discount_percent'], reverse=True)

    return render_template('wishlist.html',
                           games=filtered_games,
                           total_games = len(games),
                           filtered_count = len(filtered_games),
                           min_discount = min_discount,
                           max_discount = max_discount)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)