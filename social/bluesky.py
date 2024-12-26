import os
from atproto import Client, models


handle = os.environ.get("BSKY_HANDLE")
password = os.environ.get("BSKY_PASSWORD")

client = Client()
client.login(handle, password)


def publish(post_text=None, recap_date=None, post_image=None):
    post_text += "\n\n#NBASky\n#NBA"
    facets = [
        models.AppBskyRichtextFacet.Main(
            models.AppBskyRichtextFacet.Tag(
                tag="#NBASky",
                index=models.AppBskyRichtextFacet.ByteSlice(
                    byte_start=len(post_text)-12, byte_end=len(post_text) - 5)
            )
        ),
        models.AppBskyRichtextFacet.Main(
            models.AppBskyRichtextFacet.Tag(
                tag="#NBA",
                index=models.AppBskyRichtextFacet.ByteSlice(
                    byte_start=len(post_text)-5, byte_end=len(post_text))
            )
        ),
    ]

    client.send_post(text=post_text, facets=facets)
    return
