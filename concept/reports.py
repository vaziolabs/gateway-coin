import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from datetime import datetime

def create_analysis_report(scenarios_results):
    """Generate comprehensive analysis report with visualizations"""
    
    # Create report directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = f"reports"
    os.makedirs(report_dir, exist_ok=True)
    
    # Generate scenario summaries and trend analysis
    scenario_summaries = []
    for scenario in scenarios_results:
        df_scenario = pd.DataFrame(scenario)
        summary = create_scenario_summary(df_scenario)
        scenario_summaries.append(summary)
        
        # Generate individual scenario visualizations
        scenario_name = df_scenario['scenario_name'].iloc[0]
        create_scenario_charts(df_scenario, report_dir, scenario_name)
    
    # Create summary DataFrame
    df_summary = pd.DataFrame(scenario_summaries)
    
    # Generate HTML report
    create_html_report(df_summary, scenarios_results, report_dir, timestamp)

def create_scenario_summary(df):
    """Create statistical summary for a scenario"""
    metrics = ['price_stability_index', 'network_utility_score', 'liquidity_health_index',
              'market_pressure', 'convergence_rate', 'dynamic_spread']
    
    summary = {
        'scenario_name': df['scenario_name'].iloc[0],
        'epochs': len(df),
        'avg_epoch_duration': df['epoch_duration'].mean()
    }
    
    # Calculate statistics for each metric
    for metric in metrics:
        summary.update({
            f'{metric}_mean': df[metric].mean(),
            f'{metric}_min': df[metric].min(),
            f'{metric}_max': df[metric].max(),
            f'{metric}_std': df[metric].std()
        })
    
    return summary

