#!/usr/bin/env python3

import argparse
import logging
import os

import matplotlib.pyplot as plt
import numpy as np


aspect = 1/1.618
resolution = 72.27
columnwidth = 246/resolution
textwidth = 510/resolution
textiny, texsmall, texnormal = 8.0, 9.25, 10.0
offblack = '#262626'

plt.rcdefaults()
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['CMU Serif'],
    'mathtext.fontset': 'cm',
    'font.size': texsmall,
    'legend.fontsize': texsmall,
    'axes.labelsize': texsmall,
    'axes.titlesize': texsmall,
    'xtick.labelsize': textiny,
    'ytick.labelsize': textiny,
    'font.weight': 400,
    'axes.labelweight': 400,
    'axes.titleweight': 400,
    'lines.linewidth': .9,
    'lines.markersize': 3,
    'lines.markeredgewidth': .1,
    'patch.linewidth': .9,
    'axes.linewidth': .5,
    'xtick.major.width': .5,
    'ytick.major.width': .5,
    'xtick.minor.width': .5,
    'ytick.minor.width': .5,
    'xtick.major.size': 2,
    'ytick.major.size': 2,
    'xtick.minor.size': 1.3,
    'ytick.minor.size': 1.3,
    'xtick.major.pad': 1.8,
    'ytick.major.pad': 1.8,
    'text.color': 'black',
    'axes.edgecolor': 'black',
    'axes.labelcolor': 'black',
    'xtick.color': 'black',
    'ytick.color': 'black',
    'legend.numpoints': 1,
    'legend.scatterpoints': 1,
    'legend.frameon': False,
    'image.interpolation': 'none',
    'pdf.fonttype': 42,
})


plot_functions = {}


def plot(f):
    os.makedirs('plots', exist_ok=True)
    def wrapper(*args, **kwargs):
        print(f.__name__)
        f(*args, **kwargs)
        plt.savefig('plots/{}.pdf'.format(f.__name__))
        plt.close()

    plot_functions[f.__name__] = wrapper

    return wrapper


def finish(despine=True, remove_ticks=False, pad=0.1, h_pad=None, w_pad=None,
           rect=[0, 0, 1, 1]):
    fig = plt.gcf()

    for ax in fig.axes:
        if despine:
            for spine in 'top', 'right':
                ax.spines[spine].set_visible(False)

        if remove_ticks:
            for ax_name in 'xaxis', 'yaxis':
                getattr(ax, ax_name).set_ticks_position('none')
        else:
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')

    fig.tight_layout(pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)


def auto_ticks(ax, axis='both', minor=False, **kwargs):
    """
    Convenient interface to matplotlib.ticker locators.

    """
    axis_list = []

    if axis in {'x', 'both'}:
        axis_list.append(ax.xaxis)
    if axis in {'y', 'both'}:
        axis_list.append(ax.yaxis)

    for axis in axis_list:
        axis.get_major_locator().set_params(**kwargs)
        if minor:
            axis.set_minor_locator(ticker.AutoMinorLocator(minor))

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


@plot
def entropy_norm():
    """
    Determine Trento entropy normalization at 5.44 TeV
    from experimental data and Bayesian calibration at
    2.76, 5.02 TeV.

    """
    fig = plt.figure(figsize=(columnwidth, aspect*columnwidth))

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
    plt.plot(5.44, dNchdeta_fit(5.44), 'o', mfc='white', mew=.9, label=' ')

    # plot trento predictions
    handles, labels = plt.gca().get_legend_handles_labels()
    for n, s_gev in enumerate([2760, 5020, 5440]):

        s_tev = s_gev/1000.
        fname = 'data/PbPb{}.dat'.format(s_gev)

        minbias_mult = np.loadtxt(fname, usecols=(3,))
        mult = np.sort(minbias_mult)[-1000:].mean()
        norm = dNchdeta_fit(s_tev)/mult

        plt.annotate(
            '{} TeV'.format(s_tev),
            xy=(s_tev + .1, dNchdeta_fit(s_tev)),
            xycoords='data', ha='left', va='top',
            fontsize=textiny
        )

        labels[n] = '{0:.2f} [arb]'.format(norm)

    plt.xlabel(r'$\sqrt{s_\mathrm{NN}}$ [TeV]')
    plt.ylabel(r'$(dN_\mathrm{ch}/d\eta)(0–10\%)$')
    plt.title('Trento energy dependence')

    legend = plt.legend(
        handles, labels, title='Pb+Pb norm', fontsize=textiny
    )

    plt.setp(legend.get_title(), fontsize=textiny)

    for t in legend.get_texts():
        t.set_ha('right')
        t.set_position((30, 0))

    finish()

@plot
def xenon_cross_section():
    """
    Extrapolate Xe+Xe 5.44 TeV cross section
    from experimental cross section measurements
    at other beam energies.

    """
    # figure size
    fig = plt.figure(figsize=(columnwidth, aspect*columnwidth))

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
    finish()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('plots', nargs='*')
    args = parser.parse_args()

    if args.plots:
        for i in args.plots:
            if i.endswith('.pdf'):
                i = i[:-4]
            if i in plot_functions:
                plot_functions[i]()
            else:
                print('unknown plot:', i)
    else:
        for f in plot_functions.values():
            f()


if __name__ == "__main__":
    main()
