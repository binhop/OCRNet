from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import numpy as np

#TODO: add numeros, caracteres especiais
#TODO: canny nos dados
#TODO: x == X

wSize, hSize = 100, 100
charSize = (32, 32)

dir = 'data/train/'
#dir = 'data/test/'
# Treino
# Futuramente: Edwardian Script ITC
fonts = ["arial.ttf", "consola.ttf", "AGENCYR.TTF", "COLONNA.TTF", "ARLRDBD.TTF", "BROADW.TTF",
         "BRUSHSCI.TTF", "GOTHIC.TTF", "CHILLER.TTF", "comic.ttf", "COOPBL.TTF", "CURLZ___.TTF",
         "JOKERMAN.TTF"]
# Teste
#fonts = ["YuGothL.ttc", "ntailu.ttf", "LATINWD.TTF", "CENTAUR.TTF"]

# Considerações:
# 'c' == 'C'
# 'k' == 'K'
# 'l' (L) ignorado por parecer com 'i' (I)
# 'o' == 'O'
# 'p' == 'P'
# 's' == 'S'
# 'u' == 'U'
# 'v' == 'V'
# 'w' === 'W'
# 'x' == 'X'
# 'z' == 'Z'
chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',\
         'A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'Q', 'R', 'T', 'Y']
        # 'ç', 'Ç', 'á', 'à', 'é', 'ê', 'ó', 'ô', 'í', 'î', 'Á', 'À', 'É', 'Ê', 'Ó', 'Ô', 'Í', 'Î']

# Modo da imagem
# 1 -> pixel só ter valor de 0 ou 1
# "L" -> pixel varia de 0 a 255
modoImagem = "L"

# Margem na hora de recortar a imagem
marginX = 10
marginTop = 10
marginBottom = 15

n = 0
for f in fonts:

    font = ImageFont.truetype(f, 50)

    def imgCreate(c, crop = True):
        img  = Image.new(mode = modoImagem, size = (wSize, hSize))
        draw = ImageDraw.Draw(img)

        # Adiciona ruído à imagem
        gauss = np.random.normal(10,5,wSize*hSize)
        img.putdata(gauss)

        # Adiciona ruído à posição
        noiseX = np.random.randint(-5,5)
        noiseY = np.random.randint(-5,5)
        
        draw.text((wSize//2 + noiseX, hSize//2 + noiseY), c, 255, font=font, anchor="mm")

        # Recorta a região de interesse
        if crop:
            (w, h), _ = font.font.getsize(c)

            top = hSize//2 - h//2 - marginTop
            bottom = hSize//2 + h//2 + marginBottom
            left = wSize//2 - w//2 - marginX
            right = wSize//2 + w//2 + marginX
            img = img.crop((left, top, right, bottom))

        # Ajusta o tamanho da imagem
        img = img.resize(charSize)
   

        return img


    def imgCreateBlank(strongNoise = False):
        img  = Image.new(mode = modoImagem, size = charSize)

        if strongNoise:
            gauss = np.random.normal(127,50,charSize[0]*charSize[1])
        else:
            gauss = np.random.normal(20,10,charSize[0]*charSize[1])

        img.putdata(gauss)

        return img


    def imgSave(c, img):
        name = dir + c + str(n) + ".jpg"

        img.save(name)


    # Cria n imagens 'iguais' variando a posição
    # e adicionando ruído
    for _ in range(50):
        # Caractere normal
        for c in chars:
            img = imgCreate(c)

            imgSave(c, img)
        
            n += 1

        # Caractere rotacionado 15º
        for c in chars:
            img = imgCreate(c)

            img = img.rotate(15)

            imgSave(c, img)
        
            n += 1

        # Caractere rotacionado -15º
        for c in chars:
            img = imgCreate(c)

            img = img.rotate(-15)

            imgSave(c, img)

            n += 1

        # Caractere rotacionado 30º
        for c in chars:
            img = imgCreate(c)

            img = img.rotate(30)

            imgSave(c, img)
        
            n += 1

        # Caractere rotacionado -30º
        for c in chars:
            img = imgCreate(c)

            img = img.rotate(-30)

            imgSave(c, img)

            n += 1

        # Imagens vazias
        for _ in range(5):
            img = imgCreateBlank()

            imgSave('_', img)

            n += 1

        # Imagens com ruído forte
        for _ in range(5):
            img = imgCreateBlank(strongNoise=True)

            imgSave('(', img)

            n += 1

        