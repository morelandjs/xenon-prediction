#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np


def cross_section_fit(x):
    """
    Polynomial fit to the inelastic nucleon-nucleon
    cross section as a function of log(sqrts)

    """
    cross_sections = [
        (0.20, 4.23),
        (2.76, 6.40),
        (5.02, 7.00),
        (7.00, 7.32),
    ]

    sqrts, sigma_inel = zip(*cross_sections)
    coeff = np.polyfit(np.log(sqrts), sigma_inel, 2)

    return np.polyval(coeff, x)


def dNchdeta_fit(x):
    """
    Power law fit to Pb+Pb dNch/deta
    in 0-10% centrality using 2.76 and 5.02 TeV
    data.

    """
    dNchdeta_central = [
        (2.76, 1447.5),
        (5.02, 1764.0),
    ]

    (x0, F0), (x1, F1) = dNchdeta_central

    # see https://en.wikipedia.org/wiki/Log-log_plot
    return F0*(x/x0)**(np.log(F1/F0)/np.log(x1/x0))

def entropy_norm():
    """
    Determine Trento entropy normalization at 5.44 TeV
    from experimental data and Bayesian calibration at
    2.76, 5.02 TeV.

    """
    fig = plt.figure(figsize=(6, 4.5))

    dNchdeta_central = [
        (2.76, 1447.5),
        (5.02, 1764.0),
    ]

    # plot dNch/deta 0-10% fit function
    x = np.linspace(2, 8, 100)
    plt.plot(x, dNchdeta_fit(x))

    # plot dNch/deta measurements
    for measurement in dNchdeta_central:
        plt.plot(*measurement, 'o', label=' ')

    # plot dNch/deta Xe+Xe 5.44 TeV prediction
    plt.plot(5.44, dNchdeta_fit(5.44), 'o', mfc='white', label=' ')

    # plot trento predictions
    handles, labels = plt.gca().get_legend_handles_labels()
    for n, s_gev in enumerate([2760, 5020, 5440]):

        s_tev = s_gev/1000.
        fname = 'trento/PbPb{}.dat'.format(s_gev)

        minbias_mult = np.loadtxt(fname, usecols=(3,))
        mult = np.sort(minbias_mult)[-1000:].mean()
        norm = dNchdeta_fit(s_tev)/mult

        plt.annotate(
            '{} TeV'.format(s_tev),
            xy=(s_tev + .1, dNchdeta_fit(s_tev)),
            xycoords='data', ha='left', va='top'
        )

        labels[n] = '{0:.2f} [arb]'.format(norm)

    plt.xlabel(r'$\sqrt{s_\mathrm{NN}}$ [TeV]')
    plt.ylabel(r'$(dN_\mathrm{ch}/d\eta)(0–10\%)$')
    plt.title('Trento energy dependence')

    legend = plt.legend(handles, labels, title='Pb+Pb norm')
    for t in legend.get_texts():
        t.set_ha('right')
        t.set_position((50, 0))

    plt.savefig('entropy_norm.pdf')


def xenon_cross_section():
    """
    Extrapolate Xe+Xe 5.44 TeV cross section
    from experimental cross section measurements
    at other beam energies.

    """
    # figure size
    fig = plt.figure(figsize=(6, 4.5))

    # experimental cross sections
    cross_sections = [
        (0.20, 4.23),
        (2.76, 6.40),
        (5.02, 7.00),
        (7.00, 7.32),
    ]

    sqrts, sigma_inel = zip(*cross_sections)
    plt.plot(np.log(sqrts), sigma_inel, 'o', zorder=1)

    # plot fit
    x = np.linspace(-2, 3, 100)
    plt.plot(x, cross_section_fit(x), zorder=0)

    # predict xenon
    xenon_sqrts = 5.44
    xenon_sigma_inel = cross_section_fit(np.log(xenon_sqrts))
    plt.plot(np.log(xenon_sqrts), xenon_sigma_inel, 'o', zorder=1) 

    plt.xlabel(r'$\log(\sqrt{s_\mathrm{NN}})$')
    plt.ylabel(r'$\sigma_\mathrm{NN}^\mathrm{inel}$')

    label = ''.join([
        r'$\sigma_\mathrm{NN}^\mathrm{inel}$',
        r'$={0:.2f}$ fm$^2$'.format(xenon_sigma_inel)
    ])

    plt.annotate(
        label, xy=(np.log(xenon_sqrts), xenon_sigma_inel),
        xycoords='data', ha='left', va='top'
    )

    plt.title(r'Xe+Xe, $\sqrt{s_\mathrm{NN}}=5.44$ TeV cross section')
    plt.tight_layout()

    plt.savefig('cross_section.pdf')


def main():
    """
    Determine Trento entropy normalization and increase in cross section
    for Xe+Xe collisions at 5.44 TeV

    """
    entropy_norm()
    xenon_cross_section()


if __name__ == "__main__":
    main()
