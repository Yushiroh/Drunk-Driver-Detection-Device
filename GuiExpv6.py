import pygame
import sys
import cv2
import threading
import os
from deepface import DeepFace
import RPi.GPIO as GPIO
from time import sleep

APPWIDTH, APPHEIGHT = 800, 480
FPS = 60
pygame.init()
pygame.display.set_caption("Final System")
sensorActivated = False
timerTickState = False

#GPIO Setup
drunkBut = 10
soberBut = 8
sensAct = 12
led1 = 18
led2 = 16
carStarter = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(led1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(sensAct,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(carStarter,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(drunkBut, GPIO.IN)
GPIO.setup(soberBut, GPIO.IN)

#COLORS
Black = (0,0,0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

#Master Pin

mPin = [0,0,0,0] 

currPin = []

#ANIMATION TIMERS
warnTick = 0
brtTick = 0
timerTick = 0

#ASSETS
d_Font = pygame.font.SysFont('arial', 30)
back_Font = pygame.font.SysFont('arial', 20)

vidCap = cv2.VideoCapture(0)
vidCap.set(cv2.CAP_PROP_FRAME_WIDTH, 670)
vidCap.set(cv2.CAP_PROP_FRAME_HEIGHT, 440)

counter = 0
face_match = False
reference_img = cv2.imread('registeredFace.jpg')

#Sound Assets

drunkAudio = pygame.mixer.Sound('/home/user/commisionProjectV3/gui_assets/drunkWarning.mp3')
soberAudio = pygame.mixer.Sound('/home/user/commisionProjectV3/gui_assets/soberAudio.mp3')
one = pygame.mixer.Sound('/home/user/commisionProjectV3/gui_assets/1.mp3')
two = pygame.mixer.Sound('/home/user/commisionProjectV3/gui_assets/2.mp3')
three = pygame.mixer.Sound('/home/user/commisionProjectV3/gui_assets/3.mp3')
#Scene1 Assets
mainBG = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'main_bg.jpg')), (APPWIDTH, APPHEIGHT))


header = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'headBanner.png')), (800, 153))

startVerify = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'startVerify.png')), (427, 107))

registerButt = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'regButt.png')), (101, 45))

#inversions

startVerify_h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'startVerify_h.png')), (427, 107))

registerButt_h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'regButt_h.png')), (101, 45))

#Scene2 Assets

sysPinIn = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'sysPinIn.png')), (800, 121))

pinBox = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'pinBox.png')), (104, 131))

hidePin = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'hidePin.png')), (77, 74))

buttonInstruct = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'buttonInstruct.png')), (537, 36))

p1 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '1.png')), (73, 76))

p2 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '2.png')), (73, 76))

p3 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '3.png')), (73, 76))

p4 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '4.png')), (73, 76))

p5 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '5.png')), (73, 76))

p6 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '6.png')), (73, 76))

p7 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '7.png')), (73, 76))

p8 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '8.png')), (73, 76))

p9 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '9.png')), (73, 76))

p0 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '0.png')), (73, 76))

#inversions

p1h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '1h.png')), (73, 76))

p2h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '2h.png')), (73, 76))

p3h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '3h.png')), (73, 76))

p4h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '4h.png')), (73, 76))

p5h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '5h.png')), (73, 76))

p6h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '6h.png')), (73, 76))

p7h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '7h.png')), (73, 76))

p8h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '8h.png')), (73, 76))

p9h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '9h.png')), (73, 76))

p0h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', '0h.png')), (73, 76))

#Scene3 Assets

backButt = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'back.png')), (72, 64))

regButt = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'regFace.png')), (314, 97))

#inversions

backButt_h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'back_h.png')), (72, 64))

regButt_h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'regFace_h.png')), (314, 97))

#Scene4 Assets

backButt = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'back.png')), (72, 64))

verifyButt = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'verify.png')), (314, 97))

#inversions

backButt_h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'back_h.png')), (72, 64))

verifyButt_h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'verify_h.png')), (314, 97))

