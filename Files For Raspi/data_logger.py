import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime
import board
import busio
import serial
import os
import subprocess
from pathlib import Path
from adafruit_ht16k33.segments import Seg7x4
import adafruit_vl53l0x
import adafruit_gps

# --- Setup working directory ---
os.chdir("/home/lavapub/Desktop/Pen_data")

# --- Setup I2C for LED and TOF ---
i2c = busio.I2C(board.SCL, board.SDA)
display = Seg7x4(i2c)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# --- Setup GPIO Switches ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Switch 1
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Switch 2

# --- Setup Force Gauge Serial ---
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=38400, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

# --- Setup GPS Serial ---
uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

# --- GPS Time Sync ---
gps_synced = False
blink_state = True
last_blink = time.time()

def set_system_time_from_gps(gps_time):
    year = gps_time.tm_year
    month = gps_time.tm_mon
    day = gps_time.tm_mday
    hour = gps_time.tm_hour
    minute = gps_time.tm_min
    second = gps_time.tm_sec
    time_str = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    subprocess.call(["sudo", "date", "--set", time_str])
    #subprocess.call(["sudo", "hwclock", "--systohc"])

# --- Main Loop ---
while not gps_synced:
    gps.update()
    if gps.has_fix and gps.timestamp_utc and gps.timestamp_utc.tm_year >= 2000:
        set_system_time_from_gps(gps.timestamp_utc)
        gps_synced = True
        display.print("GPS")
        time.sleep(1.5)
        break
    else:
        now = time.time()
        if now - last_blink >= 0.5:
            display.print("SYNC" if blink_state else "    ")
            blink_state = not blink_state
            last_blink = now
        time.sleep(0.1)

while True:
    switch1 = GPIO.input(12)
    switch2 = GPIO.input(16)

    if switch1 == True:
        display.print("0000")
        time.sleep(0.5)
    else:
        if switch2 == True:
            D = datetime.now().strftime('%H:%M')
            display.print(D)
            time.sleep(0.5)
        else:
            switch1 = GPIO.input(12)
            if switch1 == True:
                break
            filename = f"{time.strftime('%Y-%m-%d_%H-%M-%S')}_log.txt"
            folder1 = "/home/lavapub/Desktop/Pen_data/"
            filename1 = folder1 + filename
            with open(filename1, mode='w') as dd1:
                dd1.write('Time(s) Force(N) Distance_mm\n')
                print("created " + filename1)
                t0 = time.time()
                i = 0
                while GPIO.input(16) == False:
                    i += 1
                    t = time.time() - t0
                    d = float(vl53.range)
                    ser.write("x".encode('Ascii'))
                    receive = ser.readline().decode('Ascii')
                    x = receive.split('\t')
                    if len(x) >= 3:
                        try:
                            f = float(x[0])
                            if x[2] == 'Live Tension':
                                f *= -1
                            F = "0%.1f" % f
                            display.print(F)
                            dd1.write(f"{t:.4f} {f:.4f} {d:.4f}\n")
                            dd1.flush()
                        except:
                            pass
                    time.sleep(0.033)
                    if GPIO.input(12) == True:
                        break
