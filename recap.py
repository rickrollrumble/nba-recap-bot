from datetime import datetime, timedelta
from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2

results = {}


def fetch_game_results() -> str | None:
    previous_day = datetime.now() - timedelta(days=1)
    date_str = previous_day.strftime('%Y-%m-%d')  # Format: YYYY-MM-DD

    # Fetch scoreboard data for the previous day
    scoreboard = ScoreboardV2(game_date=date_str)
    games = scoreboard.line_score.get_dict()['data']

    if not games:
        return 'There were no games yesterday,  I hope you got some fresh air, touched some grass, etc. x'
    
    # Process and print game results
    game_id_index = 2
    for game in games:
        if game[game_id_index] not in games:
            results[game[game_id_index]] = {}

    team_abbrev_index = 4
    points_index = 22
    for game in games:
        if 'team_1' not in results[game[game_id_index]]:
            results[game[game_id_index]]['team_1'] = game[team_abbrev_index]
            results[game[game_id_index]]['team_1_score'] = game[points_index]
            continue
        if 'team_2' not in results[game[game_id_index]]:
            results[game[game_id_index]]['team_2'] = game[team_abbrev_index]
            results[game[game_id_index]]['team_2_score'] = game[points_index]
            continue

    results_text = []
    for result in results.values():
        results_text.append(
            f"{result['team_1']} {"{:<3}".format(
                result['team_1_score'])} - {"{:>3}".format(result['team_2_score'])} {result['team_2']}"
        )

    return '\n'.join(results_text)
