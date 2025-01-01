# Gateway Token (GATE)

A protocol-agnostic cross-chain bridge enabling seamless asset transfers between blockchain networks, built on FragMint Chain. Gateway Token leverages FragMint's blockchain for exceptional overhead through domain-specific utilization and validation using a hybrid consensus proof mechanism. The system employs the STOQ (Secure Tokenization Over QUIC) protocol to ensure secure tokenization with post-quantum TLS and DNS verification for certification/authorization of network participants.

The cross-chain bridge supports multiple major blockchain networks:
- Ethereum (ERC-20, ERC-721, ERC-1155)
- Solana
- Bitcoin
- Polygon
- NEAR
- Radix
- Cosmos (ATOM)
- 0x Protocol
- Dogecoin

The Gateway Token functions as a crypto layer for contract execution, interfacing with the FragMint BlockMesh API to manage assets through FragMint's secure infrastructure, enabling real-world transactions on a stable and secure platform.

## Overview
![Architecture Overview](image.png)

## Architecture
The Gateway Token operates on FragMint's block-matrix architecture, utilizing:
- Temporal-spatial epochs organized in tensor format
- 2D vector allocations for improved transaction mapping
- Matrix-based state verification instead of traditional Merkle trees
- Multi-dimensional transaction routing

### Price Stability Mechanism
- **Time-Decay Value System**:
  - Base value: 1:1 USDC peg for immediate transactions
  - Progressive demurrage based on holding duration
  - Value decay tracked through tensor epochs
  - No staking or yield mechanisms

### Economic Design
- **Anti-Speculation Features**:
  - Transaction fees increase with token age
  - No yield/staking rewards
  - Programmatic demurrage (negative interest)
  - Value derived purely from utility as bridge medium

### Temporal Value Mechanics
- **Decay Formula**:
  - Initial Value: 1 USDC
  - Decay Rate: [X]% per tensor epoch
  - Maximum Holding Penalty: [Y]%
  - Reset on transfer/bridge operation

### Stability Pool Economics
- **Revenue Structure**:
  - Time-decay penalties feed stability pool
  - Bridge operation fees
  - Tensor transaction fees
- **Usage**:
  - Maintaining 1:1 USDC liquidity
  - Emergency stability operations
  - Cross-chain bridge reserves

### Matrix-Based Implementation
- Tensor epochs track holding duration
- 2D vector mapping of token age
- Cross-chain decay synchronization
- Real-time value adjustment calculations

### Circuit Breakers
- Maximum decay rate limits
- Emergency value floor
- Cross-chain synchronization delays
- Minimum transaction thresholds

### Elastic Supply Operations
- **Rebase Mechanics**:
  - Automatic token quantity adjustments for all holders based on price movements
  - Example: 10 GATE → 20 GATE when price doubles, maintaining $1.00 per token value
  - Rebases occur at epoch boundaries within the tensor structure

### Stability Pool Economics
- **Earnings Structure**:
  - Accumulates fees from tensor transactions
  - Revenue from epoch updates across the network
  - Cross-chain bridge operation fees
- **Fee Distribution**:
  - Portion allocated to maintain stability reserves
  - Remainder used for automatic rebase operations
  - Emergency buffer for extreme market conditions

### Matrix-Based Rebase Protocol
- Tensor-synchronized supply adjustments
- 2D vector tracking of holder balances
- Epoch-boundary rebase calculations
- Cross-chain balance synchronization
- Proportional distribution across all wallets

## Key Features
- Multi-chain support (Ethereum, Solana, Bitcoin, Polygon, NEAR, Radix, Cosmos)
- Secure bridge operations via STOQ Protocol
- Decentralized validator network
- Native token (GATE) for governance and operations

## Token Economics
- **Target Price**: $1.00 (1:1 with USDC)
- **Total Supply**: Dynamic based on demand
- **Distribution**:
  - Validator Pool: [X]%
  - Stability Reserve: [Y]% (New)
  - Development Fund: [Z]%
  - Community Reserve: [W]%

## Core Components

### 1. Bridge Infrastructure
- Asset locking/unlocking mechanism
- Cross-chain state management
- Protocol-specific bridge implementations
- Liquidity pool management

### 2. Security
- STOQ Protocol for secure transactions
- Decentralized Certificate Authority
- Multi-layer verification
- Emergency controls

