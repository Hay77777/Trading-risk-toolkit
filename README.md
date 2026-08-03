# A+ Trading Risk Calculator

A small Python utility for the trading workflow:

**4H liquidity -> 15M confirmation -> entry/SL/TP -> risk calculation -> position size**

## Assets

- BTCUSDT
- NZDCAD
- GBPUSD
- EURUSD
- EURCAD

DXY is deliberately not included as a tradeable instrument because it is used as context for USD pairs.

## Important

Instrument specifications differ by broker/prop-firm/platform, especially for BTC and CFDs.

Before using this calculator for an actual order, open the symbol's **Specification** in the same MT5 environment you will trade and verify:

- contract/tick value
- tick size / pip size
- minimum lot
- lot step
- maximum lot

The calculator therefore keeps those specifications configurable instead of pretending one formula works identically for every asset.

## Running it

```bash
python risk_calculator.py
```

No external Python packages are required.

## Example workflow

1. Identify a 4H liquidity zone.
2. Wait for price to reach the zone.
3. Use 15M for displacement/reversal confirmation.
4. Define the logical stop-loss.
5. Define the next liquidity target.
6. Run the calculator.
7. Only execute if the setup still meets your rules.

## Strategy constraints to keep separate from the calculator

- Typical frequency: about 2 A+ trades/week.
- Maximum planned trades: 3/account/week.
- Evaluation risk: usually 0.8%-1% per trade.
- Funded risk: lower than evaluation.
- No requirement to trade every day.
- No chasing a missed entry.

The calculator computes risk; it does not decide whether a setup is A+.
