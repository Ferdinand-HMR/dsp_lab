
import cv2

print(ord('a'))
print(ord('b'))
print(ord('c'))

img = cv2.imread('image_01.png')

cv2.imshow('image', img)

print('Select the image window, then press a key on the keyboard')
print('Press q key to quit')

while True:

	key = cv2.waitKey(1)	# 1 means wait for 1 millisecond for key press
							# If there is no key press in 1 millisecond, then return -1

	if key != -1:
		print('You pressed key', key)

	if key == ord('q'):
		break

print('Good bye')
