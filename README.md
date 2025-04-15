# CS4090 Quantum Communication and Cryptography: Programming Project


## How to run NetQASM simulations

Change directory to the folder of the protocol you want to run, e.g., DEJMPS:

> ```~$ cd ~/CS4090/project/dejmps```

Simulate a single run of the protocol by running the following command in the protocol folder, e.g., DEJMPS:

> ```~/CS4090/project/dejmps$ netsquid simulate```

To sweep over the parameter grid, a corresponding python script is provided the folder of each protocol. To run the parameter sweep, execute the following command in the protocol folder, e.g., DEJMPS:

> ```~/CS4090/project/dejmps$ python3 run_dejmps.py```

The ranges of the parameter sweeps and the number of _samples_ (i.e., number of single runs of the NetQASM implementation of the protocol) can be changed directly in the `run_[YOUR_PROTOCOL_NAME].py` file (e.g., `run_dejmps.py`). This python script also provides a fail safety, which attempts a given number of times to generate a single sample, in the case that a run of the NetQASM simulation fails. The parameter specifying this maximum number of attempts can be changed in the same file.


## Distillation protocols

Entanglement distillation protocols provided in this project:
1. DEJMPS;
2. EPL;
3. BBPSSW;
4. Three-to-one

We used only __depolarizing noise__, originating from only two possible sources of noise:
* __Entangle state noise__;
* __Gate noise__.


### Entangled gate noise:
* To perform distillation, Alice and Bob must share entangled EPR (Einstein-Podolsky-Rosen) pairs.

* These EPR pairs are assumed to be __Werner states__ (always), wherein a depolarizing channel of parameter $p$ is applied to the pure Bell state $\vert\phi_{00}\rangle = \frac{1}{\sqrt{2}} \left( \vert00\rangle + \vert11\rangle \right)$:
$$
\begin{equation}
  \rho_{AB}(p) = p \vert\phi_{00}\rangle \langle\phi_{00}\vert + \frac{1 - p}{4} \mathbb{I}_4.
\end{equation}
$$


### Gate noise

* Unitary operations used during distillation are assumed to be noisy gates and are modelled by a depolarizing channel of parameter $g$ taking effect after applying the pure version of the unitary:
$$
\begin{equation}
  U_\text{noisy} \rho_{AB} U_\text{noisy}^\dagger = g U \rho_{AB} U^\dagger + \frac{1 - g}{d} \mathbb{I}_d.
\end{equation}
$$
where $d$ is the dimension of the state space.


## NumPy simulations

In addition to NetQASM implementations of the aforementioned distillation protocols, we provide implementations of the four distillation schemes using our own library of quantum operations, amongst which Pauli gates and single qubit rotations, a few two-qubit gates and trace-preserving operations (e.g., depolarizing channel, partial trace, POVM). For this, we made of use of solely Python and NumPy code.

 
