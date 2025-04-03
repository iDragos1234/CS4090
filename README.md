# CS4090 Quantum Communication and Cryptography Project

## Entanglement Distillation Protocols:

For this project, we implemented the following four entanglement distillation protocols:
1. __DEJMPS__;
2. __EPL__;
3. __BBPSSW__;
4. __Three-to-one__;

We will use only __depolarizing noise__, with only two possible sources of noise:
* __Entangle state noise__;
* __Gate noise__.


## Entangled gate noise:

* To perform distillation, Alice and Bob must share entangled pairs.

* These pairs are assumed to be __Werner states__ (always):
$$ \rho_{AB}(p) = p \vert\phi_{00}\rangle \langle\phi_{00}\vert + \frac{1 - p}{4} \mathbb{I}_4 $$
where $\vert\phi_{00}\rangle = \frac{1}{\sqrt{2}} \left( \vert00\rangle + \vert11\rangle \right)$.

* A Werner state is a Bell state subject to a depolarizing channel of parameter $p$.


## Gate noise

* 