from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import numpy as np

import sys
import time

#TODO: garantir letras pretas 0 e fundo branco 255 com contorno pequeno

TYPE = "TRAIN"
#TYPE = "TEST"

# Quantas vezes criar cada tipo de letra
repeatType = 50
# Total de imagens =  (nºchars*4 + 4)*repeatType * nº fontes
# Imagens de cada caractere = 4 * repeatType * nº fontes
#
# Imagens de cada caractere = 4 * 50 * 16 = 3200

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
# 'Ç' == 'ç'
CHARS = ['a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'q', 'r', 's', 't', 'v', 'x', 'z',\
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'T', 'U', 'Y', 'W',\
         'Ç', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '?', '/', '%']

# Margem na hora de recortar a imagem
MARGINX = 8
MARGINTOP = 5
MARGINBOTTOM = 5

# Modo da imagem
# 1 -> pixel só ter valor de 0 ou 1
# "L" -> pixel varia de 0 a 255
MODOIMAGEM = "L"


n = 0
elapsed = time.time()
meanElapsed = 0
for f in range(len(FONTS)):

    font = ImageFont.truetype(FONTS[f], 50)

    def imgCreate(c, crop = True, posNoise = True, textWhite = True):            
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
            posX = STARTPOSX + noiseX
            posY = STARTPOSY + noiseY
        else:
            posX = STARTPOSX
            posY = STARTPOSY

        # Texto branco com contorno preto
        # ou texto preto com contorno branco
        if textWhite:
            fill = np.random.randint(200,255)
            strokeF = np.random.randint(0,115)
            strokeW = np.random.randint(1,10)
        else:
            strokeF = np.random.randint(200,255)
            strokeW = np.random.randint(2,10)
            fill = np.random.randint(0,10*strokeW)


        draw.text((posX, posY), c, fill, font=font, anchor="lt", stroke_width=strokeW, stroke_fill=strokeF)

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

            left -= strokeW
            right += strokeW
            top -= strokeW
            bottom += strokeW

            img = img.crop((left, top, right, bottom))


        # Ajusta o tamanho da imagem
        #img = imgResize(img, CHARSIZE)
        img = img.resize((32,32), Image.BICUBIC)

        if noiseX > 3:
            draw = ImageDraw.Draw(img)
            # Desenha um quadrado aleatório ao redor da tela
            posX = np.random.randint(0,28)
            posY = np.random.randint(0,28)
            if textWhite:
                draw.rectangle((posX, posY, posX+noiseX, posY+noiseX), fill=255)
            else:
                draw.rectangle((posX, posY, posX+noiseX, posY+noiseX), fill=0) 
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


    def imgResize(img, size):
        '''Redimensiona o tamanho da imagem mantendo a proporção

            Args:
                img: imagem para redimensionar
                size: tamanho desejado em formato de tuple (w,h)
        '''

        w, h = img.size            

        if w > h:
            blank = np.zeros((32,32), dtype=np.uint8)

            img = img.resize((32, int(h*32/w)))
            h = img.size[1]
            offset = (32-h)//2

            img = np.array(img.getdata())
            img = img.reshape(h, 32)
            blank[offset:offset+h, :] = img[:,:]

            img = Image.fromarray(blank)
        elif h > w:
            blank = np.zeros((32,32), dtype=np.uint8)

            img = img.resize((int(w*32/h), 32))
            w = img.size[0]
            offset = (32-w)//2
            
            img = np.array(img.getdata())
            img = img.reshape(32, w)
            blank[:, offset:offset+w] = img[:,:]

            img = Image.fromarray(blank)
        else:
            img = img.resize((32, 32))
        
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
        # ? e / não podem ser usados para nomear arquivo,
        # então muda o nome para outro simbolo
        if c == '?':
            c = '+'
        elif c== '/':
            c = '-'
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
        # Não inclui a /
        rotation = np.random.randint(-45,45)
        for c in CHARS:
            if c == '/':
                continue
            img = imgCreate(c)

            img = img.rotate(rotation)

            imgSave(c, img)
        
            n += 1

        # Inverte a cor
        # Caractere normal (sem ruído de posição)
        for c in CHARS:
            img = imgCreate(c, posNoise = False, textWhite=False)

            imgSave(c, img)
        
            n += 1

        # Caractere rotacionado -45 a 45º
        # Usa a rotação anterior
        # Não inclui a /
        for c in CHARS:
            if c == '/':
                continue
            img = imgCreate(c, textWhite=False)

            img = img.rotate(rotation)

            imgSave(c, img)
        
            n += 1


        processed = r + 1 + repeatType*f
        meanElapsed = ((time.time() - elapsed)*(TOTALSIZE-processed) + meanElapsed)//2
        sys.stdout.write("\rConjunto de imagens processadas: %d/%d - %.1f%% - Imagens: %d - ETC: %d s     "%(processed, TOTALSIZE, 100*processed/TOTALSIZE, n, meanElapsed))
        elapsed = time.time()
