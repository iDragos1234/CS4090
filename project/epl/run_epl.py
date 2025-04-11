import subprocess
import time
from time import perf_counter
import numpy as np

# Configuration
GATE_FID_SWEEP = np.linspace(0.5, 1.0, 5)  # Gate fidelity range
EPR_FID_SWEEP = np.linspace(0.4, 1.0, 5)  # Channel fidelity range
NUM_SAMPLES = 10  # Samples per configuration
MAX_ATTEMPTS = 5  # Max attempts per sample
TIMEOUT = 10  # Seconds per simulation attempt

# sed commands template
CMD_GATE_FID = r'sed -i "s/^\(    gate_fidelity: \).*/\1{}/" network.yaml'
CMD_CHANNEL_FID = r'sed -i "s/^\(    fidelity: \).*/\1{}/" network.yaml'


def parse_success(output: bytes) -> bool:
    """Parse simulation output for success/failure"""
    output_str = output.decode()
    alice_success = "EPL protocol success: True" in output_str
    bob_success = "EPL protocol success: True" in output_str
    return alice_success and bob_success


def run_simulation():
    """Run single simulation and return success status"""
    try:
        output = subprocess.check_output(
            "netqasm simulate",
            shell=True,
            timeout=TIMEOUT
        )
        return parse_success(output)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False


def main():
    results = []
    num_errors = 0
    t0 = perf_counter()

    for gate_fid in GATE_FID_SWEEP:
        # Update gate fidelity for all nodes
        subprocess.run(
            CMD_GATE_FID.format(gate_fid),
            shell=True,
            check=True
        )

        for epr_fid in EPR_FID_SWEEP:
            # Update channel fidelity
            subprocess.run(
                CMD_CHANNEL_FID.format(epr_fid),
                shell=True,
                check=True
            )

            successes = 0
            for _ in range(NUM_SAMPLES):
                attempt = 0
                while attempt < MAX_ATTEMPTS:
                    try:
                        if run_simulation():
                            successes += 1
                            break
                    except Exception as e:
                        num_errors += 1
                    finally:
                        attempt += 1

            success_rate = successes / NUM_SAMPLES
            results.append({
                'gate_fidelity': round(gate_fid, 2),
                'epr_fidelity': round(epr_fid, 2),
                'success_rate': success_rate,
                'samples': NUM_SAMPLES,
                'errors': num_errors
            })

    # Restore original network.yaml
    subprocess.run("git checkout -- network.yaml", shell=True)

    print(f"\nCompleted in {perf_counter() - t0:.2f}s")
    print("Results:")
    for result in results:
        print(
            f"Gate Fid: {result['gate_fidelity']} | "
            f"EPR Fid: {result['epr_fidelity']} | "
            f"Success: {result['success_rate']:.2%} | "
            f"Errors: {result['errors']}"
        )


if __name__ == "__main__":
    main()