"""
Configuration file

This file stores personal trading settings.
Change these values here instead of editing multiple scripts.
"""

# -------------------------------------------------
# ACCOUNT PROFILES
# -------------------------------------------------

ACCOUNTS = {
    "GOAT_8K_EVAL": {
        "balance": 8000,
        "default_risk_percent": 0.8,
    },

    "GOAT_10K_EVAL": {
        "balance": 10000,
        "default_risk_percent": 0.8,
    },

    "CUSTOM": {
        "balance": None,
        "default_risk_percent": None,
    }
}

# -------------------------------------------------
# PERSONAL TRADING RULES
# -------------------------------------------------

MAX_TRADES_PER_WEEK = 3

TYPICAL_TRADES_PER_WEEK = 2

MINIMUM_ACCEPTABLE_RR = 2

FUNDED_DEFAULT_RISK = 0.5