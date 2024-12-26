import os
from atproto import Client, models


handle = os.environ.get("BSKY_HANDLE")
password = os.environ.get("BSKY_PASSWORD")

client = Client()
client.login(handle, password)


def publish(post_text=None, recap_date=None, post_image=None):
    text = "#NBASky #NBA"
    facets = [
        models.AppBskyRichtextFacet.Main(
            features=[models.AppBskyRichtextFacet.Tag(tag="NBASky")],
            index=models.AppBskyRichtextFacet.ByteSlice(
                byte_start=0, byte_end=7
            )
        ),
        models.AppBskyRichtextFacet.Main(
            features=[models.AppBskyRichtextFacet.Tag(tag="NBA")],
            index=models.AppBskyRichtextFacet.ByteSlice(
                byte_start=8, byte_end=12,
            )
        )
    ]
    text += f"\n\n{post_text}"
    client.send_post(text=text, facets=facets)

    return
