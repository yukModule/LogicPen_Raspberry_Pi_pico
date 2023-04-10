from machine import Pin, SoftI2C, ADC, Timer
from time import sleep
import ssd1306

pin_input=Pin(12,Pin.IN)
data=[1 for i in range(64)]
delay=0.001
modswitch=Pin(4,Pin.IN)
mod=1
ADC0= ADC(Pin(26))

def writedata():
    for i in range(64):
        sleep(delay)
        if (pin_input.value()==1):
            data[i]=1
        else :
            data[i]=0

def putpoint():
    writedata()
    oled.fill(0)
    delayc=str(delay)
    oled.text('Sampling', 0, 0)
    oled.text(delayc, 80, 0)
    for i in range(64):
        oled.pixel(1*i,30-data[i]*15,2)
    ratio=sum(data)/64*100
    ratio=str(ratio)[0:5]
    oled.text(ratio+'%', 80, 20)
    oled.show()

def putresistance():
    reading = ADC0.read_u16()*3.3/65535
    if reading==3.3:
        return
    k=reading/(3.3-reading)

    oled.fill(0)
    oled.text('resistance', 0, 0)
    char_value1=str(k*10)[0:5]
    char_value2=str(k*100)[0:5]
    char_value3=str(k*1000)[0:5]
    oled.text(char_value1, 0, 20)
    oled.text(char_value2, 45, 20)
    oled.text(char_value3, 90, 20)
    oled.show()


def restart():
    global oled
    i2c = SoftI2C(scl=Pin(6), sda=Pin(7))
    oled_width = 128
    oled_height = 32
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

restart()
oled.text('Hello!', 0, 0)
oled.show()

interruptCounter = 0#声明一个计数器
timer = Timer() #新建一个Timer类的对象，定时器硬件
def handleInterrupt(timer):# 声明handleInterrupt中断处理函数
    global interruptCounter, mod, delay
    if (modswitch.value()==1):
        interruptCounter = interruptCounter+1
        if interruptCounter>100 :
            mod = 1-mod
            interruptCounter = 1
        
    else:
        if 1< interruptCounter < 100 :
            delay=delay*10
            if delay>0.01:
                delay=0.0001
        interruptCounter = 1
                
timer.init(period=10, mode=Timer.PERIODIC, callback=handleInterrupt)

while True:
    if mod == 1:
        putpoint()
    else:
        putresistance()
        sleep(0.1)