### 3. Network Operations
- Binary participation verification (device/wallet/network)
- One active device per wallet per network domain
- Transaction routing
- Fee distribution
- State verification

## Integration

### Quick Start
```solidity
interface IGATEIntegration {
    // Core integration functions
    function integrateGATE(
        address gateToken,
        uint256 amount,
        bytes32 tensorEpoch,
        bytes calldata integrationData
    ) external returns (bool);

    function withdrawGATE(
        address recipient,
        uint256 amount,
        bytes32 tensorEpoch,
        bytes calldata withdrawData
    ) external returns (bool);

    // Rebase tracking
    function getRebaseRatio(
        bytes32 tensorEpoch
    ) external view returns (uint256 ratio);

    function getAdjustedBalance(
        address account,
        bytes32 tensorEpoch
    ) external view returns (uint256 balance);

    // Matrix state verification
    function verifyMatrixState(
        bytes32 tensorEpoch,
        bytes calldata stateProof
    ) external view returns (bool);
}

interface IGATEEvents {
    event RebaseOccurred(
        bytes32 indexed tensorEpoch,
        uint256 rebaseRatio,
        uint256 newTotalSupply
    );
    
    event TensorStateUpdate(
        bytes32 indexed tensorEpoch,
        bytes32 stateRoot,
        uint256 timestamp
    );
}
```

### Integration Requirements
- Matrix-state verification capability
- Tensor epoch synchronization
- Rebase-aware balance tracking
- Minimum stability pool liquidity
- Cross-chain compatibility verification
- Security audit compliance

### Integration Considerations
- Account for elastic supply changes during rebases
- Handle tensor epoch boundaries
- Implement matrix-based state verification
- Monitor stability pool status
- Support cross-chain balance synchronization

## Documentation
For detailed integration guides and API documentation, visit [docs link]

## Risk Management
- Transaction limits and thresholds
- Multi-signature security
- Automated monitoring
- Emergency pause mechanisms

## Installation
to install Solana we need to ensure protobuf is installed, as well as the solana cli and anchor
`sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"`
`cargo install --git https://github.com/coral-xyz/anchor --tag v0.30.1 anchor-cli`

## Commands to update solana
`solana config set --url mainnet-beta`
`solana config set --url devnet`
`solana config set --url localhost`
`solana config set --url testnet`

### Economic Equilibrium Model

#### Transaction Spread Formula
```
S(v,s) = β * (1/L) * I(s)

Where:
S(v,s) = Spread per transaction
β = Base spread rate (e.g., 0.001)
L = Current liquidity ratio
I(s) = Network participation indicator {0,1}
```

#### Network Participant Share
```
R(p) = S(v,s) * P(w,d,n)

Where:
R(p) = Reward per participant
P(w,d,n) = min(1, w * d * n)
w = wallet constraint {0,1}
d = device constraint {0,1}
n = network domain constraint {0,1}
```

#### Holding Cost (Anti-Speculation)
```
D(t,L) = H * (1/L) * t * (1 - stability_index)

Where:
D(t,L) = Decay cost
H = Base holding rate
L = Liquidity ratio
t = Time held
stability_index = min(1, (AP/TH) * (1/|1-p(t)|))
```

Note: Decay approaches zero as price stability increases

#### Net Position Formula
```
NP = Tv * S(v) - D(t,L)

Where:
Tv = Transaction volume
Must satisfy: NP = 0 when price = $1 and volume > 0
```

### Stability Mechanics

#### Value Preservation Conditions
```
For any epoch E:
∑(Inflows) = ∑(Outflows)
Where:
- Inflows = New deposits + Network rewards
- Outflows = Withdrawals + Decay penalties
```

#### Liquidity Balance
```
L(t) = ∑(Active_Holdings) / ∑(Total_Supply)

Target: 0.7 ≤ L(t) ≤ 0.9
```

### Network Participation Rewards

#### Transaction Fee Distribution
```
F(p) = b * (1 + μp)

Where:
F(p) = Fee for participant p
b = Base fee (0.001 USDC)
μ = Participation multiplier
p = Participation score (0 to 1)
```

#### Negative Interest Offset
```
O(a) = ∑(D(t)) * (τa/τt)

Where:
O(a) = Offset amount
τa = Active participation time
τt = Total time period
```

