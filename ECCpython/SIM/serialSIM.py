import numpy as np
import matplotlib.pyplot as plt
from ecc import ECC
from TurboCodes.serial import Serial
from BlockCodes.spc import SPC

"""
    Simulation of SPC3 and SPC4 serial turbo code
"""

S3 = SPC(3)
S4 = SPC(4)

SS = Serial(S3, S4)
SS.set_interleaver('block', 3, 4)

Rc_dB = 10 * np.log10(SS.Rc)
u_len = 9
depth = 100
SNR_range = np.arange(-10, 10, 1)
error = np.zeros((depth, len(SNR_range)))

for loop in range(depth):
    for i, SNR_dB in enumerate(SNR_range):
        u = np.random.randint(2, size=u_len)
        x = SS.transmit(u)

        # channel
        SNR_lin = 10 ** (SNR_dB / 10)
        mu, sigma = 0, np.sqrt(1 / SNR_lin)
        w = np.random.normal(mu, sigma, size=len(x))

        y = x + w
        u_ = SS.receive(y, SNR_dB, iterations=5)

        error[loop, i] = np.count_nonzero(u_ - u)
    error_rate = np.mean(error, axis=0) / u_len

"""
    Simulation of RSC and RSC serial codes
"""

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.semilogy(SNR_range, error_rate)
ax1.set_xlabel('$E_s/N_0(dB)$')
ax1.set_ylabel('Symbol Error Rate ($P_s$)')
ax1.set_title('Probability of Symbol Error over AWGN channel')
ax1.set_xlim(SNR_range[0] - 1, SNR_range[-1] + 1)
ax1.grid(True)
ax2.semilogy(SNR_range - Rc_dB, error_rate)
ax2.set_xlabel('$E_b/N_0(dB)$')
ax2.set_ylabel('Bit Error Rate ($P_b$)')
ax2.set_title('Probability of Bit Error over AWGN channel')
ax2.set_xlim(SNR_range[0] - 1 - Rc_dB, SNR_range[-1] + 1 - Rc_dB)
ax2.grid(True)
plt.show()
