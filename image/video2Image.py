#-*-coding:utf-8-*-
import os
import numpy as np
import cv2

IMG_EXTENSIONS = ['.jpg', '.JPG', '.jpeg', '.JPEG',
				'.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP', '']

VIDEO_EXTENSIONS = ['.avi']

def is_image_file(filename):
	return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)

def make_if_not_exist(path):
	if not os.path.exists(path):
		os.makedirs(path)

def fileToTxt(dir, file):
	filedir = os.listdir(dir)

	for name in filedir:
		fullname = os.path.join(dir, name)
		print(fullname)

		if(os.path.isdir(fullname)):
			fileToTxt(fullname, file)
		else:
			if(fullname.endswith('.jpg') or fullname.endswith('.png')):
				file.write(fullname+'\n')


def rm_empty_image(path):
	for roots, dirs, files in os.walk(path):
		print('processing dir:', roots)
		for f in files:
			imageName = os.path.join(roots, f)
			if not os.path.isfile(imageName):
				continue
			if ext not in IMG_EXTENSIONS:
				continue
			im = cv2.imread(imageName)
			if im is None:
				print(path, f)
				os.remove(imageName)
			else:
				w, h, c = np.shape(im)
				if (w < 20 or h < 20):
					print(w, h, c)
					os.remove(imageName)

def imageInfo(image):
	mat = cv2.imread(image)
	shape = mat.shape
	return mat, shape[0], shape[1], shape[2]


def image2Video(videoName, imagePath, frameWidth=1920, frameHeight=1080, frameFPS=25):
	out = cv2.VideoWriter(videoName, cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'),
		frameFPS, (frameWidth, frameHeight))

	files = os.listdir(imagePath)
	files.sort(key=lambda x:int(x[:-4]))

	for image in files:
		imageName = os.path.join(imagePath, image)
		print(imageName)
		mat = cv2.imread(imageName)
		out.write(mat)
		cv2.imshow('frame', mat)

		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	out.release()


def video2Image(videoName, imagePath, show):
	cap = cv2.VideoCapture(videoName)

	if (cap.isOpened() == False):
		print('Error opening video stream of file')

	count = 0
	while(cap.isOpened()):
		count += 1
		ret, frame = cap.read()
		if ret == True:
			imageName = os.path.join(imagePath, str(count) + '.jpg')
			if show:
				cv2.imshow('Frame', frame)
			cv2.imwrite(imageName, frame)

			if cv2.waitKey(25) & 0xFF == ord('q'):
				break

		else:
			break

	cap.release()

	cv2.destroyAllWindows()


if __name__ == '__main__':
	cur = os.getcwd()
	print(cur)

	videoPath = '.'
	for roots, parents, files in os.walk(videoPath):
		for file in files:
			print(file)
			if file.endswith('avi'):
				name = file.replace(' ', '-')
				dirName = os.path.join(roots, name[:-4])
				videoName = os.path.join(roots, file)
				make_if_not_exist(dirName)
				video2Image(videoName, dirName, 1)
