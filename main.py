import recap
import bluesky
import flask
import functions_framework


@functions_framework.http
def run_bot(request):
    try:
        bluesky.publish(recap.fetch_game_results())
        bluesky.publish(recap.fetch_top_performers())
    except Exception as e:
        return flask.Response(response= f"{e}", status=500)
    return "Published!" 