#Scene5 Assets

alcTest = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'alcTest.png')), (738, 226))

btlzr1 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'btlzr1.png')), (226, 249))

btlzr2 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'btlzr2.png')), (226, 249))

btlzr3 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'btlzr3.png')), (226, 249))

activateButt = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'activateButt.png')), (231, 172))

sensorOFF = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'sensorOFF.png')), (113, 192))

sensorON = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'sensorON.png')), (113, 192))

#inversions

activateButt_h = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'activateButt_h.png')), (231, 172))

#Scene6 Assets

warn0 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'warn0.png')), (276, 48))

warn1 = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'warn1.png')), (276, 48))

alcWarn = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'alcWarn.png')), (638, 146))

#inversions

#Scene7 Assets

carStarted = pygame.transform.scale(pygame.image.load(
    os.path.join('gui_assets', 'carStarted.png')), (800, 121))


#ASSETS
d_Font = pygame.font.SysFont('arial', 30)
counterFont = pygame.font.SysFont('arial', 100) 

def pinManager(self, currPinVal):

    currPin.append(currPinVal)

    if len(currPin) >= 4:
        if currPin == mPin:
            print("MATCH")
            self.stateManager.setState('scene3')
            list.clear(currPin)
        else:
            print("MISMATCH")
            list.clear(currPin)
            
    


    print(currPin)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((APPWIDTH, APPHEIGHT))
        self.clock = pygame.time.Clock()

        self.stateManager = stateManager('scene1')
        self.scene1 = scene1(self.screen, self.stateManager)
        self.scene2 = scene2(self.screen, self.stateManager)
        self.scene3 = scene3(self.screen, self.stateManager)
        self.scene4 = scene4(self.screen, self.stateManager)
        self.scene5 = scene5(self.screen, self.stateManager)
        self.scene6 = scene6(self.screen, self.stateManager)
        self.scene7 = scene7(self.screen, self.stateManager)

        self.states = {'scene1': self.scene1, 'scene2': self.scene2, 'scene3': self.scene3
                        , 'scene4': self.scene4, 'scene5': self.scene5, 'scene6': self.scene6, 'scene7': self.scene7}

    def run(self):
        while True:
            mouse = pygame.mouse.get_pos()
            clicker = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.states[self.stateManager.getState()].run(mouse,clicker)

            #print(mouse)
            #print(counter)

            pygame.display.update()
            self.clock.tick(FPS)

class scene1:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(carStarter, GPIO.LOW)
        
        self.display.blit(mainBG,(0,0))
        self.display.blit(header,(0,100))

        self.display.blit(startVerify,(190,250))
        self.display.blit(registerButt,(690,10))

        if 190+427 > mouse[0] > 190 and 250+107 > mouse[1] > 250:
            self.display.blit(startVerify_h,(190,250))

        if 190+427 > mouse[0] > 190 and 250+107 > mouse[1] > 250 and True == clicker[0]:
            self.stateManager.setState('scene4')

        if 690+101 > mouse[0] > 690 and 10+45 > mouse[1] > 10:
            self.display.blit(registerButt_h,(690,10))

        if 690+101 > mouse[0] > 690 and 10+45 > mouse[1] > 10 and True == clicker[0]:        
            self.stateManager.setState('scene2')

