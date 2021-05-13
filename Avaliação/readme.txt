Padrão: 30 epochs

Dados: Apenas letras sem Ç:
• Rede 1:
MLP

• Rede 2:
CNN c/ 2 Fully connected layers - 512
Rede CNN batch_size 512


Dados: Letras e números (incluindo Ç)
• Rede 3:
CNN c/ 2 Fully connected layers - 512
Rede CNN batch_size 256: 95,96 %
Rede CNN batch_size 512: 96,24 %
Rede CNN batch_size 128: 96,30 %

• Rede 4:
CNN c/ 1 Fully connected layer - 512
Rede CNN batch_size 128: 96,10 %


Dados: Letras e numeros (incluindo Ç, ? e /)
• Rede 5:
CNN c/ 1 Fully connected layer - 512
       80 filtros 1a camada e 64 2a
Rede CNN batch_size 256: 94,97 %	

• Rede 6:
CNN c/ 1 Fully connected layer - 256
       80 filtros 1a camada kernel 5x5
       64 filtros na 2a e kernel 3x3
Rede CNN batch_size 256: 95,32 %



Dados: Letras e numeros (incluindo Ç ? / ( ) e !)
• Rede 7:
CNN c/ 1 Fully connected layer - 256
       80 filtros 1a camada kernel 5x5
       64 filtros na 2a e kernel 3x3
Rede CNN batch_size 256: 95,78 %

• Rede 8:
CNN igual a do artigo para ICDAR 03, 05...
Rede CNN batch_size 64: 90,25%

• Rede 9:
CNN igual a do artigo para ICDAR 03, 05...
+ 1º layer = normalização
Rede CNN batch_size 64: 92,83%

• Rede 10:
CNN c/ 1 Fully connected layer - 256
       80 filtros 1a camada kernel 5x5
       64 filtros na 2a e kernel 3x3
	strides de tamanho 1
Rede CNN batch_size 256: 94,78 %

• Rede 11:
CNN c/ 1 Fully connected layer - 256
       80 filtros 1a camada kernel 5x5
       64 filtros na 2a e kernel 3x3
	strides de tamanho 2
Rede CNN batch_size 256: 95,00 %

• Rede 12:
CNN c/ 1 Fully connected layer - 256
       80 filtros 1a camada kernel 7x7
       64 filtros na 2a e kernel 5x5
	strides de tamanho 2
Rede CNN batch_size 256: 94,16 %

• Rede 13:
CNN c/ 1 Fully connected layer - 256
       80 filtros 1a camada kernel 5x5
       64 filtros na 2a e kernel 3x3
       64 filtros na 3a e kernel 3x3
	strides de tamanho 2
Rede CNN batch_size 256: 94,03 %