peaks = [2*x+65 for x in range(10)]
print(peaks)
peak_every = 9
low = 40
hold = 50

ramp = []
peak_ndx = 0
for index, x in enumerate(range(99)):
    if not index % peak_every and peak_ndx < len(peaks):
        ramp.append(peaks[peak_ndx])
        peak_ndx += 1
    else:
        ramp.append(low)


ramp.append(hold)



print(ramp)
