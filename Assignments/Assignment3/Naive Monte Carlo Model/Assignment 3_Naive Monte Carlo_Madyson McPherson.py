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

def NaiveMonteCarloPricer(option, spot, rate, div, vol, steps):
    nodes = steps + 1
    M = 1000000
    spot_t = np.empty((M,))
    call_t = 0.0
    nudt = (rate - div - 0.5 * vol * vol) * T
    sigdt = vol * np.sqrt(T)
    z = np.random.normal(size=(M,))
    disc = np.exp(-rate * dt)
    
    
    spotT = spot * np.exp(nudt + sigdt * z)
    
    #payoffT = option.payoff(spotT)
    #prc = payoffT.mean() * disc
    
    meanCall = call_t.mean()
    put_t = VanillaPutPayoff(spot_t, k)
    meanPut = put_t.mean()
    prc = payoff.mean() * disc
    return prc

spot = 41.0
K = 40.0
rate = 0.08
vol = 0.30
div = 0.0
T = 1.0
N = 3
callPrc = np.exp(-rate * T) * meanCall
putPrc = np.exp(-rate * T) * meanPut

#theCall = VanillaCallPayoff(K, T)
#callPrice = NaiveMonteCarloPricer(theCall, spot, rate, div, vol, steps)
#print("The price of the call is:" , callPrice)

#thePut = VanillaPutPayoff(K,T)
#putPrice = NaiveMonteCarloPricer(thePut, spot rate, div, vol, steps)
#print("The price of the put is:" , putPrice)

callPrc
putPrc