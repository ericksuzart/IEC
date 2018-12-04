import os  # biblioteca para manipular os arquivos
import wave # biblioteca para trabalhar com arquivos .wav
import numpy as np # biblioteca para manipular os vetores/canais de áudio (pip install numpy)
import soundfile as sf  # biblioteca para manipular os áudios (pip install pysoundfile)
import matplotlib.pyplot as plt # biblioteca para plotar a função (pip install -U matplotlib)

pasta = str(input("Digite o caminho completo da pasta que deseja manipular os arquivos de áudio: "))
### Comando que vai para a pasta destino onde estão os arquivos ###
os.chdir('%s'%pasta)
### Comando que lista os arquivos que estão no diretório ###
diretorio = os.listdir('.')

num = 1
### Para cada arquivo no diretório ###
for arquivo in diretorio:
    ### Extraio um vetor contendo os dados e a taxa de amostragem ###
    dados, samplerate = sf.read('%s'%arquivo)
    ### Crio uma lista vazia ###
    data_list = []

    ### Testo se é uma matriz ou um vetor, se sim: ###
    if dados[0].size == 2:
        ### Para cada amostra na matriz orignal ###
        for amostra in dados:
            ### Adiciono um valor correspondente a média dos dois valores na lista vazia ###
            data_list.append((amostra[0] + amostra[1])/2)

        ### Transformo a lista em um vetor(objeto) através da biblioteca "numpy" ###
        data_mono = np.array(data_list)
        ### Edito o arquivo transformando-o em "mono" ###
        sf.write('%s'%arquivo, data_mono,samplerate)

    ### Se não: ###
    else:
        ### Digo que o arquivo não é estereo ###
        print('O arquivo "%s" não é estereo!!'%arquivo)

    ### Se não, se o nome do arquivo for diferente do padrão: ###
    if arquivo != '%d.wav'%num:        
        ### Renomeio o arquivo original no padrão "n.wav", onde "n" é um inteiro ###
        os.rename('%s'%arquivo,'%d.wav'%num)
        ### Digo que o arquivo(e o novo nome dele) não é estereo ###
        print('O arquivo "%s" foi renomeado para %d.wav"'%(arquivo, num))

    num +=1

arquivo = str(input("Digite o nome do arquivo que deseja plotar no gráfico: "))
### Para cada arquivo no diretório(após a modificação) ###
for arq in os.listdir('.'):
    if arquivo == arq:
        ### Seleciono e abro .wav o arquivo digitado em questão no modo somente leitura ###
        musica = wave.open('%s'%arq,'r')
        ### Leio todos os frames (amostras) do áudio, transformando-os em strings ###
        form_onda = musica.readframes(-1)
        ### Transformo as strings lidas anteriormente em vetores ###
        form_onda = np.fromstring(form_onda, 'Int16')
        ### Obtenho a frequência de amostragem da música ###
        fa = musica.getframerate()
        ### Faço a divisão da quantidade total de amostras pela fa
        ### para obter o tempo (em segundos) ###
        tempo = np.linspace(0, len(form_onda)/fa, num=len(form_onda))
        ### Afim de obter a amplitude com referência em tensão (-1 a +1V),
        ### divido os níveis de quantização por (2^16)/2 ###
        amplit = form_onda/32768
        ### Faz a plotagem gráfico, com o título indicado, em função do tempo ###
        plt.figure(1)
        plt.xlabel("Tempo")
        plt.ylabel("Amplitude")
        plt.title('Formas de onda do arquivo %s'%arq)
        plt.plot(tempo, amplit)
        plt.show()
