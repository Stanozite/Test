# Index — Quant Scout digests & dedupe ledger

## Digest log
Newest first. Each run appends a row.

| Date | Digest | # findings | Highlights |
| --- | --- | --- | --- |
| 2026-06-23 | [2026-06-23-quant-scout.md](digests/2026-06-23-quant-scout.md) | 6 | Risk-sensitive RL allocation via free-energy/entropy duality → LQG game + q-learning, fractional-Kelly readout (Lleo/Runggaldier); growth-optimal AMM fee = pro-cyclical, ∝ variance, wealth/CRRA-independent, dominates static heuristics (Ghasemlu/LVR); KineticSim GPU sim 54.7B events/s, 3,406× NumPy; Ethereum/L2 on-chain cost map (Mizrach); ZOC-TN LGD boundary-mass model (Sigrist); path-integral default-intensity quanto-CDS pricing (Capriotti). Fresh 2606.21–22 batch above prior ceiling |
| 2026-06-22 | [2026-06-22-quant-scout.md](digests/2026-06-22-quant-scout.md) | 3 | Interest-rate calibration as WLS — leverage diagnostics + CIs, "low RMSRE not sufficient" (Mahler/Ruckdeschel); tempered Skew-t for accumulated S&P500 tails (Shao/Serota); CAP slope = Bayes, Gini/Somers'D/AR unified (Burakov); QuantTradingOS agentic OS. Thin Mon — weekend arXiv gap (no 20–22 Jun announce), 16–19 Jun residue |
| 2026-06-21 | [2026-06-21-quant-scout.md](digests/2026-06-21-quant-scout.md) | 7 | Geometric theory of when LLM factor discovery helps (Li Xia); VLMs can't read candlesticks — evidence sign-flipped (Ziyao Wang); Epps effect decomposed in coupled LOBs (Angstmann/Gebbie); agentic-AI belief-VaR model risk (Dixon); skew-elliptical-t option-portfolio weights; microsecond error-bounded NN option pricing (van den Berg). Thin Sunday — 16–17 Jun residue + ML-method/agentic-risk |
| 2026-06-20 | [2026-06-20-quant-scout.md](digests/2026-06-20-quant-scout.md) | 8 | Trend-conditioned vol/correlation forecasting (Schmidhuber); factor-model rankings are construction artifacts (Shin); 5.6pp Polymarket↔Binance BTC mispricing (Portnaya); conv-VAE crypto IV surfaces; DeXposure-Claw agentic DeFi risk; AlphaPROBE DAG alpha mining; Vibe-Trading harness. Thin weekend window — alpha/microstructure lean |
| 2026-06-17 | [2026-06-17-quant-scout.md](digests/2026-06-17-quant-scout.md) | 10 | Per-action causal impact detection (Zovko); Schur-damping HRP↔min-var identity (Cotton); PIVOT differentiable IV layer (Horvath/Buehler); CFO LLM digital twins (Campbell Harvey); crypto downside-diversification collapse; CARLOS optimal-stopping RL; RRMV multiperiod MV |
| 2026-06-16 (run 2) | [2026-06-16-quant-scout.md](digests/2026-06-16-quant-scout.md#run-2--same-day-refresh-2026-06-16) | 6 | Execution slot refilled: TT-DAC-PS RL execution; AS≡CJ market-making unification; Hyperliquid sunshine-trading (Lillo); DeePM regime-robust macro (Zohren); FactorEngine doc-infused alpha mining |
| 2026-06-16 | [2026-06-16-quant-scout.md](digests/2026-06-16-quant-scout.md) | 7 | LLM alpha mining (QuantaAlpha, Alpha-R1); ReCAP regime continual learning; informed-trading detection; LLM backtest benchmarks |

---

## Dedupe ledger
Every captured finding gets one line here so future runs don't re-surface it.
Fingerprint = normalized title + primary author/source (or canonical URL).

<!-- Format: - [YYYY-MM-DD] <fingerprint> | <url> -->

_(empty — populated as findings are captured)_

- [2026-06-16] quantaalpha evolutionary framework llm-driven alpha mining | https://arxiv.org/abs/2602.07085
- [2026-06-16] alpha-r1 alpha screening llm reasoning reinforcement learning | https://arxiv.org/abs/2512.23515
- [2026-06-16] alphaforgebench benchmarking end-to-end trading strategy design llms | https://arxiv.org/abs/2602.18481
- [2026-06-16] per-market information leakage and order-flow skill informed trading prediction markets | https://arxiv.org/abs/2605.02287
- [2026-06-16] regime-adaptive continual learning for portfolio management recap | https://arxiv.org/abs/2606.00143
- [2026-06-16] from classical optimization to bayesian integration systematic portfolio management | https://arxiv.org/abs/2605.29413
- [2026-06-16] pricing options on the cryptocurrency futures contracts | https://arxiv.org/abs/2506.14614
- [2026-06-16] backtestbench benchmarking llms automated quantitative strategy backtesting | https://arxiv.org/abs/2605.17937
- [2026-06-16] factorengine program-level knowledge-infused factor mining quantitative investment lin feng | https://arxiv.org/abs/2603.16365
- [2026-06-16] tt-dac-ps twin-target deterministic actor-critic policy smoothing optimal trade execution zaznov | https://arxiv.org/abs/2606.08379
- [2026-06-16] avellaneda-stoikov cartea-jaimungal one framework forced uniqueness theorem inventory market making feys | https://arxiv.org/abs/2606.01477
- [2026-06-16] trading in the sunshine or shade market impact adverse selection hyperliquid barone lillo | https://arxiv.org/abs/2606.15715
- [2026-06-16] deepm regime-robust deep learning systematic macro portfolio management wood roberts zohren | https://arxiv.org/abs/2601.05975
- [2026-06-16] dynamic multi-pair trading cryptocurrency markets deep reinforcement learning lebiedz slepaczuk | https://arxiv.org/abs/2606.04574
- [2026-06-17] cfos meet llms digital twins executives expectations graham harvey jha | https://arxiv.org/abs/2606.13812
- [2026-06-17] carlos continuous-time optimal stopping deep reinforcement learning borsa ludkovski | https://arxiv.org/abs/2606.17545
- [2026-06-17] robust transformer one-step stock index forecasting shifted data augmentation thach | https://arxiv.org/abs/2606.15701
- [2026-06-17] realtime price impact detection timing synchronicity zovko | https://arxiv.org/abs/2606.13419
- [2026-06-17] revisiting trade-sign long-memory square-root law price impact angstmann gebbie | https://arxiv.org/abs/2606.16269
- [2026-06-17] two sides of schur damping high-dimensional pseudo-likelihoods portfolio allocation cotton | https://arxiv.org/abs/2606.14798
- [2026-06-17] reference-regulated multiperiod mean-variance portfolio optimization high dimensions rrmv deng gao wang | https://arxiv.org/abs/2606.13697
- [2026-06-17] multiplex network hawkes model systemic risk measurement zelvyte griffin | https://arxiv.org/abs/2606.15755
- [2026-06-17] pivot differentiable jackel implied-volatility price objective saqur horvath buehler | https://arxiv.org/abs/2606.17065
- [2026-06-17] crashing together rallying apart tail dependence cryptocurrency mallela leonelli | https://arxiv.org/abs/2606.16840
- [2026-06-20] alphaprobe alpha mining principled retrieval on-graph biased evolution dag guo shen luo | https://arxiv.org/abs/2602.11917
- [2026-06-20] trends volatility correlations critical phenomena financial markets lattice gas safari schmidhuber | https://arxiv.org/abs/2606.20145
- [2026-06-20] which portfolios construction dependence factor model performance shin | https://arxiv.org/abs/2606.19550
- [2026-06-20] how to spot outliers ensemble anomaly detection framework risk outputs peysakhovich sieradzki | https://arxiv.org/abs/2606.20079
- [2026-06-20] do prediction markets match option prices bitcoin threshold binance polymarket portnaya | https://arxiv.org/abs/2606.19517
- [2026-06-20] beyond the smile hybrid convolutional vae crypto volatility surfaces singh reddy chopra | https://arxiv.org/abs/2606.16961
- [2026-06-20] dexposure-claw agentic system defi risk supervision shu chen wu he | https://arxiv.org/abs/2606.19501
- [2026-06-20] vibe-trading multi-agent natural-language trading research framework hkuds | https://github.com/HKUDS/Vibe-Trading
- [2026-06-20] finstressts parametric synthetic benchmark time-series forecasting finance sun koa ni | https://arxiv.org/abs/2606.03184
- [2026-06-21] discovery under hypothesis redundancy geometric theory discovery bottlenecks search compression li xia wang | https://arxiv.org/abs/2606.14386
- [2026-06-21] martingale doppelganger-eval auditing candlestick understanding vision-language models ziyao wang | https://arxiv.org/abs/2606.17423
- [2026-06-21] correlation emergence epps effect two coupled limit order books angstmann gebbie | https://arxiv.org/abs/2606.14182
- [2026-06-21] sharpe ratio return-var maximization option portfolios skew-elliptical t sung pirvu | https://arxiv.org/abs/2606.17032
- [2026-06-21] belief at risk quantifying agentic ai model risk llm-inferred bayesian state filters dixon | https://arxiv.org/abs/2606.15473
- [2026-06-21] model validation agentic ai systems pomdp belief-state forecast policy validation dixon | https://arxiv.org/abs/2606.17383
- [2026-06-21] extendable integrated dynamic forecasting stress-testing credit risk muller botha beyers | https://arxiv.org/abs/2606.19052
- [2026-06-21] fast reliable error-bounded option pricing pretrained neural networks gjr-garch van den berg | https://arxiv.org/abs/2606.15502
- [2026-06-22] fitting accumulated stock returns tempered skew-t distribution shao serota | https://arxiv.org/abs/2606.19318
- [2026-06-22] gini-bayes connection cap slope bayes theorem weight of evidence somers d calibration burakov | https://arxiv.org/abs/2606.18545
- [2026-06-22] advanced calibration analysis influential observations stochastic interest rate model calibration mahler ruckdeschel | https://arxiv.org/abs/2606.20420
- [2026-06-22] quanttradingos modular agentic trading operating system orchestrator qtos-core | https://github.com/QuantTradingOS
- [2026-06-22] optimal order multi-agent general many-body systems jake xia | https://arxiv.org/abs/2606.20485
- [2026-06-23] reinforcement learning risk-sensitive investment management free energy entropy duality lleo runggaldier | https://arxiv.org/abs/2606.20903
- [2026-06-23] optimal dynamic fees automated market makers stochastic control loss-versus-rebalancing ghasemlu | https://arxiv.org/abs/2606.21769
- [2026-06-23] transaction costs speed ethereum ecosystem scalability mainnet layer 2s ambrosia mizrach | https://arxiv.org/abs/2606.22206
- [2026-06-23] censored transformed model proportional outcomes boundary mass loss given default zoc-tn qiang sigrist | https://arxiv.org/abs/2606.21515
- [2026-06-23] semi-analytical pricing general default intensity models path integral quanto cds parker stedman capriotti | https://arxiv.org/abs/2606.21800
- [2026-06-23] kineticsim lightweight high-performance gpu execution engine real-time market simulators jayakody | https://arxiv.org/abs/2606.21784
