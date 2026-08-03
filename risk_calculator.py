#!/usr/bin/env python3
"""
Trading Risk & Position Size Calculator

Purpose
-------
Calculate:
  - account risk in USD
  - stop distance
  - position/lot size
  - potential profit/loss
  - R:R

Important
---------
The calculator deliberately does NOT hard-code broker/prop-firm
contract specifications. Those vary by instrument/platform.

For each asset, enter the USD value of a 1.0 price move for 1.0 lot
(or use the pip mode for forex if you know the pip value per lot).

Before live use, verify the symbol's contract size/tick value in
your GoatFunded/MT5 symbol specification.
"""
import math

from config import ACCOUNTS
from assets import ASSETS




# ------------------------------------------------------------------
# ASSET CONFIGURATION
# ------------------------------------------------------------------
# Replace these example values with the specifications from your
# trading platform. Do NOT assume the BTC specification below.
#
# For "pip" mode:
#   value_per_unit_per_lot = USD value of ONE pip for 1 standard lot
#   pip_size               = price size of one pip (normally 0.0001)
#
# For "price" mode:
#   value_per_unit_per_lot = USD P/L for a 1.0 price move on 1 lot
#


def round_down_to_step(value: float, step: float) -> float:
    """Round a lot size down so it never exceeds the calculated risk."""
    if step <= 0:
        raise ValueError("lot_step must be > 0")
    return math.floor((value + 1e-12) / step) * step


def calculate(
    account_size: float,
    risk_percent: float,
    direction: str,
    entry: float,
    stop: float,
    target: float,
    spec: AssetSpec,
) -> dict:

    if account_size <= 0:
        raise ValueError("Account size must be > 0.")
    if not 0 < risk_percent <= 100:
        raise ValueError("Risk percent must be between 0 and 100.")
    if entry <= 0 or stop <= 0 or target <= 0:
        raise ValueError("Entry, stop and target must be > 0.")

    direction = direction.upper()
    if direction not in {"BUY", "SELL"}:
        raise ValueError("Direction must be BUY or SELL.")

    if spec.contract_size<= 0:
        raise ValueError(
            f"{spec.name}: enter a valid USD value per unit/pip per lot "
            "in ASSETS before calculating."
        )

    if direction == "BUY":
        risk_distance = entry - stop
        reward_distance = target - entry
    else:
        risk_distance = stop - entry
        reward_distance = entry - target

    if risk_distance <= 0:
        raise ValueError(
            "Stop is on the wrong side of entry for this direction."
        )
    if reward_distance <= 0:
        raise ValueError(
            "Target is on the wrong side of entry for this direction."
        )

    if spec.mode == "pip":
        if spec.pip_size is None or spec.pip_size <= 0:
            raise ValueError(f"{spec.name}: pip_size is required.")
        stop_units = risk_distance / spec.pip_size
        target_units = reward_distance / spec.pip_size
    elif spec.mode == "price":
        stop_units = risk_distance
        target_units = reward_distance
    else:
        raise ValueError("mode must be 'pip' or 'price'.")

    risk_usd = account_size * (risk_percent / 100.0)
    reward_per_lot = target_units * spec.contract_size
    risk_per_lot = stop_units * spec.contract_size

    raw_lots = risk_usd / risk_per_lot
    lots = round_down_to_step(raw_lots, spec.lot_step)

    if spec.min_lot and lots < spec.min_lot:
        lots = 0.0

    if spec.max_lot is not None:
        lots = min(lots, spec.max_lot)

    actual_risk = lots * risk_per_lot
    potential_profit = lots * reward_per_lot
    rr = reward_distance / risk_distance

    return {
        "asset": spec.name,
        "direction": direction,
        "account_size": account_size,
        "risk_percent": risk_percent,
        "risk_usd": risk_usd,
        "entry": entry,
        "stop": stop,
        "target": target,
        "stop_distance_price": risk_distance,
        "target_distance_price": reward_distance,
        "stop_units": stop_units,
        "target_units": target_units,
        "raw_lots": raw_lots,
        "recommended_lots": lots,
        "actual_risk": actual_risk,
        "potential_profit": potential_profit,
        "rr": rr,
    }


def money(x: float) -> str:
    return f"${x:,.2f}"


def print_report(result: dict) -> None:
    print("\n" + "=" * 54)
    print(f"{result['asset']}  |  {result['direction']}")
    print("=" * 54)
    print(f"Account size:          {money(result['account_size'])}")
    print(f"Risk:                  {result['risk_percent']:.2f}%")
    print(f"Risk amount:           {money(result['risk_usd'])}")
    print(f"Entry:                 {result['entry']}")
    print(f"Stop:                  {result['stop']}")
    print(f"Target:                {result['target']}")
    print(f"Stop distance:         {result['stop_distance_price']:.8f}")
    print(f"Target distance:       {result['target_distance_price']:.8f}")
    print(f"Raw lot size:          {result['raw_lots']:.4f}")
    print(f"Recommended lot size:  {result['recommended_lots']:.2f}")
    print(f"Actual max risk:       {money(result['actual_risk'])}")
    print(f"Potential profit:      {money(result['potential_profit'])}")
    print(f"Risk : Reward:         1 : {result['rr']:.2f}")
    print("=" * 54)

    if result["recommended_lots"] == 0:
        print("WARNING: calculated size is below the minimum lot size.")


def choose_asset() -> str:
    print("\nYour assets:")
    names = list(ASSETS)
    for i, name in enumerate(names, start=1):
        print(f"  {i}. {name}")

    while True:
        choice = input("Select asset: ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(names):
                return names[index]
        except ValueError:
            pass
        print("Please enter one of the listed numbers.")


def get_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a number greater than zero.")


def main() -> None:
    print("A+ SETUP RISK CALCULATOR")
    print("4H liquidity -> 15M execution -> position sizing\n")

    asset_name = choose_asset()
    spec = ASSETS[asset_name]

    account_size = get_float("Account size ($): ")
    risk_percent = get_float("Risk per trade (%): ")

    direction = input("Direction (BUY/SELL): ").strip().upper()
    while direction not in {"BUY", "SELL"}:
        direction = input("Direction must be BUY or SELL: ").strip().upper()

    entry = get_float("Entry price: ")
    stop = get_float("Stop-loss price: ")
    target = get_float("Take-profit price: ")

    result = calculate(
        account_size=account_size,
        risk_percent=risk_percent,
        direction=direction,
        entry=entry,
        stop=stop,
        target=target,
        spec=spec,
    )

    print_report(result)


if __name__ == "__main__":
    main()
