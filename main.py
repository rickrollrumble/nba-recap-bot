from PIL import Image, ImageDraw, ImageFont
import recap
from social import bluesky 
# create an image
out = Image.new("RGB", (1280, 720), (255, 255, 255))

fnt = ImageFont.truetype("font.ttf", 60)
# get a drawing context
d = ImageDraw.Draw(out)

# draw multiline text
d.multiline_text(
    xy=(10, 10),
    text="Final Scores".center(17) + "\n" + recap.fetch_game_results(),
    font=fnt, fill=(0, 0, 0)
)
d.line((50, 50), fill='black', width=5)
out.save(fp="recap.jpg")
