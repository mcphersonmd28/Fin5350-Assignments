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

def EuropeanBinomialPricer(option, spot, rate, div, vol, steps):
    nodes = steps + 1
    spotT = 0.0
    callT = 0.0
    dt = T/steps
    u = np.exp(((rate - div) * dt) + vol * np.sqrt(dt))
    d = np.exp(((rate - div) * dt) - vol * np.sqrt(dt))
    pu = (np.exp((rate - div) * dt) - d) / (u - d)
    pd = 1 - pu
    
    for i in range(nodes):
        spotT = spot * (u ** (steps - i)) * (d ** (i))
        callT += option.value(spotT) * binom.pmf(steps - i, steps, pu)
    
    price = callT * np.exp(-rate*T)
    
    return price

spot = 41.0
K = 40.0
rate = 0.08
vol = 0.30
div = 0.0
T = 1.0
N = 3

theCall = VanillaCallPayoff(K, T)
callPrice = EuropeanBinomialPricer(theCall, spot, rate, div, vol, N)
print("The price of the call is :", (callPrice))

thePut = VanillaPutPayoff(K, T)
putPrice = EuropeanBinomialPricer(thePut, spot, rate, div, vol, N)
print("The price of the put is :", (putPrice))
    