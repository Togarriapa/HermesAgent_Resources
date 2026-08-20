# Investment and Wealth Governance

The financial/investment domain is an internal decision-support and explicitly authorized execution system under the normal Hermes topology:

`User <-> Hermes <-> Orchestrator <-> Wealth / Investment / Execution Profiles`

## Role hierarchy

- **Financial Advisor** — goals, constraints, risk capacity, liquidity and investment-policy planning.
- **Wealth Manager** — coordinates the whole wealth picture and recruits accounting/legal/investment specialists.
- **Portfolio Manager** — portfolio construction, allocation, rebalancing, performance and portfolio-level risk.
- **Asset Manager** — mandate, external-manager and asset oversight.
- **Stocks Manager** — public-equity portfolio domain.
- **Cryptocurrency Manager** — digital-asset portfolio domain.
- **Real Estate Manager** — real-estate investment portfolio domain.
- **Financial Data Steward** — bank/broker/exchange/Ledger aggregation, normalization, freshness and reconciliation.
- **Financial Execution Operator** — executes one exact real-money action only from an explicit user order and fresh confirmation.
- **Crypto Live Wallet Operator** — operates the dedicated Hermes real-value wallet under the same explicit-order gate.
- **Crypto Sandbox Operator** — autonomous testnet wallet experimentation only; never production custody.

Analysts/researchers provide independent specialist evidence rather than inheriting execution authority:

- Investment Research Analyst
- Equity Analyst
- Fixed Income Analyst
- Macroeconomic Analyst
- Quantitative Investment Analyst
- Investment Risk Analyst
- Crypto Asset Analyst
- Blockchain Researcher
- Real Estate Investment Analyst

## Independent research and challenge

Material decisions should recruit the smallest competent research set. Independent work may run in parallel. Investment Risk Analyst should remain separate from the thesis owner for material portfolio decisions and should actively test concentration, liquidity, leverage, counterparty, custody, currency and tail-risk assumptions.

Research outputs should preserve source provenance, dates, assumptions, scenarios, counterarguments, uncertainty and thesis-break conditions. Historical returns, backtests and forecasts must not be represented as guaranteed future performance.

## Read-only financial account access

`financial-data-hub` may ingest read-only observations from:

- Revolut, Banco BPI and moey through regulated PSD2 Account Information Service Provider connections, subject to provider/institution coverage and user consent;
- Trading 212 through a permission-scoped read key;
- Pionex through a `Read` key;
- Ledger through Ledger Wallet API `account.list`.

`financial-data-steward` normalizes those observations for internal finance specialists. Raw passwords, PINs, MFA secrets, API secrets, Ledger private keys, seed phrases, recovery codes and signing secrets remain outside Profile-visible context.

## Explicit-order real-money execution

`financial-execution-gateway@1.0.0` is write-capable for supported providers, but it is not autonomous. Every action requires an explicit user order routed through Hermes plus a fresh confirmation of the exact final payload.

Configured write paths include:

- bank payment initiation through a regulated PISP adapter for supported Revolut/BPI/moey payment flows;
- Trading 212 live Market, Limit, Stop and Stop-Limit orders plus pending-order cancellation using a separate execution credential;
- Pionex order placement/cancellation using a separate key with `Trade` permission;
- Ledger `transaction.sign` / `transaction.signAndBroadcast` with Ledger hardware/on-device confirmation.

The authorization is one-shot, expires after five minutes, cannot be wildcarded or reused, and is bound to provider, account, operation, recipient/instrument, side, amount/quantity, currency, and price/limit when applicable.

The Financial Execution Operator executes exactly the confirmed action. It cannot optimize size, substitute an asset, change a recipient, split an order, retry with changed parameters, create follow-on transactions, or infer permission from a strategy or recommendation.

Still denied without a separate future capability:

- autonomous real-money execution;
- broker/bank account administration;
- beneficiary administration;
- withdrawals or transfers from Pionex;
- arbitrary Ledger message signing;
- handling user private keys, seed phrases, recovery codes or signing secrets;
- property purchase/sale/financing/title/contract execution.

See `FINANCIAL_ACCESS.md` for provider-specific details.

## Dedicated Hermes live wallet

`agent-live-wallet@1.0.0` defines a separate real-value wallet owned for Hermes use. Its key material is generated locally and stays in the host encrypted secret boundary; it is never derived from or mixed with the user's Ledger or other wallets.

The wallet may receive real assets and may construct, simulate, sign and broadcast transactions on an explicit configured network allowlist. Real-value signing, however, requires an explicit user order plus fresh confirmation for every transaction. The agent may independently research opportunities, monitor state and prepare transaction proposals, but it cannot autonomously commit real economic value.

This restriction is intentional and does not apply to the separate testnet sandbox.

## Agent crypto sandbox

`agent-sandbox-wallet` may autonomously sign and send transactions using faucet/test assets on approved public test networks. The sandbox currently permits Ethereum Sepolia and Solana Devnet and rejects mainnet, real-value deposits, fiat on-ramps, production exchange funding, mainnet bridges, production wallet connections, and imported user wallet secrets.

Sandbox authority must never be reused for the user's Ledger, Pionex, Trading 212, bank accounts, or the Hermes live wallet.

## Professional and jurisdiction boundaries

Financial planning, investment management, securities activity, tax, legal, estate, insurance and property transactions may be regulated differently by jurisdiction. Profiles must distinguish general research/planning from activities requiring licensed or regulated professionals.

- Portuguese tax/accounting questions can recruit Accountant — Portugal.
- International accounting questions can recruit Accountant — International.
- Portuguese legal questions can recruit Portuguese Law Specialist.
- Cross-border/international legal questions can recruit International Law Specialist.

The appropriate qualified professional should be involved when licensing, fiduciary duties, suitability, regulated advice, filings, contracts, title, tax treatment or other material jurisdiction-specific obligations require it.

## Team bundles

- `wealth-investment-team` — overall wealth/portfolio planning and risk.
- `public-markets-team` — equities, fixed income, macro, quant and risk.
- `digital-assets-team` — crypto portfolio, protocol, custody and cybersecurity analysis.
- `real-assets-team` — real estate, asset oversight, property-condition and risk analysis.
- `financial-data-team` — financial source aggregation plus wealth/portfolio/risk interpretation.
- `financial-execution-team` — explicitly ordered one-shot real-money execution separated from recommendation roles.
- `crypto-sandbox-team` — autonomous testnet-only wallet and blockchain experimentation.

Bundles are starting compositions, not recruitment ceilings. Orchestrator and Team Leader may create multiple analyst instances for parallel research when useful, subject to host/resource policy.
