import os
from PIL import Image
import random
import numpy as np


class dataHandler():
    '''Contém funções para ler imagens de caracteres
       e retornar features e labels
    '''
    def __init__(self):
        self.train_features = []
        self.train_labels = []
        self.test_features = []
        self.test_labels = []
        

    def loadData(self, dir = "data/", nShuffle = 10):
        '''Lê os dados e armazena as features
           e labels dentro das variáveis internas

           Args:
               dir: diretório de onde ler dados
               nShuffle: quantidade de vezes para
                         embaralhar dados
        '''
        for f in os.listdir(dir + "train/"):
            img = Image.open(dir + "train/" + f)
            feature = list(img.getdata())
            
            self.train_features.append(feature)
            # Letras minúsculas == letras maísculas
            self.train_labels.append(f[0].lower())

        for f in os.listdir(dir + "test/"):
            img = Image.open(dir + "test/" + f)
            feature = list(img.getdata())
            
            self.test_features.append(feature)
            # Letras minúsculas == letras maísculas
            self.test_labels.append(f[0].lower())

        # Embaralha os dados
        emb = list(zip(self.train_features, self.train_labels))
        
        for _ in range(nShuffle):
            random.shuffle(emb)

        self.train_features, self.train_labels = zip(*emb)

        emb = list(zip(self.test_features, self.test_labels))
        
        for _ in range(nShuffle):
            random.shuffle(emb)

        self.test_features, self.test_labels = zip(*emb)        


    def oneHotEncode(self):
        ''' Codifica os labels usando One Hot Encoding
        '''
        self.classes = list(set(self.train_labels))
        newLabels = []

        for i in self.train_labels:
            encoded = [0 for x in range(len(self.classes))]
            index = self.classes.index(i)
            encoded[index] = 1
            newLabels.append(encoded)
            
        self.train_labels = newLabels

        newLabels = []

        for i in self.test_labels:
            encoded = [0 for x in range(len(self.classes))]
            index = self.classes.index(i)
            encoded[index] = 1
            newLabels.append(encoded)
            
        self.test_labels = newLabels

    
    def oneHotDecode(self, label):
        '''Informa qual é a classe a partir do label
           codificado
        '''
        index = np.argmax(label)

        return self.classes[index]


    def getFeatures(self):
        '''Retorna as features divididas em treino e teste
        '''
        return self.train_features, self.test_features


    def getLabels(self):
        '''Retorna os labels divididos em treino e teste
        '''
        return self.train_labels, self.test_labels

    
    def getClassCount(self):
        '''Retorna a quantidade de classes diferentes
        '''
        return len(self.classes)

