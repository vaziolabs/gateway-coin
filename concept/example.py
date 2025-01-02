from formulas import *
from reports import *

def calculate_economics(
    validator_count,
    total_holders,
    daily_transactions,
    current_price,
    avg_transaction_size,
    avg_holding_balance,
    days_held,
    liquidity_ratio=0.8,
    network_participation_indicator=1.0,
    cross_chain_transfers=1000,
    target_transfers=2000,
    stability_reserve=1000000,
    buys_volume=50000,
    sells_volume=50000,
    market_metrics=None
):
    """Calculate real-world economics with enhanced validation and metrics tracking"""
    # Input validation
    if validator_count <= 0 or total_holders <= 0:
        raise ValueError("Validator count and total holders must be positive")
    if current_price <= 0:
        raise ValueError("Price must be positive")
    if liquidity_ratio < 0 or liquidity_ratio > 1:
        raise ValueError("Liquidity ratio must be between 0 and 1")

    # Initialize or use existing market metrics
    if market_metrics is None:
        market_metrics = MarketMetrics()
    
    # Calculate market pressure and volatility
    pressure = market_pressure(
        buys_volume, 
        sells_volume, 
        liquidity_ratio * stability_reserve,
        validator_count
    )
    
    # Update market metrics
    market_metrics.update_metrics(current_price, daily_transactions, pressure)
    
    # Calculate volatility from metrics
    volatility = market_metrics.get_volatility()
    
    # Determine epoch duration based on market conditions
    epoch_duration = determine_epoch_duration(
        transaction_volume=daily_transactions,
        network_throughput=validator_count * 1000,  # Assuming 1000 tx per validator capacity
        market_volatility=volatility
    )

    # Calculate validator participation ratio
    validator_participation = validator_count / max(1000, total_holders)
    holder_participation = daily_transactions / max(1000, total_holders)

    # Calculate enhanced price stability index
    psi = price_stability_index(
        current_price,
        pressure,
        validator_participation,
        holder_participation
    )

    # Base rates (USDC)
    BASE_VALIDATOR_REWARD = 0.001
    BASE_HOLDING_RATE = 0.00002
    BASE_TX_FEE = 0.002
    BASE_SPREAD_RATE = 0.001
    TARGET_DAILY_VOLUME = 200000000000  # $200B daily volume target

    # Calculate network utility score
    nus = network_utility_score(
        daily_transactions, 
        TARGET_DAILY_VOLUME,
        cross_chain_transfers, 
        target_transfers
    )
    
    # Calculate liquidity health
    required_reserve = stability_reserve_requirement(
        total_supply=10000000,  # Example total supply
        total_decay_penalties=50000  # Example daily decay
    )
    
    lhi = liquidity_health_index(
        validator_count,
        total_holders,
        liquidity_ratio,
        stability_reserve,
        required_reserve
    )

    # Circuit breaker check
    halt_trading, emergency_spreads, needs_rebase = circuit_breaker_conditions(
        liquidity_ratio, 
        current_price, 
        lhi
    )

    # Calculate spreads and fees
    spread = (emergency_spread(BASE_SPREAD_RATE, liquidity_ratio) 
             if emergency_spreads 
             else dynamic_spread(BASE_SPREAD_RATE, liquidity_ratio, 
                               daily_transactions, TARGET_DAILY_VOLUME))

    # Core economic calculations
    daily_reward = validator_reward(
        BASE_VALIDATOR_REWARD,
        daily_transactions,
        validator_count,
        psi  # Added PSI parameter
    )
    
    daily_cost = holder_cost(
        BASE_HOLDING_RATE,
        days_held,
        avg_holding_balance,
        psi
    )
    
    validator_net = validator_holder_cost(
        daily_cost,
        daily_reward,
        validator_participation  # Using validator participation instead of fixed value
    )
    
    tx_fee = transaction_fee(
        BASE_TX_FEE,
        psi,
        avg_transaction_size,
        liquidity_ratio  # Added liquidity ratio parameter
    )

    # Calculate equilibrium state
    is_equilibrium, failing_metrics = equilibrium_state(
        psi, lhi, nus, pressure  # Using pressure instead of conv_rate
    )

    # Calculate convergence rate
    conv_rate = convergence_rate(
        current_price=current_price,
        target_price=1.0,  # Target price is always 1 USDC
        market_pressure=pressure,
        stability_index=psi
    )

    return {
        "price_stability_index": psi,
        "network_utility_score": nus,
        "liquidity_health_index": lhi,
        "market_pressure": pressure,
        "convergence_rate": conv_rate,
        "daily_validator_reward_usdc": daily_reward,
        "daily_holder_cost_usdc": daily_cost,
        "validator_holder_net_usdc": validator_net,
        "transaction_fee_usdc": tx_fee,
        "dynamic_spread": spread,
        "circuit_breakers": {
            "halt_trading": halt_trading,
            "emergency_spreads": emergency_spreads,
            "needs_rebase": needs_rebase
        },
        "equilibrium": {
            "is_equilibrium": is_equilibrium,
            "failing_metrics": failing_metrics
        },
        "epoch_duration": epoch_duration
    }

