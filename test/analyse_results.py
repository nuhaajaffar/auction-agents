import os
import json
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = "results"
SUMMARY_DIR = os.path.join(RESULTS_DIR, "summaries")
FIGURE_DIR = os.path.join(RESULTS_DIR, "figures")

os.makedirs(FIGURE_DIR, exist_ok = True)
os.makedirs(SUMMARY_DIR, exist_ok = True)

AGENT_LABELS = {
    "RandomAgent": "Random Agent",
    "ConservativeAgent": "Conservative Agent",
    "AggressiveAgent": "Aggressive Agent",
    "SniperAgent": "Sniper Agent",
    "AdaptiveAgent": "Adaptive Agent",
    "Random Agent": "Random Agent",
    "Conservative Agent": "Conservative Agent",
    "Aggressive Agent": "Aggressive Agent",
    "Sniper Agent": "Sniper Agent",
    "Adaptive Agent": "Adaptive Agent"
}

AGENT_ORDER = [
    "Random Agent",
    "Conservative Agent",
    "Aggressive Agent",
    "Sniper Agent",
    "Adaptive Agent"
]

NOISE_ORDER = {
    "low": 0,
    "medium": 1,
    "high": 2
}

def load_csv(path):

    if not os.path.exists(path):
        print(f"Missing file, skipped: {path}")
        return None

    return pd.read_csv(path)

def add_agent_labels(df):
    
    if "agent_type" in df.columns:
        df["agent_label"] = df["agent_type"].map(AGENT_LABELS)

    if "agent" in df.columns:
        df["agent_label"] = df["agent"].map(AGENT_LABELS).fillna(df["agent"])

    return df

def save_bar_chart(df, x_col, y_col, title, xlabel, ylabel, filename, error_col = None):

    plt.figure(figsize = (9, 6))

    if error_col is not None and error_col in df.columns:
        plt.bar(
            df[x_col],
            df[y_col],
            yerr = df[error_col],
            capsize = 5
        )
    else:
        plt.bar(df[x_col], df[y_col])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation = 30, ha = "right")
    plt.tight_layout()

    output_path = os.path.join(FIGURE_DIR, filename)
    plt.savefig(output_path, dpi = 300)
    plt.close()

    print(f"Saved figure: {output_path}")

def save_line_chart(       
    df,
    x_col,
    y_col,
    title,
    xlabel,
    ylabel,
    filename,
    group_col = None,
    error_col = None,
    x_ticks = None,
    x_tick_labels = None,
    legend_title = None
):
    
    plt.figure(figsize = (9, 6))

    if group_col is None:
        df = df.sort_values(x_col)

        if error_col is not None and error_col in df.columns:
            plt.errorbar(
                df[x_col],
                df[y_col],
                yerr = df[error_col],
                marker = "o",
                capsize = 5
            )
        else:
            plt.plot(df[x_col], df[y_col], marker = "o")

    else:
        for group_name, group_df in df.groupby(group_col):
            group_df = group_df.sort_values(x_col)

            plt.plot(
                group_df[x_col],
                group_df[y_col],
                marker = "o",
                label = group_name
            )

        plt.legend(title=legend_title if legend_title is not None else group_col)

    if x_ticks is not None and x_tick_labels is not None:
        plt.xticks(x_ticks, x_tick_labels)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    output_path = os.path.join(FIGURE_DIR, filename)
    plt.savefig(output_path, dpi = 300)
    plt.close()

    print(f"Saved figure: {output_path}")

