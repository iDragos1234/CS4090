import subprocess
import numpy as np
import pandas as pd
from time import perf_counter


def main():
    # NOTE: To simulate a protocol, this python file needs to be executed
    # inside the folder of the simulated protocol, with venv activated.

    # Parameter sweeps
    GATE_FID_SWEEP = [1.0]  # np.linspace(0, 1, 25)
    EPR_FID_SWEEP = [0.8]  # np.linspace(0, 1, 25)
    NUM_SAMPLES = 100  # Set number of samples for each parameter configuration
    MAX_ATTEMPTS = 3  # Maximum number of attempts for generating a single sample

    # # Change directory into the folder of the simulated protocol
    # subprocess.run('ls -lahF', shell=True, cwd='/home/cs4090/CS4090/project/dejmps')

    def parse(bytestring: bytes):
        """Parses simulation outputs."""
        # Decode bytes
        s = bytestring.decode('utf-8')
        # Parse output given as the string of two integers and a float separated by whitespaces
        s = s[:-1].split(' ')  # Ignore the '\n' at the end, tokenize string by the ' ' separator
        m_alice, m_bob, fidelity = s
        return int(m_alice), int(m_bob), float(fidelity)

    # Commands to change the gate and channel fidelities in network.yaml
    CMD_GATE_FID = 'sed -i "s/^    gate_fidelity: .*$/    gate_fidelity: {}/g" network.yaml'
    CMD_CHANNEL_FID = 'sed -i "s/^    fidelity: .*$/    fidelity: {}/g" network.yaml'

    results = []
    t0 = perf_counter()
    num_errors = 0  # Keep track of the number of errors raised by netqasm simulation

    try:
        for gate_fidelity in GATE_FID_SWEEP:
            # Set gate fidelity
            _ = subprocess.check_output(CMD_GATE_FID.format(gate_fidelity), shell=True)
            for epr_fidelity in EPR_FID_SWEEP:
                # Set EPR channel fidelity
                _ = subprocess.check_output(CMD_CHANNEL_FID.format(epr_fidelity), shell=True)

                for sample_idx in range(NUM_SAMPLES):
                    # Attempt multiple times to generate a single sample
                    output = None
                    flag = False
                    attempt_num = 0
                    while not flag and attempt_num < MAX_ATTEMPTS:
                        try:
                            output = subprocess.check_output('netqasm simulate', shell=True)
                        except subprocess.SubprocessError | TimeoutError as err:
                            num_errors += 1
                            attempt_num += 1
                            pass
                        except Exception as other_err:
                            print(f'Other errors: {other_err}')
                            raise Exception(f'Other errors: {other_err}')
                        else:
                            # Signal that sample was successfully generated
                            flag = True
                    # If max attempts is reached, terminate
                    if attempt_num >= MAX_ATTEMPTS:
                        raise Exception('Maximum number of attempts reached.')

                    m_alice, m_bob, fidelity = parse(output)
                    results.append([gate_fidelity, epr_fidelity, sample_idx, m_alice, m_bob, fidelity])
                    print(results[-1])
    finally:
        # Save simulation results
        print('Saving ...')
        # Create DataFrame of simulation results and save to CSV file
        cols = ['Gate fidelity', 'EPR channel fidelity', 'Sample index', 'M_Alice', 'M_Bob', 'Fidelity']
        results = pd.DataFrame(
            results,
            columns=cols,
        )
        results.to_csv('./out.csv', mode='a')
        # NOTE: to read DataFrame from CSV file, do: `pd.read_csv('./store.pkl')`

        print(f'Elapsed time: {perf_counter() - t0}')
        print(f'No. Errors: {num_errors}')
        print('Results:')
        print(results)


if __name__ == '__main__':
    main()
