# import libraries for Raspiberry Pi
import time
import RPi.GPIO as GPIO

# import libraries for user-interface using Tkinter
from tkinter import *
from tkinter.ttk import *


# GPIO settings
GPIO.setwarnings(False)

# servo motor pin numbers and setup
servo_pin1 = 17
servo_pin2 = 22
servo_pin3 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)
GPIO.setup(servo_pin3, GPIO.OUT)
# motor variables
pwm1 = GPIO.PWM(servo_pin1, 100)
pwm2 = GPIO.PWM(servo_pin2, 100)
pwm3 = GPIO.PWM(servo_pin3, 100)

# pressure sensor input pin number and setup
pressure_sens = 4
GPIO.setup(pressure_sens, GPIO.IN)
# water pump pin number and setup
water_pump = 21
GPIO.setup(water_pump, GPIO.OUT)

# updates if pressure is sensed
input = GPIO.input(pressure_sens)


# wash function - runs device to "wash" the shoe; moves the three brushes back and forward
def wash():
    # set inital variables
    touch = False
    stop_movement = False

    # previous pressure input (no pressure detected)
    prev_input = 0

    # terminates movement
    if stop_movement:
        return

    # updates pressure sensed
    input = GPIO.input(pressure_sens)

    # sense if there is pressure
    if input == 1:
        touch = True

    # updates pressure sensed
    input = GPIO.input(pressure_sens)

    # dispenses water from water pump when there is shoe detected (from touch), begins wash cycle
    if touch:
        print('Start Wash Cycle')
        time.sleep(1)  # 1 sec lag before water is dispensed
        GPIO.output(water_pump, True)
        time.sleep(1)
        GPIO.output(water_pump, False)
        time.sleep(1)

    # count num of rotations (currently at 10 rotations)
    rotation = 0
    num_rotate = 10

    # runs servo motors
    while touch and rotation <= num_rotate:
        stop_movement = True
        rotation = 0
        left_rotation = False

        # refreshes / update pressure detection
        input = GPIO.input(pressure_sens)

        # if there is pressure, moves motors
        if ((not prev_input) and input):
            # refreshes again
            input = GPIO.input(pressure_sens)

            # turns motors left and right every 1 second using time
            left_rotation = False
            now_time = time.time()
            end_time = time.time() + 2
            while now_time != end_time and rotation != num_rotate:
                if left_rotation:
                    pwm1.start(25)
                    pwm2.start(25)
                    pwm3.start(25)
                    time.sleep(1)
                    rotation += 1
                    if rotation == num_rotate:
                        pwm1.stop()
                        pwm2.stop()
                        pwm3.stop()
                        touch = False
                        return
                    left_rotation = False
                else:
                    pwm1.start(10)
                    pwm2.start(10)
                    pwm3.start(10)
                    time.sleep(1)
                    rotation += 1
                    if rotation == num_rotate:
                        pwm1.stop()
                        pwm2.stop()
                        pwm3.stop()
                        touch = False
                        return
                    left_rotation = True

        # if no pressure detected, stops movement of motors
        else:
            input = GPIO.input(pressure_sens)
            pwm1.stop()
            pwm2.stop()
            pwm3.stop()
            touch = False
            return
        return
    return


# first start cycle run function
def start():
    # detects if there is shoe/pressure on pressure sensor
    input = GPIO.input(4)

    # if there is no pressure, it keeps refreshing until there is shoe detected
    while input != 1:
        input = GPIO.input(4)

    # when there is a shoe detected, it runs the wash function / starts washing the shoe
    if input == 1:
        wash()


# asks user if they want another cycle function
def again():
    # reinforce user-interface page style
    welcome.title('Sketchy Klean')
    welcome_page = ttk.Frame(welcome, padding=10)
    welcome_page.grid()

    # text that ask if user wants another wash
    ttk.Label(welcome_page, text='Another wash?').grid(row=1, column=0)

    # button for another wash to start, if the button is pressed, it goes to the wash function (by command)
    Button(welcome_page, text='Yes', command=wash).grid(row=2, column=0)


# main run
try:
    while True:  # when device is running/open
        # creates new user-interface page called welcome
        welcome = Tk()

        # set style of welcome
        welcome.geometry('500x500')
        welcome.title('Sketchy Klean')

        # sets text section of welcome as welcome_page in grid
        welcome_page = ttk.Frame(welcome, padding=10)
        welcome_page.grid()

        # add text/label
        ttk.Label(welcome_page, text='Welcome to Sketchy Klean!').grid(
            row=0, column=0)
        ttk.Label(welcome_page, text='Please place your shoe on the stand to start.').grid(
            row=1, column=0)

        # in tkinter, you need the mainloop() to display the interface page but mainloop would block all th code after
        # to run the page along with the code, you can use the after() method
        welcome.after(500, start)
        welcome.after(500, again)
        # this runs the start and again method 500 milliseconds after the display with mainloop()

        # displays interface page
        mainloop()

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup
