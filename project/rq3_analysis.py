import pandas as pd
import matplotlib.pyplot as plt
import glob

PROTOCOLS = {
    'BBPSSW': {'pattern': './data/BBPSSW_data.csv', 'success_fn': lambda df: (df['M_Alice'] == df['M_Bob'])},
    'DEJMPS': {'pattern': './data/DEJMPS_data.csv', 'success_fn': lambda df: (df['M_Alice'] == df['M_Bob'])},
    'EPL': {'pattern': './data/EPL_data.csv', 'success_fn': lambda df: (df['M_Alice'] == 1) & (df['M_Bob'] == 1)},
    '3-to-1': {
        'pattern': './data/3_to_1_data.csv',
        'success_fn': lambda df: (df['M_Alice_1'] == df['M_Bob_1']) & (df['M_Alice_2'] == df['M_Bob_2'])
    }
}


def load_protocol_data(file_pattern, success_condition):
    files = glob.glob(file_pattern)
    if not files:
        return pd.DataFrame()

    df = pd.concat([pd.read_csv(f) for f in files])
    df['Success'] = success_condition(df).astype(int)

    def calc_fidelity(x):
        success_cases = x[x['Success'] == 1]
        return success_cases['Fidelity'].mean() if not success_cases.empty else 0

    grouped = df.groupby(['Gate fidelity', 'EPR channel fidelity']).apply(
        lambda x: pd.Series({
            'Success Probability': x['Success'].mean(),
            'Avg Fidelity': calc_fidelity(x),
            'Sample Count': len(x)
        })
    ).reset_index()

    return grouped


def create_comparison_plots(results):
    fig, axs = plt.subplots(2, 2, figsize=(18, 12))

    # Varying EPR fidelity (Gate fidelity = 1.0)
    plot_noise_regime(axs[0, 0], axs[0, 1], results,
                      fixed_param='Gate fidelity', fixed_value=1.0,
                      vary_param='EPR channel fidelity',
                      title='Fixed Gate Fidelity = 1.0')

    # Varying Gate fidelity (EPR fidelity = 1.0)
    plot_noise_regime(axs[1, 0], axs[1, 1], results,
                      fixed_param='EPR channel fidelity', fixed_value=1.0,
                      vary_param='Gate fidelity',
                      title='Fixed EPR Fidelity = 1.0')

    plt.tight_layout()
    plt.show()


def plot_noise_regime(fid_ax, succ_ax, results, fixed_param, fixed_value, vary_param, title):
    markers = ['o', 's', '^', 'D']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for idx, (protocol, df) in enumerate(results.items()):
        mask = (df[fixed_param] == fixed_value) & (df[vary_param] <= 1.0)
        subset = df[mask].sort_values(vary_param)

        if not subset.empty:
            fid_ax.plot(subset[vary_param], subset['Avg Fidelity'],
                        marker=markers[idx], color=colors[idx],
                        linestyle='-', markersize=8,
                        label=protocol)

    fid_ax.set_xlabel(vary_param.replace('_', ' ').title())
    fid_ax.set_ylabel('Fidelity Given Success')
    fid_ax.set_ylim(-0.05, 1.05)
    fid_ax.grid(True)
    fid_ax.set_title(f'Fidelity Comparison ({title})')
    fid_ax.legend()

    # Plot success probability comparison
    for idx, (protocol, df) in enumerate(results.items()):
        mask = (df[fixed_param] == fixed_value) & (df[vary_param] <= 1.0)
        subset = df[mask].sort_values(vary_param)

        if not subset.empty:
            succ_ax.plot(subset[vary_param], subset['Success Probability'],
                         marker=markers[idx], color=colors[idx],
                         linestyle='-', markersize=8,
                         label=protocol)

    succ_ax.set_xlabel(vary_param.replace('_', ' ').title())
    succ_ax.set_ylabel('Success Probability')
    succ_ax.set_ylim(-0.05, 1.05)
    succ_ax.grid(True)
    succ_ax.set_title(f'Success Probability ({title})')
    succ_ax.legend()


if __name__ == "__main__":
    # Load and process all data
    protocol_data = {}
    for name, config in PROTOCOLS.items():
        df = load_protocol_data(config['pattern'], config['success_fn'])
        if not df.empty:
            protocol_data[name] = df
        else:
            print(f"⚠️ No data loaded for {name} - check file pattern")

    # Generate comparison plots
    if protocol_data:
        create_comparison_plots(protocol_data)

        # Print statistics
        print("\nProtocol Performance Summary:")
        for name, df in protocol_data.items():
            best_fid = df['Avg Fidelity'].max()
            best_success = df['Success Probability'].max()
            print(f"{name}: Max fidelity = {best_fid:.2f}, Max success = {best_success:.2f}")
    else:
        print("No data loaded for any protocols")