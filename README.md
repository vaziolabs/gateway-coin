# Gateway Token (GATE)

A protocol-agnostic cross-chain bridge enabling seamless asset transfers between blockchain networks, built on FragMint Chain.

## Overview
![alt text](image.png)

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
- Validator staking ([STAKE_AMOUNT] GATE required)
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
S(v) = β * (1/L)

Where:
S(v) = Spread per transaction
β = Base spread rate (e.g., 0.001)
L = Current liquidity ratio
```

#### Network Participant Share
```
R(p,v) = S(v) * (p/P)

Where:
R(p,v) = Reward per participant
p = Individual participant's transaction volume
P = Total network transaction volume
```

#### Holding Cost (Anti-Speculation)
```
D(t,L) = H * (1/L) * t

Where:
D(t,L) = Decay cost
H = Base holding rate (smaller than transaction spread)
L = Liquidity ratio
t = Time held without transactions
```

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
S(v) = β * (1/L)
β = 0.001 (0.1% base spread)

Scenario A (High Liquidity):
L = 0.9 (90% of tokens actively used)
S(v) = 0.001 * (1/0.9) = 0.00111
→ 0.111% spread per transaction

Scenario B (Low Liquidity):
L = 0.5 (50% of tokens actively used)
S(v) = 0.001 * (1/0.5) = 0.002
→ 0.2% spread per transaction
```

#### 2. Network Participant Share Example
```
R(p,v) = S(v) * (p/P)

Example with $1M daily volume:
Total network volume (P) = $1,000,000
Spread (S(v)) = 0.00111 (from high liquidity scenario)

Participant A (Large):
p = $100,000 (10% of volume)
R = 0.00111 * (100,000/1,000,000)
→ $0.111 per $1,000 traded
→ Daily earnings = $11.10

Participant B (Small):
p = $1,000 (0.1% of volume)
R = 0.00111 * (1,000/1,000,000)
→ $0.111 per $1,000 traded
→ Daily earnings = $0.111
```

#### 3. Holding Cost Example
```
D(t,L) = H * (1/L) * t
H = 0.0005 (0.05% base holding rate)
t = days held

High Liquidity (L = 0.9):
1 day hold: D = 0.0005 * (1/0.9) * 1 = 0.00056 (0.056%)
7 day hold: D = 0.0005 * (1/0.9) * 7 = 0.00389 (0.389%)

Low Liquidity (L = 0.5):
1 day hold: D = 0.0005 * (1/0.5) * 1 = 0.001 (0.1%)
7 day hold: D = 0.0005 * (1/0.5) * 7 = 0.007 (0.7%)
```

#### 4. Net Position Example
```
NP = Tv * S(v) - D(t,L)

Active Trader Example:
Daily volume (Tv) = $10,000
Spread (S(v)) = 0.00111
Holding time = 1 day
L = 0.9

Revenue = $10,000 * 0.00111 = $11.10
Holding cost = $10,000 * 0.00056 = $5.60
Net Position = $11.10 - $5.60 = $5.50 profit

Inactive Holder Example:
Daily volume (Tv) = $0
Holding time = 7 days
L = 0.9

Revenue = $0 * 0.00111 = $0
Holding cost = $10,000 * 0.00389 = $38.90
Net Position = $0 - $38.90 = -$38.90 loss
```

### Key Observations:
1. Active traders can profit from spreads (similar to how Visa merchants receive a portion of transaction fees)
2. Higher liquidity leads to lower spreads and holding costs
3. Holding without trading becomes increasingly expensive
4. The system encourages frequent transactions and discourages hoarding
5. With $1M daily volume, the system generates about $1,110 in daily spreads ($405,150 annually) to be shared among participants

This creates a sustainable model where:
- Active participants are rewarded (like payment processors)
- Holding