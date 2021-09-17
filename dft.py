from numpy import sin as sinus
from numpy import cos as cosinus
from numpy import dot, asfarray, pi, sqrt
twopi = pi * 2

def convertunitstomicrovolts(units):
    return units * 0.0447

def calculateamplitude(sinesum, cosinesum, period):
    temp = sqrt(sinesum ** 2 + cosinesum ** 2)
    return 2 * temp/period


def fivehertzamptransform(values):
    sines = [sinus(twopi * i/100) for i in range(len(values))]
    cosines =  [cosinus(twopi * i/100) for i in range(len(values))]
    sinesum = dot(sines, values)
    cosinesum = dot(cosines, values)
    return convertunitstomicrovolts(calculateamplitude(sinesum, cosinesum, len(values)))

def checknoisetest(values):
    data = convertunitstomicrovolts(max(values) - min(values))
    if data < 6:
        return ['passed', data]
    else:
        return ['FAILED', data]

def checkwithoutR(values):
    data = fivehertzamptransform(values)
    if data > 80 and data < 110:
        return ['passed', data]
    else:
        return ['FAILED', data]

def checkwithR(values):
    data = fivehertzamptransform(values)
    if data > 40 and data < 55:
        return ['passed', data]
    else:
        return ['FAILED', data]

def checkidle(values):
    data = fivehertzamptransform(values[100::])
    if data < 1:
        return ['passed', data]
    else:
        return ['FAILED', data]

def checkdata(testindex, electrodeindex, values):
    if testindex == 0:
        return checknoisetest(values)
    elif (testindex-1)/2 == electrodeindex:
        return checkwithoutR(values)
    elif (testindex-2)/2 == electrodeindex:
        return checkwithR(values)
    else:
        return checkidle(values)    
    

#checking for 100 timepoints, 1 period
def continuoustransform(values, times, deltat):
    firstindex = round(60/deltat)
    times = times[firstindex:]
    values = values[firstindex:]
    sines = asfarray([sinus(5 * twopi * t) for t in times])
    cosines = asfarray([cosinus(5 * twopi * t) for t in times])
    sinesum = dot(sines[:100], values[:100])
    cosinesum = dot(cosines[:100], values[:100])
    amp = calculateamplitude(sinesum, cosinesum, deltat)
    i = 0
    while amp < 95000000:
        sinesum -= sines[i] * values[i]
        cosinesum -= cosines[i] * values[i]
        sinesum += sines[i+100] * values[i+100]
        cosinesum += cosines[i+100] * values[i+100]
        amp = calculateamplitude(sinesum, cosinesum, deltat)
        i += 1
    for k in range(20):
        sinesum -= sines[i] * values[i]
        cosinesum -= cosines[i] * values[i]
        sinesum += sines[i+100] * values[i+100]
        cosinesum += cosines[i+100] * values[i+100]
        amp = calculateamplitude(sinesum, cosinesum, deltat)
        i += 1
    tmp0 = i
    tmp = i + 100
    amplist = []
    while i < tmp:
        sinesum -= sines[i] * values[i]
        cosinesum -= cosines[i] * values[i]
        sinesum += sines[i+100] * values[i+100]
        cosinesum += cosines[i+100] * values[i+100]
        amp = calculateamplitude(sinesum, cosinesum, deltat)
        amplist.append(amp)
        i += 1
    ind = amplist.index(min(amplist))
    return tmp0 + ind




        





