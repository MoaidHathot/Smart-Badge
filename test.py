import feedback
import ForceLibrary
import time
import CameraLibrary
import NSLibrary



#import CameraLibrary as cl
#cl.capture_picture('../pictures/singleNew00.jpg')


def test_feedback():
	fb = feedback.Feedbacker()
	try:
		fb.start()
	except Exception as ex:
		print ex

def test_force():
	first = ForceLibrary.ForceEngine(10, 1)
	second = ForceLibrary.ForceEngine(9, 1)
	while True:
		print 'first is %d, second is %d' % (first.isPushed(), second.isPushed())
		time.sleep(1)
	#for i in range (100):
	#	print 'first is %d, second is %d' % (first.isPushed(), second.isPushed())
	#	time.sleep(1)

def test_picture():
	cl = CameraLibrary.RecordingEngine()
	cl.capturePicture('../pictures/test_00.jpg')

def test_NS():
	e = NSLibrary.NSEngine('4e57c9')
	result = e.ReadStats()
	print 'result: ' + str(result)

test_feedback()
#test_force()
#test_picture()

#for i in range(100):
#	test_NS()