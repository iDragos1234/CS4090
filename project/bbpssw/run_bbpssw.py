import subprocess
import numpy as np
import pandas as pd
from time import perf_counter


def parse(bytestring: bytes):
    s = bytestring.decode('utf-8').strip().split(' ')
    m_alice, m_bob, fidelity = s
    return int(m_alice), int(m_bob), float(fidelity)


def main():
    GATE_FID_SWEEP = [1.0]
    EPR_FID_SWEEP = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    NUM_SAMPLES = 100
    MAX_ATTEMPTS = 5

    CMD_GATE_FID = 'sed -i "s/^    gate_fidelity: .*$/    gate_fidelity: {}/g" network.yaml'
    CMD_CHANNEL_FID = 'sed -i "s/^    fidelity: .*$/    fidelity: {}/g" network.yaml'

    results = []
    t0 = perf_counter()
    num_errors = 0

    try:
        for gate_fid in GATE_FID_SWEEP:
            _ = subprocess.check_output(CMD_GATE_FID.format(gate_fid), shell=True)
            for epr_fid in EPR_FID_SWEEP:
                _ = subprocess.check_output(CMD_CHANNEL_FID.format(epr_fid), shell=True)

                for sample_idx in range(NUM_SAMPLES):
                    attempt_num = 0
                    flag = False
                    output = None

                    while not flag and attempt_num < MAX_ATTEMPTS:
                        try:
                            output = subprocess.check_output('netqasm simulate', shell=True)
                        except Exception:
                            num_errors += 1
                            attempt_num += 1
                            continue
                        else:
                            flag = True

                    if attempt_num >= MAX_ATTEMPTS:
                        raise Exception("Max attempts reached")

                    m_alice, m_bob, fidelity = parse(output)
                    results.append([gate_fid, epr_fid, sample_idx, m_alice, m_bob, fidelity])
                    print(results[-1])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        df = pd.DataFrame(
            results, columns=["Gate fidelity", "EPR channel fidelity", "Sample index", "M_Alice", "M_Bob", "Fidelity"]
        )
        df.to_csv('./out_bbpssw.csv', mode='a')
        print("Simulation completed.")
        print(f"Total runtime: {perf_counter() - t0:.2f}s")
        print(f"Total errors: {num_errors}")


if __name__ == "__main__":
    main()
