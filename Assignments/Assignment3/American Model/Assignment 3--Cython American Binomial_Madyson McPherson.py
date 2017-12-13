# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:07:26 2017

@author: maddi
"""
import numpy as np
cimport numpy as np
from scipy.stats import binom

cdef class OptionFacade:
    def__init__(self, option, engine, data):
        self._option = option
        self._engine = engine
        self._data = data
    cpdef price(self):
        return self._engine.calculate(self._option, self._data)

cdef class VanillaPayoff:
    def__init__(self, strike, expiry):
        self._strike = strike
        self._expiry = expirty
    cdef double value(self):
        pass

cdef class VanillaCallPayoff(VanillaPayoff):
    cdef double value(self, spot):
        return np.maximum(spot-self._strike, 0.0)

cdef class VanillaPutPayoff(VanillaPayoff):
    cdef double value(self, spot):
        return np.maximum(self._strike - spot, 0.0)

cdef class MarketData:
    def__init__(self, spot, rate, vol, div):
        self._spot = spot
        self._rate = rate
        self._vol = vol
        self._div = div

cdef class Option:
    def__init__(self, expiry, payoff):
        self._expiry = expiry
        self._payoff= payoff
    cpdef payoff(self, double spot):
        return self._payoff.payoff(spot)
    
cdef class PriceEngine:
    cdef double calculate(self, Option option, MarketData data):
        pass

cdef class BinomialEngine(PriceEngine):
    def__init__(self, nsteps):
        self._nsteps = nsteps
    
    cdef double calculate(self, Option option, MarketData data):
        pass
    

#everywhere the binomial can go the american engine can go
#cythonize the American python code
cdef class AmericanBinomialEngine(BinomialEngine):
    cdef double calculate(self, Option option, MarketData data):
        cdef double dt = option.expiry / self._nsteps
        cdef double u = np.exp((data.rate - data.div) * dt + data.vol * np.sqrt(dt))
        cdef double d = np.exp((data.rate - data.div) * dt - data.vol * np.sqrt(dt))
        cdef double pu = (np.exp((data.rate - data.div) * dt) - d) / (u - d)
        cdef double pd = 1.0 - pu
        cdef double disc = np.exp(-data.rate *dt)
        cdef double dpu = disc * pu
        cdef double dpd = disc * pd
        cdef unsigned long numNodes = self._nsteps + 1
        cdef double[::1] spot_t = np.empty(numNodes, dtype=np.float64)
        cdef double[::1] call_t = np.empty(numNodes, dtype=np.float64)
        cdef unsigned long i, j
        
        for i in range(numNodes):
            spot_t[i] = data.spot * cpow(u, self._nsteps - i) * cpow(d, i)
            call_t[i] = option.payoff(spot_t[i])
        
        for i in range(self._nsteps - 1, -1, -1):
            for j in range(i +1):
                call_t[j] = dpu * call_[j] + dpd * call_t[j+1]
                spot_t[j] = spot_t[j] / u
                call_t[j] = np.maximum(call_t[j], option.payoff(spot_t[j]))
                
        return call_t[0]

strike = 40.0
spot = 41.0
rate = 0.08
vol = 0.30
div = 0.0
steps = 500
reps = 5000

data = MarketData(spot, rate, vol, div)
theCall = Option(1.0, VanillaCallPayoff(strike))
thePut = Option(1.0, VanillaPutPayoff(strike))
theEngine = AmericanBinomialEngine(steps)
option1 = OptionFacade(theCall, theEngine, data)
option2 = OptionFacade(thePut, theEngine, data)

print("The call price is: {0:0.3f}".format(option1.price()))
print("The put price is : {0:0.3f}".format(option2.price()))
