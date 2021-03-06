import os, sys # biblioteca para manipular os arquivos
import wave # biblioteca para trabalhar com arquivos .wav
import numpy as np # biblioteca para manipular os vetores/canais de áudio (pip install numpy)
import soundfile as sf # biblioteca para manipular os áudios (pip install pysoundfile)
import matplotlib.pyplot as plt # biblioteca para plotar a função (pip install -U matplotlib)
from tkinter import * # biblioteca para a interface gráfica
from tkinter import filedialog
import tkinter.font as tf
from pygame import mixer #biblioteca para o reprodutor (pip install pygame)
import click # biblioteca para sim ou não (pip install click)
from pydub import AudioSegment # biblioteca para manipular mp3 (pip install pydub e http://www.ffmpeg.org/download.html)

class Application:
    ### Inicializa o mixer do pygame ###
    mixer.init(44100)
    def selec_button():
        diretorio = filedialog.askdirectory()
        ### Comando que vai para a pasta destino onde estão os arquivos ###
        os.chdir(diretorio)
        ### Comando que lista os arquivos que estão no diretório ###
        diretorio_L = os.listdir('.')
        num = 1

        ### Para cada arquivo no diretório ###
        for arquivo in diretorio_L:
            ### se o arquivo tiver o final de seu nome igual a "mp3" ###
            if arquivo[-1] =='3' and arquivo[-2] == 'p' and arquivo[-3] == 'm':
                ### crio um novo arquivo com o mesmo nome do original porém no formato wav ###
                print('O arquivo "%s" está sendo convertido para ".wav"...(aguarde!)'%arquivo)
                src = "%s/%s"%(diretorio, arquivo)
                dst = "%s/%s.wav"%(diretorio, arquivo)
                sound = AudioSegment.from_mp3(src)
                sound.export(dst, format="wav")
                ### removo o arquivo original (mp3) ###
                os.remove(arquivo)
                ### a variável que representa o arquivo muda ###
                print('O arquivo "%s" foi convertido como: '%arquivo, end='')
                arquivo = "%s.wav"%arquivo
                print(arquivo)

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

                ### Transformo a lista em um vetor (objeto) através da biblioteca "numpy" ###
                data_mono = np.array(data_list)
                ### Edito o arquivo transformando-o em "mono" ###
                sf.write('%s'%arquivo, data_mono, samplerate)

            ### Se não: ###
            else:
                ### Digo que o arquivo não é estéreo ###
                print('O arquivo "%s" não é estéreo!!'%arquivo)

            ### Caso o nome do arquivo seja diferente do padrão: ###
            if arquivo != '%d.wav'%num:
                ### Renomeio o arquivo original no padrão "n.wav", onde "n" é um inteiro ###
                os.rename('%s'%arquivo, '%d.wav'%num)
                ### Digo que o arquivo (e o novo nome dele) não é estéreo ###
                print('O arquivo "%s" foi renomeado para %d.wav"'%(arquivo, num))
            num += 1
        arquivo = str(input("Digite o nome do arquivo que deseja plotar no gráfico: "))
        ### Para cada arquivo no diretório (após a modificação) ###
        for arq in os.listdir('.'):
            if arquivo == arq:
                ### Seleciono e abro o arquivo .wav digitado em questão no modo somente leitura ###
                musica = wave.open('%s'%arq, 'r')
                ### Leio todos os frames (amostras) do áudio, transformando-os em strings ###
                form_onda = musica.readframes(-1)
                ### Inicializo um vetor através de uma string ###
                form_onda = np.fromstring(form_onda, 'Int16')
                ### Obtenho a frequência de amostragem da música ###
                fa = musica.getframerate()
                ### Faço a divisão da quantidade total de amostras pela fa
                # para obter o tempo (em segundos) ###
                tempo = np.linspace(0, len(form_onda)/fa, num=len(form_onda))
                ### Afim de obter a amplitude com referência em tensão (-1 a +1V),
                # divido os níveis de quantização por (2^16)/2 ###
                amplit = form_onda/32768
                ### Pergunto se quero que a música seja tocada
                # se sim, toco a música ###
                if input('Deseja tocar a música? (Sim/Não)\n').lower()[0]=='s': 
                    mixer.music.load('%s'%arq)
                    mixer.music.play()
                ### se não, apenas carrego ela para ser tocada no player futuramente ###
                else:
                    mixer.music.load('%s'%arq)
                ### Faço a plotagem gráfico da amplitude em função do tempo ###
                plt.xlabel("Tempo")
                plt.ylabel("Amplitude")
                plt.title('Formas de onda do arquivo %s'%arq)
                plt.plot(tempo, amplit)
                plt.show()             
                
    ### Rotina para reiniciar o shell do Python ###
    def restart():
        python = sys.executable
        os.execl(python, python, *sys.argv)
        selec_button()

    ### Rotina do Tkinter para os botões e os rótulos ###
    root = Tk()
    root.geometry("480x160")
    times12 = tf.Font(family="Times New Roman", size=12)
    times13 = tf.Font(family="Times New Roman", size=13, weight='bold')
    
    ### Rotina de Menu para a interface ###
    menu = Menu(root)
    root.config(menu = menu)
    menuPrinc = Menu(menu)
    menuRepro = Menu(menu)
    
    menu.add_cascade(label = "Arquivo", menu = menuPrinc)
    menuPrinc.add_command(label = "Selecionar pasta", command = selec_button)
    menuPrinc.add_separator()
    menuPrinc.add_command(label = "Fechar", command = root.destroy)
    menu.add_cascade(label = "Reproduzir", menu = menuRepro)
    menuRepro.add_command(label = "Reproduzir", command = mixer.music.play)
    menuRepro.add_command(label = "Pausar", command = mixer.music.pause)
    menuRepro.add_command(label = "Resumir", command = mixer.music.unpause)
    menuRepro.add_command(label = "Parar", command = mixer.music.stop)
    
    ### Crio o rótulo para escolher o diretório ###
    rotulo = Label(master = root, text = "Por favor, escolha a pasta que deseja manipular os arquivos de áudio")
    rotulo.pack(anchor = CENTER)
    
    ### Crio botões no layout da GUI para o mini-player ### 
    play = Button(text = "TOCAR", command = mixer.music.play, font = times12)
    play.place(x = 200, y = 25)
    resume = Button(text = "►", command = mixer.music.unpause, font = times12)
    resume.place(x = 175, y = 65)
    pause = Button(text = " | | ", command = mixer.music.pause, font = times13)
    pause.place(x = 214, y = 65)
    stop = Button(text = " ■ ", command = mixer.music.stop, font = times13)
    stop.place(x = 255, y = 65)
    
    ### Botão para reiniciar o shell do Python ###
    restart = Button(master = root, text = "Deu ruim? Clique aqui", command = restart, font = times12)
    restart.place(x = 158, y = 100)
    root.mainloop()