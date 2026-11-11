# FX Weekly — 06 November 2026

Generated 2026-11-11 from the Friday close of 06 Nov 2026.

> ⚠️ **Sample data.** At least one market uses synthetic data (no download available). Run `python cli.py fetch-data` for real prices.

## At a glance

| Market | Close | P(up next week) | 80% range | Volatility regime |
|---|---:|---:|---|---|
| EUR/USD | 1.2047 | 53% | 1.1927 – 1.2169 | normal |
| EUR/CHF | 0.9684 | 43% | 0.9624 – 0.9744 | low |
| EUR/PLN | 3.7442 | 49% | 3.7075 – 3.7813 | normal |
| BTC/USD | 100,786 | 55% | 92,560 – 109,744 | normal |

## EUR/USD

*The most traded currency pair; driven by ECB vs. Fed policy.*

| | |
|---|---|
| Close Fri 06 Nov 2026 | **1.2047** |
| P(higher by 13 Nov) | **53%** — no clear direction |
| 80% expected range | 1.1927 – 1.2169 |
| Expected weekly volatility | 0.78% — **normal** (higher than 48% of past weeks) |

**What moves the signal:** weekly RSI (+), 12-week volatility (+), last week's trading range (−) (sign = push towards up / down).

**Track record** (2018-06-29 to 2026-10-30, 436 weeks): Out of sample, the direction model does **not** beat the base rate, the random walk remains the better return forecast and the volatility model beats the 4-week average.

## EUR/CHF

*Safe-haven barometer for the DACH region; SNB policy matters.*

| | |
|---|---|
| Close Fri 06 Nov 2026 | **0.9684** |
| P(higher by 13 Nov) | **43%** — leaning down |
| 80% expected range | 0.9624 – 0.9744 |
| Expected weekly volatility | 0.49% — **low** (higher than 30% of past weeks) |

**What moves the signal:** interest-rate differential (−), 12-week volatility (+), 4-week volatility (−) (sign = push towards up / down).

**Track record** (2018-06-29 to 2026-10-30, 436 weeks): Out of sample, the direction model does **not** beat the base rate, the random walk remains the better return forecast and the volatility model beats the 4-week average.

## EUR/PLN

*Largest CEE currency; relevant for banks active in Central & Eastern Europe.*

| | |
|---|---|
| Close Fri 06 Nov 2026 | **3.7442** |
| P(higher by 13 Nov) | **49%** — no clear direction |
| 80% expected range | 3.7075 – 3.7813 |
| Expected weekly volatility | 0.77% — **normal** (higher than 60% of past weeks) |

**What moves the signal:** last week's volatility (+), distance to 26-week average (+), last week's trading range (−) (sign = push towards up / down).

**Track record** (2018-06-29 to 2026-10-30, 436 weeks): Out of sample, the direction model does **not** beat the base rate, the random walk remains the better return forecast and the volatility model beats the 4-week average.

## BTC/USD

*Since Oct 2026 Sparkassen offer crypto trading in their app; RBI is rolling out crypto via Bitpanda across its CEE network banks.*

| | |
|---|---|
| Close Fri 06 Nov 2026 | **100,786** |
| P(higher by 13 Nov) | **55%** — no clear direction |
| 80% expected range | 92,560 – 109,744 |
| Expected weekly volatility | 6.64% — **normal** (higher than 57% of past weeks) |

**What moves the signal:** distance to 26-week average (+), weekly RSI (−), last week's move (−) (sign = push towards up / down).

**Track record** (2018-06-29 to 2026-10-30, 436 weeks): Out of sample, the direction model does **not** beat the base rate, the random walk remains the better return forecast and the volatility model beats the 4-week average.

## Track record (walk-forward, out of sample)

| Market | Weeks | Hit rate (bench) | Brier (bench) | Theil's U | Vol RMSE ratio | 80% band coverage |
|---|---:|---:|---:|---:|---:|---:|
| EUR/USD | 436 | 51.1% (50.0%) | 0.259 (0.251) | 1.014 | 0.945 | 78.2% |
| EUR/CHF | 436 | 46.6% (46.6%) | 0.269 (0.253) | 1.032 | 0.956 | 80.0% |
| EUR/PLN | 436 | 45.9% (46.6%) | 0.265 (0.251) | 1.038 | 0.963 | 79.4% |
| BTC/USD | 436 | 53.9% (55.3%) | 0.256 (0.249) | 1.012 | 0.947 | 74.3% |

*Theil's U and the vol RMSE ratio are below 1 when the model beats its benchmark (random walk / 4-week average vol). Lower Brier is better. A well-calibrated 80% band contains next week's close about 80% of the time.*

## How to read this

- **P(up)** comes from a logistic regression on weekly momentum, volatility, RSI, trend and (for FX) the interest-rate differential. Values near 50% mean the model sees no edge — which is the normal state of affairs in FX.
- **The 80% range** is centred on today's close (random walk) and sized by the volatility forecast. It is a risk measure, not a price target.
- **Validation:** every number in the track record comes from forecasts made with only past data (expanding window, refitted every 4 weeks).

*Educational project — not investment advice.*
