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
				bot = pycreate2.Create2(port=port, baud=baud["default"])
				bot.start()
				bot.safe()
				print("Hello World!")
			except AttributeError:
				print("No connection detected!")
			time.sleep(3)
	except KeyboardInterrupt: # ctrl + C
		print("Goodbye!")
		pass
