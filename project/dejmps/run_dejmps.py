import subprocess
import numpy as np
import re
from time import perf_counter


def main():
    # NOTE: To simulate a protocol, this python file needs to be executed
    # inside the folder of the simulated protocol, with venv activated.

    NUM_SAMPLES = 4
    GRID_SIZE = 3

    # # Change directory into the folder of the simulated protocol
    # subprocess.run('ls -lahF', shell=True, cwd='/home/cs4090/CS4090/project/dejmps')

    # Run netqasm simulation and get the results

    def parse(bytestring: bytes):
        """Parses simulation outputs."""
        # Decode bytes
        s = bytestring.decode('utf-8')
        # Parse output given as the string of two integers and a float separated by whitespaces
        s = s[:-1].split(' ')  # Ignore the '\n' at the end, tokenize string by the ' ' separator
        m_alice, m_bob, fidelity = s
        return int(m_alice), int(m_bob), float(fidelity)

    results = []

    t0 = perf_counter()

    CMD_GATE_FID = 'sed -i "s/^    gate_fidelity: .*$/    gate_fidelity: {}/g" network.yaml'
    CMD_CHANNEL_FID = 'sed -i "s/^    fidelity: .*$/    fidelity: {}/g" network.yaml'

    for gate_fidelity in np.linspace(0, 1, GRID_SIZE):
        # Set gate fidelity
        _ = subprocess.check_output(CMD_GATE_FID.format(gate_fidelity), shell=True)
        for epr_fidelity in np.linspace(0, 1, GRID_SIZE):
            # Set EPR channel fidelity
            _ = subprocess.check_output(CMD_CHANNEL_FID.format(gate_fidelity), shell=True)

            for sample_idx in range(NUM_SAMPLES):
                output = subprocess.check_output('netqasm simulate', shell=True)
                m_alice, m_bob, fidelity = parse(output)
                is_success = 1 - (m_alice ^ m_bob)
                print([gate_fidelity, epr_fidelity, sample_idx, is_success, fidelity])
                results.append([gate_fidelity, epr_fidelity, sample_idx, is_success, fidelity])
                # TODO: Implement fail safety

    results = np.array(results)

    print(f'Elapsed time: {perf_counter() - t0}')
    print('Results:')
    print(results)


if __name__ == '__main__':
    main()
