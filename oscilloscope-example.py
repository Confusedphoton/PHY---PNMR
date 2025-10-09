# Example code to read data from a Tektronix oscilloscope
# Requires the pyvisa package
#
# Code written by Adam Jaros, a 451 student in spring 2025

import pyvisa

# Oscilloscope IP Address
OSCILLOSCOPE_IP = "35.15.225.124"  # Change if needed

# Connect to oscilloscope
rm = pyvisa.ResourceManager('@py')
oscilloscope = rm.open_resource(f"TCPIP::{OSCILLOSCOPE_IP}::INSTR")

# Set communication parameters
oscilloscope.timeout = 5000  # 5 seconds
oscilloscope.write_termination = '\n'
oscilloscope.read_termination = '\n'

# Get waveform parameters
ymult = float(oscilloscope.query("WFMPRE:YMULT?"))
yoff = float(oscilloscope.query("WFMPRE:YOFF?"))
yzero = float(oscilloscope.query("WFMPRE:YZERO?"))
xzero = float(oscilloscope.query("WFMPRE:XZERO?"))
time_scale = float(oscilloscope.query("HORizontal:SCAle?"))
t_offset = int(-1 * float(oscilloscope.query("WFMPRE:xzero?")) / float(oscilloscope.query("WFMPRE:XINCR?")))

# Set up acquisition parameters
oscilloscope.write("DATa:STOP 10000")
oscilloscope.write("ACQuire:NUMAVg 512") # max averaging


# Return a waveform from the oscilloscope after clearing any old data
# and then waiting for data_wait seconds (useful to allow averaging to converge)
def read_scope(data_wait=1):
    # restart acquisition
    oscilloscope.write("ACQuire:STATE 0")
    oscilloscope.write("ACQuire:STATE 1")
    # Read data from oscilloscope
    time.sleep(data_wait)
    oscilloscope.write("CURVE?")
    data = oscilloscope.read_raw()
    data = np.frombuffer(data, dtype=np.int8)
    data = yzero + ymult * (data - 128)
    return data


