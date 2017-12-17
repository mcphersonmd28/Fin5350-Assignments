import numpy as np
from scipy.stats import norm
import time 
 
class ExoticOption(object):
        def __init__(self, strike, expiry):
            self.strike = strike
            self.expiry = expiry
        def value(self,spot):
            pass
       
class FixedStrikeLookBackCallOption(ExoticOption):
        def value(self, spot):
            max = np.maximumm(spot - self.strike, 0.0)
            return max
       
class FixedStrikeLookBackPutOption(ExoticOption):
        def value(self, spot):
            max = np.maximum(self.strike - spot, 0.0)
            return max
           
def value(strike, spot):
    max = np.maximum(strike - spot, 0.0)
    return max

def se(r,T,M):
    sum_CT = 0
    sum_CT2 = 0
    sd = np.sqrt((sum_CT2 - sum_CT * sum_CT/M) * np.exp(-2 * r * T)/(M-1))
    se = sd/np.sqrt(M)
    return se
 
def BlackScholesCall(S, K, r, v, q, tau):
    d1 = (np.log(S/K) + (r - q + 0.5 * v * v) * tau / (v * np.sqrt(tau)))
    d2 = d1 - v * np.sqrt(tau)
    callPrc = (S * np.exp(-q * tau) * norm.cdf(d1)) - (K * np.exp(-r * tau) * norm.cdf(d2))
    return callPrc
 
def BlackScholesDelta(S, K, r, v, q, tau):
    d1 = (np.log(S/K) + (r - q + 0.5 * v * v) * tau) / (v * np.sqrt(tau))
    delta = np.exp(-q * tau) * norm.cdf(d1)
    return delta 
     
def CVMonteCarloPricer(K, T, S, v, r, q, N, M):
    dt = T/N
    nudt = (r - q - 0.5 * (v * v)) * dt
    sigsdt = v * np.sqrt(dt)
    erddt = np.exp((r - q) * dt)
    c_t = np.empty(M)
    St = np.empty(N)
    cv = np.empty(N)
    beta1 = -1
    sum_CT = 0
    sum_CT2 = 0
    
    for j in range(1, M):
        z = np.random.normal(size = int(N/2))
        z = np.concatenate((z,-z))
        St[0] = S
        cv[0] = 0
       
        for i in range(1, N):
            tau = (i - 1) * dt
            delta = BlackScholesDelta(St[i], K, v, r, q,tau)
            Stn = St[i] * np.exp(nudt + sigsdt * z[i])
            cv[i] = cv[i-1] + delta*(Stn-St[i]*erddt)
        x = cv.mean()
        c_t[j] = value(K, np.max(St)) + beta1 * x
        sum_CT = sum_CT + CT
        sum_CT2 = sum_CT2 + CT * CT
           
    call_value = c_t.mean() * np.exp(-r * T)
    return call_value

    SD = np.sqrt((sum_CT2 - sum_CT * sum_CT/M) * np.exp(-2 * r * T)/(M-1))
    SE = SD/np.sqrt(M)
    
def main():
    start = time.time()
    K = 100
    T = 1
    S = 100
    v = 0.20
    r = 0.06
    q = 0.03
    M = 1000
    N = 52
    callPrc = BlackScholesCall(S, K, r, v, q, T)
    callDelta = BlackScholesDelta(S, K, r, v, q, T)
    end = time.time()
    print("The time to run is: {0:0.10f}".format(end-start)) 
    print("The Call Price is: {0:0.3f}".format(callPrc))
    print("The Call Delta is: {0:0.3f}".format(callDelta))
    stdErr = se(r,T,M)
    print("The Standard Error is: {0:0.3f}".format(stdErr))
   
main()