def run_scenario(description, scenario_params, epochs=10040):
    """Run scenario over a specified number of epochs and return results"""
    results_over_time = []
    current_params = scenario_params.copy()
    
    for epoch in range(epochs):
        # Calculate market pressure and adjust parameters
        results = calculate_economics(**current_params)
        
        # Update parameters based on market conditions
        if results['circuit_breakers']['needs_rebase']:
            # Price correction during rebase
            current_params['current_price'] = max(0.95, min(1.05, 
                (1 + current_params['current_price']) / 2))
            
        # Gradual market stabilization
        if abs(current_params['current_price'] - 1.0) > 0.01:
            # Price gradually moves toward 1.0
            price_adjustment = (1.0 - current_params['current_price']) * 0.01
            current_params['current_price'] += price_adjustment
            
            # Volumes stabilize
            volume_delta = (current_params['buys_volume'] - 
                          current_params['sells_volume']) * 0.05
            current_params['buys_volume'] -= volume_delta
            current_params['sells_volume'] += volume_delta
            
        # Liquidity recovery
        if current_params['liquidity_ratio'] < 0.7:
            current_params['liquidity_ratio'] = min(0.8, 
                current_params['liquidity_ratio'] * 1.02)
            
        # Market participant behavior
        if results['price_stability_index'] < 0.8:
            # Reduced activity during instability
            current_params['daily_transactions'] *= 0.95
            current_params['total_holders'] *= 0.99
        else:
            # Growth during stability
            current_params['daily_transactions'] *= 1.01
            current_params['total_holders'] *= 1.005
        
        # Record results
        results['epoch'] = epoch
        results['scenario_name'] = description
        results_over_time.append(results)
    
    print_scenario_results(description, results)

    return results_over_time

