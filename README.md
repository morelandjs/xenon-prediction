# LHC Xe+Xe 5.44 TeV predictions

This repository contains predictions for Xenon-Xenon collisions at √s = 5.44 TeV.

## Regenerating figures

The prediction figures are stored in the git repo plots folder for convenience, but they can easily be regenerated.

First make sure the prerequisite Python libraries are installed,
```
pip install -r requirements.txt
```
Then run `python3 -m src.plots` from the git repo directory to regenerate the
prediction figures.

## Figure descriptions

The following documentation describes each of the figures in the `plots` directory.

### Xenon cross section
![alt text](https://github.com/morelandjs/xenon-prediction/blob/master/plots/xenon_cross_section.png =892x551)

The trento initial condition model takes as input the inelastic nucleon-nucleon cross section and an overall entropy normalization factor which should be tuned at each collision beam energy. To make predictions for Xe+Xe collisions at 5.44 TeV, we need to extrapolate their values from previous measurements. 

The inelastic nucleon-nucleon cross section is measured experimentally. We use measurements made at 0.2, 2.76, 5.02 and 7 TeV listed with references on the [trento documentation page](http://qcd.phy.duke.edu/trento/usage.html). The cross section values are then fit with a second order polynomial in log(√s).

We find an inelastic nucleon-nucleon cross section at 5.44 TeV of 7.07 fm<sup>2</sup>.

### Entropy normalization
![alt text](https://github.com/morelandjs/xenon-prediction/blob/master/plots/entropy_norm.png)

In addition to the increasing cross section, we must extrapolate the increase in the normalization factor from 5.02 to 5.44 TeV. 

We start by running three sets of trento initial condition events at 2.76, 5.02 and 5.44 TeV _with the correct inelastic nucleon-nucleon cross section at each beam energy_. We then then use the empirically verified scaling law dNch/dη ≈ norm * dS/dη to find the requisite entropy normalization at each beam energy to reproduce observed particle production at 2.76 and 5.02 TeV.

The two normalization factors, norm(2.76 TeV) and norm(5.02 TeV), are then fit with a power law to predict norm(5.44 TeV). We then convert this scaling normalization into a physical normalization by measuring the ratio norm(5.44 TeV) / norm(5.02 TeV) and using it to scale up our best fit Pb+Pb 5.02 TeV normalization from the combined Bayesian analysis.

This yields a modest ~2% increase in the entropy normalization from 5.02 to 5.44 TeV.

### Observables from maximum posterior density
![alt text](https://github.com/morelandjs/xenon-prediction/blob/master/plots/observables_map.png)

We show self consistent calculations for Pb+Pb collisions at 5.02 TeV and Xe+Xe collisions at 5.44 TeV using model parameters which have been calibrated to fit available data for Pb+Pb collisions at 2.76 and 5.02 TeV. Note that most of the 5.02 Pb+Pb data is missing, and hence our model calculations represent predictions for those observables as well. For observables where the 5.02 and 5.44 TeV measurements are missing, we use the same centrality bins as 2.76 TeV measurements.

The observables are calculated from ~1 million minimum bias Pb+Pb events and ~1.5 million minimum bias Xe+Xe events. The minimum bias events are sorted into centrality bins exactly as done by experiment.

Solid lines show model calculations for 5.02 TeV Pb+Pb collisions and dashed lines model calculations for 5.44 TeV Xe+Xe collisions. The inset at the bottom of each panel is the ratio of 5.44 TeV Xe+Xe to 5.02 TeV Pb+Pb.

### Calculation of (dNch/dη)(Npart/2)
![alt text](https://github.com/morelandjs/xenon-prediction/blob/master/plots/nch_per_npart.png)

We calculate the participant scaled yield (dNch/dη)/(Npart/2) for Pb-Pb collisions at 5.02 TeV using maximum a posteriori parameters (listed below) determined by calibrating the model to fit multiple Pb-Pb collision observables at 2.76 and 5.02 TeV.
We also predict this quantity for Xe-Xe collisions at 5.44 TeV using the same parameters as Pb-Pb at 5.02 TeV, except for a slightly larger normalization to reflect the difference in beam energy.

There is one important quirk in this calculation. 
Strictly speaking, (dNch/dη)/(Npart/2) is *not* a measurable quantity since Npart must be estimated from a model.
The ALICE experimental collaboration uses a specific Monte Carlo Glauber model to calculate their Npart values.
Our calculations use the Trento initial condition model which predicts somewhat different values of Npart compared to the ALICE Glauber model (e.g. see [glauber-attributes](https://github.com/morelandjs/glauber-attributes)).
The difference arises from how nucleons collide in the two models.
In the ALICE Glauber model, nucleons collide if they pass within some maximum distance of each other.
In Trento, nucleons collide with collision probability Pcoll(b) which takes the form of a Gaussian.
It makes little sense to compare (dNch/dη)/(Npart/2) between model and experiment using two different model calculations for Npart, so we reproduce the ALICE Glauber model nucleon interactions for the purpose of calculating Npart in the denominator of our Trento model predictions.

Lastly, it is worth noting that our Pb-Pb postdiction and Xe-Xe prediction are not just fitting (dNch/dη)/(Npart/2), these are the same parameters that fit the global observables discussed in the previous section. 
If, on the other hand, we just want to predict (dNch/dη)/(Npart/2) for Xe-Xe collisions at 5.44 TeV, it would be reasonable to rescale our model calculation using Pb-Pb at 5.02 TeV as a baseline since the overall normalization factor in the model is free to vary anyhow.
We do not plot such a rescaling in the figure, but the rescaled values for (dNch/dη)/(Npart/2) are included in the `predict` directory.

## Physics model

Minimum bias events are generated using the [trento](https://arxiv.org/abs/1412.4708) initial condition model with a pre-equilibrium free streaming stage. The subsequent transport dynamics are then simulated using the [iEBE-VISHNU](https://arxiv.org/abs/1409.8164) hydro + micro model with shear and bulk viscous corrections.

It's worth noting that this version of the physics model is updated compared to the versions shown at Quark Matter 2017 and in previously published work. Namely, significant changes have been made to the particle sampler. These changes have not yet been documented, so please contact Jonah Bernhard for additional information.

## Bayesian parameter estimation

The initial condition and hydro model parameters are chosen using maximum aposteriori (MAP) parameter values from a combined Bayesian analysis of particle yields, mean pT, mean pT fluctuations and multiparticle correlations in Pb+Pb collisions at 2.76 and 5.02 TeV. Specifically, the parameter values are determined by maximizing the posterior probability density of the obtained Bayesian posterior distribution.

We use the same parameter values for both 5.44 TeV Xe+Xe collisions and 5.02 TeV Pb+Pb collisions, _except_ for the initial entropy normalization and inelastic nucleon-nucleon cross section which depend strongly on beam energy as discussed previously.

The shared MAP parameter values are:

| Parameter | Description | Value |
| --------- | ----------- | ------ |
| p         | Entropy deposition parameter | 0.0 |
| k fluct   | Multiplicity fluct. shape | 1.186 |
| d min     | Minimum nucleon distance | 1.267 fm |
| w         | Gaussian nucleon width | 0.956 fm |
| τ-fs      | Free streaming time | 1.162 fm/c |
| η/s min   | Shear viscosity at T<sub>c</sub> | 0.08 |
| η/s slope | Slope above T<sub>c</sub> | 1.113 GeV<sup>-1</sup> |
| η/s curv  | Shear viscosity curvature param | -0.479 |
| ζ/s max   | Cauchy dist. peak height | 0.052 |
| ζ/s width | Cauchy dist. scale | 0.022 GeV |
| ζ/s T0    | Cauchy dist. location | 0.183 GeV |
| T switch  | Particlization temperature | 0.151 GeV |
