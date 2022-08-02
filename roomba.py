from enum import IntEnum
from pycreate600 import Create
import numpy as np
import random
import time

from pycreate600.errors import NoConnectionError


class Directions(IntEnum):
    FORWARD = 0,
    BACK = 1,
    LEFT = 2,
    RIGHT = 3


directions = [np.array([1, 1]), np.array([-1, -1]), np.array([0, 1]), np.array([1, 0])]
random.seed()

def clean(bot: Create, vel: int = 200, duration: int = 1):
    """
    Start a custom cleaning cycle.
    """
    print("Start cleaning!")
    timeout = duration * 60
    is_cleaning = True
    movement = directions[Directions.FORWARD] * vel

    bot.motors(13)

    while is_cleaning:
        is_colliding = False
        collision = None
        while is_cleaning and not is_colliding:
            bot.drive_direct(int(movement[0]), int(movement[1]))
            time.sleep(0.03)
            timeout -= 0.03

            sensors = bot.sensors()
            if sensors.bumps_wheeldrops.bump_left == True and sensors.bumps_wheeldrops.bump_right == True:
                print("Bump Middle!")
                is_colliding = True
                collision = Directions.FORWARD
            elif sensors.bumps_wheeldrops.bump_left == True:
                print("Bump Left!")
                is_colliding = True
                collision = Directions.LEFT
            elif sensors.bumps_wheeldrops.bump_right == True:
                print("Bump Right!")
                is_colliding = True
                collision = Directions.RIGHT

            if timeout <= 0:
                is_cleaning = False

        bot.drive_stop()
        time.sleep(0.1)
        timeout -= 0.1

        print("Changing directions!")
        movement = directions[Directions.BACK] * vel
        bot.drive_direct(int(movement[0]), int(movement[1]))
        time.sleep(0.5)
        timeout -= 0.5

        if collision == Directions.FORWARD:
            print("Turning Around.")
            i = random.randint(0, 1)
            movement = directions[Directions.LEFT] * vel if i == 0 else directions[Directions.RIGHT] * vel
            bot.drive_direct(int(movement[0]), int(movement[1]))
            time.sleep(1.8)
            timeout -= 1.8
        elif collision == Directions.LEFT:
            print("Turning Right")
            movement = directions[Directions.RIGHT] * vel
            bot.drive_direct(int(movement[0]), int(movement[1]))
            time.sleep(1.8)
            timeout -= 1.8
        elif collision == Directions.RIGHT:
            print("Turning Left!")
            movement = directions[Directions.LEFT] * vel
            bot.drive_direct(int(movement[0]), int(movement[1]))
            time.sleep(1.8)
            timeout -= 1.8
        
        movement = directions[Directions.FORWARD] * vel
    
        if timeout <= 0:
            is_cleaning = False

    bot.motors_stop()
    print("Done cleaning!")


if __name__ == "__main__":
    port = "COM4"

    try:
        bot = Create(port=port)

        while True:
            try:
                bot.start()
                bot.full()

                clean(bot)
            except NoConnectionError:
                print("No connection detected.")
            except Exception:
                print("Error occured.")
            time.sleep(3)
    except KeyboardInterrupt:
        print("Goodbye!")
    except Exception:
        print("Unable to open serial connection.")
