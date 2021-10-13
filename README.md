# Requirements 
install TIO terminal monitor or any app you know for arch os use this [link](https://snapcraft.io/install/tio/arch).
# install
`pip install -r requirements.txt`
# Permisson and Flash
`sudo chmod a+wr <port>`
`esptool.py --port <port> erase_flash`

# Upload new image
for esp32

`esptool.py --port <port> --baud 115200 write_flash 0x1000 <binfile>`

for esp8266

`esptool.py --port <port> --baud 115200 write_flash 0x00 <binfile>`

# Upload libs and files
`ampy -p <port> put libs`

`ampy -p <port> put <all_files>`

# Monitor
`tio <port>`

