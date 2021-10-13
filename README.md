#install
1-tio:https://snapcraft.io/install/tio/arch
2-pip install -r requirements.txt
#run
1-sudo chmod a+wr <port>
2-esptool.py --port <port> erase_flash

for esp32
3-esptool.py --port <port> --baud 115200 write_flash 0x1000 <binfile>
for esp8266
3-esptool.py --port <port> --baud 115200 write_flash 0x00 <binfile>

4-ampy -p <port> put libs
5-ampy -p <port> put <all_files>
6-tio <port>