def save_grouped_bar_chart(
    df,
    x_col,
    group_col,
    y_col,
    title,
    xlabel,
    ylabel,
    filename,
    error_col = None,
    x_order = None,
    group_order = None,
    legend_title = None
):
    
    if x_order is not None:
        df[x_col] = pd.Categorical(df[x_col], categories = x_order, ordered = True)
        df = df.sort_values(x_col)

    if group_order is not None:
        df[group_col] = pd.Categorical(df[group_col], categories = group_order, ordered = True)
        df = df.sort_values(group_col)

    x_values = list(df[x_col].dropna().unique())
    group_values = list(df[group_col].dropna().unique())

    x_positions = range(len(x_values))
    bar_width = 0.8 / len(group_values)

    plt.figure(figsize = (10, 6))

    for i, group_value in enumerate(group_values):
        group_df = df[df[group_col] == group_value]

        y_values = []
        error_values = []

        for x_value in x_values:
            row = group_df[group_df[x_col] == x_value]

            if row.empty:
                y_values.append(0)
                error_values.append(0)
            else:
                y_values.append(row[y_col].iloc[0])

                if error_col is not None and error_col in row.columns:
                    error_values.append(row[error_col].iloc[0])
                else:
                    error_values.append(0)

        positions = [x + (i - len(group_values) / 2) * bar_width + bar_width / 2 for x in x_positions]

        if error_col is not None:
            plt.bar(
                positions,
                y_values,
                width = bar_width,
                yerr = error_values,
                capsize = 4,
                label = group_value
            )
        else:
            plt.bar(
                positions,
                y_values,
                width = bar_width,
                label = group_value
            )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(list(x_positions), x_values, rotation = 30, ha = "right")
    plt.legend(title = legend_title if legend_title is not None else group_col)
    plt.tight_layout()

    output_path = os.path.join(FIGURE_DIR, filename)
    plt.savefig(output_path, dpi = 300)
    plt.close()

    print(f"Saved figure: {output_path}")

def analyse_experiment_1():

    print("\nAnalysing Experiment 1...")

    path = os.path.join(SUMMARY_DIR, "experiment_1_strategy_comparison_summary.csv")
    df = load_csv(path)

    if df is None:
        return

    df = add_agent_labels(df)

    save_bar_chart(
        df = df,
        x_col = "agent_label",
        y_col = "avg_profit",
        error_col = "std_profit",
        title = "Experiment 1: Average Profit by Agent Strategy",
        xlabel = "Agent Strategy",
        ylabel = "Average Profit",
        filename = "experiment_1_profit.png"
    )

    save_bar_chart(
        df = df,
        x_col = "agent_label",
        y_col = "avg_win_rate",
        error_col = "std_win_rate",
        title = "Experiment 1: Average Win Rate by Agent Strategy",
        xlabel = "Agent Strategy",
        ylabel = "Average Win Rate",
        filename = "experiment_1_win_rate.png"
    )

    save_bar_chart(
        df = df,
        x_col = "agent_label",
        y_col = "avg_efficiency",
        error_col = "std_efficiency",
        title = "Experiment 1: Average Efficiency by Agent Strategy",
        xlabel = "Agent Strategy",
        ylabel = "Average Efficiency",
        filename = "experiment_1_efficiency.png"
    )

def analyse_experiment_2():

    print("\nAnalysing Experiment 2...")

    summary_path = os.path.join(SUMMARY_DIR, "experiment_2_number_of_agents_summary.csv")
    grouped_path = os.path.join(SUMMARY_DIR, "experiment_2_number_of_agents_by_type_summary.csv")

    summary_df = load_csv(summary_path)
    grouped_df = load_csv(grouped_path)

    if summary_df is not None:
        save_line_chart(
            df = summary_df,
            x_col = "num_agents",
            y_col = "avg_profit",
            error_col = "std_profit",
            title = "Experiment 2: Average Profit as Number of Agents Increases",
            xlabel = "Number of Agents",
            ylabel = "Average Profit",
            filename = "experiment_2_profit_by_agents.png"
        )

        save_line_chart(
            df = summary_df,
            x_col = "num_agents",
            y_col = "avg_efficiency",
            error_col = "std_efficiency",
            title = "Experiment 2: Average Efficiency as Number of Agents Increases",
            xlabel = "Number of Agents",
            ylabel = "Average Efficiency",
            filename = "experiment_2_efficiency_by_agents.png"
        )

    if grouped_df is not None:
        grouped_df = add_agent_labels(grouped_df)

        save_line_chart(
            df = grouped_df,
            x_col = "num_agents",
            y_col = "avg_profit",
            group_col = "agent_label",
            title = "Experiment 2: Profit by Agent Type as Competition Increases",
            xlabel = "Number of Agents",
            ylabel = "Average Profit",
            filename = "experiment_2_profit_by_type.png",
            legend_title = "Agent Type"
        )

