from sys import stdout
import PySimpleGUI as sg                       
import subprocess



class TelaFFMPEG:

    def __init__(self):
        vetor = self.testandosaidas()
        placasdetectadas = []
        placasdetectadas = self.selectPlaca(vetor)
        bitratelist = ["80", "96", "112", "128", "160", "192", "224", "256","320"]

        layout = [  [sg.Text("Digite o IP do Servidor")],    
                    [sg.Input(key='ip')],
                    [sg.Text("Digite a PORTA do Servidor")],
                    [sg.Input(key='port')],
                    [sg.Text("                       Parametros de Transmissão")],
                    [sg.Text("Placa de Transmissão"),sg.Combo(placasdetectadas, size=18,key='placa')],
                    [sg.Text("Bitrate Transmissão    "),sg.Combo(bitratelist, size=18,key='bitrate')],
                    [sg.Radio('libmp3lame','selecao',key='decod',default=True),sg.Radio('libopus','selecao',key='decod1')],
                    
                    [sg.Button('Start'),sg.Button('Stop'),sg.Exit()],
                    
                    
                    [sg.Output(size=(50,20))]
                    
                ]
        self.window = sg.Window('Transmissor FFMPEG').layout(layout)   
        self.sair = False
        self.transmitindo = False
    
    def iniciandoServidor(self,placa,selecao,bitrate,ip,port):
        cmd = ['gnome-terminal','-e' ,"ffmpeg -vn -f alsa -i sysdefault:CARD="+placa+" -ac 2 -acodec "+selecao+" -b:a "+bitrate+" -f rtp rtp://"+ip+":"+port]
        subprocess.call(cmd)
        
    def stopservidor(self):
        if(self.transmitindo):
            cmd = ['gnome-terminal','-e','killall ffmpeg']
            print("\n\n**********************************************************************\n")
            print("                             Parando Transmissão")
            print("\n**********************************************************************\n\n")
            self.transmitindo = False
            subprocess.call(cmd)
        else:
            print("\n\n**********************************************************************\n")
            print("                      Nenhuma Transmissão Iniciada")
            print("\n**********************************************************************\n\n")
    def testandosaidas(self):
        valores= []
        linha = []
        result = subprocess.run(["arecord", "-l"],capture_output=True, text=True)
        with open('list.txt','w',encoding='utf-8') as arq:
            arq.writelines(result.stdout)
        arquivo = open('list.txt','r',encoding='utf-8')
        for i in arquivo:
            valores.append(i)
        for i in range(1,len(valores)-2):
            linha.append(valores[i])
        arquivo.close()
        return linha
    def selectPlaca(self,listplacas):
        chaves = []
        for i in range(len(listplacas)):
            valr = listplacas[i].split(",")
            teste = valr[i].split(" ")
            chaves.append(teste[2])
        return chaves
    def StartServidor(self):
        while self.sair != True:
            event, values = self.window.read()    
            if(event == 'Start'):
                ip = values['ip']
                port = values['port']
                placa = values['placa']
                bitrate = values['bitrate']
                if values['decod'] == True:
                    selecao = 'libmp3lame'
                else:
                    selecao = 'libopus'
                
                if((ip!="" or len(ip)>=13) and (port!="") and (placa!="") and selecao != "" and bitrate != ""): 
                    print("transmistindo")
                    print("******************** FFMPEG Transmitindo *********************\n"+"IP de Transmissão.: "+ ip + "\nPorta de Transmissao.: " + port + "\nPlaca Selecionada.: " + placa+"\nBitrade Transmissao.: " + bitrate + "\nAcodec.: " + selecao)
                    self.iniciandoServidor(placa,selecao,bitrate,ip,port)
                    self.transmitindo = True

                else:
                    print("************* FFMPEG Nao Conseguiu Transmitir *************\n\n                Insira os Parametros de Transmissão\n")
                    print("**********************************************************************\n\n")
            elif(event == 'Exit'):
                self.sair = True
            else:
                self.stopservidor()

        self.closedapp()
    

tela = TelaFFMPEG()
tela.StartServidor()