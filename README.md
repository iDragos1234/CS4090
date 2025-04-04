# CS4090 Quantum Communication and Cryptography: Programming Project


## How to run

Change directory to the folder of the protocol you want to run, e.g., DEJMPS:

> ```cd ~/CS4090/project/dejmps```

Simulate the protocol by running the following command in the DEJMPS folder:

> ```netsquid simulate```


## Distillation Protocols

In this project, we provide implementations for the following four entanglement distillation protocols:
1. DEJMPS;
2. EPL;
3. BBPSSW;
4. Three-to-one

We will use only __depolarizing noise__, originating from only two possible sources of noise:
* __Entangle state noise__;
* __Gate noise__.


### Entangled gate noise:
* To perform distillation, Alice and Bob must share entangled pairs.

* These pairs are assumed to be __Werner states__ (always):
$$ \rho_{AB}(p) = p \vert\phi_{00}\rangle \langle\phi_{00}\vert + \frac{1 - p}{4} \mathbb{I}_4 $$
where $\vert\phi_{00}\rangle = \frac{1}{\sqrt{2}} \left( \vert00\rangle + \vert11\rangle \right)$.

* A Werner state is a Bell state subject to a depolarizing channel of parameter $p$.

### Gate noise
[placeholder]