def analyse_experiment_3():

    print("\nAnalysing Experiment 3...")

    adaptive_path = os.path.join(SUMMARY_DIR, "experiment_3_information_availability_adaptive_summary.csv")
    grouped_path = os.path.join(SUMMARY_DIR, "experiment_3_information_availability_by_type_summary.csv")

    adaptive_df = load_csv(adaptive_path)
    grouped_df = load_csv(grouped_path)

    memory_order = {"yes": 0, "no": 1}
    memory_labels = {
        "yes": "With Memory",
        "no": "Without Memory"
    }

    if adaptive_df is not None:
        adaptive_df["sort_order"] = adaptive_df["memory_access"].map(memory_order)
        adaptive_df["memory_label"] = adaptive_df["memory_access"].map(memory_labels)
        adaptive_df = adaptive_df.sort_values("sort_order")

        save_bar_chart(
            df = adaptive_df,
            x_col = "memory_label",
            y_col = "avg_profit",
            error_col = "std_profit",
            title = "Experiment 3: Adaptive Agent Profit With and Without Memory",
            xlabel = "Memory Access",
            ylabel = "Average Profit",
            filename = "experiment_3_profit_by_memory.png"
        )

        save_bar_chart(
            df = adaptive_df,
            x_col = "memory_label",
            y_col = "avg_win_rate",
            error_col = "std_win_rate",
            title = "Experiment 3: Adaptive Agent Win Rate With and Without Memory",
            xlabel = "Memory Access",
            ylabel = "Average Win Rate",
            filename = "experiment_3_win_rate_by_memory.png"
        )

        save_bar_chart(
            df = adaptive_df,
            x_col = "memory_label",
            y_col = "avg_efficiency",
            error_col = "std_efficiency",
            title = "Experiment 3: Adaptive Agent Efficiency With and Without Memory",
            xlabel = "Memory Access",
            ylabel = "Average Efficiency",
            filename = "experiment_3_efficiency_by_memory.png"
        )

    if grouped_df is not None:
        grouped_df = add_agent_labels(grouped_df)
        grouped_df["memory_label"] = grouped_df["memory_access"].map(memory_labels)

        save_grouped_bar_chart(
            df = grouped_df,
            x_col = "agent_label",
            group_col = "memory_label",
            y_col = "avg_profit",
            error_col = "std_profit",
            title = "Experiment 3: Average Profit by Agent Type and Memory Condition",
            xlabel = "Agent Type",
            ylabel = "Average Profit",
            filename = "experiment_3_profit_by_agent_type_and_memory.png",
            x_order = AGENT_ORDER,
            group_order = ["With Memory", "Without Memory"],
            legend_title = "Memory Access"
        )

