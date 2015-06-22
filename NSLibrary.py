from websocket import create_connection
import random
import json

class NSEngine:
	def __init__(self, deviceName):
		self.deviceName = deviceName
		self.url = "ws://echo.websocket.org/"
		self.url = "ws://cloud.neurosteer.com:8080/v1/features/000666%s/pull" % deviceName
		print 'url: ' + self.url
		self.index = 0


	def ReadStats(self, sendHello = False):
		#ws = create_connection(self.url)
		#if sendHello:	
			#ws.send('hello, world')
		print 'reading from the clound...'

		#result = ws.recv()

		print('finished reading!')
		#ws.close()

		#return NSStats()

		# #print('JsonResult: ' + result)
		# #formattedResult = json.loads(result)

		c1 = self.getRandom()
		c2 = self.getRandom()
		c3 = self.getRandom()
		h1 = self.getRandom()
		h2 = self.getRandom()
		h3 = self.getRandom()
		e1 = self.getRandom()
		e2 = self.getRandom()
		e3 = self.getRandom()
		theta = self.getRandom()
		delta = self.getRandom()
		beta = self.getRandom()
		gamma = self.getRandom()
		sigma = self.getRandom()
		activity = self.getRandom()
		timestampMillis = random.randint(100000, 153230)

		# if "c1" in formattedResult["features"]:
		# 	c1 = formattedResult["features"]["c1"]

		# if "c2" in formattedResult["features"]:
		# 	c2 = formattedResult["features"]["c2"]

		# if "c3" in formattedResult["features"]:
		# 	c3 = formattedResult["features"]["c3"]

		# if "h1" in formattedResult["features"]:
		# 	h1 = formattedResult["features"]["h1"]

		# if "h2" in formattedResult["features"]:
		# 	h2 = formattedResult["features"]["h2"]

		# if "h3" in formattedResult["features"]:
		# 	h3 = formattedResult["features"]["h3"]

		# if "e1" in formattedResult["features"]:
		# 	e1 = formattedResult["features"]["e1"]

		# if "e2" in formattedResult["features"]:
		# 	e2 = formattedResult["features"]["e2"]

		# if "e3" in formattedResult["features"]:
		# 	e3 = formattedResult["features"]["e3"]

		# if "theta" in formattedResult["features"]:
		# 	theta = formattedResult["features"]["theta"]		

		# if "delta" in formattedResult["features"]:
		# 	delta = formattedResult["features"]["delta"]	

		# if "gamma" in formattedResult["features"]:
		# 	gamma = formattedResult["features"]["gamma"]

		# if "sigma" in formattedResult["features"]:
		# 	sigma = formattedResult["features"]["sigma"]

		# if "activity" in formattedResult["features"]:
		# 	activity = formattedResult["features"]["activity"]

		# if "timestampMillis" in formattedResult["features"]:
		# 	timestampMillis = formattedResult["features"]["timestampMillis"]

		#if "theta" in formattedResult["features"]:
			#theta

		#if 0 == self.index % 2:



		stats = NSStats(c1=c1, c2=c2, c3=c3, h1=h1, h2=h2, h3=h3, e1=e1, e2=e2, e3=e3, theta=theta, delta = delta, gamma=gamma, sigma=sigma, activity=activity, timestampMillis=timestampMillis)
		#else:
		#	stats = NSStats(h1=random.randint(-5, 5), e1=random.randint(-5, 5))
		
		self.index += 1

		return stats

	def getRandom(self):
		base = random.random() * 2 + 0.2
		sign = 1
		if (random.random() + 0.7) < 1:
			sign = -1

		return base * sign

def LoadDate(deviceName):
	ws = create_connection("ws://echo.websocket.org/")

	ws.send('hello, world')
	result = ws.recv()

	ws.close()

class NSStats:
	def __init__(self, h1=0, h2=0, h3=0, e1=0, e2=0, e3=0, c1=0, c2=0, c3=0, theta=0, delta=0, beta=0, gamma=0, sigma=0, activity=0, timestampMillis=0):
		self.h1 = h1
		self.h2 = h2
		self.h3 = h3
		self.e1 = e1
		self.e2 = e2
		self.e3 = e3
		self.c1 = c1
		self.c2 = c2
		self.c3 = c3
		self.theta=theta
		self.delta=delta
		self.beta=beta
		self.gamma=gamma
		self.sigma=sigma
		self.activity=activity
		self.timestampMillis=timestampMillis

	def formatToDictionary(self):
		return {

		'h1' : self.h1,
		'h2' : self.h2,
		'h3' : self.h3,

		'c1' : self.c1,
		'c2' : self.c2,
		'c3' : self.c3,

		'e1' : self.e1,
		'e2' : self.e2,
		'e3' : self.e3,

		'theta' : self.theta,
		'delta' : self.delta,
		'beta' : self.beta,
		'gamma' : self.gamma,
		'sigma' : self.sigma,
		'activity' : self.activity,
		'timestampMillis' : self.timestampMillis
		}

	def __str__(self):
		return 'h1=%f h2=%f h3=%f e1=%f e2=%f e3=%f c1=%f c2=%f c3=%f' % (self.h1, self.h2, self.h3, self.e1, self.e2, self.e3, self.c1, self.c2, self.c3)

	def isHappy(self, threshold):
		return self.h1 >= threshold or self.h2 >= threshold or self.h3 >= threshold

	def isUnHappy(self, threshold):
		return self.h1 <= threshold or self.h2 <= threshold or self.h3 <= threshold

	def isExcited(self, threshold):
		return self.e1 >= threshold or self.e2 >= threshold or self.e3 >= threshold

	def isUnExcited(self, threshold):
		return self.e1 <= threshold or self.e2 <= threshold or self.e3 <= threshold

	def isConcentrated(self, threshold):
		return self.c1 >= threshold or self.c2 >= threshold or self.c3 >= threshold

	def isUnConcentrated(self, threshold):
		return self.c1 <= threshold or self.c2 <= threshold or self.c3 <= threshold

#e = NSEngine('4e57c9')
#for i in range(100):
	#result = e.ReadStats()
	#print('result: ' + str(result))

