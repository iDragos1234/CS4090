import subprocess
import pandas as pd
from time import perf_counter

def parse(bytestring: bytes):
    m_alice, m_bob, fidelity = bytestring.decode('utf-8').split()
    return int(m_alice), int(m_bob), float(fidelity)

def main():
    GATE_FID_SWEEP = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    EPR_FID_SWEEP = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    NUM_SAMPLES = 100
    MAX_ATTEMPTS = 5

    CMD_GATE_FID = 'sed -i "s/^    gate_fidelity: .*$/    gate_fidelity: {}/g" network.yaml'
    CMD_CHANNEL_FID = 'sed -i "s/^    fidelity: .*$/    fidelity: {}/g" network.yaml'

    results = []
    t0 = perf_counter()
    num_errors = 0

    try:
        for gate_fidelity in GATE_FID_SWEEP:
            subprocess.run(CMD_GATE_FID.format(gate_fidelity), shell=True)
            for epr_fidelity in EPR_FID_SWEEP:
                subprocess.run(CMD_CHANNEL_FID.format(epr_fidelity), shell=True)
                for sample_idx in range(NUM_SAMPLES):
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

                    m_alice, m_bob, fidelity = parse(output)
                    results.append([gate_fidelity, epr_fidelity, sample_idx, m_alice, m_bob, fidelity])
                    print(results[-1])
    except Exception as err:
        raise Exception(f'Error: {err}')
    finally:
        cols = ['Gate fidelity', 'EPR channel fidelity', 'Sample index', 'M_Alice', 'M_Bob', 'Fidelity']
        results_df = pd.DataFrame(results, columns=cols)
        results_df.to_csv('./out_bbpssw.csv', mode='a')
        print(f'Finished. Time: {perf_counter() - t0}, Errors: {num_errors}')

if __name__ == '__main__':
    main()