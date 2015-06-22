import time
import picamera
import IOLibrary as iol

class RecordingEngine:

    def capturePicture(self, fileName, givenCamera = None):
        print 'capturing picture %s' % fileName

        camera = givenCamera

        if None == camera:
            camera = picamera.PiCamera()

        try:
            camera.capture(fileName)
        finally:
            camera.close()

    #def capturePicture(self, fileName):
        #capturePicture(self, fileName)

    #def capturePicture(self, directory, fileName):
        #capturePicture(directory + fileName)

    def startRecording(self, directory, fileName, framerate = -1):

        try:
            print 'getting piCamera for %s ' % fileName
            camera = picamera.PiCamera()

            #camera.resolution = (640, 480)

            framerate = 25

            if -1 < framerate:
                camera.framerate = framerate

            print 'start recording'
            camera.start_recording(directory + fileName, format='h264')
            print 'returning camera'
            return VideoData(camera, directory, fileName)
        except:
            print 'getting piCamera for %s ' % fileName
            camera = picamera.PiCamera()
            if -1 < framerate:
                camera.framerate = framerate

            print 'start recording'
            camera.start_recording(directory + fileName)
            print 'returning camera'
            return VideoData(camera, directory, fileName)


    def endRecording(self, videoData):
        try:
            print 'stop recording'
            videoData.camera.stop_recording()
        finally:
            videoData.camera.close()


class VideoData:
    def __init__(self, camera, filePath, fileName):
        self.camera = camera
        self.fileName = fileName
        self.fileFullPath = filePath + fileName
        self.eventName = None
        self.intervals = 0
        self.shouldBeKept = False
        self.event = None


def capture_picture(saveTo):

    print 'capturing %s' % saveTo
    camera = picamera.PiCamera()
    try:
        camera.capture(saveTo)
    finally:
        camera.close()

def start_capture_video(saveTo, framerate = -1):
    camera = picamera.PiCamera()

    if -1 < framerate:
        camera.framerate = framerate

    camera.start_recording(saveTo)
    return camera

def stop_capture_video(camera):
    try:
        camera.stop_recording()
    finally:
        camera.close()


def capture_video_duration(directory, fileName, duration, framerate = -1, foramt = '.h264'):

    currentFileName = directory + fileName + format

    print 'capturing file ' + currentFileName
    camera = start_capture_video(directory + fileName, framerate)

    print 'waiting for ' + str(duration)
    camera.wait_recording(duration)

    print 'End capture of file ' + currentFileName
    stop_capture_video(camera)

def capture_video_loops(directory, fileNamePrefix, loopDuration, times, format = '.h264'):

    for i in range(times):
        currentFileName = directory + fileNamePrefix + "_" + str(i) + format;

        print 'capturing file ' + currentFileName
        camera = start_capture_video(currentFileName)

        print 'waiting for ' + str(loopDuration)
        #time.sleep(loopDuration)
        camera.wait_recording(loopDuration)

        print 'End capture of file ' + currentFileName
        stop_capture_video(camera)

def capture_video_buffer(directory, fileNamesPrefix, duration, fileNumber, times = 10, format = '.h264'):
    for i in range(times):
        for index in fileNumber:
            currentFileName = directory + fileNamesPrefix + "_" + str(i) + format;

            print 'capturing file ' + currentFileName
            camera = start_capture_video(currentFileName)

            print 'waiting for ' + str(loopDuration)
            #time.sleep(loopDuration)
            camera.wait_recording(loopDuration)

            print 'End capture of file ' + currentFileName
            stop_capture_video(camera)