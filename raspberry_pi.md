
## Como rodar com Docker

- Formata micro sd com o app da raspberry, aplicando a imagem desejada. Usei a lite 64bits
- Edita o config para habilitar ssh por padrao pois nao tem na lite

- pinga toda a rede: for /l %i in (1,1,254) do @ping -n 1 -w 100 192.168.0.%i > nul
arp -a
arp prefixo b8-27-eb é oficial da Raspberry Pi Foundation, 

usuario padrao:
usuario: pi
senha: raspberry

Com o cartao micro sd no windows: 
Ele aparecerá como um drive chamado boot (ou similar)
Na raiz da partição boot, crie um arquivo vazio chamado ssh (sem extensão!)
Nomeie como: ssh
Apague qualquer extensão .txt (certifique-se que está desabilitada nas opções de pasta)
O nome deve ser exatamente ssh, sem .txt, sem conteúdo.

ssh pi@192.168.0.69

ativar ssh:
sudo systemctl enable ssh
sudo systemctl start ssh

atualiza so:
sudo apt update && sudo apt upgrade -y

prepara python:
sudo apt install -y python3 python3-pip python3-venv git

ver ips:
ip a

Ver o nome da rede (SSID) conectada:
iwgetid

Atualiza o sistema:
sudo apt update && sudo apt upgrade -y

Prepara Python:
sudo apt install -y python3 python3-pip python3-venv git

Ver IPs das interfaces:
ip a

Ver o nome da rede (SSID) conectada:
iwgetid


-- GERAIS:

restart/reboot:
sudo reboot

desligar:
sudo shutdown -r now


-- TECLADO:

iniciar wizard config: (Generic 105-key (Intl) PC)
sudo dpkg-reconfigure keyboard-configuration

editar na mao (so resolveu assim)
sudo nano /etc/default/keyboard
colocar: XKBVARIANT="abnt2"
sudo setupcon
sudo service keyboard-setup restart
sudo reboot

-- WIFI

Ativar o Wi-Fi (desbloqueia se estiver bloqueado):
sudo rfkill unblock wifi

Criar configuração do Wi-Fi com SSID e senha:
sudo tee /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null <<EOF
country=BR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="MurchNet_2G"
    psk="1234567890"
    key_mgmt=WPA-PSK
}

Copiar config para interface wlan0:
sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant-wlan0.conf

Ativar serviço de Wi-Fi na interface wlan0:
sudo systemctl enable wpa_supplicant@wlan0

Iniciar o serviço:
sudo systemctl start wpa_supplicant@wlan0

Subir interface wlan0:
sudo ip link set wlan0 up

Pedir IP via DHCP:
sudo dhclient wlan0

Ver IP atual do Wi-Fi:
ip a show wlan0

Ver se está conectado a uma rede:
iw wlan0 link

-- DEBUG WIFI:

Ver todas as interfaces de rede e seus IPs:
ip a

Ver apenas a interface Wi-Fi:
ip a show wlan0

Listar redes Wi-Fi disponíveis (precisa que o wpa_supplicant esteja parado):
sudo iwlist wlan0 scan | grep ESSID

Ver o status do bloqueio da interface Wi-Fi (soft/hard block):
rfkill list wlan

Desbloquear o Wi-Fi (soft block):
sudo rfkill unblock wlan

Ver status do serviço wpa_supplicant para wlan0:
sudo systemctl status wpa_supplicant@wlan0

Ver todos os processos relacionados ao wpa_supplicant:
ps aux | grep wpa_supplicant

Reiniciar o serviço wpa_supplicant da wlan0:
sudo systemctl restart wpa_supplicant@wlan0

Parar o serviço wpa_supplicant da wlan0:
sudo systemctl stop wpa_supplicant@wlan0

Rodar o wpa_supplicant manualmente (útil para debug):
sudo wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf -d

Pedir IP manualmente via DHCP:
sudo dhclient wlan0

Ver SSID conectado:
iwgetid

Ver se está conectado a alguma rede Wi-Fi:
iw wlan0 link

Ver informações detalhadas da conexão Wi-Fi:
iw dev wlan0 link

Ver rotas (para saber por onde sai para a internet):
ip route

ping -I eth0 google.com
ping -I wlan0 google.com

-- CRIACAO DO VENV normalmente. Mas, usamos a versao abaixo por causa do pyaudio
mkdir ~/keila
cd ~/keila
python3 -m venv venv
source venv/bin/activate

-- CLONE
git clone https://github.com/murchelon/Keila

-- ESPACO EM DISCO
df -h

-- Audio Para a Keila

fora do venv e antes de cria-lo:
sudo apt update
sudo apt install -y python3-pyaudio

python3 -m venv venv --system-site-packages
source venv/bin/activate
dentro do venv: pip install -r requirements.txt

testar audio:
aplay /usr/share/sounds/alsa/Front_Center.wav

testar microfone:
arecord -l


-- PARA CRIAR requirements.txt COM O QUE REALMENTE USA:
fora do venv:
pip install pipreqs
pipreqs /caminho/do/seu/projeto


