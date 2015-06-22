import os, errno, sys, shutil


def silentRemove(filename):
	try:
		print 'deleting ' + filename
		os.remove(filename)
	except OSError as e: # this would be "except OSError, e:" before Python 2.6
		if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
			raise # re-raise exception if a different error occurred

def createDirectory(directory):
	#realDirPath = os.path.dirname(__file__) + '/'
	#realPath = os.path.join(realDirPath, directory)

	#print 'directory: %s, realDirPath: %s, realPath: %s' % (directory, realDirPath, realPath)

	if not isDirectoryExists(directory):
		os.makedirs(directory)

def isDirectoryExists(directory):
	return os.path.isdir(directory)

def moveFile(source, destination):
	print 'moving %s to %s' % (source, destination)
	if not os.path.isfile(destination):
		shutil.move(source, destination)
	else:
		print 'file %s already exists' % destination

#def copyFile(source, destination):
	#print 'copying %s to %s' % (source, destination)
	#shutil.copy(source, destination)#

def copyFile(source, destination, destinationDirectory):
	createDirectory(destinationDirectory)
	shutil.copy(source, destination)

def createFile(fileDirectory, fileName):
	createDirectory(fileDirectory)
	return open(fileDirectory + fileName, 'a')

def writeFile(file, message):
	file.write(message)
	file.close()

    