class scene2:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager
        self.clock = pygame.time.Clock()

    def run(self, mouse, clicker):

        self.clock.tick(15)

        self.display.blit(mainBG,(0,0))
        self.display.blit(sysPinIn,(0,0))

        self.display.blit(pinBox,(170,112))
        self.display.blit(pinBox,(291,112))
        self.display.blit(pinBox,(407,112))
        self.display.blit(pinBox,(524,112))

        self.display.blit(buttonInstruct,(130,335))
        
        self.display.blit(p1,(5, 395))
        self.display.blit(p2,(85,395))
        self.display.blit(p3,(165,395))
        self.display.blit(p4,(245,395))
        self.display.blit(p5,(325,395))
        self.display.blit(p6,(405,395))
        self.display.blit(p7,(485,395))
        self.display.blit(p8,(565,395))
        self.display.blit(p9,(645,395))
        self.display.blit(p0,(725,395))
        
        if 5+73 > mouse[0] > 5 and 395+76 > mouse[1] > 395:
            self.display.blit(p1h,(5, 395))

        if 5+73 > mouse[0] > 5 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 1
            pinManager(self,currPinVal)

        if 85+73 > mouse[0] > 85 and 395+76 > mouse[1] > 395:
            self.display.blit(p2h,(85,395))
        
        if 85+73 > mouse[0] > 85 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 2
            pinManager(self,currPinVal)

        if 165+73 > mouse[0] > 165 and 395+76 > mouse[1] > 395:
            self.display.blit(p3h,(165,395))

        if 165+73 > mouse[0] > 165 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 3
            pinManager(self,currPinVal)

        if 245+73 > mouse[0] > 245 and 395+76 > mouse[1] > 395:
            self.display.blit(p4h,(245,395))

        if 245+73 > mouse[0] > 245 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 4
            pinManager(self,currPinVal)

        if 325+73 > mouse[0] > 325 and 395+76 > mouse[1] > 395:
            self.display.blit(p5h,(325,395))

        if 325+73 > mouse[0] > 325 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 5
            pinManager(self,currPinVal)

        if 405+73 > mouse[0] > 405 and 395+76 > mouse[1] > 395:
            self.display.blit(p6h,(405,395))

        if 405+73 > mouse[0] > 405 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 6
            pinManager(self,currPinVal)

        if 485+73 > mouse[0] > 485 and 395+76 > mouse[1] > 395:
            self.display.blit(p7h,(485,395))

        if 485+73 > mouse[0] > 485 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 7
            pinManager(self,currPinVal)

        if 565+73 > mouse[0] > 565 and 395+76 > mouse[1] > 395:
            self.display.blit(p8h,(565,395))

        if 565+73 > mouse[0] > 565 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 8
            pinManager(self,currPinVal)

        if 645+73 > mouse[0] > 645 and 395+76 > mouse[1] > 395:
            self.display.blit(p9h,(645,395))

        if 645+73 > mouse[0] > 645 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 9
            pinManager(self,currPinVal)

        if 725+73 > mouse[0] > 725 and 395+76 > mouse[1] > 395:
            self.display.blit(p0h,(725,395))

        if 725+73 > mouse[0] > 725 and 395+76 > mouse[1] > 395 and True == clicker[0]:
            currPinVal = 0
            pinManager(self,currPinVal)


        if len(currPin) == 1:
            self.display.blit(hidePin,(185, 140))
        if len(currPin) == 2:
            self.display.blit(hidePin,(185, 140))
            self.display.blit(hidePin,(305, 140))
        if len(currPin) == 3:
            self.display.blit(hidePin,(185, 140))
            self.display.blit(hidePin,(305, 140))
            self.display.blit(hidePin,(420, 140))
        if len(currPin) == 4:
            self.display.blit(hidePin,(185, 140))
            self.display.blit(hidePin,(305, 140))
            self.display.blit(hidePin,(420, 140))
            self.display.blit(hidePin,(540, 140))

