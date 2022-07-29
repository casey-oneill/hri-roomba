import pycreate2
import time

if __name__ == "__main__":
	port = "COM4"
	baud = {
        'default': 115200,
        'alt': 19200
    }

	try:
		while True:
			try:
				bot = pycreate2.Create2(port=port)
				bot.start()
				bot.safe()
				
				bot.led(14, 255, 0)
				song = [72, 12, 20, 24, 67, 12, 20, 24, 64, 24, 69, 16, 71, 16, 69, 16, 68, 24, 70, 24, 68, 24, 67, 12, 65, 12, 67, 48]

				print(">> song len: ", len(song) // 2)

				# song number can be 0-3
				song_num = 3
				bot.createSong(song_num, song)
				time.sleep(0.1)
				how_long = bot.playSong(song_num)

				# The song will run in the back ground, don't interrupt it
				# how_long is the time in secods for it to finish
				print('Sleep for:', how_long)
				time.sleep(how_long)

				break
			except AttributeError:
				print("No connection detected!")
			time.sleep(3)
	except KeyboardInterrupt: # ctrl + C
		print("Goodbye!")
		pass
