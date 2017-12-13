# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 17:45:03 2017

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
    
cdef class EuropeanBinomialEngine(BinomialEngine):
    cdef double calculate(self, Option option, MarketData data):
        cdef double expiry = option.expiry
        cdef double strike = option.strike
        cdef double spot = data.spot
        cdef double rate = data.rate
        cdef double vol = data.vol
        cdef double div = data.div
        cdef double dt = expirty / self._nsteps
        cdef double u = cexp(((rate - div) *dt) + vol * csqrt(dt))
        cdef double d = cexp(((rate - div) * dt) - vol * csqrt(dt))
        cdef double pu = (cexp((rate - div) * dt) - d) / (u - d)
        cdef double pd = 1.0 - pu
        cdef double df = cexp(-rate * expiry)
        cdef double spot_t = 0.0
        cdef double payoff_t = 0.0
        cdef unsigned long nodes = self._nsteps + 1
        cdef unsigned long i
        
        for i in range(nodes):
            spot_t = spot * (u ** (self._nsteps - i)) * (d ** i)
            payoff_t += option.payoff(spot_t) * dbinom(self._nsteps - i, self._nsteps, pu_)
            
        return df * payoff_t
    
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
theEngine = EuropeanBinomialEngine(steps)
option1 = OptionFacade(theCall, theEngine, data)
option2 = OptionFacade(thePut, theEngine, data)

print("The call price is: {0:0.3f}".format(option1.price()))
print("The put price is : {0:0.3f}".format(option2.price()))