class scene3:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        global timerTick
        global timerTickState
        
        self.display.fill(Black)

        ret, frameORIG = vidCap.read()
        
        if not ret:
            print("NO CAM")
            
        if ret is True:
            frame = cv2.cvtColor(frameORIG, cv2.COLOR_BGR2RGB)
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame = pygame.surfarray.make_surface(frame)

            self.display.blit(frame, (90,0,0,0))
            if cv2.waitKey(25) == ord('q'):
                vidCap.release()
                
        self.display.blit(regButt,(242,384))
        self.display.blit(backButt,(10,10))

        if 242+314 > mouse[0] > 242 and 384+97 > mouse[1] > 384:
            self.display.blit(regButt_h,(242,384))

        if 10+72 > mouse[0] > 10 and 10+64 > mouse[1] > 10:
            self.display.blit(backButt_h,(10,10))

        if 242+314 > mouse[0] > 242 and 384+97 > mouse[1] > 384 and True == clicker[0]:
         timerTickState = True
         
        if timerTickState:
            timerTick+=1
            print(timerTick)

        if timerTick < 30 and timerTickState:
            faceReg = counterFont.render("3", 1, Black)
            self.display.blit(faceReg, (90, 0, 160, 20))

        if timerTick > 30 and timerTick < 60 and timerTickState:
            
            faceReg = counterFont.render("2", 1, Black)
            self.display.blit(faceReg, (90, 0, 160, 20))

        if timerTick > 60 and timerTick < 90 and timerTickState:
            
            faceReg = counterFont.render("1", 1, Black)
            self.display.blit(faceReg, (90, 0, 160, 20))


        if 10+72 > mouse[0] > 10 and 10+64 > mouse[1] > 10 and True == clicker[0]:
            self.stateManager.setState('scene1')
            
        if timerTick == 90:
            print("CAPTURED")
            cv2.imwrite("registeredFace.jpg", frameORIG)
            faceReg = d_Font.render("Face Registered!", 1, Black)
            self.display.blit(faceReg, (90, 0, 160, 20))
            pygame.time.wait(1000)
            
        if timerTick > 90:
            timerTickState = False
            timerTick = 0
            
        if timerTick == 5:
            three.play()
        if timerTick == 30:
            two.play()
        if timerTick == 60:
            one.play()
            
class scene4:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        self.display.fill(Black)
        global timerTick
        global timerTickState
        
        ret, matcherORIG = vidCap.read()
        
        if not ret:
            print("NO CAM")
            
        if ret is True:
            matchframe = cv2.cvtColor(matcherORIG, cv2.COLOR_BGR2RGB)
            matchframe = cv2.rotate(matchframe, cv2.ROTATE_90_COUNTERCLOCKWISE)
            matchframe = pygame.surfarray.make_surface(matchframe)

            self.display.blit(matchframe, (90,0,0,0))

            if cv2.waitKey(25) == ord('q'):
                vidCap.release()



        self.display.blit(verifyButt,(242,384))
        self.display.blit(backButt,(10,10))

        if 242+314 > mouse[0] > 242 and 384+97 > mouse[1] > 384:
            self.display.blit(verifyButt_h,(242,384))

        if 10+72 > mouse[0] > 10 and 10+64 > mouse[1] > 10:
            self.display.blit(backButt_h,(10,10))

        if 242+314 > mouse[0] > 242 and 384+97 > mouse[1] > 384 and True == clicker[0]:
         timerTickState = True
         
        if timerTickState:
            timerTick+=1
            print(timerTick)

        if timerTick < 30 and timerTickState:
            faceReg = counterFont.render("3", 1, Black)
            self.display.blit(faceReg, (90, 0, 160, 20))

        if timerTick > 30 and timerTick < 60 and timerTickState:
            faceReg = counterFont.render("2", 1, Black)
            self.display.blit(faceReg, (90, 0, 160, 20))

        if timerTick > 60 and timerTick < 90 and timerTickState:
            faceReg = counterFont.render("1", 1, Black)
            self.display.blit(faceReg, (90, 0, 160, 20))
            
        if timerTick == 90:
            print("CAPTURED")
            cv2.imwrite("attemptingFace.jpg", matcherORIG)
            result = DeepFace.verify("registeredFace.jpg", "attemptingFace.jpg", "OpenFace", enforce_detection= False)

            if result["verified"] == True:
                print("Face Matched!")
                faceDetect = d_Font.render("Face Recognized!", 1, Green)
                self.display.blit(faceDetect, (15, 0, 160, 20))
                self.stateManager.setState('scene5')
                
            if result["verified"] == False:
                print("Face Mismatch!")
                faceDetect = d_Font.render("Face  NOT Recognized!", 1, Red)
                self.display.blit(faceDetect, (15, 0, 160, 20))
                
        if 10+72 > mouse[0] > 10 and 10+64 > mouse[1] > 10 and True == clicker[0]:
            self.stateManager.setState('scene1')
            
        if timerTick > 90:
            timerTickState = False
            timerTick = 0
            
        if timerTick == 5:
            three.play()
        if timerTick == 30:
            two.play()
        if timerTick == 60:
            one.play()


