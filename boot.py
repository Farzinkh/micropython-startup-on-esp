import sys
import ubinascii
import time,uos,esp,gc
import network,os,machine
if "libs" in os.listdir(): #loading modules
    sys.path.insert(0, "/libs") 
    
import ulogging as logging

global HOST,PORT,sta_if,tim
####  Config
ssid_ = "ssid"
Password = "password"
mountsd=False
rool='s' #station s acceccpoint a
debug_enable=True
######
def mem_manager(timer):
    bootlog.debug('memory:{} ,rssi:{}'.format(gc.mem_free(),sta_if.status('rssi')))
    gc.collect()
    
def mem_manager_ap(timer):
    if os.uname()[1]=='esp32':
        l=[]
        for i in sta_if.status('stations'):
            l.append(ubinascii.hexlify(i[0]))
        bootlog.debug('memory:{},devices mac:{} '.format(gc.mem_free(),l))
    else:
        bootlog.debug('memory:{} '.format(gc.mem_free()))
    gc.collect()

def scaner(s):
    for i in s.scan():
        ssid,RSSI,hidden=i[0],i[3],i[5]
        if RSSI>=-65:
            signal='EXCELLENT'
        elif RSSI>=-75:
            signal='GOOD'
        elif RSSI>=-85:
            signal='FAIR'     
        else:
            signal='POOR'
        bootlog.info('signal:{},ssid:{},RSSI:{},hidden:{}'.format(signal,ssid.decode('utf-8'),RSSI,hidden))
    bootlog.info('done')

bootlog=logging.getLogger(os.uname()[1]+':boot')  
if debug_enable:
    bootlog.setLevel(logging.DEBUG)
tim = machine.Timer(-1)
gc.collect()
if mountsd:
  sd=machine.SDCard(slot=2,width=8,sck=18,mosi=23,miso=19,cs=5,freq=19000000)
  try:
    uos.mount(sd,"/sd")
    bootlog.info("sd card mounted:\n{}".format(uos.listdir('/sd')))
  except Exception as e:
    bootlog.info('sd card not found {}'.format(e))
if rool=='s':
  bootlog.info('Station mode')
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  sta_if.connect(ssid_, Password)
  counter=0
  if not sta_if.isconnected():
    bootlog.info('connecting to network...')
    while not sta_if.isconnected(): #STAT_GOT_IP
        state=sta_if.status()
        if not state==network.STAT_CONNECTING and not state==network.STAT_NO_AP_FOUND :
            bootlog.debug(state)
        if state==network.STAT_CONNECTING:
            pass
        elif state==network.STAT_NO_AP_FOUND:
            counter+=1
            if counter==60:
                bootlog.info('cannot find accesspoint searching...')
                scaner(sta_if)
                counter=0
        elif state==network.STAT_WRONG_PASSWORD or state==network.STAT_CONNECT_FAIL:    
            bootlog.error('Wrong password')
            raise Exception('wrong password')        
        elif state==network.STAT_IDLE :
            machine.reset()
        time.sleep(0.5)
    bootlog.info('IP:{},GATEWAY:{}'.format(sta_if.ifconfig()[0],sta_if.ifconfig()[2])) 
    bootlog.info('MAC ADDRESS:{}'.format(ubinascii.hexlify(sta_if.config('mac')).decode('utf-8')))
    tim.init(period=5000, mode=machine.Timer.PERIODIC, callback=mem_manager)
  else:
    bootlog.info('IP:{},GATEWAY:{}'.format(sta_if.ifconfig()[0],sta_if.ifconfig()[2])) 
    bootlog.info('MAC ADDRESS:{}'.format(ubinascii.hexlify(sta_if.config('mac')).decode('utf-8')))
    tim.init(period=5000, mode=machine.Timer.PERIODIC, callback=mem_manager)

else:
  bootlog.info('Access Point mode')
  sta_if = network.WLAN(network.AP_IF)
  sta_if.active(True)
  sta_if.config(hidden=False)
  sta_if.config(essid=ssid_,authmode=network.AUTH_WPA_WPA2_PSK,password=Password)
  bootlog.info('IP:{},GATEWAY:{}'.format(sta_if.ifconfig()[0],sta_if.ifconfig()[2]))  
  bootlog.info('hidden state:{}'.format(sta_if.config('hidden')))
  tim.init(period=5000, mode=machine.Timer.PERIODIC, callback=mem_manager_ap)

  
esp.osdebug(None)  
bootlog.info('remain space:{}'.format(gc.mem_free()))
bootlog.info("cpu freq:{}".format(machine.freq()))
gc.enable()


#os.remove('boot.py')




