from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import numpy as np

import sys
import time

#TODO: add numeros, caracteres especiais
#TODO: g diferente nas fontes (talvez sumir com 'g')
#TODO: n sendo confundido com m (talvez sumir com 'm')

#TODO: Inverter plano de fundo?
#TODO: desenhar f minusculo quando for F maisuculo

TYPE = "TRAIN"
#TYPE = "TEST"

# Quantas vezes criar cada tipo de letra
repeatType = 100
# Total de imagens =  (nºchars*2 + 4)*repeatType * nº fontes
# Imagens de cada caractere = 2 * repeatType * nº fontes
#
# Imagens de cada caractere = 2 * 100 * 16 = 3200

WSIZE, HSIZE = 100, 100
CHARSIZE = (32, 32)

STARTPOSX = 20
STARTPOSY = 20

# Treino
if TYPE.lower() == "train":
    DIR = 'data/train/'
    FONTS = ("arial.ttf", "consola.ttf", "AGENCYR.TTF", "COLONNA.TTF", "ARLRDBD.TTF", "FRAHV.TTF",
             "JUICE___.TTF", "GOTHIC.TTF", "CHILLER.TTF", "comic.ttf", "COOPBL.TTF", "CURLZ___.TTF",
             "JOKERMAN.TTF", "ariali.ttf", "BELLI.TTF", "couri.ttf")
# Teste
else:
    DIR = 'data/test/'
    FONTS = ("YuGothL.ttc", "ntailu.ttf", "LATINWD.TTF", "CENTAUR.TTF")

TOTALSIZE = len(FONTS)*repeatType

# Considerações:
# 'C' == 'c'
# 'f' == 'F'
# 'k' == 'K'
# 'l' (L) ignorado por parecer com 'i' (I)
# 'o' == 'O'
# 'p' == 'P'
# 's' == 'S'
# 'u' == 'U'
# 'v' == 'V'
# 'w' === 'W'
# 'x' == 'X'
# 'Y' == 'y' 
# 'z' == 'Z'
CHARS = ['a', 'b', 'd', 'e', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'z',\
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'T', 'Y',\
         'Ç', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Margem na hora de recortar a imagem
MARGINX = 10
MARGINTOP = 5
MARGINBOTTOM = 5

# Modo da imagem
# 1 -> pixel só ter valor de 0 ou 1
# "L" -> pixel varia de 0 a 255
MODOIMAGEM = "L"


n = 0
elapsed = time.time()
for f in range(len(FONTS)):

    font = ImageFont.truetype(FONTS[f], 50)

    def imgCreate(c, crop = True, posNoise = True):
        img  = Image.new(mode = MODOIMAGEM, size = (WSIZE, HSIZE))
        draw = ImageDraw.Draw(img)

        # Calcula ruído à posição (utilizado também para decidir se aplica ruído agressivo na imagem)
        noiseX = np.random.randint(-5,5)

        # Adiciona ruído à imagem
        gauss = np.random.normal(10,5,WSIZE*HSIZE) # Ruido branco
        # Ruído "agressivo"
        if noiseX > 4:
            gauss += np.random.choice([0, 255], size=WSIZE*HSIZE, p=[0.8, 0.2])
        elif noiseX > 0:
            gauss += np.random.choice([0, 255], size=WSIZE*HSIZE, p=[0.9, 0.1])

        img.putdata(gauss)

        # Ruído à posição
        if posNoise:
            noiseY = np.random.randint(-5,5)
            draw.text((STARTPOSX + noiseX, STARTPOSY + noiseY), c, 255, font=font, anchor="lt")
        else:
            draw.text((STARTPOSX, STARTPOSY), c, 255, font=font, anchor="lt")


        # Recorta a região de interesse
        if crop:
            (w, h), _ = font.font.getsize(c)

            top = STARTPOSY
            bottom = STARTPOSY + h
            left = STARTPOSX
            right = STARTPOSX + w

            # No caso de haver ruído de posição,
            # é importante ter uma margem para não cortar o caractere
            if posNoise:
                top -= MARGINTOP
                bottom += MARGINBOTTOM
                left -= MARGINX
                right += MARGINX

            img = img.crop((left, top, right, bottom))


        # Ajusta o tamanho da imagem
        img = img.resize(CHARSIZE)

        if noiseX > 3:
            draw = ImageDraw.Draw(img)
            # Desenha um quadrado aleatório ao redor da tela
            posX = np.random.randint(0,28)
            posY = np.random.randint(0,28)
            draw.rectangle((posX, posY, posX+noiseX, posY+noiseX), fill=255)
        elif noiseX < -4:
            draw = ImageDraw.Draw(img)
            # Desenha uma linha preta aleatória cortando a letra
            posY1 = np.random.randint(0,25)
            posY2 = np.random.randint(0,25)
            draw.line((0, posY1, 32, posY2), fill=0, width=2)
        elif noiseX < -3:
            draw = ImageDraw.Draw(img)
            # Desenha uma linha branca aleatória cortando a letra
            posY1 = np.random.randint(0,25)
            posY2 = np.random.randint(0,25)
            draw.line((0, posY1, 32, posY2), fill=255, width=2)

        return img


    def imgCreateBlank(strongNoise = False):
        img  = Image.new(mode = MODOIMAGEM, size = CHARSIZE)

        if strongNoise:
            gauss = np.random.normal(127,50,CHARSIZE[0]*CHARSIZE[1])
        else:
            gauss = np.random.choice([0, 255], size=CHARSIZE[0]*CHARSIZE[1], p=[0.8, 0.2])

        img.putdata(gauss)

        draw = ImageDraw.Draw(img)
        # Desenha um quadrado aleatório ao redor da tela
        posX = np.random.randint(0,28)
        posY = np.random.randint(0,28)
        size = np.random.randint(-5,5)
        draw.rectangle((posX, posY, posX+size, posY+size), fill=255)

        return img


    def imgSave(c, img):
        name = DIR + c + str(n) + ".jpg"

        img.save(name)


    # Cria n imagens 'iguais' variando a posição
    # e adicionando ruído
    for r in range(repeatType):
        # Caractere normal (sem ruído de posição)
        for c in CHARS:
            img = imgCreate(c, posNoise = False)

            imgSave(c, img)
        
            n += 1

        # Caractere rotacionado -45 a 45º
        rotation = np.random.randint(-45,45)
        for c in CHARS:
            img = imgCreate(c)

            img = img.rotate(rotation)

            imgSave(c, img)
        
            n += 1


        # Imagens vazias
        for _ in range(2):
            img = imgCreateBlank()

            imgSave('_', img)

            n += 1

        # Imagens com ruído forte
        for _ in range(2):
            img = imgCreateBlank(strongNoise=True)

            imgSave('(', img)

            n += 1

        processed = r + 1 + repeatType*f
        sys.stdout.write("\rConjunto de imagens processadas: %d/%d - %.1f%% - Imagens: %d - ETC: %d s       "%(processed, TOTALSIZE, 100*processed/TOTALSIZE, n, (time.time() - elapsed)*(TOTALSIZE-processed)))
        elapsed = time.time()
