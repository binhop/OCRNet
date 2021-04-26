from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

w_size, h_size = 100, 100

dir = 'data/train/'
#dir = 'data/test/'
# Treino
fonts = ["arial.ttf", "consola.ttf", "AGENCYR.TTF", "ALGER.TTF", "ARLRDBD.TTF", "BROADW.TTF",
         "BRUSHSCI.TTF", "GOTHIC.TTF", "CHILLER.TTF", "comic.ttf", "COOPBL.TTF", "CURLZ___.TTF",
         "GOUDYSTO.TTF"]
# Teste
#fonts = ["YuGothL.ttc", "ntailu.ttf", "LATINWD.TTF", "CENTAUR.TTF"]
# Futuramente: Edwardian Script ITC

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',\
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        # 'ç', 'Ç', 'á', 'à', 'é', 'ê', 'ó', 'ô', 'í', 'î', 'Á', 'À', 'É', 'Ê', 'Ó', 'Ô', 'Í', 'Î']

# Modo da imagem
# 1 -> pixel só ter valor de 0 ou 1
# "L" -> pixel varia de 0 a 255
modoImagem = "1"

n = 0
for f in fonts:

    font = ImageFont.truetype(f, 50)

    # Caractere normal
    for c in chars:
        img  = Image.new(mode = modoImagem, size = (w_size, h_size))
        draw = ImageDraw.Draw(img)
        
        draw.text((w_size//2, h_size//2), c, 255, font=font, anchor="mm")

        # Diferencia o nome se for minúsculo (l) ou maiúsculo (u)
        name = c + "l" if c.islower() else c + "u"
        name += str(n) + ".jpg"

        img.save(dir + name)
    
    n += 1

    # Caractere rotacionado 15º
    for c in chars:
        img  = Image.new(mode = modoImagem, size = (w_size, h_size))
        draw = ImageDraw.Draw(img)
        
        draw.text((w_size//2, h_size//2), c, 255, font=font, anchor="mm")

        img = img.rotate(15,  expand=0)

        # Diferencia o nome se for minúsculo (l) ou maiúsculo (u)
        name = c + "l" if c.islower() else c + "u"
        name += str(n) + ".jpg"

        img.save(dir + name) 
    
    n += 1

    # Caractere rotacionado -15º
    for c in chars:
        img  = Image.new(mode = modoImagem, size = (w_size, h_size))
        draw = ImageDraw.Draw(img)
        
        draw.text((w_size//2, h_size//2), c, 255, font=font, anchor="mm")

        img = img.rotate(-15,  expand=0)

        # Diferencia o nome se for minúsculo (l) ou maiúsculo (u)
        name = c + "l" if c.islower() else c + "u"
        name += str(n) + ".jpg"

        img.save(dir + name) 
    
    n += 1