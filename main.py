import recap
from social import bluesky

bluesky.publish(recap.fetch_game_results())

bluesky.publish(recap.fetch_top_performers())