def create_scenario_charts(df, report_dir, scenario_name):
    """Generate visualizations for individual scenario"""
    # Create directory for scenario
    scenario_dir = f"{report_dir}/{scenario_name.replace(' ', '_')}"
    os.makedirs(scenario_dir, exist_ok=True)
    
    try:
        # Stability metrics over time
        fig, ax = plt.subplots(figsize=(12, 6))
        stability_metrics = ['price_stability_index', 'network_utility_score', 'liquidity_health_index']
        df[stability_metrics].plot(ax=ax, alpha=0.7)
        ax.set_title(f'Stability Metrics Over Time - {scenario_name}')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Score')
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        plt.savefig(f"{scenario_dir}/stability_metrics.png")
        plt.close('all')
        
        # Market conditions over time
        fig, ax = plt.subplots(figsize=(12, 6))
        market_metrics = ['market_pressure', 'convergence_rate']
        df[market_metrics].plot(ax=ax, alpha=0.7)
        ax.set_title(f'Market Conditions Over Time - {scenario_name}')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Value')
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        plt.savefig(f"{scenario_dir}/market_conditions.png")
        plt.close('all')
        
        # Economic impacts over time
        fig, ax = plt.subplots(figsize=(12, 6))
        economic_metrics = ['daily_validator_reward_usdc', 'daily_holder_cost_usdc',
                          'validator_holder_net_usdc', 'transaction_fee_usdc']
        df[economic_metrics].plot(ax=ax, alpha=0.7)
        ax.set_title(f'Economic Impacts Over Time - {scenario_name}')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('USDC')
        plt.legend(bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        plt.savefig(f"{scenario_dir}/economic_impacts.png")
        plt.close('all')
        
    except Exception as e:
        print(f"Error generating charts for {scenario_name}: {str(e)}")
    finally:
        # Ensure all figures are closed
        plt.close('all')

def create_html_report(df_summary, scenarios_results, report_dir, timestamp):
    """Generate HTML report with tabs and visualizations"""
    html_report = f"""
    <html>
    <head>
        <title>Stability Analysis Report - {timestamp}</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 40px;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .tabs {{
                display: flex;
                cursor: pointer;
                margin-bottom: 20px;
            }}
            .tab {{
                padding: 10px 20px;
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 5px 5px 0 0;
                margin-right: 5px;
            }}
            .tab.active {{
                background-color: #fff;
                border-bottom: none;
            }}
            .tab-content {{
                display: none;
                border: 1px solid #ddd;
                border-radius: 0 5px 5px 5px;
                padding: 20px;
                background-color: #fff;
            }}
            .tab-content.active {{
                display: block;
            }}
            .metric-table {{ 
                border-collapse: collapse; 
                width: 100%;
                margin: 20px 0;
            }}
            .metric-table td, .metric-table th {{ 
                border: 1px solid #ddd; 
                padding: 12px; 
            }}
            .metric-table th {{
                background-color: #f8f9fa;
                font-weight: bold;
            }}
            .metric-table tr:nth-child(even) {{ 
                background-color: #f2f2f2; 
            }}
            .alert {{ 
                color: #dc3545;
                font-weight: bold;
            }}
            .success {{ 
                color: #28a745;
                font-weight: bold;
            }}
            .section {{
                margin: 30px 0;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1, h2, h3 {{
                color: #333;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
            }}
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                // Show first tab by default
                document.querySelector('.tab').classList.add('active');
                document.querySelector('.tab-content').style.display = 'block';
            }});

            function openTab(evt, tabName) {{
                // Hide all tab content
                var tabcontent = document.getElementsByClassName("tab-content");
                for (var i = 0; i < tabcontent.length; i++) {{
                    tabcontent[i].style.display = "none";
                }}

                // Remove active class from all tabs
                var tablinks = document.getElementsByClassName("tab");
                for (var i = 0; i < tablinks.length; i++) {{
                    tablinks[i].classList.remove("active");
                }}

                // Show the selected tab content and mark tab as active
                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.classList.add("active");
            }}
        </script>
    </head>
    <body>
        <h1>Stability Analysis Report</h1>
        <h2>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</h2>
        
        <div class="tabs">
            <div class="tab active" onclick="openTab(event, 'Overview')">Overview</div>
            {"".join(f'<div class="tab" onclick="openTab(event, \'{scenario["scenario_name"]}\')">{scenario["scenario_name"]}</div>' for scenario in df_summary.to_dict('records'))}
        </div>
        
        <div id="Overview" class="tab-content active">
            <h3>Simulation Summary</h3>
            {df_summary.to_html(classes='metric-table', float_format=lambda x: '{:.6f}'.format(x) if isinstance(x, float) else x)}
        </div>
        
        {"".join(f'''
        <div id="{scenario["scenario_name"]}" class="tab-content">
            <h3>{scenario["scenario_name"]}</h3>
            <div class="section">
                <h3>Stability Metrics</h3>
                <img src="{scenario["scenario_name"].replace(' ', '_')}/stability_metrics.png" alt="Stability Metrics">
                <h3>Market Conditions</h3>
                <img src="{scenario["scenario_name"].replace(' ', '_')}/market_conditions.png" alt="Market Conditions">
                <h3>Economic Impacts</h3>
                <img src="{scenario["scenario_name"].replace(' ', '_')}/economic_impacts.png" alt="Economic Impacts">
            </div>
        </div>
        ''' for scenario in df_summary.to_dict('records'))}
    </body>
    </html>
    """
    
    with open(f"{report_dir}/report.html", 'w') as f:
        f.write(html_report)

def print_scenario_results(description, results):
    """Print formatted scenario results to console for debugging"""
    print("\n" + "=" * 80)
    print(f"Scenario: {description}")
    print("=" * 80 + "\n")

    print("Core Stability Metrics:")
    print(f"Price Stability Index: {results['price_stability_index']:.4f}")
    print(f"Network Utility Score: {results['network_utility_score']:.4f}")
    print(f"Liquidity Health Index: {results['liquidity_health_index']:.4f}\n")

    print("Market Conditions:")
    print(f"Market Pressure: {results['market_pressure']:.4f}")
    print(f"Convergence Rate: {results['convergence_rate']:.4f}")
    print(f"Dynamic Spread: {results['dynamic_spread']:.4f}\n")

    print("Economic Impacts:")
    print(f"Validator Daily Reward: {results['daily_validator_reward_usdc']:.6f} USDC")
    print(f"Holder Daily Cost: {results['daily_holder_cost_usdc']:.6f} USDC")
    print(f"Validator Net Position: {results['validator_holder_net_usdc']:.6f} USDC")
    print(f"Transaction Fee: {results['transaction_fee_usdc']:.6f} USDC\n")

    print("System State:")
    breakers = results['circuit_breakers']
    print(f"Circuit Breakers: [Halt: {breakers['halt_trading']}, "
          f"Emergency: {breakers['emergency_spreads']}, "
          f"Rebase: {breakers['needs_rebase']}]")
    
    equilibrium = results['equilibrium']
    print(f"Equilibrium: {equilibrium['is_equilibrium']}")
    if not equilibrium['is_equilibrium']:
        print(f"Failing Metrics: {', '.join(equilibrium['failing_metrics'])}")
    print()