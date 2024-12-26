import recap
import bluesky
import flask
import functions_framework


@functions_framework.http
def run_bot() -> flask.typing.ResponseReturnValue:
    try:
        bluesky.publish(recap.fetch_game_results())
        bluesky.publish(recap.fetch_top_performers())
    except:
        return flask.Response(status=500)
    return "OK"
