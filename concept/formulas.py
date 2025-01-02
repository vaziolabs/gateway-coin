import math
import numpy as np
from scipy import stats
from collections import deque

class MarketMetrics:
    def __init__(self, window_size=30):
        """Initialize market metrics with configurable window size"""
        self.price_window = deque(maxlen=window_size)
        self.volume_window = deque(maxlen=window_size)
        self.pressure_window = deque(maxlen=window_size)
        self.window_size = window_size

    def update_metrics(self, price, volume, pressure):
        """Update all metrics with new values"""
        self.price_window.append(price)
        self.volume_window.append(volume)
        self.pressure_window.append(pressure)

    def get_volatility(self):
        """Get current volatility based on price window"""
        return calculate_historical_volatility(list(self.price_window), self.window_size)

    def get_volume_weight(self):
        """Get current volume weight"""
        return calculate_volume_weight(list(self.volume_window))

def calculate_historical_volatility(price_history, window=30):
    """
    Calculate historical volatility using log returns
    """
    if len(price_history) < 2:
        return 0
    log_returns = np.log(np.array(price_history[1:]) / np.array(price_history[:-1]))
    return np.std(log_returns) * np.sqrt(window)

def calculate_volume_weight(volume_history):
    """
    Calculate volume-weighted importance factor
    """
    if not volume_history:
        return 1
    recent_vol = np.mean(volume_history[-5:])  # Last 5 periods
    total_vol = np.mean(volume_history)  # All periods
    return min(1, (recent_vol / total_vol) if total_vol > 0 else 1)

def calculate_order_imbalance(order_book):
    """
    Calculate order book imbalance
    """
    bid_volume = sum(order.volume for order in order_book.bids)
    ask_volume = sum(order.volume for order in order_book.asks)
    total_volume = bid_volume + ask_volume
    
    if total_volume == 0:
        return 0
        
    return (bid_volume - ask_volume) / total_volume

def calculate_time_weighted_flow(buys_history, sells_history, decay_factor=0.94):
    """
    Calculate time-weighted average flow with exponential decay
    """
    weights = np.array([decay_factor ** i for i in range(len(buys_history))])
    weighted_buys = np.sum(weights * np.array(buys_history))
    weighted_sells = np.sum(weights * np.array(sells_history))
    return weighted_buys - weighted_sells

def enhanced_price_stability_index(
    active_participants,
    total_holders,
    current_price,
    price_history,
    volume_history,
    market_depth,
    weights={
        'participation': 0.25,
        'price': 0.15,
        'volatility': 0.1,
        'volume': 0.1,
        'depth': 0.2
    }
):
    """
    Enhanced PSI with improved stability calculation
    """
    # Current issue: Never reaches optimal stability
    # Fix: Add adaptive baseline and improved scaling
    if total_holders <= 0:
        raise ValueError("Total holders must be positive")
        
    participation_ratio = min(1, active_participants / total_holders)
    price_deviation = abs(1 - current_price)
    
    # Improved volatility calculation with minimum baseline
    volatility = max(0.1, calculate_historical_volatility(price_history))
    volume_weight = calculate_volume_weight(volume_history)
    
    # Exponential depth scaling
    depth_factor = 1 - math.exp(-market_depth / 1000)
    
    # Adaptive baseline based on market conditions
    adaptive_base = 0.4 + (0.1 * participation_ratio + 0.1 * depth_factor)
    
    # Combined stability score with adaptive baseline
    stability = adaptive_base + (
        weights['participation'] * participation_ratio +
        weights['price'] * (1 / (1 + price_deviation)) +
        weights['volatility'] * (1 / (1 + volatility)) +
        weights['volume'] * volume_weight +
        weights['depth'] * depth_factor
    )
    
    return min(1, max(adaptive_base, stability))

def enhanced_network_utility_score(
    daily_volume,
    target_volume,
    cross_chain_transfers,
    target_transfers,
    unique_addresses,
    target_addresses,
    success_rate
):
    """
    Enhanced network utility with multiple metrics
    """
    # Core metrics
    volume_score = min(1, daily_volume / target_volume)
    transfer_score = min(1, cross_chain_transfers / target_transfers)
    address_score = min(1, unique_addresses / target_addresses)
    
    # Weighted combination
    weights = {
        'volume': 0.35,
        'transfers': 0.25,
        'addresses': 0.25,
        'success_rate': 0.15
    }
    
    final_score = (
        weights['volume'] * volume_score +
        weights['transfers'] * transfer_score +
        weights['addresses'] * address_score +
        weights['success_rate'] * success_rate
    )
    
    return min(1, max(0, final_score))

def enhanced_liquidity_health_index(
    active_participants,
    total_holders,
    current_liquidity,
    stability_reserve,
    required_reserve,
    slippage_impact,
    depth_distribution
):
    """
    Enhanced liquidity health with depth analysis
    """
    # Base ratios
    participation_ratio = active_participants / total_holders
    liquidity_ratio = current_liquidity / 0.8
    reserve_ratio = stability_reserve / required_reserve
    
    # Slippage and depth factors
    slippage_factor = 1 / (1 + slippage_impact)
    depth_score = calculate_depth_score(depth_distribution)
    
    # Combined health score
    base_health = 0.3 + (
        0.25 * participation_ratio +
        0.20 * liquidity_ratio +
        0.15 * reserve_ratio +
        0.10 * slippage_factor
    )
    
    # Apply depth adjustment
    final_health = base_health * (0.8 + 0.2 * depth_score)
    
    return min(1, max(0, final_health))

def enhanced_market_pressure(
    buys_volume,
    sells_volume,
    liquidity_pool,
    order_book,
    volatility_history,
    time_window=30
):
    """
    Enhanced market pressure with multiple factors
    """
    # Basic flow pressure
    net_flow = buys_volume - sells_volume
    base_pressure = net_flow / liquidity_pool
    
    # Order book imbalance
    imbalance = calculate_order_imbalance(order_book)
    
    # Volatility impact
    vol_impact = calculate_historical_volatility(volatility_history, time_window)
    
    # Combined pressure score
    weights = {
        'flow': 0.4,
        'imbalance': 0.35,
        'volatility': 0.25
    }
    
    pressure = (
        weights['flow'] * base_pressure +
        weights['imbalance'] * imbalance +
        weights['volatility'] * vol_impact
    )
    
    # Normalize to [-1, 1] range
    return np.tanh(pressure)

def calculate_depth_score(depth_distribution):
    """
    Calculate liquidity depth score based on distribution
    """
    # Analyze price levels and corresponding liquidity
    concentrations = np.array([d['liquidity'] for d in depth_distribution])
    price_levels = np.array([d['price'] for d in depth_distribution])
    
    # Calculate concentration Gini coefficient
    gini = calculate_gini_coefficient(concentrations)
    
    # Calculate price level coverage
    coverage = len(price_levels) / 100  # Normalize to expected coverage
    
    return (1 - gini) * min(1, coverage)

def calculate_gini_coefficient(values):
    """
    Calculate Gini coefficient for distribution analysis
    """
    values = np.sort(values)
    n = len(values)
    index = np.arange(1, n + 1)
    return (np.sum((2 * index - n - 1) * values)) / (n * np.sum(values))

def price_stability_index(price, pressure, validator_participation, holder_participation):
    """
    Calculate Price Stability Index (PSI) based on market conditions and participation.
    Target: Price convergence to 1 USDC with high participation.
    """
    price_stability = 1 / (1 + abs(1 - price))
    market_stability = 1 / (1 + abs(pressure))
    participation_impact = (validator_participation + holder_participation) / 2
    
    return min(1, (0.4 * price_stability + 
                   0.3 * market_stability +
                   0.3 * participation_impact))

def validator_reward(base_reward_rate, daily_transactions, validator_count, psi):
    """
    Calculate validator rewards based on transaction share and stability.
    90% of network revenue goes to validators.
    """
    transaction_share = daily_transactions / max(1, validator_count)
    market_reward = transaction_share * base_reward_rate * 0.9
    stability_bonus = market_reward * psi
    
    return market_reward + stability_bonus

def holder_cost(base_rate, time_held, balance, price_stability_index):
    """
    Calculate holding cost with logarithmic scaling.
    From whitepaper: D(t,L) = H * (1/L) * t * (1 - stability_index)
    """
    # Logarithmic scaling for large balances
    balance_factor = math.log2(1 + balance/1000)
    
    # Higher costs during instability
    stability_factor = 1 - price_stability_index
    
    return base_rate * time_held * balance_factor * stability_factor

def validator_holder_cost(holder_cost, validator_reward, participation_score):
    """
    Calculate net cost/reward for validators who are also holders.
    """
    return holder_cost - (validator_reward * participation_score)

def transaction_fee(base_fee, price_stability_index, transaction_size, liquidity_ratio):
    """
    Dynamic fee calculation based on market conditions.
    From whitepaper: S(v,s) = β * (1/L) * (1 + log₂(v/v₀)) * I(s)
    """
    # Volume scaling
    volume_factor = 1 + math.log2(1 + transaction_size/10000)
    
    # Liquidity impact
    liquidity_factor = 1 / max(0.1, liquidity_ratio)
    
    # Stability adjustment
    stability_factor = 1 + (1 - price_stability_index)
    
    return base_fee * volume_factor * liquidity_factor * stability_factor

def network_utility_score(daily_volume, target_volume, cross_chain_transfers, target_transfers):
    """
    Calculate network utility based on volume and transfer metrics.
    From factor2.md: Combined volume and transfer effectiveness.
    """
    volume_score = min(1, daily_volume / target_volume)
    transfer_score = min(1, cross_chain_transfers / target_transfers)
    
    # Add minimum baseline and logarithmic scaling
    base_score = 0.2
    scaling_factor = math.log1p(daily_volume/1000000) / math.log1p(target_volume/1000000)
    
    return min(1, max(base_score, (volume_score + transfer_score) * scaling_factor))

def liquidity_health_index(active_participants, total_holders, current_liquidity, stability_reserve, required_reserve):
    """
    Calculate liquidity health based on whitepaper formula:
    H(t) = (AP/TH) * (L(t)/0.8) * (SR(t)/RR)
    """
    participation_ratio = active_participants / max(1, total_holders)
    liquidity_ratio = current_liquidity / 0.8  # Target liquidity ratio
    reserve_ratio = stability_reserve / max(1, required_reserve)
    
    # Combined health score with minimum baseline
    return max(0.2, min(1, participation_ratio * liquidity_ratio * reserve_ratio))

def dynamic_spread(base_spread, current_liquidity, volume, baseline_volume):
    """
    Calculate dynamic spread based on market conditions.
    Base spread typically 0.001 USDC
    """
    volume_factor = 1 + math.log2(1 + volume / baseline_volume)
    return base_spread * (1 / current_liquidity) * volume_factor

def emergency_spread(base_spread, current_liquidity, target_liquidity=0.8):
    """
    Calculate emergency spread during stress conditions.
    """
    return base_spread * max(1, (target_liquidity / current_liquidity) ** 2)

def rebase_supply(current_supply, current_price, target_price=1.0):
    """
    Calculate new supply after rebase operation.
    """
    return (target_price / current_price) * current_supply

def stability_reserve_requirement(total_supply, total_decay_penalties):
    """
    Calculate minimum stability pool size needed.
    """
    return max(0.2 * total_supply, total_decay_penalties)

def inflation_rate(total_supply_t0, total_supply_t1):
    """
    Calculate inflation rate between two time periods
    Target range: -2% to +2% annual
    """
    return ((total_supply_t1 - total_supply_t0) / total_supply_t0) * 100

def circuit_breaker_conditions(
    liquidity_ratio,
    price,
    health_index,
    min_liquidity=0.05,
    emergency_liquidity=0.15,
    max_price_deviation=0.3
):
    """
    Determine if circuit breakers should activate
    Returns tuple of (halt_trading, emergency_spreads, needs_rebase)
    """
    halt_trading = liquidity_ratio < min_liquidity or health_index < 0.2
    emergency_spreads = liquidity_ratio < emergency_liquidity or health_index < 0.5
    needs_rebase = abs(1 - price) > max_price_deviation
    
    return (halt_trading, emergency_spreads, needs_rebase)

def market_pressure(buys_volume, sells_volume, liquidity_pool, active_validators):
    """
    Calculate market pressure with validator influence.
    Formula from whitepaper: dp/dt = -α(p-1) - βD(t,L) + γS(v,s)
    """
    if liquidity_pool == 0:
        return 0
        
    net_flow = buys_volume - sells_volume
    total_volume = buys_volume + sells_volume
    validator_factor = math.log1p(active_validators / 1000)
    
    # Volume-weighted pressure with validator influence
    raw_pressure = (net_flow / total_volume) * math.log1p(total_volume / liquidity_pool)
    return np.tanh(raw_pressure * validator_factor)  # Normalize to [-1, 1]

def convergence_rate(
    current_price,
    target_price,
    market_pressure,
    stability_index
):
    """
    Calculate expected price convergence rate
    Returns estimated time to reach target in epochs
    """
    pressure_factor = 1 / (1 + abs(market_pressure))
    stability_factor = stability_index
    price_gap = abs(current_price - target_price)
    
    return price_gap / (pressure_factor * stability_factor)

def equilibrium_state(
    price_stability_index,
    liquidity_health_index,
    network_utility_score,
    convergence_rate,
    target_thresholds={
        'psi_min': 0.8,
        'lhi_min': 0.7,
        'nus_min': 0.6,
        'conv_max': 10
    }
):
    """
    Determine if system is in equilibrium state
    Returns (is_equilibrium, failing_metrics)
    """
    checks = {
        'price_stability': price_stability_index >= target_thresholds['psi_min'],
        'liquidity_health': liquidity_health_index >= target_thresholds['lhi_min'],
        'network_utility': network_utility_score >= target_thresholds['nus_min'],
        'convergence': convergence_rate <= target_thresholds['conv_max']
    }
    
    failing = [k for k, v in checks.items() if not v]
    return (len(failing) == 0, failing)


def determine_epoch_duration(transaction_volume, network_throughput, market_volatility):
    # Example logic to determine epoch duration
    base_epoch_duration = 10  # seconds
    if transaction_volume > network_throughput * 0.8:
        return max(5, base_epoch_duration - 2)  # Shorten epoch during high load
    elif market_volatility > 0.5:
        return max(5, base_epoch_duration - 1)  # Shorten epoch during high volatility
    else:
        return base_epoch_duration

def determine_matrix_size(transaction_volume, expected_growth, base_matrix_size=256):
    # Example logic to determine matrix size
    if expected_growth > 0.2:
        return min(1024, base_matrix_size * 2)  # Increase size for high growth
    elif expected_growth < 0.1:
        return max(16, base_matrix_size / 2)  # Decrease size for low growth
    else:
        return base_matrix_size