### Stability Pool Mechanics

#### Reserve Requirements
```
SR(t) = max(0.2 * TS, ∑(D(t)))

Where:
SR(t) = Stability reserve at time t
TS = Total supply
∑(D(t)) = Sum of all decay penalties
```

#### Network Health Index
```
H(t) = (AP/TH) * (L(t)/0.8) * (SR(t)/RR)

Where:
H(t) = Health index (target > 1.0)
AP = Active participants
TH = Total holders
L(t) = Liquidity ratio
RR = Required reserve
```

### Integration Considerations
- Balance tracking must account for both decay and participation rewards
- Real-time participation metrics influence reward distribution
- Cross-chain operations must maintain consistent reward/decay ratios
- Tensor epochs synchronize reward and decay calculations

### Real-World Examples

#### 1. Transaction Spread Example
```
S(v,s) = β * (1/L) * I(s)
β = 0.001 (0.1% base spread)
I(s) = Binary participation indicator {0,1}

Scenario A (Valid Network Participant):
L = 0.9 (90% of tokens actively used)
I(s) = 1 (verified device/wallet/network)
S(v,s) = 0.001 * (1/0.9) * 1 = 0.00111
→ 0.111% spread per transaction

Scenario B (Invalid Participant):
L = 0.9 (90% of tokens actively used)
I(s) = 0 (unverified or duplicate device/wallet)
S(v,s) = 0.001 * (1/0.9) * 0 = 0
→ Transaction rejected
```

#### 2. Network Participant Reward Example
```
R(p) = S(v,s) * P(w,d,n)

Example with $1M daily volume:
Spread (S(v,s)) = 0.00111 (from high liquidity scenario)

Participant A (Valid Configuration):
w = 1 (unique wallet)
d = 1 (unique device)
n = 1 (valid network domain)
P(w,d,n) = min(1, 1 * 1 * 1) = 1
R = 0.00111 * 1
→ Full spread earnings

Participant B (Invalid Configuration):
w = 1 (unique wallet)
d = 0 (duplicate device)
n = 1 (valid network domain)
P(w,d,n) = min(1, 1 * 0 * 1) = 0
→ No participation allowed
```

#### 3. Holding Cost Example with Stability Index
```
D(t,L) = H * (1/L) * t * (1 - stability_index)
H = 0.0005 (0.05% base holding rate)
t = days held

Stable Market (p ≈ 1.00):
L = 0.9
stability_index = 0.98 (near perfect stability)
1 day hold: D = 0.0005 * (1/0.9) * 1 * (1-0.98) = 0.000011 (0.001%)
→ Minimal decay during stability

Unstable Market (p = 1.20):
L = 0.5
stability_index = 0.40 (high instability)
1 day hold: D = 0.0005 * (1/0.5) * 1 * (1-0.40) = 0.0006 (0.06%)
→ Higher decay during instability
```

#### 4. Net Position Example with Stability
```
NP = Tv * S(v,s) * P(w,d,n) - D(t,L)

Valid Participant in Stable Market:
Transaction value (Tv) = $10,000
Spread (S(v,s)) = 0.00111
P(w,d,n) = 1 (valid configuration)
L = 0.9
stability_index = 0.98

Revenue = $10,000 * 0.00111 * 1 = $11.10
Holding cost = $10,000 * 0.000011 = $0.11
Net Position = $11.10 - $0.11 = $10.99 profit

Invalid Participant:
P(w,d,n) = 0
→ Transaction rejected, no position possible
```

### Key Observations:
1. Only valid device/wallet/network combinations can participate
2. Decay approaches zero during stable conditions
3. Multiple devices or wallets provide no advantage
4. System rewards network stability
5. Participation is binary, not proportional to volume

This creates a sustainable model where:
- Network stability reduces holding costs
- Valid participants earn full rewards
- Multiple accounts/devices provide no benefit
- System naturally maintains price stability

### Stability Mechanics Examples

#### Value Preservation Example
```
For epoch E (24-hour period):
Total Supply: 1,000,000 GATE

Inflows:
- New deposits: 50,000 GATE
- Network rewards: 1,110 GATE (from $1M daily volume)
Total Inflows = 51,110 GATE

Outflows:
- Withdrawals: 49,500 GATE
- Decay penalties: 1,610 GATE
Total Outflows = 51,110 GATE

Balance: 51,110 - 51,110 = 0 (Equilibrium maintained)
```

#### Liquidity Balance Example
```
L(t) = ∑(Active_Holdings) / ∑(Total_Supply)

Scenario:
Total Supply = 1,000,000 GATE
Active Holdings (traded within 24h) = 800,000 GATE

L(t) = 800,000 / 1,000,000 = 0.8
→ Within target range (0.7 ≤ L(t) ≤ 0.9)
```

#### Transaction Fee Distribution Example
```
F(p) = b * (1 + μp)
b = 0.001 (0.1% base fee)
μ = 0.5 (participation multiplier)

Low Activity Participant (p = 0.2):
F(0.2) = 0.001 * (1 + 0.5 * 0.2)
= 0.001 * 1.1
= 0.0011 (0.11% fee)

High Activity Participant (p = 0.8):
F(0.8) = 0.001 * (1 + 0.5 * 0.8)
= 0.001 * 1.4
= 0.0014 (0.14% fee)
```

#### Negative Interest Offset Example
```
O(a) = ∑(D(t)) * (τa/τt)

Monthly Example:
Total decay penalties = 1,610 GATE
Participant active 21 days out of 30:

O(a) = 1,610 * (21/30)
= 1,127 GATE offset earned
```

#### Stability Reserve Requirements Example
```
SR(t) = max(0.2 * TS, ∑(D(t)))

Given:
Total Supply (TS) = 1,000,000 GATE
Monthly decay penalties = 48,300 GATE

Required Reserve:
0.2 * 1,000,000 = 200,000 GATE
max(200,000, 48,300) = 200,000 GATE
```

### Network Stability Mechanics
```
stability_index = min(1, (AP/TH) * (1/|1-p(t)|))
where:
AP = Active participants (unique device/wallet/network combinations)
TH = Total holders
p(t) = current price relative to target

When p(t) = 1:
- stability_index → 1
- D(t) → 0 (no decay during stability)
```

#### Network Health Index Example
```
H(t) = (AP/TH) * (L(t)/0.8) * (SR(t)/RR)

Given:
Active Participants (AP) = 8,000
Total Holders (TH) = 10,000
Liquidity Ratio L(t) = 0.85
Stability Reserve (SR) = 250,000 GATE
Required Reserve (RR) = 200,000 GATE

H(t) = (8,000/10,000) * (0.85/0.8) * (250,000/200,000)
= 0.8 * 1.0625 * 1.25
= 1.0625
→ Healthy network (> 1.0)
```

### Real-World Participant Scenarios

#### 1. Merchant Processor Example
```
Daily volume: $50,000
Participation score: 0.9
Monthly activity: 30 days

Revenue:
- Transaction spreads: $50,000 * 0.00111 * 30 = $1,665
- Activity bonus: $1,665 * 0.9 = $1,498.50
- Decay offset: $150 (from active participation)
Net Monthly Earnings: $3,313.50
```

#### 2. Casual User Example
```
Daily volume: $1,000
Participation score: 0.3
Monthly activity: 15 days

Revenue:
- Transaction spreads: $1,000 * 0.00111 * 15 = $16.65
- Activity bonus: $16.65 * 0.3 = $4.99
- Decay cost: -$25 (from inactive days)
Net Monthly Position: -$3.36
```

### System Performance Metrics (Monthly)

```
With $1M daily volume:
- Total spread revenue: $33,300
- Active participant rewards: $26,640
- Stability pool contribution: $6,660
- Average participant ROI: 0.8% (active) to -2% (inactive)
```

These examples demonstrate how the system:
1. Rewards active participation proportionally
2. Maintains stability through balanced inflows/outflows
3. Creates natural incentives for regular usage
4. Penalizes inactive holding
5. Builds system reserves without traditional staking

The model effectively creates a utility-focused token that behaves more like a payment network than a speculative asset.

### Market Stress Scenarios