if __name__ == "__main__":
    # Define comprehensive stress test scenarios
    stress_scenarios = [
        # === STABLE MARKET CONDITIONS ===
        {
            "name": "Stable - More Transactions Than Validators",
            "validator_count": 5000,
            "total_holders": 1000000,
            "daily_transactions": 35000000,      # 7000x validators
            "current_price": 1.001,              # Very stable
            "avg_transaction_size": 6000,
            "avg_holding_balance": 10000,
            "days_held": 30,
            "liquidity_ratio": 0.8,
            "cross_chain_transfers": 100000,
            "buys_volume": 109000000000,
            "sells_volume": 109000000000
        },
        {
            "name": "Stable - More Holders Than Transactions",
            "validator_count": 5000,
            "total_holders": 50000000,          # More holders than daily tx
            "daily_transactions": 35000000,
            "current_price": 1.002,
            "avg_transaction_size": 6000,
            "avg_holding_balance": 8000,
            "days_held": 90,                    # Longer hold time
            "liquidity_ratio": 0.8,
            "cross_chain_transfers": 80000,
            "buys_volume": 109000000000,
            "sells_volume": 109000000000
        },
        {
            "name": "Stable - More Validators Than Transactions",
            "validator_count": 100000,          # High validator count
            "total_holders": 1000000,
            "daily_transactions": 50000,        # Low tx count
            "current_price": 1.001,
            "avg_transaction_size": 100000,     # Larger trades
            "avg_holding_balance": 15000,
            "days_held": 30,
            "liquidity_ratio": 0.85,
            "cross_chain_transfers": 10000,
            "buys_volume": 5000000000,
            "sells_volume": 5000000000
        },

        # === HIGH PRESSURE CONDITIONS ===
        {
            "name": "High Pressure - More Transactions Than Validators",
            "validator_count": 4000,            # Reduced validators
            "total_holders": 800000,
            "daily_transactions": 50000000,     # 12500x validators
            "current_price": 1.4,
            "avg_transaction_size": 8000,
            "avg_holding_balance": 12000,
            "days_held": 15,                    # Shorter hold time
            "liquidity_ratio": 0.6,
            "cross_chain_transfers": 200000,
            "buys_volume": 180000000000,
            "sells_volume": 60000000000
        },
        {
            "name": "High Pressure - More Holders Than Transactions",
            "validator_count": 4000,
            "total_holders": 60000000,          # High holder count
            "daily_transactions": 45000000,
            "current_price": 1.35,
            "avg_transaction_size": 7500,
            "avg_holding_balance": 11000,
            "days_held": 20,
            "liquidity_ratio": 0.65,
            "cross_chain_transfers": 180000,
            "buys_volume": 160000000000,
            "sells_volume": 70000000000
        },
        {
            "name": "High Pressure - More Validators Than Transactions",
            "validator_count": 150000,          # Very high validator count
            "total_holders": 800000,
            "daily_transactions": 40000,
            "current_price": 1.25,
            "avg_transaction_size": 150000,     # Larger trades
            "avg_holding_balance": 13000,
            "days_held": 25,
            "liquidity_ratio": 0.7,
            "cross_chain_transfers": 15000,
            "buys_volume": 4000000000,
            "sells_volume": 2000000000
        },

        # === LIQUIDITY CRISIS CONDITIONS ===
        {
            "name": "Crisis - More Transactions Than Validators",
            "validator_count": 2500,
            "total_holders": 600000,
            "daily_transactions": 70000000,     # 28000x validators
            "current_price": 0.7,
            "avg_transaction_size": 4000,
            "avg_holding_balance": 8000,
            "days_held": 5,                     # Very short hold time
            "liquidity_ratio": 0.15,
            "cross_chain_transfers": 500000,
            "buys_volume": 40000000000,
            "sells_volume": 160000000000
        },
        {
            "name": "Crisis - More Holders Than Transactions",
            "validator_count": 2000,
            "total_holders": 80000000,          # High holder count
            "daily_transactions": 65000000,
            "current_price": 0.65,
            "avg_transaction_size": 3800,
            "avg_holding_balance": 7500,
            "days_held": 10,
            "liquidity_ratio": 0.2,
            "cross_chain_transfers": 450000,
            "buys_volume": 35000000000,
            "sells_volume": 150000000000
        },
        {
            "name": "Crisis - More Validators Than Transactions",
            "validator_count": 200000,          # Very high validator count
            "total_holders": 500000,
            "daily_transactions": 30000,
            "current_price": 0.75,
            "avg_transaction_size": 200000,     # Large trades
            "avg_holding_balance": 6000,
            "days_held": 15,
            "liquidity_ratio": 0.25,
            "cross_chain_transfers": 8000,
            "buys_volume": 3000000000,
            "sells_volume": 9000000000
        },

        # === RECOVERY CONDITIONS ===
        {
            "name": "Recovery - More Transactions Than Validators",
            "validator_count": 3500,
            "total_holders": 750000,
            "daily_transactions": 45000000,     # ~13000x validators
            "current_price": 0.98,
            "avg_transaction_size": 5000,
            "avg_holding_balance": 9000,
            "days_held": 25,
            "liquidity_ratio": 0.75,
            "cross_chain_transfers": 150000,
            "buys_volume": 120000000000,
            "sells_volume": 90000000000
        },
        {
            "name": "Recovery - More Holders Than Transactions",
            "validator_count": 3000,
            "total_holders": 70000000,          # High holder count
            "daily_transactions": 40000000,
            "current_price": 0.97,
            "avg_transaction_size": 4800,
            "avg_holding_balance": 8500,
            "days_held": 35,
            "liquidity_ratio": 0.7,
            "cross_chain_transfers": 130000,
            "buys_volume": 110000000000,
            "sells_volume": 85000000000
        },
        {
            "name": "Recovery - More Validators Than Transactions",
            "validator_count": 180000,          # Very high validator count
            "total_holders": 700000,
            "daily_transactions": 35000,
            "current_price": 0.99,
            "avg_transaction_size": 175000,
            "avg_holding_balance": 9500,
            "days_held": 40,
            "liquidity_ratio": 0.8,
            "cross_chain_transfers": 12000,
            "buys_volume": 3500000000,
            "sells_volume": 2800000000
        }
    ]

    # Run scenarios and collect results
    scenarios_results = []
    for scenario in stress_scenarios:
        name = scenario.pop("name")
        results = run_scenario(name, scenario)
        scenarios_results.append(results)
        
    # Generate analysis report
    create_analysis_report(scenarios_results)
    
    print("\nAnalysis report generated in reports/stability_analysis_<timestamp>/")