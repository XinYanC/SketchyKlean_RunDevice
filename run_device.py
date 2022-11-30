# import libraries for Raspiberry Pi
import time
import RPi.GPIO as GPIO

# GPIO settings
GPIO.setwarnings(False)

# servo motor pin numbers and setup
servo_pin1 = 17
servo_pin2 = 22
servo_pin3 = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)
GPIO.setup(servo_pin3, GPIO.OUT)

# lcd input pin number and setup

# again button input pin number and setup; initally set as off
again_but = 16
GPIO.setup(again_but, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
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

    # always reset frequency of pin back to 100
    pwm1 = GPIO.PWM(servo_pin1, 100)
    pwm2 = GPIO.PWM(servo_pin2, 100)
    pwm3 = GPIO.PWM(servo_pin3, 100)

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
        print('Water Dispensed')
        time.sleep(1)  # 1 sec lag before water is dispensed
        GPIO.output(water_pump, True)
        time.sleep(1)
        GPIO.output(water_pump, False)
        time.sleep(1)

    # count num of rotations (currently at 10 rotations)
    rotation = 0
    num_rotate = 4

    # runs servo motors
    while touch and rotation <= num_rotate:
        stop_movement = True
        rotation = 0
        left_rotation = False

        # refreshes / update pressure detection
        input = GPIO.input(pressure_sens)

        # if there is pressure, moves motors
        if ((not prev_input) and input):
            print('Start Wash')

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
                        print('Your shoes are Klean!')
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
                        print('Your shoes are Klean!')
                        return
                    left_rotation = True

        # if no pressure detected, stops movement of motors
        else:
            input = GPIO.input(pressure_sens)
            pwm1.stop()
            pwm2.stop()
            pwm3.stop()
            touch = False
            print('No Shoe Detected')
            return
        return
    return


# first start cycle run function
def start():
    # detects if there is shoe/pressure on pressure sensor
    input = GPIO.input(pressure_sens)

    # if there is no pressure, it keeps refreshing until there is shoe detected
    while input != 1:
        input = GPIO.input(pressure_sens)

    # when there is a shoe detected, it runs the wash function / starts washing the shoe
    if input == 1:
        wash()  # one initial wash cycle
    return


# asks user if they want another cycle function
def again():
    # detects if the button is pressed
    input = GPIO.input(again_but)

    # gets out of the loop if button is pressed but no shoe is detected
    if input == 1 and GPIO.input(pressure_sens) == 0:
        return

    # asks user for input
    print("Wash again? Yes- press the button.")
    print("If not, take out your Klean shoes and press the button.")

    # if there is button pressed, it keeps detecting/refreshing for button input
    while input != 1:
        input = GPIO.input(again_but)
        now_time = time.time()

    # if button is pressed, it does another wash cycle and ask for this loop again
    # this ensures that users can choose to continue to wash multiple times
    if input == 1:
        wash()
        again()
    return


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer)
        time.sleep(1)
        t -= 1
    print('Your shoes are clean!')


# main run
try:
    while True:  # when device is running/open
        print("Start Device")
        start()
        again()
        print('Close Device')
        break
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup
