# Example commands for equipment on pulse NMR system
#
# Code by Adam Jaros, a 451 student in spring 2025

# Power supply for magnet
# -----------------------
gpid.addr(power_supply_addr)
gpib('output:state 1') # Enable

def set_current(current):
    #gpib('output:state 0')
    gpib(f'current {current}')
    gpib('voltage max')
    gpib('output:state 1')


# Delay generator
gpid.addr(delay_gen)
gpib(f'DLAY 3,2,{time_delay}') # Delay between A and B (first pulse width) in seconds
gpib(f'DLAY 4,3,{time_delay}') # Delay between B and C (time between pulses) in seconds

