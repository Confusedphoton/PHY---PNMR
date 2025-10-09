import sys
import gpip_package
import time

class YokogawaGS200(object):
	def __init__(self, gpib, addr):
		self.gpib = gpib
		self.addr = addr
		
		self.gpib.addr(self.addr)
		id = self.gpib('*idn?', True)
		if not id.startswith('YOKOGAWA,GS2'):
			raise ValueError('Device identifies as ' + id)

	def output(self, on):
		self.gpib.addr(self.addr)
		if on:
			self.gpib(':OUTP 1')
		else:
			self.gpib(':OUTP 0')

	def voltage_mode(self):
		self.gpib.addr(self.addr)
		self.gpib(':SOUR:FUNC VOLT')

	def current_mode(self):
		self.gpib.addr(self.addr)
		self.gpib(':SOUR:FUNC CURR')

	def set_range(self, range):
		''' Valid values are .001, .01, .1, .2, 1, 10, 30 '''
		self.gpib.addr(self.addr)

		if range < 1:
			self.gpib(':SOUR:RANG %dE-3' % (range*1000))
		else:
			self.gpib(':SOUR:RANG %dE+0' % range)

		newrange = self.gpib(':SOUR:RANG?', True)
		if float(newrange) != range:
			raise ValueError('GS200 did not accept request for range %f, returned %s' % (range, newrange))
		return newrange

	def set_level(self, level):
		self.gpib.addr(self.addr)
		self.gpib(':SOUR:LEV %f' % level)

class Keysight34420A(object):
	def __init__(self, gpib, addr):
		self.gpib = gpib
		self.addr = addr
		
		self.gpib.addr(self.addr)
		id = self.gpib('*idn?', True)
		if not id.startswith('HEWLETT-PACKARD,34420A'):
			raise ValueError('Device identifies as ' + id)

	def get_value(self, range='AUTO', channel=1):
		''' Gets the value before this command, then triggers an update for the next call '''
		self.gpib.addr(self.addr)
		return float(self.gpib('MEAS:VOLT:DC? %s,(@%d)' % (range, channel), True))

class Kiethley196(object):
	def __init__(self, gpib, addr):
		self.gpib = gpib
		self.addr = addr
		
		self.gpib.addr(self.addr)
		id = self.gpib('', True)
		if not id.startswith('N'):
			raise ValueError('Unexpected device response ' + id)

	def dc_volts(self):
		self.gpib.addr(self.addr)
		self.gpib('F0X', True)
	def ac_volts(self):
		self.gpib.addr(self.addr)
		self.gpib('F1X', True)
	def dc_amps(self):
		self.gpib.addr(self.addr)
		self.gpib('F3X', True)
	def ac_amps(self):
		self.gpib.addr(self.addr)
		self.gpib('F4X', True)
	def ohms(self):
		self.gpib.addr(self.addr)
		self.gpib('F2X', True)
	def range(self, range):
		'''Set range to a value in 0-7. 0 is AUTO, while higher numbers are 3 * 10^(x0 + range), with x0 = -4 for voltages, -7 for current, and +1 for resistance. '''
		self.gpib.addr(self.addr)
		self.gpib('F%dX' % range, True)
	def get_value(self):
		self.gpib.addr(self.addr)
		rval = self.gpib('', True)
		bk = rval.find('+')
		if bk < 0 or (0 < rval.find('-') < bk):
			bk = rval.find('-')
		return (float(rval[bk:]), rval[1:bk])

if __name__ == '__main__':
	gpibint = gpip_package.PrologixGPIB(sys.argv[1])
	yk = YokogawaGS200(gpibint, 1)
	dvm = Keysight34420A(gpibint, 23)
	dmm = Kiethley196(gpibint, 9)

	yk.current_mode()
	yk.set_range(.1)
	yk.set_level(.03)
	yk.output(True)

	try:
		dvm.get_value(channel=1)
	except TimeoutError:
		time.sleep(3)


	print('Resistance is: %.3f ohms' % (dvm.get_value(channel=1)/30e-3))

