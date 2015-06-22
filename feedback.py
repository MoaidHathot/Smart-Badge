import time
from datetime import datetime
import CameraLibrary as cl
import NSLibrary as nsl
import ForceLibrary as force
import IOLibrary as io
import json

class Feedbacker:

	def __init__(self):

		self.lastEvent = None
		self.threshold = 3.6

		self.rootDataPath = 'data/'
		self.recordingsStorageFolder = 'storage/'
		self.tempStorageFolder = 'temp/'
		self.photoFormat = '.jpg'
		self.startPhotoName = 'EventStartedPicture'
		self.endPhotoName = 'EventEndedPicture'

		self.videoFormat = '.h264'
		self.recordingMaxDuration = 10
		self.intervalsLeftForRecording = self.recordingMaxDuration
		self.eventRecordingDuration = 10

		self.tempRecordingPath = self.rootDataPath + self.recordingsStorageFolder + self.tempStorageFolder

		self.lastRecording = None

		print 'Initializing NS engine...'
		self.nsEngine = nsl.NSEngine('01c010')

		print 'Initializing force engine...'
		self.forceEngine = force.ForceEngine(10, 1)
		self.forceEngine2 = force.ForceEngine(9, 1)

		print 'Initializing recording engine...'
		self.recordingEngine = cl.RecordingEngine()


		print 'Initialization completed.'

	def start(self):

		print 'Feedbacker is starting...'

		print 'starting recording in start...'

		io.createDirectory(self.tempRecordingPath)

		self.currentRecording = self.recordingEngine.startRecording(self.tempRecordingPath, formatDate(datetime.now()) + self.videoFormat)

		print 'starting index in start'
		for index in range(100):
			nsStats = self.nsEngine.ReadStats()
			print 'nsStats: ' + str(nsStats)

			forceStatus = self.forceEngine.isPushed()
			forceStatus2 = self.forceEngine2.isPushed()
			print 'forceStatus: ' + str(forceStatus)
			print 'forceStatus2: ' + str(forceStatus2)

			print ''

			event = self.processData(nsStats, forceStatus, forceStatus2)

			if None != event:
				if None == self.lastEvent:
					self.lastEvent = event
					self.handleEventStart(event)
				else:
					self.handleEventContinuing(self.lastEvent, nsStats, forceStatus, forceStatus2)
			else:
				if None != self.lastEvent:
					self.handleEventEnd(self.lastEvent)
					self.lastEvent = None

			time.sleep(1)

			self.handleIntervalPassed()

	def handleIntervalPassed(self):

		self.intervalsLeftForRecording -= 1
		self.currentRecording.intervals += 1

		if None != self.lastEvent:
			if None == self.currentRecording.eventName:
				self.currentRecording.eventName = self.lastEvent.eventDirectory
				self.currentRecording.shouldBeKept = True
				self.lastEvent.shouldBeSaved = True
				self.currentRecording.event = self.lastEvent

			self.intervalsLeftForRecording += 1
		else:
			if 0 >= self.intervalsLeftForRecording:
				self.recordingEngine.endRecording(self.currentRecording)
				self.intervalsLeftForRecording = self.recordingMaxDuration

				if None != self.lastRecording:
					if self.currentRecording.intervals < self.eventRecordingDuration and None != self.currentRecording.eventName:
						self.lastRecording.shouldBeKept = True
						self.lastEvent.shouldBeSaved = True
						self.lastRecording.eventName = self.currentRecording.eventName
						self.lastRecording.event = self.currentRecording.event

					if not self.lastRecording.shouldBeKept:
						io.silentRemove(self.lastRecording.fileFullPath)
					else:
						io.moveFile(self.lastRecording.fileFullPath, self.lastRecording.event.eventDirectory + self.lastRecording.fileName)

				if self.currentRecording.shouldBeKept:
					io.copyFile(self.currentRecording.fileFullPath, self.currentRecording.event.eventDirectory + self.currentRecording.fileName, self.currentRecording.event.eventDirectory)

				#self.recordingEngine.endRecording(self.currentRecording)
				self.lastRecording = self.currentRecording
				self.currentRecording = self.recordingEngine.startRecording(self.tempRecordingPath, formatDate(datetime.now()) + self.videoFormat)






	def processData(self, nsStats, forceStatus, forceStatus2):
		if nsStats.isHappy(self.threshold) or nsStats.isUnHappy(-self.threshold) or nsStats.isExcited(self.threshold) or nsStats.isUnExcited(-self.threshold) \
			or nsStats.isConcentrated(self.threshold) or nsStats.isUnConcentrated(-self.threshold) or forceStatus or forceStatus2:

			return FeedbackEvent(nsStats, forceStatus, forceStatus2, self.rootDataPath + self.recordingsStorageFolder)

		return None

	def handleEventStart(self, event):
		event.startEvent(datetime.now())
		#self.capturePicture(event, self.startPhotoName + self.photoFormat)
		print '*** event has started'

	def handleEventEnd(self, event):
		event.endEvent(datetime.now())

		if self.lastEvent.shouldBeSaved:
			meta = self.formateMetaData(event)
			metaFile = io.createFile(event.eventDirectory, 'metadata.json')
			io.writeFile(metaFile, meta)
		#self.capturePicture(event, self.endPhotoName + self.photoFormat)
		print '$$$ event has ended. # of nsStatus: %d, # of foceStatus: %d' % (len(event.nsStatsCollection), len(event.forceStatusCollection))

	def handleEventContinuing(self, event, nsStats, forceStatus, forceStatus2):
		event.AddEventData(nsStats, forceStatus, forceStatus2)
		print 'event is continuing'

	def capturePicture(self, event, pictureName):
		io.createDirectory(event.eventDirectory)
		self.recordingEngine.capturePicture(event.eventDirectory + pictureName, self.currentRecording.camera)	

	def formateMetaData(self, event):

		return json.dumps([
				{
					'Event': {
						'EventName' : event.name,
						'startTimestamp' : formatDate(event.startTimestamp),
						'endTimestamp' : formatDate(event.endTimestamp),
						'rootDirectoryPath' : event.rootDirectoryPath,
						'eventDirectory' : event.eventDirectory,
						'FrontSensorSamples' : event.forceStatus2Collection,
						'BackSensonorSamples' : event.forceStatusCollection,
						'nsStatsCollection' : [ns.formatToDictionary() for ns in event.nsStatsCollection]
					}
				}
			])

