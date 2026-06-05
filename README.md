# Autonomous Auction Bidding Agents

This repository contains the code and output files for the COMP3004 Designing Intelligent Agents coursework project: **Autonomous Auction Bidding Agents**.

The project investigates how different autonomous bidding agents behave in a simulated multi-agent auction market. The environment uses repeated first-price auction rounds, where agents bid for generated items and are evaluated using profit, win rate, bidding efficiency and stability across repeated runs.

## Project Overview

The aim of this project is to compare how different bidding strategies perform under changing auction conditions. The implemented agents compete in a simulated auction environment and use different decision-making strategies.

The main research questions are:

1. How do different bidding strategies affect agent profitability and performance?
2. How does performance change as market competition increases?
3. Can an adaptive agent improve its behaviour using previous auction outcomes?
4. How does access to market information affect agent decision-making?
5. How does market noise affect bidding performance and stability?

## Implemented Agents

The simulation includes five main bidding agents:

* **Random Agent**: places random valid bids and acts as a baseline.
* **Conservative Agent**: places cautious bids to protect profit margins.
* **Aggressive Agent**: places larger bids to increase its chance of winning.
* **Sniper Agent**: waits until later in the auction before bidding.
* **Adaptive Agent**: uses auction memory and previous outcomes to adjust its bidding behaviour.

## Additional Testing Agent

A simple **Fixed Agent** is also included in the codebase. This agent places a fixed bid and was used for early testing and comparison of the auction environment and adaptive behaviour.

The Fixed Agent is not part of the main four experiments reported in the coursework. The main experiments focus on the Random, Conservative, Aggressive, Sniper and Adaptive agents.

## Auction Environment

The auction environment manages the full simulation process:

1. Generates auction items.
2. Allows agents to submit bids.
3. Validates bids against auction rules.
4. Selects the winning bid.
5. Calculates profit.
6. Updates agent statistics.
7. Stores results for analysis.

Profit is calculated as:

```text
profit = item.true_value - winning_bid
```

In the market noise experiment, agents make decisions using perceived item values, while profit is still calculated using the true item value. This allows the simulation to test how agents behave when their valuation information is uncertain.

## Experiments

Four main experiments were conducted.

### Experiment 1: Strategy Comparison

Compares the Random, Conservative, Aggressive, Sniper and Adaptive agents under the same auction conditions.

### Experiment 2: Number of Agents and Competition

Tests how performance changes as the number of agents increases across 5, 10 and 20 agents.

### Experiment 3: Information Availability

Compares the Adaptive Agent with and without access to auction memory.

### Experiment 4: Market Noise

Tests agent robustness under low, medium and high levels of market noise.

## Reproducibility

The final experiment scripts use fixed random seeds and consistent generated auction conditions where required, so the main results and figures can be regenerated consistently.

Repeated runs are still used to calculate average performance and standard deviation, but the final code is designed so that the same experiment setup can be reproduced.

The adaptive learning behaviour graph is generated from a separate learning behaviour test. Therefore, to fully regenerate all results and figures, the scripts should be run in this order:

```bash
python scripts/experiments.py
python scripts/learning_test.py
python scripts/analyse_results.py
```

## Project Structure

```text
auction-agents/
│
├── src/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── random_agent.py
│   │   ├── conservative_agent.py
│   │   ├── aggressive_agent.py
│   │   ├── sniper_agent.py
│   │   ├── adaptive_agent.py
│   │   └── fixed_agent.py
│   │
│   ├── environment/
│   │   ├── auction_environment.py
│   │   └── item.py
│   │
│   ├── memory.py
│   └── main.py
│
├── scripts/
│   ├── analyse_results.py
│   ├── experiments.py
│   ├── comparison_test.py
│   └── learning_test.py
│
├── results/
│   ├── raw/
│   ├── summaries/
│   ├── figures/
│   └── learning_metrics.json
│
├── .gitignore
└── README.md
```

## Technologies Used

The project was implemented in Python.

Main libraries and modules used:

* `pandas` for loading and analysing CSV result files.
* `matplotlib` for generating charts and figures.
* `json` and `csv` for storing simulation outputs.
* `os` for file and folder management.
* `random` for item generation, bidding behaviour, ordering and market noise.

## Requirements

This project uses:

* Python 3
* pandas
* matplotlib

Install the required libraries using:

```bash
pip install pandas matplotlib
```

## How to Run

### Basic Demonstration Run

`main.py` provides a simple demonstration run of the auction environment.

From the project root folder, run:

```bash
python src/main.py
```

This is only a small example simulation and is not the full experimental evaluation used in the report.

### Run the Full Experiments

To reproduce the four main experiments reported in the coursework, run:

```bash
python scripts/experiments.py
```

This runs the repeated simulations for the four experiments and stores the raw and summary result files in the `results/` folder.

### Run the Adaptive Learning Test

The adaptive learning behaviour graph uses a separate learning test. Run this before generating the final figures:

```bash
python scripts/learning_test.py
```

This creates `results/learning_metrics.json`, which is used by the analysis script to generate the adaptive learning behaviour graph.

### Generate Figures and Summary Tables

To regenerate the figures and processed result tables used in the report, run:

```bash
python scripts/analyse_results.py
```

The generated outputs are stored in the `results/figures/` folder.

### Full Reproduction Order

To fully reproduce all results and figures from the project root folder, run:

```bash
python scripts/experiments.py
python scripts/learning_test.py
python scripts/analyse_results.py
```

## Important Note on `main.py`

The `main.py` file is only a simple example simulation. The full experimental evaluation is implemented separately in the experiment script, the adaptive learning behaviour test is implemented in the learning test script, and the visualisation/statistical analysis is implemented in the analysis script.

The report results are based on the repeated experiment runs and generated CSV/figure outputs, not only on the basic `main.py` demonstration.

## Output Files

The `results/` folder contains the evidence used in the report.

### Raw Results

The `results/raw/` folder contains detailed experiment outputs from individual simulation runs.

### Summary Results

The `results/summaries/` folder contains processed CSV files with average results and standard deviations.

### Learning Metrics

The `results/learning_metrics.json` file contains the Adaptive Agent aggressiveness history generated by `scripts/learning_test.py`.

### Figures

The `results/figures/` folder contains the graphs used in the report, including:

* Strategy comparison charts.
* Competition line graphs.
* Memory access comparison charts.
* Market noise graphs.
* Adaptive learning behaviour graph.

## Evaluation Metrics

The agents are evaluated using the following metrics:

* **Average profit**: how much value an agent gained after paying winning bids.
* **Win rate**: how often an agent won auctions.
* **Average bid**: the average amount submitted by an agent when bidding.
* **Bidding efficiency**: how much profit was gained relative to spending.
* **Failed bids**: how often an agent could not place a valid bid.
* **Standard deviation**: how stable the results were across repeated simulation runs.

## Notes for Markers

The report explains the project motivation, related literature, agent design, environment design, experimental setup, results, discussion, reflection and future work.

The code in this repository supports the experiments described in the report. The `results/` folder is also included so that generated outputs and figures can be inspected without needing to rerun every experiment.