import labrad
from labrad.units import WithUnit
with labrad.connect() as cxn:
    duration = WithUnit(100, 'ms')
    pulser = cxn.pulser
    pulser.new_sequence()
    channels = pulser.get_channels()
    channel_names = [chan[0] for chan in channels]
    
    #print channel_names
    
#     for i in range(len(channels)):
#         start = i * duration
#         pulser.add_ttl_pulse((channel_names[i],  start , duration))
    period = WithUnit(0.05,'ms')
    pulsed_length = WithUnit(80,'ns')
    for i in range(500):
        #print i
        pulser.add_ttl_pulse('ttl_0',(i+1)*period,pulsed_length)
    #pulser.add_ttl_pulse('ttl_0',WithUnit(0,'ms'),WithUnit(250,'ms'))
    #pulser.add_ttl_pulse('ttl_0',WithUnit(500,'ms'),WithUnit(250,'ms'))
    #pulser.add_ttl_pulse('ttl_0',WithUnit(1000,'ms'),WithUnit(250,'ms'))
    #pulser.add_ttl_pulse('ttl_0',WithUnit(1500,'ms'),WithUnit(250,'ms'))
    

    pulser.program_sequence()
    for j in range(200):
        print j
        pulser.start_number(1000)
        pulser.wait_sequence_done()
        pulser.stop_sequence()