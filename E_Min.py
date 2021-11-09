import time
from time import sleep
import pyaudio
from numpy import zeros,linspace,short,fromstring,hstack,transpose,log2, log
from scipy import fft, signal
from scipy.signal import hamming, convolve
import RPi.GPIO as GPIO


from neopixel import *

import argparse
import signal
import sys

def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:

                signal.signal(signal.SIGINT, signal_handler)
# Function for frequency detect
def getfreq():
    while _stream.get_read_available()< NUM_SAMPLES: sleep(0.01)
    audio_data  = fromstring(_stream.read(
         _stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]
    # Each data point is a signed 16 bit number, so we can normalize by dividing 32*1024
    normalized_data = audio_data / 32768.0

    w = hamming(4096)  
    intensity = abs(w*fft(normalized_data))[:NUM_SAMPLES/2]

    if frequencyoutput:
        which = intensity[1:].argmax()+1
        # use quadratic interpolation around the max
        adjfreq = 1
        y0,y1,y2 = log(intensity[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output:w it
        thefreq = (which+x1)*SAMPLING_RATE/NUM_SAMPLES
        if thefreq < MIN_FREQUENCY or thefreq > MAX_FREQUENCY:
                adjfreq = -9999
        else:
             thefreq = which*SAMPLING_RATE/NUM_SAMPLES
             if thefreq > MIN_FREQUENCY:
                    adjfreq = thefreq
    if (adjfreq != -9999):
        #print "RAW FREQ:", adjfreq
        adjfreq = 1200 *log2(RELATIVE_FREQ/adjfreq)/100
        adjfreq = adjfreq % 12
        return thefreq



# Sensitivity for input
SENSITIVITY= 1
#Bandwidth for detection (i.e., detect frequencies within this margin of error of the TONE)
BANDWIDTH = 1
# Show the most intense frequency detected (useful for configuration)
frequencyoutput=True

#holds previous frequency
prevFreq = 0
z1 = 10
z2 = 0
z0 = 0
MIN_FREQUENCY = 60
MAX_FREQUENCY = 600
#Max & Min cent value we care about
MAX_CENT = 11
MIN_CENT = 0
RELATIVE_FREQ = 440.0
if len(sys.argv) > 1:
    if (sys.argv[1] >= 415.0 and sys.argv[1] <= 445.0):
        RELATIVE_FREQ = sys.argv[1]

# LED strip configuration from neopixel code:
LED_COUNT      = 72      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering



# Functions for various neopixel animations

#one led at a time
def LED(strip,pos, color):
	strip.setPixelColor(pos, color)
	strip.show()
	

def LED2(strip,pos, color, wait_ms=50):
	strip.setPixelColor(pos, color)
	strip.show()
	time.sleep(wait_ms/1000.0)
	

#colour wipe animation
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

#rainbow animation for end of program
def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)


#Neopixel configuration for start of program
        # Process arguments
opt_parse()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
strip.begin()


#Audio sampler, with increased number of samples- 
NUM_SAMPLES = 4096
SAMPLING_RATE = 48000
pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  frames_per_buffer=NUM_SAMPLES)

def G_Pentatonic():
        
        LED(strip,9, Color(0,255,0))
        LED(strip,6, Color(255,255,255))
        LED(strip,14, Color(255,255,255))
        LED(strip,16, Color(255,255,255))
        LED(strip,33, Color(255,255,255))
        LED(strip,31, Color(255,255,255))
        LED(strip,38, Color(255,255,255))
        LED(strip,40, Color(255,255,255))
        LED(strip,57, Color(255,255,255))
        LED(strip,54, Color(255,255,255))
        LED(strip,62, Color(255,255,255))
        LED(strip,65, Color(255,255,255))

        print "Play G"
        while True:
                thefreq=getfreq()
                
                #print thefreq
                if thefreq >= 195 and thefreq <=205:
                        LED(strip,9, Color(0,0,255))
                        LED(strip,6, Color(0,255,0))
                        LED(strip,10, Color(0,0,0))
                        LED(strip,8, Color(0,0,0))
                        break
                elif thefreq < 195 and thefreq > 60 :
                        LED2(strip,10, Color(255,0,0))
                        LED2(strip,10, Color(0,0,0))

                elif thefreq > 205 :
                        LED2(strip,8, Color(255,0,0))
                        LED2(strip,8, Color(0,0,0))

        print "Play A#"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 230 and thefreq <=240:
                        LED(strip,6, Color(0,0,255))
                        LED(strip,14, Color(0,255,0))
                        LED(strip,7, Color(0,0,0))
                        LED(strip,5, Color(0,0,0))
                        break
                elif thefreq < 230 and thefreq > 60 :
                        LED2(strip,7, Color(255,0,0))
                        LED2(strip,7, Color(0,0,0))

                elif thefreq > 240 :
                        LED2(strip,5, Color(255,0,0))
                        LED2(strip,5, Color(0,0,0))

        print "Play C"
        while True:
                thefreq=getfreq()
               # print thefreq
                if thefreq >= 255 and thefreq <=265:
                        LED(strip,14, Color(0,0,255))
                        LED(strip,16, Color(0,255,0))
                        LED(strip,13, Color(0,0,0))
                        LED(strip,15, Color(0,0,0))
                        break

                elif thefreq < 255 and thefreq > 60 :
                        LED2(strip,13, Color(255,0,0))
                        LED2(strip,13, Color(0,0,0))

                elif thefreq > 265 :
                        LED2(strip,15, Color(255,0,0))
                        LED2(strip,15, Color(0,0,0))

        print "Play D"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 285 and thefreq <=295:
                        LED(strip,16, Color(0,0,255))
                        LED(strip,33, Color(0,255,0))
                        LED(strip,15, Color(0,0,0))
                        LED(strip,17, Color(0,0,0))
                        break
                elif thefreq < 285 and thefreq > 60 :
                        LED2(strip,15, Color(255,0,0))
                        LED2(strip,15, Color(0,0,0))

                elif thefreq > 295 :
                        LED2(strip,17, Color(255,0,0))
                        LED2(strip,17, Color(0,0,0))

        print "Play F"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 345 and thefreq <=355:
                        LED(strip,33, Color(0,0,255))
                        LED(strip,31, Color(0,255,0))
                        LED(strip,34, Color(0,0,0))
                        LED(strip,32, Color(0,0,0))
                        break
                elif thefreq < 345 and thefreq > 60 :
                        LED2(strip,34, Color(255,0,0))
                        LED2(strip,34, Color(0,0,0))

                elif thefreq > 355 :
                        LED2(strip,32, Color(255,0,0))
                        LED2(strip,32, Color(0,0,0))

        print "Play G"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 195 and thefreq <=205:
                        LED(strip,31, Color(0,0,255))
                        LED(strip,38, Color(0,255,0))
                        LED(strip,30, Color(0,0,0))
                        LED(strip,32, Color(0,0,0))
                        break
                elif thefreq < 195 and thefreq > 60 :
                        LED2(strip,30, Color(255,0,0))
                        LED2(strip,30, Color(0,0,0))

                elif thefreq > 205 :
                        LED2(strip,32, Color(255,0,0))
                        LED2(strip,32, Color(0,0,0))

        print "Play A#"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 230 and thefreq <=240:
                        LED(strip,38, Color(0,0,255))
                        LED(strip,40, Color(0,255,0))
                        LED(strip,37, Color(0,0,0))
                        LED(strip,39, Color(0,0,0))
                        break
                elif thefreq < 230 and thefreq > 60 :
                        LED2(strip,37, Color(255,0,0))
                        LED2(strip,37, Color(0,0,0))

                elif thefreq > 240 :
                        LED2(strip,39, Color(255,0,0))
                        LED2(strip,39, Color(0,0,0))

        print "Play C"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 255 and thefreq <=265:
                        LED(strip,40, Color(0,0,255))
                        LED(strip,57, Color(0,255,0))
                        LED(strip,39, Color(0,0,0))
                        LED(strip,41, Color(0,0,0))
                        break
                elif thefreq < 255 and thefreq > 60 :
                        LED2(strip,39, Color(255,0,0))
                        LED2(strip,39, Color(0,0,0))

                elif thefreq > 265 :
                        LED2(strip,41, Color(255,0,0))
                        LED2(strip,41, Color(0,0,0))

        print "Play D"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 285 and thefreq <=295:
                        LED(strip,57, Color(0,0,255))
                        LED(strip,54, Color(0,255,0))
                        LED(strip,58, Color(0,0,0))
                        LED(strip,56, Color(0,0,0))
                        break
                elif thefreq < 285 and thefreq > 60 :
                        LED2(strip,58, Color(255,0,0))
                        LED2(strip,58, Color(0,0,0))

                elif thefreq > 295 :
                        LED2(strip,56, Color(255,0,0))
                        LED2(strip,56, Color(0,0,0))

        print "Play F"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 345 and thefreq <=355:
                        LED(strip,54, Color(0,0,255))
                        LED(strip,62, Color(0,255,0))
                        LED(strip,55, Color(0,0,0))
                        LED(strip,53, Color(0,0,0))
                        break
                elif thefreq < 345 and thefreq > 60 :
                        LED2(strip,55, Color(255,0,0))
                        LED2(strip,55, Color(0,0,0))

                elif thefreq > 355 :
                        LED2(strip,53, Color(255,0,0))
                        LED2(strip,53, Color(0,0,0))

        print "Play G"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 380 and thefreq <=390:
                        LED(strip,62, Color(0,0,255))
                        LED(strip,65, Color(0,255,0))
                        LED(strip,61, Color(0,0,0))
                        LED(strip,63, Color(0,0,0))
                        break
                elif thefreq < 380 and thefreq > 60 :
                        LED2(strip,61, Color(255,0,0))
                        LED2(strip,61, Color(0,0,0))

                elif thefreq > 390 :
                        LED2(strip,63, Color(255,0,0))
                        LED2(strip,63, Color(0,0,0))

        print "Play A#"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 465 and thefreq <=475:
                        LED(strip,65, Color(0,0,255))
                        LED(strip,64, Color(0,0,0))
                        LED(strip,66, Color(0,0,0))
                        colorWipe(strip, Color(0, 0, 255))
                        
                        break
                elif thefreq < 465 and thefreq > 60 :
                        LED2(strip,64, Color(255,0,0))
                        LED2(strip,64, Color(0,0,0))

                elif thefreq > 475 :
                        LED2(strip,66, Color(255,0,0))
                        LED2(strip,66, Color(0,0,0))
        
        print "Well Done!"
        while True:
                rainbow(strip)
                break


def A_Pentatonic():

        
        LED(strip,7, Color(0,255,0))
        LED(strip,4, Color(255,255,255))
        LED(strip,16, Color(255,255,255))
        LED(strip,18, Color(255,255,255))
        LED(strip,31, Color(255,255,255))
        LED(strip,29, Color(255,255,255))
        LED(strip,40, Color(255,255,255))
        LED(strip,42, Color(255,255,255))
        LED(strip,55, Color(255,255,255))
        LED(strip,52, Color(255,255,255))
        LED(strip,64, Color(255,255,255))
        LED(strip,67, Color(255,255,255))

        print "Play A"
        while True:
                thefreq=getfreq()
                
               # print thefreq
                if thefreq >= 215 and thefreq <=225:
                        LED(strip,7, Color(0,0,255))
                        LED(strip,4, Color(0,255,0))
                        LED(strip,8, Color(0,0,0))
                        LED(strip,6, Color(0,0,0))
                        break
                elif thefreq < 215 and thefreq > 60 :
                        LED2(strip,8, Color(255,0,0))
                        LED2(strip,8, Color(0,0,0))

                elif thefreq > 230 :
                        LED2(strip,6, Color(255,0,0))
                        LED2(strip,6, Color(0,0,0))


        print "Play C"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 125 and thefreq <=135:
                        LED(strip,4, Color(0,0,255))
                        LED(strip,16, Color(0,255,0))
                        LED(strip,5, Color(0,0,0))
                        LED(strip,3, Color(0,0,0))
                        break
                elif thefreq < 125 and thefreq > 60 :
                        LED2(strip,5, Color(255,0,0))
                        LED2(strip,5, Color(0,0,0))

                elif thefreq > 140 :
                        LED2(strip,3, Color(255,0,0))
                        LED2(strip,3, Color(0,0,0))

        print "Play D"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 285 and thefreq <=295:
                        LED(strip,16, Color(0,0,255))
                        LED(strip,18, Color(0,255,0))
                        LED(strip,15, Color(0,0,0))
                        LED(strip,17, Color(0,0,0))
                        break
                elif thefreq < 285 and thefreq > 60 :
                        LED2(strip,15, Color(255,0,0))
                        LED2(strip,15, Color(0,0,0))

                elif thefreq > 300 :
                        LED2(strip,17, Color(255,0,0))
                        LED2(strip,17, Color(0,0,0))

        print "Play E"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 160 and thefreq <=170:
                        LED(strip,18, Color(0,0,255))
                        LED(strip,31, Color(0,255,0))
                        LED(strip,17, Color(0,0,0))
                        LED(strip,19, Color(0,0,0))
                        break
                elif thefreq < 160 and thefreq > 60 :
                        LED2(strip,17, Color(255,0,0))
                        LED2(strip,17, Color(0,0,0))

                elif thefreq > 170 :
                        LED2(strip,19, Color(255,0,0))
                        LED2(strip,19, Color(0,0,0))

        print "Play G"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 195 and thefreq <=205:
                        LED(strip,31, Color(0,0,255))
                        LED(strip,29, Color(0,255,0))
                        LED(strip,32, Color(0,0,0))
                        LED(strip,30, Color(0,0,0))
                        break
                elif thefreq < 195 and thefreq > 60 :
                        LED2(strip,32, Color(255,0,0))
                        LED2(strip,32, Color(0,0,0))

                elif thefreq > 205 :
                        LED2(strip,30, Color(255,0,0))
                        LED2(strip,30, Color(0,0,0))

        print "Play A"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 215 and thefreq <=225:
                        LED(strip,29, Color(0,0,255))
                        LED(strip,40, Color(0,255,0))
                        LED(strip,30, Color(0,0,0))
                        LED(strip,28, Color(0,0,0))
                        break
                elif thefreq < 215 and thefreq > 60 :
                        LED2(strip,30, Color(255,0,0))
                        LED2(strip,30, Color(0,0,0))

                elif thefreq > 225 :
                        LED2(strip,28, Color(255,0,0))
                        LED2(strip,28, Color(0,0,0))

        print "Play C"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 255 and thefreq <=265:
                        LED(strip,40, Color(0,0,255))
                        LED(strip,42, Color(0,255,0))
                        LED(strip,39, Color(0,0,0))
                        LED(strip,41, Color(0,0,0))
                        break
                elif thefreq < 255 and thefreq > 60 :
                        LED2(strip,39, Color(255,0,0))
                        LED2(strip,39, Color(0,0,0))

                elif thefreq > 265 :
                        LED2(strip,41, Color(255,0,0))
                        LED2(strip,41, Color(0,0,0))

        print "Play D"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 285 and thefreq <=295:
                        LED(strip,42, Color(0,0,255))
                        LED(strip,55, Color(0,255,0))
                        LED(strip,41, Color(0,0,0))
                        LED(strip,43, Color(0,0,0))
                        break
                elif thefreq < 285 and thefreq > 60 :
                        LED2(strip,41, Color(255,0,0))
                        LED2(strip,41, Color(0,0,0))

                elif thefreq > 300 :
                        LED2(strip,43, Color(255,0,0))
                        LED2(strip,43, Color(0,0,0))

        print "Play E"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 325 and thefreq <=335:
                        LED(strip,55, Color(0,0,255))
                        LED(strip,52, Color(0,255,0))
                        LED(strip,56, Color(0,0,0))
                        LED(strip,54, Color(0,0,0))
                        break
                elif thefreq < 325 and thefreq > 60 :
                        LED2(strip,56, Color(255,0,0))
                        LED2(strip,56, Color(0,0,0))

                elif thefreq > 335 :
                        LED2(strip,54, Color(255,0,0))
                        LED2(strip,54, Color(0,0,0))

        print "Play G"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 395 and thefreq <=405:
                        LED(strip,52, Color(0,0,255))
                        LED(strip,64, Color(0,255,0))
                        LED(strip,53, Color(0,0,0))
                        LED(strip,51, Color(0,0,0))
                        break
                elif thefreq < 395 and thefreq > 60 :
                        LED2(strip,53, Color(255,0,0))
                        LED2(strip,53, Color(0,0,0))

                elif thefreq > 405 :
                        LED2(strip,51, Color(255,0,0))
                        LED2(strip,51, Color(0,0,0))

        print "Play A"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 440 and thefreq <=450:
                        LED(strip,64, Color(0,0,255))
                        LED(strip,67, Color(0,255,0))
                        LED(strip,65, Color(0,0,0))
                        LED(strip,63, Color(0,0,0))
                        break
                elif thefreq < 440 and thefreq > 60 :
                        LED2(strip,65, Color(255,0,0))
                        LED2(strip,65, Color(0,0,0))

                elif thefreq > 450 :
                        LED2(strip,63, Color(255,0,0))
                        LED2(strip,63, Color(0,0,0))

        print "Play C"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 525 and thefreq <=535:
                        LED(strip,67, Color(0,0,255))
                        LED(strip,68, Color(0,0,0))
                        LED(strip,66, Color(0,0,0))
                        colorWipe(strip, Color(0, 0, 255))  
                        break
                elif thefreq < 525 and thefreq > 60 :
                        LED2(strip,68, Color(255,0,0))
                        LED2(strip,68, Color(0,0,0))

                elif thefreq > 535 :
                        LED2(strip,66, Color(255,0,0))
                        LED2(strip,66, Color(0,0,0))
        
        print "Well Done!"
        while True:
                rainbow(strip)
                break

def A_Major():
        LED(strip,7, Color(0,255,0))
        LED(strip,5, Color(255,255,255))
        LED(strip,15, Color(255,255,255))
        LED(strip,16, Color(255,255,255))
        LED(strip,18, Color(255,255,255))
        LED(strip,29, Color(255,255,255))
        LED(strip,30, Color(255,255,255))
        LED(strip,32, Color(255,255,255))


        print "Play A"
        while True:
                thefreq=getfreq()

                if thefreq >= 215 and thefreq <=225:
                        LED(strip,7, Color(0,0,255))
                        LED(strip,5, Color(0,255,0))
                        LED(strip,8, Color(0,0,0))
                        LED(strip,6, Color(0,0,0))
                        break
                elif thefreq < 215 and thefreq > 60 :
                        LED2(strip,8, Color(255,0,0))
                        LED2(strip,8, Color(0,0,0))

                elif thefreq > 215 :
                        LED2(strip,6, Color(255,0,0))
                        LED2(strip,6, Color(0,0,0))


        print "Play B"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 240 and thefreq <=250:
                        LED(strip,5, Color(0,0,255))
                        LED(strip,15, Color(0,255,0))
                        LED(strip,6, Color(0,0,0))
                        LED(strip,4, Color(0,0,0))
                        break
                elif thefreq < 240 and thefreq > 60 :
                        LED2(strip,6, Color(255,0,0))
                        LED2(strip,6, Color(0,0,0))

                elif thefreq > 250 :
                        LED2(strip,4, Color(255,0,0))
                        LED2(strip,4, Color(0,0,0))

        print "Play C#"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 275 and thefreq <=285:
                        LED(strip,15, Color(0,0,255))
                        LED(strip,16, Color(0,255,0))
                        LED(strip,14, Color(0,0,0))
                        LED(strip,17, Color(0,0,0))
                        break
                elif thefreq < 275 and thefreq > 60 :
                        LED2(strip,14, Color(255,0,0))
                        LED2(strip,14, Color(0,0,0))

                elif thefreq > 285 :
                        LED2(strip,17, Color(255,0,0))
                        LED2(strip,17, Color(0,0,0))

        print "Play D"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 285 and thefreq <=295:
                        LED(strip,16, Color(0,0,255))
                        LED(strip,18, Color(0,255,0))
                        LED(strip,14, Color(0,0,0))
                        LED(strip,17, Color(0,0,0))
                        break
                elif thefreq < 285 and thefreq > 60 :
                        LED2(strip,14, Color(255,0,0))
                        LED2(strip,14, Color(0,0,0))

                elif thefreq > 295 :
                        LED2(strip,17, Color(255,0,0))
                        LED2(strip,17, Color(0,0,0))

        print "Play E"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 160 and thefreq <=170:
                        LED(strip,18, Color(0,0,255))
                        LED(strip,32, Color(0,255,0))
                        LED(strip,17, Color(0,0,0))
                        LED(strip,19, Color(0,0,0))
                        break
                elif thefreq < 160 and thefreq > 60 :
                        LED2(strip,17, Color(255,0,0))
                        LED2(strip,17, Color(0,0,0))

                elif thefreq > 170 :
                        LED2(strip,19, Color(255,0,0))
                        LED2(strip,19, Color(0,0,0))

        print "Play F#"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 360 and thefreq <=370:
                        LED(strip,32, Color(0,0,255))
                        LED(strip,30, Color(0,255,0))
                        LED(strip,33, Color(0,0,0))
                        LED(strip,31, Color(0,0,0))
                        break
                elif thefreq < 360 and thefreq > 60 :
                        LED2(strip,33, Color(255,0,0))
                        LED2(strip,33, Color(0,0,0))

                elif thefreq > 370 :
                        LED2(strip,31, Color(255,0,0))
                        LED2(strip,31, Color(0,0,0))

        print "Play G"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 205 and thefreq <=215:
                        LED(strip,30, Color(0,0,255))
                        LED(strip,29, Color(0,255,0))
                        LED(strip,31, Color(0,0,0))
                        LED(strip,28, Color(0,0,0))
                        break
                elif thefreq < 205 and thefreq > 60 :
                        LED2(strip,31, Color(255,0,0))
                        LED2(strip,31, Color(0,0,0))

                elif thefreq > 215 :
                        LED2(strip,28, Color(255,0,0))
                        LED2(strip,28, Color(0,0,0))


        print "Play A"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 215 and thefreq <=225:
                        LED(strip,29, Color(0,0,255))
                        LED(strip,31, Color(0,0,0))
                        LED(strip,28, Color(0,0,0))
                        colorWipe(strip, Color(0, 0, 255))
                        break
                elif thefreq < 215 and thefreq > 60 :
                        LED2(strip,31, Color(255,0,0))
                        LED2(strip,31, Color(0,0,0))

                elif thefreq > 215 :
                        LED2(strip,28, Color(255,0,0))
                        LED2(strip,28, Color(0,0,0))
        
        print "Well Done!"
        while True:
                rainbow(strip)
                break

def E_Minor():
        LED(strip,18, Color(0,255,0))
        LED(strip,20, Color(255,255,255))
        LED(strip,21, Color(255,255,255))
        LED(strip,29, Color(255,255,255))
        LED(strip,27, Color(255,255,255))
        LED(strip,26, Color(255,255,255))
        LED(strip,42, Color(255,255,255))
        LED(strip,44, Color(255,255,255))


        print "Play E"
        while True:
                thefreq=getfreq()
                #print thefreq

                if thefreq >= 160 and thefreq <=170:
                        LED(strip,18, Color(0,0,255))
                        LED(strip,20, Color(0,255,0))
                        LED(strip,17, Color(0,0,0))
                        LED(strip,19, Color(0,0,0))
                        break
                elif thefreq < 160 and thefreq > 60 :
                        LED2(strip,17, Color(255,0,0))
                        LED2(strip,17, Color(0,0,0))

                elif thefreq > 170 :
                        LED2(strip,19, Color(255,0,0))
                        LED2(strip,19, Color(0,0,0))


        print "Play F#"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 185 and thefreq <=190:
                        LED(strip,20, Color(0,0,255))
                        LED(strip,21, Color(0,255,0))
                        LED(strip,19, Color(0,0,0))
                        LED(strip,22, Color(0,0,0))
                        break
                elif thefreq < 185 and thefreq > 60 :
                        LED2(strip,19, Color(255,0,0))
                        LED2(strip,19, Color(0,0,0))

                elif thefreq > 190 :
                        LED2(strip,22, Color(255,0,0))
                        LED2(strip,22, Color(0,0,0))

        print "Play G"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 195 and thefreq <=205:
                        LED(strip,21, Color(0,0,255))
                        LED(strip,29, Color(0,255,0))
                        LED(strip,19, Color(0,0,0))
                        LED(strip,22, Color(0,0,0))
                        break
                elif thefreq < 195 and thefreq > 60 :
                        LED2(strip,19, Color(255,0,0))
                        LED2(strip,19, Color(0,0,0))

                elif thefreq > 205 :
                        LED2(strip,22, Color(255,0,0))
                        LED2(strip,22, Color(0,0,0))

        print "Play A"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 220 and thefreq <=230:
                        LED(strip,29, Color(0,0,255))
                        LED(strip,27, Color(0,255,0))
                        LED(strip,30, Color(0,0,0))
                        LED(strip,28, Color(0,0,0))
                        break
                elif thefreq < 220 and thefreq > 60 :
                        LED2(strip,30, Color(255,0,0))
                        LED2(strip,30, Color(0,0,0))

                elif thefreq > 230 :
                        LED2(strip,28, Color(255,0,0))
                        LED2(strip,28, Color(0,0,0))

        print "Play B"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 240 and thefreq <=250:
                        LED(strip,27, Color(0,0,255))
                        LED(strip,26, Color(0,255,0))
                        LED(strip,28, Color(0,0,0))
                        LED(strip,25, Color(0,0,0))
                        break
                elif thefreq < 240 and thefreq > 60 :
                        LED2(strip,28, Color(255,0,0))
                        LED2(strip,28, Color(0,0,0))

                elif thefreq > 250 :
                        LED2(strip,25, Color(255,0,0))
                        LED2(strip,25, Color(0,0,0))

        print "Play C"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 265 and thefreq <=275:
                        LED(strip,26, Color(0,0,255))
                        LED(strip,42, Color(0,255,0))
                        LED(strip,28, Color(0,0,0))
                        LED(strip,25, Color(0,0,0))
                        break
                elif thefreq < 265 and thefreq > 60 :
                        LED2(strip,28, Color(255,0,0))
                        LED2(strip,28, Color(0,0,0))

                elif thefreq > 275 :
                        LED2(strip,25, Color(255,0,0))
                        LED2(strip,25, Color(0,0,0))

        print "Play D"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 285 and thefreq <=295:
                        LED(strip,42, Color(0,0,255))
                        LED(strip,44, Color(0,255,0))
                        LED(strip,41, Color(0,0,0))
                        LED(strip,43, Color(0,0,0))
                        break
                elif thefreq < 285 and thefreq > 60 :
                        LED2(strip,41, Color(255,0,0))
                        LED2(strip,41, Color(0,0,0))

                elif thefreq > 295 :
                        LED2(strip,43, Color(255,0,0))
                        LED2(strip,43, Color(0,0,0))


        print "Play E"
        while True:
                thefreq=getfreq()
                
                if thefreq >= 325 and thefreq <=335:
                        LED(strip,44, Color(0,0,255))
                        LED(strip,43, Color(0,0,0))
                        LED(strip,45, Color(0,0,0))
                        colorWipe(strip, Color(0, 0, 255))
                        break
                elif thefreq < 325 and thefreq > 60 :
                        LED2(strip,43, Color(255,0,0))
                        LED2(strip,43, Color(0,0,0))

                elif thefreq > 335 :
                        LED2(strip,45, Color(255,0,0))
                        LED2(strip,45, Color(0,0,0))
        
        print "Well Done!"
        while True:
                rainbow(strip)
                break

E_Minor()



                
