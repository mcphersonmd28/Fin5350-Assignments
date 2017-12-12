import numpy as np
from scipy.stats import binom

class VanillaPayoff(object):
    def __init__(self, strike, expiry):
        self.strike = strike
        self.expiry = expiry
        
    def value(self):
        pass
    
class VanillaCallPayoff(VanillaPayoff):
    def value(self, spot):
        return np.maximum(spot-self.strike,0.0)
    
class VanillaPutPayoff(VanillaPayoff):
    def value(self, spot):
        return np.maximum(self.strike-spot, 0.0)

def AmericanBinomialPricer(VanillaPayoff, spot, rate, div, vol, steps):
    nodes = steps + 1
    spotT = 0.0
    callT = 0.0
    dt = T/steps
    u = np.exp(((rate - div) * dt) + vol * np.sqrt(dt))
    d = np.exp(((rate - div) * dt) - vol * np.sqrt(dt))
    pu = (np.exp((rate - div) * dt) - d) / (u - d)
    pd = 1 - pu
    disc = np.exp(-rate * dt)
    dpu = disc * pu
    dpd = disc * pd
    
    callT = np.zeros(nodes)
    spotT = np.zeros(nodes)
    
    for i in range(nodes):
        spotT[i] = spot * (u ** (steps - i)) * (d ** (i))
        callT[i] = VanillaPayoff.value(spotT[i])
    
    for i in range((steps - 1), -1, -1):
        for j in range(i + 1):
            callT[j] = dpu * callT[j] + dpd * callT[j + 1]
            spotT[j] = spotT[j] / u
            callT[j] = np.maximum(callT[j], VanillaPayoff.value(spotT[j]))
    
    return callT[0]

spot = 41.0
K = 40.0
rate = 0.08
vol = 0.30
div = 0.0
T = 1.0
steps = 3

theCall = VanillaCallPayoff(K, T)
callPrice = AmericanBinomialPricer(theCall, spot, rate, div, vol, steps)
print("The price of the call is :", (callPrice))

thePut = VanillaPutPayoff(K, T)
putPrice = AmericanBinomialPricer(thePut, spot, rate, div, vol, steps)
print("The price of the put is :", (putPrice))