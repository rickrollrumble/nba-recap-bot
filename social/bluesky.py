import os
from atproto import Client


handle = os.environ.get("BSKY_HANDLE")
password = os.environ.get("BSKY_PASSWORD")

client = Client()
client.login(handle, password)


def publish(post_text=None, recap_date=None, post_image=None):
    with open(post_image, 'rb') as f:
        img_data = f.read()

    client.send_image(
        text='sweet summer child thinking all these shenanigans will make him a better developer',
        image=img_data,
        image_alt='no alt for this one'
    )

    return
