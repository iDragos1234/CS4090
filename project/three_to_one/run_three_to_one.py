import subprocess
import pandas as pd
from time import perf_counter


# TODO: write output data to CSV in batches

def parse(bytestring: bytes):
    """Decodes and parses simulation outputs."""
    m_alice_1, m_alice_2, m_bob_1, m_bob_2, fidelity = bytestring.decode('utf-8').split()
    return int(m_alice_1), int(m_alice_2), int(m_bob_1), int(m_bob_2), float(fidelity)


def main():
    # NOTE: To simulate a protocol, this python file needs to be executed
    # inside the folder of the simulated protocol, with venv activated.

    # Parameter sweeps
    GATE_FID_SWEEP = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    EPR_FID_SWEEP = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    NUM_SAMPLES = 100  # Set number of samples for each parameter configuration
    MAX_ATTEMPTS = 5  # Maximum number of attempts for generating a single sample

    # Commands to change the gate and channel fidelities in network.yaml
    CMD_GATE_FID = 'sed -i "s/^    gate_fidelity: .*$/    gate_fidelity: {}/g" network.yaml'
    CMD_CHANNEL_FID = 'sed -i "s/^    fidelity: .*$/    fidelity: {}/g" network.yaml'

    results = []
    t0 = perf_counter()
    num_errors = 0  # Keep track of the number of errors raised by netqasm simulation

    try:
        for gate_fidelity in GATE_FID_SWEEP:
            # Set gate fidelity
            subprocess.run(CMD_GATE_FID.format(gate_fidelity), shell=True)
            for epr_fidelity in EPR_FID_SWEEP:
                # Set EPR channel fidelity
                subprocess.run(CMD_CHANNEL_FID.format(epr_fidelity), shell=True)

                for sample_idx in range(NUM_SAMPLES):
                    # Fail safety: attempt multiple times to generate a single sample
                    output = None
                    flag = False
                    attempt_num = 0
                    while not flag and attempt_num < MAX_ATTEMPTS:
                        try:
                            output = subprocess.check_output('netqasm simulate', shell=True)
                        except (subprocess.SubprocessError, TimeoutError) as err:
                            num_errors += 1
                            attempt_num += 1
                            pass
                        except Exception as other_err:
                            num_errors += 1
                            raise Exception(f'Other errors: {other_err}')
                        else:
                            # Signal that sample was successfully generated
                            flag = True
                    # If max attempts is reached, terminate
                    if attempt_num >= MAX_ATTEMPTS:
                        raise Exception('Maximum number of attempts reached.')

                    m_alice_1, m_alice_2, m_bob_1, m_bob_2, fidelity = parse(output)
                    results.append([
                        gate_fidelity, epr_fidelity, sample_idx,
                        m_alice_1, m_alice_2, m_bob_1, m_bob_2,
                        fidelity,
                    ])
                    print(results[-1])
    except Exception as err:
        raise Exception(f'Simulation error: {err}')
    finally:
        # Save simulation results
        print('Saving ...')
        # Create DataFrame of simulation results and save to CSV file
        cols = [
            'Gate fidelity', 'EPR channel fidelity', 'Sample index',
            'M_Alice_1', 'M_Alice_2', 'M_Bob_1', 'M_Bob_2',
            'Fidelity',
        ]
        results = pd.DataFrame(results, columns=cols)
        # Dump results to a CSV file, in `append` mode
        results.to_csv('./three_to_one.out.csv', mode='a')
        # NOTE: to read DataFrame from CSV file, do: `pd.read_csv('./store.csv')`

        print('Simulation finished')
        print(f'Elapsed time: {perf_counter() - t0}')
        print(f'No. Errors: {num_errors}')


if __name__ == '__main__':
    main()
