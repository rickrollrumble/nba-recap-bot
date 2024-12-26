from datetime import datetime, timedelta
from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2
from nba_api.stats.endpoints.boxscoretraditionalv3 import BoxScoreTraditionalV3
import pandas as pd
import heapq

results = {}

previous_day = datetime.now() - timedelta(days=1)


def fetch_game_results() -> str | None:

    # Fetch scoreboard data for the previous day
    scoreboard = ScoreboardV2(game_date=previous_day.strftime("%Y-%m-%d"))
    games = scoreboard.line_score.get_dict()['data']

    if not games:
        return 'There were no games yesterday, or maybe we are in the off-season.\n I hope you got some fresh air, touched some grass, etc. x'

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
            "{0} {1} - {2} {3}".format(
                result['team_1'],
                "{:<3}".format(result['team_1_score']),
                "{:>3}".format(result["team_2_score"]),
                result['team_2']
            )
        )

    return "🏀 Final Scores 🏀 ({0})\n\n".format(previous_day.strftime(
        "%a, %d-%b %y")) + '\n\n'.join(results_text)


def fetch_top_performers() -> str | None:
    if not results:
        return "As I said, no games. Take it easy."

    df = pd.DataFrame()
    for game in results:
        box_score = BoxScoreTraditionalV3(game)
        box_score.load_response()
        player_stats = box_score.player_stats
        df = pd.concat([df, player_stats.get_data_frame()])

    max_scores = df.loc[df.groupby(
        'gameId')['points'].transform(max) == df['points']]

    final = max_scores[['playerSlug', 'points', 'reboundsTotal', 'assists',
                        'blocks', 'steals']].sort_values(by='points', ascending=False).head()

    box_scores = final.set_index(keys='playerSlug').rename(
        columns={
            'reboundsTotal': 'REB',
            "points": "PTS",
            "assists": "AST",
            "steals": "STL",
            "blocks": "BLK"
        }).transpose().to_dict()

    result = []
    for player in box_scores:
        top_3_stats = heapq.nlargest(
            3, box_scores[player], key=box_scores[player].get)
        statline = []
        for stat in top_3_stats:
            statline.append(f"{box_scores[player][stat]} {stat}")
        result.append(
            f"{player.replace('-',' ').title()}\n{' / '.join(statline)}\n")

    return '📈 Top Performers 🚀 ({0})\n\n'.format(previous_day.strftime(
        "%a, %d-%b %y")) + '\n'.join(result)