#### Scenario 1: Price Spike ($1.20) - Too Many Buyers
```
Initial Conditions:
- Price: $1.20 USDC per GATE
- Total Supply: 1,000,000 GATE
- Active Holdings: 400,000 GATE (Low liquidity)
- Daily Volume: $2,000,000 (Higher than normal due to buying pressure)

Liquidity Ratio:
L = 400,000/1,000,000 = 0.4 (Critically low)

Resulting Spread Adjustment:
S(v) = 0.001 * (1/0.4) = 0.0025
→ 0.25% spread (2.5x normal)

Holding Cost Increase:
D(t,L) = 0.0005 * (1/0.4) * 1 = 0.00125
→ 0.125% daily decay (2.5x normal)

24-Hour Impact on $100,000 Position:
- Trading Cost: $100,000 * 0.0025 = $250
- Holding Cost: $100,000 * 0.00125 = $125
Total Daily Cost: $375 (3.75 basis points)

Market Correction Mechanism:
1. Higher spreads discourage rapid buying
2. Increased holding costs encourage selling
3. Expected 7-day correction: -1.875% ($1.20 → $1.18)
```

#### Scenario 2: Price Drop ($0.85) - Excessive Sellers
```
Initial Conditions:
- Price: $0.85 USDC per GATE
- Total Supply: 1,000,000 GATE
- Active Holdings: 900,000 GATE (High liquidity from selling)
- Daily Volume: $1,500,000 (Higher from panic selling)

Liquidity Ratio:
L = 900,000/1,000,000 = 0.9 (Very high)

Spread Adjustment:
S(v) = 0.001 * (1/0.9) = 0.00111
→ 0.111% spread (Normal)

Holding Cost Reduction:
D(t,L) = 0.0005 * (1/0.9) * 1 = 0.00056
→ 0.056% daily decay (Lower than normal)

Market Correction Incentives:
- Low holding costs encourage keeping positions
- Normal spreads maintain trading activity
- Arbitrage opportunity: 15% potential gain
```

#### Scenario 3: Liquidity Crisis (90% Holders, 10% Traders)
```
Initial Conditions:
- Holders: 900,000 GATE
- Active Traders: 100,000 GATE
- Daily Volume: $200,000 (Severely reduced)

Liquidity Ratio:
L = 100,000/1,000,000 = 0.1 (Crisis level)

Emergency Spread Adjustment:
S(v) = 0.001 * (1/0.1) = 0.01
→ 1% spread (10x normal)

Punitive Holding Cost:
D(t,L) = 0.0005 * (1/0.1) * 1 = 0.005
→ 0.5% daily decay (10x normal)

7-Day Impact on Holders:
Initial Position: $100,000
Holding Cost: $100,000 * (0.005 * 7) = $3,500
→ Forces holders to either trade or exit

Market Recovery Path:
Day 1-7: Estimated 3.5% holder reduction
Day 8-14: Expected 20% increase in liquidity
Day 15-30: Gradual return to normal spreads
```

#### Scenario 4: Volume Shock (5x Normal Trading)
```
Normal Conditions:
- Daily Volume: $1,000,000
- Spread Revenue: $1,110

Shock Conditions:
- Daily Volume: $5,000,000
- Initial Liquidity: L = 0.7

Dynamic Spread Adjustment:
Base: S(v) = 0.001 * (1/0.7) = 0.00143
Volume Modifier: (1 + log₂(5)) = 3.32
Adjusted Spread: 0.00143 * 3.32 = 0.00475
→ 0.475% spread during high volume

24-Hour System Response:
- Increased spread revenue: $23,750
- Higher participant rewards
- Automatic liquidity rebalancing
```

### Market Correction Summary
```
Price Deviation → Spread/Decay Response:
$1.20: +150% spread/decay → 7-day correction
$0.85: -25% spread/decay → 14-day correction
$1.00: Baseline rates → Equilibrium

Volume Impact on Spreads:
2x volume: +25% spread
5x volume: +375% spread
0.5x volume: -15% spread

Liquidity Crisis Response:
< 20% liquidity: Emergency spreads
< 10% liquidity: Circuit breaker activation
> 80% liquidity: Minimum spread rates
```

These scenarios demonstrate how the system:
1. Automatically adjusts costs to discourage harmful behavior
2. Creates stronger incentives during extreme conditions
3. Self-corrects through market mechanisms
4. Protects against manipulation attempts
5. Maintains stability without central control

The key is that all adjustments are:
- Proportional to the deviation
- Automatically applied
- Self-limiting
- Market-driven
```
