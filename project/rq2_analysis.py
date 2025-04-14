import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# Configuration
PROTOCOL_NAMES = ['BBPSSW', 'EPL', 'DEJMPS', '3_to_1']
COLOR_MAP = {'BBPSSW': 'blue', 'EPL': 'green', 'DEJMPS': 'red', '3_to_1': 'purple'}
MARKER_MAP = {'BBPSSW': 'o', 'EPL': 's', 'DEJMPS': '^', '3_to_1': 'D'}


def load_and_process(protocol):
    """Load and process data for a single protocol"""
    files = glob.glob(f'./data/{protocol}_*.csv')
    if not files:
        raise FileNotFoundError(f"No CSV files found for protocol {protocol}")

    df = pd.concat([pd.read_csv(f) for f in files])

    # Filter for perfect gates and successful cases
    perfect_gate = df[df['Gate fidelity'] == 1.0]
    successful = perfect_gate[perfect_gate['Fidelity'] > 0]  # Only successful trials

    # Calculate statistics
    grouped = successful.groupby('EPR channel fidelity').agg({
        'Fidelity': ['mean', 'sem', 'count']
    }).reset_index()

    # Flatten multi-index columns
    grouped.columns = ['EPR_fid', 'mean_fid', 'sem_fid', 'n_samples']

    return grouped


def plot_comparison(all_data):
    """Create comparative fidelity plot"""
    plt.figure(figsize=(10, 6))

    for protocol, data in all_data.items():
        plt.errorbar(
            x=data['EPR_fid'],
            y=data['mean_fid'],
            yerr=data['sem_fid'],
            fmt=f'{MARKER_MAP[protocol]}--',
            color=COLOR_MAP[protocol],
            markersize=8,
            linewidth=1.5,
            label=protocol,
            capsize=5,
            capthick=1.5
        )

    plt.axhline(0.5, color='gray', linestyle='--', label='Classical Threshold')
    plt.xlabel('EPR Channel Fidelity', fontsize=12)
    plt.ylabel('Success Conditioned Fidelity', fontsize=12)
    plt.title('Protocol Performance Comparison (Perfect Gates)', fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.tight_layout()
    plt.savefig('protocol_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


def print_statistics(all_data):
    """Print key statistics for each protocol"""
    for protocol, data in all_data.items():
        print(f"\n=== {protocol} Statistics ===")
        print(data[['EPR_fid', 'n_samples', 'mean_fid', 'sem_fid']].round(3))
        print(f"Maximum Fidelity: {data['mean_fid'].max():.3f}")
        print(f"Fidelity at EPR=0.9: {data[data['EPR_fid'] == 0.9]['mean_fid'].values[0]:.3f}")


if __name__ == "__main__":
    # Load and process data for all protocols
    all_data = {proto: load_and_process(proto) for proto in PROTOCOL_NAMES}

    # Generate plots and statistics
    plot_comparison(all_data)
    print_statistics(all_data)