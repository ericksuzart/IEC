import os  # biblioteca para manipular arquivos
import numpy as np 
import soundfile as sf  # biblioteca para manipular áudios (pip install pysoundfile)

pasta = str(input("Digite o caminho completo da pasta que deseja manipular os arquivos de áudio: "))
### Comando que vai para a pasta destino onde estão os arquivos ###
os.chdir('%s'%pasta)

num = 1
### Para cada arquivo no diretório ###
for arquivo in os.listdir('.'):
    ### Extraio um vetor contendo os dados e a taxa de amostragem ###
    dados, samplerate = sf.read('%s'%arquivo)
    ### Crio uma lista vazia ###
    data_list = []

    ### Testo se é uma matriz ou um vetor ###
    if dados[0].size == 2:
        ### Para cada amostra na matriz orignal ###
        for amostra in dados:
            ### Adiciono um valor correspondente a média dos dois valores na lista vazia ###
            data_list.append((amostra[0] + amostra[1])/2)

        ### Transformo a lista em um vetor(objeto) através da biblioteca "numpy" ###
        data_mono = np.array(data_list)
        ### Renomeio o arquivo original no padrão "n.wav", onde "n" é um inteiro ###
        os.rename('%s'%arquivo,'%d.wav'%num)
        ### Edito o arquivo transformando-o em "mono" ###
        sf.write('%d.wav'%num, data_mono,samplerate)
        num +=1

    else:        
        print('O arquivo "%s" não é estereo!!'%arquivo)