class scene5:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        global sensorActivated
        global brtTick
        
        brtTick += 20
        self.display.blit(mainBG,(0,0))
        self.display.blit(btlzr1,(273,217))

        if brtTick < 300 and brtTick > 0:
            self.display.blit(btlzr1,(273,217))
        if brtTick > 300 and brtTick < 600:
            self.display.blit(btlzr2,(273,217))
        if brtTick < 900 and brtTick > 600:
            self.display.blit(btlzr3,(273,217))

        self.display.blit(alcTest,(33,15))
        
        
        if brtTick > 1000:
            brtTick = 0

        print(brtTick)
        
        self.display.blit(activateButt,(540,272))

        if sensorActivated is False:
            self.display.blit(sensorOFF,(104,292))

        if sensorActivated:
            self.display.blit(sensorON,(104,292))

        if 540+231 > mouse[0] > 540 and 272+172 > mouse[1] > 272:
            self.display.blit(activateButt_h,(540,272))

        if 540+231 > mouse[0] > 540 and 272+172 > mouse[1] > 272 and True == clicker[0]:
            print("Clicked")
            
            GPIO.output(sensAct, GPIO.HIGH)
            sensorActivated = True
            
    
        if GPIO.input(soberBut) == 1:
            print("SOBER")
            soberAudio.play()
            GPIO.output(carStarter, GPIO.HIGH)
            GPIO.output(led2, GPIO.HIGH)
            GPIO.output(sensAct, GPIO.LOW)
            sleep(.5)
            sensorActivated = False
            self.stateManager.setState('scene7')
         
        if GPIO.input(drunkBut) == 1:
            print("DRUNK")
            drunkAudio.play()
            GPIO.output(sensAct, GPIO.LOW)
            GPIO.output(led1, GPIO.HIGH)
            sleep(.5)
            sensorActivated = False
            self.stateManager.setState('scene6')

        else:
             print("wawa")
             GPIO.output(led2, GPIO.LOW)
             GPIO.output(led1, GPIO.LOW)

class scene6:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        
        GPIO.output(led1, GPIO.HIGH)
        
        global warnTick 
        warnTick += 5
        
        self.display.blit(mainBG,(0,0))
        self.display.blit(backButt,(10,10))

        if warnTick < 25:
            self.display.blit(warn0,(260,70))
        if warnTick > 26:
            self.display.blit(warn1,(260,70))

        self.display.blit(alcWarn,(84,167))

        if 10+72 > mouse[0] > 10 and 10+64 > mouse[1] > 10:
            self.display.blit(backButt_h,(10,10))
        if 10+72 > mouse[0] > 10 and 10+64 > mouse[1] > 10 and True == clicker[0]:
            self.stateManager.setState('scene1')

        if warnTick > 50:
            warnTick = 0
        print(warnTick)

        
        
class scene7:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        GPIO.output(led2, GPIO.HIGH)
        
        self.display.blit(mainBG,(0,0))
        self.display.blit(backButt,(10,10))

        self.display.blit(carStarted,(0,120))
        
        if 10+72 > mouse[0] > 10 and 10+64 > mouse[1] > 10:
            self.display.blit(backButt_h,(10,10))
        if 10+72 > mouse[0] > 10 and 10+64 > mouse[1] > 10 and True == clicker[0]:
            self.stateManager.setState('scene1')
        

class stateManager:
    def __init__(self, currentScene):
        self.currentScene = currentScene
    
    def getState(self):
        return self.currentScene
    
    def setState(self, state):
        self.currentScene = state

if __name__ == '__main__':
    game = Game()
    game.run()