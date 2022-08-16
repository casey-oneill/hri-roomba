from enum import IntEnum
from pycreate600 import Create
from pycreate600 import NoConnectionError
import numpy as np
import random
import sys
import time


class Directions(IntEnum):
    FORWARD = 0,
    BACK = 1,
    LEFT = 2,
    RIGHT = 3


class State(IntEnum):
    NEUTRAL = 0,
    NEUROTIC = 1


directions = [np.array([1, 1]), np.array([-1, -1]),
              np.array([0, 1]), np.array([1, 0])]
random.seed()


def make_songs(bot: Create):
    i = [72, 32, 71, 16, 69, 16, 74, 32, 72, 16, 71,
         32, 71, 16, 69, 16, 67, 16, 71, 16, 71, 32]
    bot.song(State.NEUTRAL, i)

    j = [52, 64, 45, 32, 41, 16, 52, 32, 45,
         32, 41, 32, 52, 32, 45, 16, 41, 16]
    bot.song(State.NEUROTIC, j)


def clean_neurotic(bot: Create, vel: int = 100, duration: int = 1):
    """
    Start a neurotic cleaning cycle.

    Args:
        bot: Create class controlling Roomba.
        vel: Roomba movement speed.
        duration: The length of the cleaning cycle (minutes).
    """
    print("Start neurotic cleaning!")

    timeout = duration

    movement = directions[Directions.FORWARD] * vel
    is_cleaning = True

    duration = bot.play_song(State.NEUROTIC)
    time.sleep(duration)

    while is_cleaning:
        is_colliding = False
        collision = None
        
        bot.motors(13)
        while is_cleaning and not is_colliding:
            bot.drive_direct(int(movement[0]), int(movement[1]))
            time.sleep(0.001)
            timeout -= 0.001

            sensors = bot.sensors()
            if sensors.bumps_wheeldrops.bump_left == True and sensors.bumps_wheeldrops.bump_right == True:
                print("Bump Middle.")
                is_colliding = True
                collision = Directions.FORWARD
            elif sensors.bumps_wheeldrops.bump_left == True:
                print("Bump Left.")
                is_colliding = True
                collision = Directions.LEFT
            elif sensors.bumps_wheeldrops.bump_right == True:
                print("Bump Right.")
                is_colliding = True
                collision = Directions.RIGHT

            if timeout <= 0:
                is_cleaning = False

        if is_colliding:
            bot.motors_stop()
            bot.drive_stop()
            time.sleep(1)
            timeout -= 1

            duration = bot.play_song(State.NEUROTIC)
            time.sleep(duration)


            print("Changing directions.")
            movement = directions[Directions.BACK] * vel
            bot.drive_direct(int(movement[0]), int(movement[1]))
            time.sleep(1)
            timeout -= 1

            if collision == Directions.FORWARD:
                print("Turning Around.")
                i = random.randint(0, 1)
                movement = directions[Directions.LEFT] * vel if i == 0 else directions[Directions.RIGHT] * vel
                bot.drive_direct(int(movement[0]), int(movement[1]))
                time.sleep(2)
                timeout -= 2
            elif collision == Directions.LEFT:
                print("Turning Right.")
                movement = directions[Directions.RIGHT] * vel
                bot.drive_direct(int(movement[0]), int(movement[1]))
                time.sleep(2)
                timeout -= 2
            elif collision == Directions.RIGHT:
                print("Turning Left.")
                movement = directions[Directions.LEFT] * vel
                bot.drive_direct(int(movement[0]), int(movement[1]))
                time.sleep(2)
                timeout -= 2

            movement = directions[Directions.FORWARD] * vel

        if timeout <= 0:
            is_cleaning = False

    bot.motors_stop()

    duration = bot.play_song(State.NEUROTIC)
    time.sleep(duration)

    print("Done neurotic cleaning!")

    return 0


if __name__ == "__main__":
    port = "COM4"

    try:
        bot = Create(port=port)
        try:
            bot.start()
            bot.full()

            make_songs(bot)

            timeout = 4 * 60
            bot.leds(8, 255, 128)
            clean_neurotic(bot, duration=(timeout))
        except NoConnectionError:
            print("No connection detected.")
        except Exception:
            print("Error occured.")
    except KeyboardInterrupt:
        print("Goodbye!")
    except Exception:
        print("Unable to open serial connection.")
    
    sys.exit()
