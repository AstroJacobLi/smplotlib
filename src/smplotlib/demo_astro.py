import numpy as np
import matplotlib.pyplot as plt
import smplotlib
from scipy.special import gamma

def plot_cmb_simulation():
    """
    Simulate a CMB-like sky map using a Gaussian Random Field.
    """
    np.random.seed(42)
    N = 256
    
    # Generate a power spectrum P(k) ~ 1/k^2 (scale invariant-ish for visual)
    # or slightly more peaked for CMB acoustic peaks look
    k = np.fft.fftfreq(N) * N
    kx, ky = np.meshgrid(k, k)
    k_mag = np.sqrt(kx**2 + ky**2)
    k_mag[0,0] = 1e-10 # Avoid division by zero
    
    # CMB Power spectrum approximation for visual purposes
    # P(k) with some peaks
    P_k = 1.0 / (k_mag**2.5 + 1e-5) * (1 + 0.5 * np.sin(k_mag/10)**2)
    
    # Generate random noise in Fourier space
    noise = np.random.normal(size=(N, N)) + 1j * np.random.normal(size=(N, N))
    
    # Apply power spectrum
    map_k = noise * np.sqrt(P_k)
    
    # Inverse FFT to get real space map
    cmb_map = np.real(np.fft.ifft2(map_k))
    
    # Normalize to microKelvin range approx +/- 200 uK
    cmb_map = (cmb_map - np.mean(cmb_map)) / np.std(cmb_map) * 200
    
    fig, ax = plt.subplots(figsize=(7, 5.5))
    
    # Plot with jet colormap (default)
    im = ax.imshow(cmb_map, extent=[-10, 10, -5, 5], origin='lower', cmap='jet', aspect='auto')
    
    cbar = fig.colorbar(im, ax=ax, label=r'$\Delta T$ ($\mu$K)')
    
    ax.set_xlabel('Galactic Longitude (deg)')
    ax.set_ylabel('Galactic Latitude (deg)')
    ax.set_title('Simulated WMAP CMB Sky Map')
    
    # Grid for that map feel
    ax.grid(True, linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('demo_cmb.png')
    print("Generated demo_cmb.png")

def schechter(M, phi_star, M_star, alpha):
    """
    Schechter Luminosity Function in terms of Magnitude M
    """
    # 0.4 * ln(10) * phi* * 10^(-0.4(M-M*)(alpha+1)) * exp(-10^(-0.4(M-M*)))
    factor = 0.4 * np.log(10) * phi_star
    term1 = 10**(-0.4 * (M - M_star) * (alpha + 1))
    term2 = np.exp(-10**(-0.4 * (M - M_star)))
    return factor * term1 * term2

def plot_luminosity_function():
    """
    Plot Galaxy Luminosity Function for different redshifts.
    """
    np.random.seed(42)
    M = np.linspace(-24, -16, 100)
    
    # Parameters for different redshifts (mock values)
    # z, phi_star, M_star, alpha
    params = [
        (0.1, 1.6e-2, -20.8, -1.2), # z=0.1 (Black)
        (0.5, 1.0e-2, -20.9, -1.25), # z=0.5 (Red)
        (1.0, 0.6e-2, -21.0, -1.3), # z=1.0 (Blue)
        (2.0, 0.3e-2, -21.2, -1.35), # z=2.0 (Green)
        (3.0, 0.1e-2, -21.5, -1.4), # z=3.0 (Cyan)
    ]
    
    fig, ax = plt.subplots(figsize=(5.5, 5.5))

    for i, (z, phi_s, M_s, alpha) in enumerate(params):
        # Theoretical line
        phi = schechter(M, phi_s, M_s, alpha)
        line, = ax.plot(M, phi, label=f'z = {z}', linewidth=2)
        
        # Mock data points with scatter
        # Sample some magnitudes
        M_data = np.linspace(-23.5, -17, 10)
        phi_data = schechter(M_data, phi_s, M_s, alpha)
        
        # Add noise (log-normal scatter)
        noise = np.random.normal(0, 0.15, size=len(M_data))
        phi_data_noisy = phi_data * 10**noise
        
        # Error bars
        yerr = phi_data_noisy * 0.2 # 20% error
        
        # Plot scatter points with same color as line
        ax.errorbar(M_data, phi_data_noisy, yerr=yerr, fmt='o', color=line.get_color(), 
                    markersize=5, capsize=3, elinewidth=1)

    ax.set_yscale('log')
    ax.set_xlabel(r'$M_{UV}$ (Magnitude)')
    ax.set_ylabel(r'$\phi(M)$ (Mpc$^{-3}$ mag$^{-1}$)')
    ax.set_title('Galaxy Luminosity Function')
    ax.legend(loc='lower left', frameon=False)
    
    # Invert x axis for magnitudes
    ax.invert_xaxis()
    
    plt.tight_layout()
    plt.savefig('demo_lf.png')
    print("Generated demo_lf.png")

if __name__ == "__main__":
    plot_cmb_simulation()
    plot_luminosity_function()
