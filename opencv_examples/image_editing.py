import cv2

img = cv2.imread('image.jpg')

# display the image
# works when connected via VNC, not SSH
# cv2.imshow('Image Display', img)
# cv2.waitKey(5000)

print('Image (height, width, data per pixel)')
print(img.shape)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray_image.jpg', img_gray)

img_blur = cv2.GaussianBlur(img, (55,55), 0) # bigger numbers means more blur?
                                             # must be odd numbers
cv2.imwrite('blur_image.jpg', img_blur)

