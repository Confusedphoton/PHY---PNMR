import sys
import serial

class PrologixGPIB(object):
	def __init__(self, devpath):
		self.gpib = serial.Serial(devpath, baudrate=115200)
		self.gpib.timeout = 1

		# Query version to make sure it is live
		self.gpib.write(b'++ver\n')
		resp = self.gpib.readline()

		if not resp.startswith(b'Prologix'):
			raise RuntimeError('Cannot communicate with GPIB adapter at ' + devpath)

		self('mode 1')

	def __call__(self, command, response=False):
		self.gpib.write((command + '\n').encode('us-ascii'))
		if response:
			out = self.gpib.readline().decode('us-ascii')
			if len(out) == 0:
				raise TimeoutError('Timeout on command %s' % command)
			return out.strip()

	def auto_rw(self, val=None):
		if val is True:
			self('++auto 1')
		elif val is False:
			self('++auto 0')
		else:
			return (self('++auto', True) == '1')

	def addr(self, addr):
		self('++addr %d' % addr)
		self.gpib.flushInput()

	def scan_bus(self):
		output = ''
		for i in range(0, 31):
			self.addr(i)
			try:
				line = f'{i} : {self('*idn?', True)}'
				output += line + '\n'
				print(line)
			except:
				pass
		return output

if __name__ == '__main__':
	gpib = PrologixGPIB(sys.argv[1])
	gpib.scan_bus()
