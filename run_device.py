# import libraries
import RPi.GPIO as GPIO
import time

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

# previous pressure input
prev_input = 0

# updates if pressure is sensed
input = GPIO.input(pressure_sens)


track_time = 1
stop_movement = False

# run device
try:
    while True:
        touch = False

        # terminates movement
        if stop_movement:
            pwm1.stop()
            pwm2.stop()
            pwm3.stop()
            touch = False

        # updates pressure sensed
        input = GPIO.input(pressure_sens)

        # sense if there is pressure
        if input == 1:
            touch = True

        # updates pressure sensed
        input = GPIO.input(pressure_sens)

        # dispenses water from water pump
        if touch:
            GPIO.output(water_pump, True)
            time.sleep(1)
            GPIO.output(water_pump, False)
            time.sleep(1)

        # count num of rotations
        rotation = 0
        num_rotate = 10

        # runs servo motors
        while touch and rotation <= num_rotate:
            stop_movement = True

            # refreshes / update pressure detection
            input = GPIO.input(pressure_sens)

            # if there is pressure, moves motors
            if ((not prev_input) and input):
                # refreshes again
                input = GPIO.input(pressure_sens)

                # turns motors left and right every 1 second using time
                left = False
                now_time = time.time()
                end_time = time.time() + 2
                while now_time != end_time and rotation != num_rotate:
                    if left:
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
                        left = False
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
                        left = True

            # if no pressure detected, stops movement of motors
            else:
                input = GPIO.input(pressure_sens)
                pwm1.stop()
                pwm2.stop()
                pwm3.stop()
                touch = False

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup
