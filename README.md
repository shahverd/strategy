# GoldenFinX sample strategies

An independently versioned Freqtrade Strategy repository for testing Strategy Lab.

The included strategies are deliberately small and readable:

- `EmaCrossStrategy`: trend-following EMA crossover, long and short.
- `RsiReversalStrategy`: RSI mean reversion, long only.
- `DonchianBreakoutStrategy`: channel breakout, long and short.

They use Freqtrade strategy interface v3 and live under the conventional
`user_data/strategies/` directory. They are educational fixtures, not trading advice or
claims of profitability. Backtest them with pinned data before any simulated forward test.

## Attach this repository as a submodule later

First create the remote and push this repository to it. From this directory:

```bash
git remote add origin <REMOTE_URL>
git push -u origin main
```

Then, from the parent Strategy Lab repository, remove the temporary `/strategies/` ignore rule
and attach the existing checkout:

```bash
git submodule add --force <REMOTE_URL> strategies
git add .gitmodules strategies .gitignore
git commit -m "chore: attach strategy repository submodule"
```

GitHub Actions must use `submodules: true` in `actions/checkout` before a hosted release should
consume the submodule directly.
