from PIL import Image, ImageFont, ImageDraw

dir = 'data/'

# Treino
# Futuramente: Edwardian Script ITC
FONTS = ("arial.ttf", "consola.ttf", "AGENCYR.TTF", "COLONNA.TTF", "ARLRDBD.TTF", "FRAHV.TTF",
         "JUICE___.TTF", "GOTHIC.TTF", "CHILLER.TTF", "comic.ttf", "COOPBL.TTF", "CURLZ___.TTF",
         "JOKERMAN.TTF", "ariali.ttf", "BELLI.TTF", "couri.ttf")
# Teste
#FONTS = ["YuGothL.ttc", "ntailu.ttf", "LATINWD.TTF", "CENTAUR.TTF"]

PHRASES = ["abcdefghijklmnopqrstuvwxyz",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "1234567890"]

for f in FONTS:
    font = ImageFont.truetype(f, 50)

    w, h = (0,0)
    for phr in PHRASES:
        (w1, h1), _ = font.font.getsize(phr)
        w = max(w1,w)
        h += h1

    img  = Image.new(mode = "L", size = (w, h+5*3))

    draw = ImageDraw.Draw(img)

    h = 5
    for i in range(len(PHRASES)):
        draw.text((0,h), PHRASES[i], 255, font=font, anchor="lt")
        (_, h1), _ = font.font.getsize(PHRASES[i])
        h += h1 + 5

    name = dir + f.split(".")[0] + ".jpg"

    img.save(name)
