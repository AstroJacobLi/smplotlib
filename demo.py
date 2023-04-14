import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import smplotlib

data = np.load('./src/test_data/test_array.npy')
Pr = data[0]
Teqs = data[1]

fig, ax = plt.subplots(figsize=(5.5, 5.5))

plt.plot(Pr[(Teqs > 5e3)], Teqs[(Teqs > 5e3)], c='k', lw=1, ls='-')
plt.plot(Pr[(Teqs < 1.8e2)], Teqs[(Teqs < 1.8e2)], c='k', lw=1, ls='-')
flag = (Teqs < 1.8e2) | (Teqs > 5e3)
plt.plot(Pr[~flag], Teqs[~flag], c='k', lw=1, ls='--')#, dashes=(6, 2.5))

plt.xlabel(r'$p/k$ (cm$^{-3}$ K)', fontsize=15, labelpad=-4)
plt.ylabel(r'$T$ (K)', fontsize=15, labelpad=2)

plt.text(0.85e3, .57e4, 'stable (WNM)', ha='center', va='center', fontsize=13, rotation=-3)

plt.text(0.85e4, 0.38e2, 'stable (CNM)', ha='center', va='center', fontsize=13, rotation=-10)

plt.text(0.7e3, 5e2, 'Net Heating', ha='center', va='center', fontsize=17)
plt.text(6e3, 5e2, 'Net Cooling', ha='center', va='center', fontsize=17)

plt.text(0.72e3, 1e2, r'$\xi_{\rm CR} = 1\times 10^{-16}$ s$^{-1}$', ha='center', va='center', fontsize=16)
plt.text(0.72e3, 0.72e2, r'MMP83 ISRF', ha='center', va='center', fontsize=14)
plt.text(0.72e3, 0.55e2, r'($\chi=1.231$)', ha='center', va='center', fontsize=14)
plt.text(0.72e3, 0.4e2, r'WD01 p.e. heating', ha='center', va='center', fontsize=14)


plt.axvline(5.05e3, 0.11, 1, ls=':', c='k', lw=0.5, dashes=(2, 4))
plt.text(5.12e3, 0.22e2, '5050', rotation=90, ha='center', va='top')
plt.axvline(1.57e3, 0.11, 1, ls=':', c='k', lw=0.5)
plt.text(1.62e3, 0.22e2, '1570', rotation=90, ha='center', va='top')

ax.annotate(None, xy=(2.7e3, 3e3), xytext=(2.7e3, 1.5e3),
            arrowprops={'arrowstyle': '->'}, va='center')
ax.annotate(None, xy=(2.7e3, 0.5e3), xytext=(2.7e3, 1e3),
            arrowprops={'arrowstyle': '->'}, va='center')
ax.annotate('unstable', xy=(2.5e3, 1.1e3), xytext=(1.2e3, 2e3),
            arrowprops={'arrowstyle': '->'}, va='center', fontsize=13)

plt.loglog()


plt.xlim(0.3e3, 1.4e4)
plt.ylim(0.1e2, 1e4)

plt.savefig('./two_phase.png', bbox_inches='tight', dpi=100)