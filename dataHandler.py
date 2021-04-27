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
            #self.train_labels.append(f[0].lower())
            self.train_labels.append(f[0])

        self.train_features = np.array(self.train_features)
        self.train_labels = np.array(self.train_labels)

        for f in os.listdir(dir + "test/"):
            img = Image.open(dir + "test/" + f)
            feature = list(img.getdata())
            
            self.test_features.append(feature)
            # Letras minúsculas == letras maísculas
            #self.test_labels.append(f[0].lower())
            self.test_labels.append(f[0])
        
        self.test_features = np.array(self.test_features)
        self.test_labels = np.array(self.test_labels)

        # Embaralha os dados
        idxEmb = np.arange(self.train_features.shape[0])

        for _ in range(nShuffle):
            np.random.shuffle(idxEmb)

        self.train_features = self.train_features[idxEmb]
        self.train_labels = self.train_labels[idxEmb]

        idxEmb = np.arange(self.test_features.shape[0])
        
        for _ in range(nShuffle):
            np.random.shuffle(idxEmb)

        self.test_features = self.test_features[idxEmb]
        self.test_labels = self.test_labels[idxEmb]

    def oneHotEncode(self):
        ''' Codifica os labels usando One Hot Encoding
        '''
        self.classes = np.unique(self.train_labels)
        newLabels = []

        for i in self.train_labels:
            encoded = np.zeros(self.classes.shape[0])
            idx = np.where(self.classes == i)
            encoded[idx] = 1
            newLabels.append(encoded)
            
        self.train_labels = np.array(newLabels)

        newLabels = []

        for i in self.test_labels:
            encoded = np.zeros(self.classes.shape[0])
            idx = np.where(self.classes == i)
            encoded[idx] = 1
            newLabels.append(encoded)
            
        self.test_labels = np.array(newLabels)

    
    def oneHotDecode(self, label):
        '''Informa qual é a classe a partir do label
           codificado
        '''
        index = np.argmax(label)

        return self.classes[index]


    def reshapeInputs(self):
        ''' Ajusta o formato das features para trabalhar
            com uma CNN
        '''
        self.train_features = self.train_features.reshape(-1,32,32,1)
        self.test_features = self.test_features.reshape(-1,32,32,1)

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
        return self.classes.shape[0]
