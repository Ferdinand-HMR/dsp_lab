
import cv2

print(ord('a'))
print(ord('b'))
print(ord('c'))

img = cv2.imread('image_01.png')

cv2.imshow('image', img)

print('Select the image window, then press a key on the keyboard')
print('Press q key to quit')

while True:

	key = cv2.waitKey(0)			# 0 means wait until key press

	print('You pressed key', key)

	if key == ord('q'):
		break

print('Good bye')
