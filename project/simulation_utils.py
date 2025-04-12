import numpy as np
from typing import Literal, List, Set
from functools import reduce


#-------------------------------------------------------------

# Define unitary gates

# Paulis
def I(nstates: int=2):
    return np.asmatrix(np.identity(nstates, dtype=complex))

def X():
    return np.matrix([
        [0, 1],
        [1, 0],
    ], dtype=complex)

def Y():
    return np.matrix([
        [ 0, -1j],
        [1j,   0],
    ], dtype=complex)

def Z():
    return np.matrix([
        [1,  0],
        [0, -1],
    ], dtype=complex)

# Single-qubit rotations
def Rot_X(theta):
    return np.cos(theta / 2) * I() - 1j * X() * np.sin(theta / 2)

def Rot_Y(theta):
    return np.cos(theta / 2) * I() - 1j * Y() * np.sin(theta / 2)

def Rot_Z(theta):
    return np.cos(theta / 2) * I() - 1j * Z() * np.sin(theta / 2)

# Hadamard
def H():
    return 1/np.sqrt(2) * np.matrix([
        [1,  1],
        [1, -1],
    ], dtype=complex)

# Two-qubit gates
def SWAP():
    return np.matrix([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ], dtype=complex)

def CNOT():
    return np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ], dtype=complex)

def CZ():
    p = -1
    return np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, p],
    ], dtype=complex)

def CPHASE(theta):
    p = np.exp(1j * theta)
    return np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, p],
    ], dtype=complex)

#-------------------------------------------------------------

class Gate:
    """
    Wrapper class for unitary matrices used as quantum gates.
    Can be applied only on Density Matrices.

    TODO: use the functions wrapping U instead of the actual matrix for U
    
    Attributes
    ----------
    U: :class:`numpy.matrix`
        Unitary matrix of this gate
    """
    def __init__(self, U: np.matrix):
        self.U = U

    def __call__(self, rho: np.matrix):
        return self.U @ rho @ self.U.H
    
    def __str__(self):
        return str(self.U)
    

# TODO: For now Moment is just an alias for Gate, 
# but, in the future (i.e., on a sunny day), 
# it is envisioned to have a different purpose.
Moment = Gate  


class QuantumCircuit:
    """
    Class encapsulating a sequence of `Gate`s to be applied on a given initial state.
    
    Attributes
    ----------
    gates: list[:class:`Gate`]
        Sequence of gates
    """

    # TODO: implement caching

    def __init__(self, gates: List[Gate]):
        self.gates = gates

    def __call__(self, rho: np.matrix):
        return reduce(lambda dm, gate: gate(dm), self.gates, rho)
    
#-------------------------------------------------------------

# Define trace-preserving operations

class DepolarizingChannel:
    """Depolarizing channel for 2-qubit state (in Density Matrix form)."""

    def __init__(self, p: float):
        assert 0 <= p <= 1
        self.p = p

    def __call__(self, rho: np.matrix, nstates: int=None):
        nrows, ncols = np.shape(rho)
        assert nrows == ncols, \
            'Depolarizing channel can be applied only to density matrices'
        if nstates is None:
            nstates = nrows
        return self.p * rho + (1 - self.p) / nstates * I(nstates)
    

class PartialTrace:
    """
    Computes the partial trace over a given density matrix.

    Attributes
    ----------
    num_qubits: `int`
        Total number of qubits in the system

    out_qubits: `list[int]`
        Indices of qubits to be traced out
    """
    
    def __init__(self, num_qubits: int, out_qubits: List[int]):
        self.num_qubits = num_qubits
        self.out_qubits = set(out_qubits)
    
    def __call__(self, rho: np.matrix):

        comp_bases = POVM._get_comp_bases(
            len(self.out_qubits)
        )

        def reduce_func(accum, basis):
            M = kron([
                next(basis) if i in self.out_qubits else I() 
                for i in range(self.num_qubits)
            ])
            return accum + (M.H @ rho @ M)

        return reduce(reduce_func, comp_bases, 0)
    

class POVM:
    """
    Constructs a POVM to be used in measuring selected qubits.

    Attributes
    ----------
    num_qubits: `int`
        Total number of qubits in the system

    meas_qubits: `list[int]`
        Indices of qubits to be measured
    
    partial_trace: `bool`, optional, default `False`
        Whether to automatically trace out measured qubits
    """

    def __init__(self, 
        num_qubits: int, 
        meas_qubits: List[int],
        partial_trace: bool=False
    ):
        self.num_qubits = num_qubits
        self.meas_qubits = set(meas_qubits)
        self.partial_trace = partial_trace

    def __call__(self, rho: np.matrix):

        Ms = POVM._create_povm(
            self.num_qubits, 
            self.meas_qubits,
            self.partial_trace,
        )

        probs = []
        rho_outs = []

        for M in Ms:
            prob = 0.0
            if self.partial_trace:
                prob = np.real(np.trace(M.H @ rho @ M))
            else:
                prob = np.real(np.trace(rho @ M))
            
            rho_out = M.H @ rho @ M
            rho_out = rho_out / prob if prob else rho_out  # Normalize

            probs.append(prob)
            rho_outs.append(rho_out)

        return np.array(probs), np.array(rho_outs)

    @staticmethod
    def _get_comp_bases(num_qubits: int):
        # NOTE: this function evaluates lazily!
        BASE = [comp_state(0), comp_state(1)]
        return iter(
            iter(BASE[(i >> j) & 1] for j in range(num_qubits))
            for i in range(2 ** num_qubits)
        )
    
    @staticmethod
    def _create_povm(
        num_qubits: int, 
        meas_qubits: Set[int],
        partial_trace: bool,
    ):
        # NOTE: this function evaluates lazily!
        comp_bases = POVM._get_comp_bases(len(meas_qubits))

        if partial_trace:
            foo = lambda ket: ket  # Ket to Ket
        else:
            foo = lambda ket: ket @ ket.H  # Ket to Density Matrix

        def map_func(basis):
            return kron([
                foo(next(basis)) if i in meas_qubits else I() 
                for i in range(num_qubits)
            ])

        return map(map_func, comp_bases)
    
#-------------------------------------------------------------

# Define some additional helpful operations

def kron(As: List[np.matrix]):
    """Kronecker product"""
    # NOTE: here, kron with foldr is faster than with foldl (i.e., reduce)
    return reduce(lambda accum, A: np.kron(A, accum), reversed(As), 1)

def fidelity(dm: np.matrix, ket: np.matrix):
    """Compute fidelity between a density matrix and a ket state."""
    f = np.trace(ket.H @ dm @ ket)  # use trace because f is wrapped in a matrix
    assert np.imag(f) == 0
    return np.real(f)

#-------------------------------------------------------------

def comp_state(n: int, nstates: int=2):
    assert 0 <= n < nstates
    psi = np.zeros(nstates, dtype=complex)
    psi[n] = 1.0
    return np.asmatrix(psi).T

def bell_state(a: Literal[0, 1]=0, b: Literal[0, 1]=0):
    phi = 1/np.sqrt(2) * np.matrix([1, 0, 0, 1], dtype=complex).T
    if b:
        phi = kron([I(), Z()]) @ phi
    if a:
        phi = kron([I(), X()]) @ phi
    return phi

def werner_state(p: float):
    phi_00 = bell_state(0, 0)
    rho_00 = phi_00 @ phi_00.H
    return DepolarizingChannel(p)(rho_00)

#-------------------------------------------------------------