class FeedbackEvent:

	def __init__(self, nsStats, forceStatus, forceStatus2, rootDirectoryPath):
		self.name = None
		self.startTimestamp = None
		self.endTimestamp = None
		#self.endTimestamp = None
		self.shouldBeSaved = False
		self.nsStatsCollection = [nsStats]
		self.forceStatusCollection = [forceStatus]
		self.forceStatus2Collection = [forceStatus2]

		self.rootDirectoryPath = rootDirectoryPath

		self.eventDirectory = None

	def startEvent(self, timestamp):
		self.startTimestamp = timestamp
		#self.name = '%d.%d.%d_%d..%d..%d' % (timestamp.day, timestamp.month, timestamp.year, timestamp.hour, timestamp.minute, timestamp.second)
		self.name = formatDate(timestamp.now())

		self.eventDirectory = self.rootDirectoryPath + self.name + '/'
		#io.createDirectory(self.directoryPath + self.name)
		#cl.capture_picture(self.directoryPath + self.name + '/' + self.startPhotoName + self.photoFormat)
 
	def endEvent(self, timestamp):
		self.endTimestamp = timestamp

		#io.createDirectory(self.directoryPath + self.name)
		#cl.capture_picture(self.directoryPath + self.name + '/' + self.startPhotoName + self.photoFormat)

	def AddEventData(self, nsStats, forceStatus, forceStatus2):
		self.nsStatsCollection.append(nsStats)
		self.forceStatusCollection.append(forceStatus)
		self.forceStatus2Collection.append(forceStatus2)

def formatDate(timestamp):
	return '%d.%d.%d_%d..%d..%d' % (timestamp.day, timestamp.month, timestamp.year, timestamp.hour, timestamp.minute, timestamp.second)