def analyse_experiment_4():

    print("\nAnalysing Experiment 4...")

    summary_path = os.path.join(SUMMARY_DIR, "experiment_4_market_noise_summary.csv")
    grouped_path = os.path.join(SUMMARY_DIR, "experiment_4_market_noise_by_type_summary.csv")

    summary_df = load_csv(summary_path)
    grouped_df = load_csv(grouped_path)

    if summary_df is not None:
        summary_df["sort_order"] = summary_df["noise_level"].map(NOISE_ORDER)
        summary_df = summary_df.sort_values("sort_order")

        save_bar_chart(
            df = summary_df,
            x_col = "noise_level",
            y_col = "avg_profit",
            error_col = "std_profit",
            title = "Experiment 4: Average Profit Under Different Market Noise Levels",
            xlabel = "Noise Level",
            ylabel = "Average Profit",
            filename = "experiment_4_noise_profit.png"
        )

        save_bar_chart(
            df = summary_df,
            x_col = "noise_level",
            y_col = "avg_efficiency",
            error_col = "std_efficiency",
            title = "Experiment 4: Average Efficiency Under Different Market Noise Levels",
            xlabel = "Noise Level",
            ylabel = "Average Efficiency",
            filename = "experiment_4_noise_efficiency.png"
        )

    if grouped_df is not None:
        grouped_df = add_agent_labels(grouped_df)
        grouped_df["sort_order"] = grouped_df["noise_level"].map(NOISE_ORDER)
        grouped_df = grouped_df.sort_values("sort_order")

        save_line_chart(
            df = grouped_df,
            x_col = "sort_order",
            y_col = "avg_profit",
            group_col = "agent_label",
            title = "Experiment 4: Profit by Agent Type Across Noise Levels",
            xlabel = "Noise Level",
            ylabel = "Average Profit",
            filename = "experiment_4_noise_by_type.png",
            x_ticks = [0, 1, 2],
            x_tick_labels = ["low", "medium", "high"],
            legend_title = "Agent Type"
        )

def plot_adaptive_learning_over_time():

    print("\nCreating adaptive learning-over-time graph...")

    path = os.path.join(RESULTS_DIR, "learning_metrics.json")

    if not os.path.exists(path):
        print(f"Missing file, skipped: {path}")
        print("Run your learning test first to generate learning_metrics.json.")
        return

    with open(path, "r") as f:
        data = json.load(f)

    aggressiveness_history = data["adaptive_agent"]["aggressiveness_history"]

    if len(aggressiveness_history) == 0:
        print("No aggressiveness history found, skipped learning graph.")
        return

    rounds = list(range(1, len(aggressiveness_history) + 1))

    learning_df = pd.DataFrame({
        "round": rounds,
        "aggressiveness": aggressiveness_history
    })

    learning_csv_path = os.path.join(SUMMARY_DIR, "adaptive_learning_history.csv")
    learning_df.to_csv(learning_csv_path, index = False)
    print(f"Saved learning history table: {learning_csv_path}")

    plt.figure(figsize = (10, 6))
    plt.plot(rounds, aggressiveness_history, marker = "o")

    plt.title("Adaptive Agent Learning Behaviour Over Time")
    plt.xlabel("Round")
    plt.ylabel("Aggressiveness")
    plt.grid(True)
    plt.tight_layout()

    output_path = os.path.join(FIGURE_DIR, "adaptive_learning_over_time.png")
    plt.savefig(output_path, dpi = 300)
    plt.close()

    print(f"Saved figure: {output_path}")

def create_combined_summary_table():

    print("\nCreating combined summary table...")

    files = {
        "experiment_1": "experiment_1_strategy_comparison_summary.csv",
        "experiment_2": "experiment_2_number_of_agents_summary.csv",
        "experiment_3": "experiment_3_information_availability_adaptive_summary.csv",
        "experiment_4": "experiment_4_market_noise_summary.csv"
    }

    combined_tables = []

    for experiment_name, filename in files.items():
        path = os.path.join(SUMMARY_DIR, filename)
        df = load_csv(path)

        if df is not None:
            df.insert(0, "experiment", experiment_name)
            combined_tables.append(df)

    if combined_tables:
        combined_df = pd.concat(combined_tables, ignore_index = True)
        output_path = os.path.join(SUMMARY_DIR, "combined_summary_table.csv")
        combined_df.to_csv(output_path, index = False)
        print(f"Saved combined summary table: {output_path}")

if __name__ == "__main__":
    analyse_experiment_1()
    analyse_experiment_2()
    analyse_experiment_3()
    analyse_experiment_4()
    plot_adaptive_learning_over_time()
    create_combined_summary_table()

    print("\nAnalysis complete.")