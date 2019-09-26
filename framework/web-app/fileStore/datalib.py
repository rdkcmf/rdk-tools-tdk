#!/usr/bin/env python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
#
# -*- coding: utf-8 -*-
#
#  datalib.py
#  
#  Apply statistical analysis to a set of raw float data
#  A. Nair, J. Aldrete
#  
import math
import random
import sys
import string

import numpy as np

class datavalidator:
	
	def __init__(self, size, unit, top, roundOffToDecimals, readings = []):
		self.readings = readings;
		self.size = size;
		self.top = top;
		self.roundOffToDecimals = roundOffToDecimals;
		
	def roundOff(self, value2RoundOff):
		if(self.roundOffToDecimals == 0):
			return value2RoundOff+0.5
		elif(self.roundOffToDecimals > 0):
			return round(value2RoundOff,self.roundOffToDecimals)
 
	def printAllData(self):
		print 'All readings: ',self.readings
		return 
		
	def setRoundToDecimals(self, roundoff2decimals):
		self.roundOffToDecimals = roundoff2decimals
		
	def getMean(self):
		sumAll = 0.0
		for i in range(self.top):
			sumAll = sumAll+self.readings[i]

		return self.roundOff(float(sumAll/self.top))
		
	def getVariance(self):
		bkup_roundto = self.roundOffToDecimals
		mean = self.getMean()
		self.setRoundToDecimals(bkup_roundto)
		temp = 0.0
		for i in range(self.top):
			temp += (mean - self.readings[i]) * (mean-self.readings[i])
		return self.roundOff(temp/(self.top))
		
	def getStdDev(self):
		bkup_roundto = self.roundOffToDecimals
		tmp = math.sqrt(self.getVariance())
		self.setRoundToDecimals(bkup_roundto)
		return tmp
	
	def getQuartile(self, size, data=[]):
		if( (size % 2) == 0 ):
			return ( (data[(size/2)] + data[(size/2)-1])/2)
		else:
			return data[(size/2)]
			
	def getFirstQuartile(self, size, data=[]):
		return self.getQuartile(size/2,data)
		
	def getThirdQuartile(self, size, data=[]):
		if ((size % 2) == 0 ):   # total size is even
			return self.getQuartile(size/2,data[(size/2):])
		else:
			return self.getQuartile(size/2,data[((size/2)+1):])

	def flushOutOutliersByIQR(self):
		copyOfData = np.sort(self.readings)
		q1 = self.getFirstQuartile(self.top, copyOfData)
		q3 = self.getThirdQuartile(self.top, copyOfData)	
		iqr = float(q3-q1)

		ilow = 0;
		ihigh = 0;
		for i in range(self.top):
			if(copyOfData[i] < (q1-1.5*iqr)):
				ilow += 1
			if(copyOfData[i]>(q3+1.5*iqr)):
				ihigh = i
				break
		if(ihigh == 0):
			# no high outliers found	
			highbound = self.top
		else:
			highbound = ihigh

		self.readings = copyOfData[ilow:highbound]
		self.top = (self.readings.shape[0])

	def getInterQuartileRange(self):
		self.readings = np.sort(self.readings)
		if((self.top % 2) == 0):
			q1 = self.getQuartile(self.top/2,self.readings)
			q3 = self.getQuartile(self.top/2,self.readings[self.top/2:])
		else:
			q1 = self.getQuartile(self.top/2,self.readings)
			q3 = self.getQuartile(self.top/2,self.readings[self.top/2:])
		return(q3-q1)
# end of class
