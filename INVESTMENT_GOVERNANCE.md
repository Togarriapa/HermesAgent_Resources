# Investment and Wealth Governance

The financial/investment domain is an internal decision-support system under the normal Hermes topology:

`User <-> Hermes <-> Orchestrator <-> Wealth / Investment Profiles`

## Role hierarchy

- **Financial Advisor** — goals, constraints, risk capacity, liquidity and investment-policy planning.
- **Wealth Manager** — coordinates the whole wealth picture and recruits accounting/legal/investment specialists.
- **Portfolio Manager** — portfolio construction, allocation, rebalancing, performance and portfolio-level risk.
- **Asset Manager** — mandate, external-manager and asset oversight.
- **Stocks Manager** — public-equity portfolio domain.
- **Cryptocurrency Manager** — digital-asset portfolio domain.
- **Real Estate Manager** — real-estate investment portfolio domain.
- **Financial Data Steward** — read-only bank/broker/exchange/Ledger aggregation, normalization, freshness and reconciliation.
- **Crypto Sandbox Operator** — agent-owned testnet wallet experimentation only; never production custody.

Analysts/researchers provide independent specialist evidence rather than inheriting manager authority:

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

Registry v1.9 may ingest read-only financial observations through `financial-data-hub`:

- Revolut, Banco BPI and moey through a regulated PSD2 Account Information Service Provider connection, subject to provider/institution coverage and user consent;
- Trading 212 through a permission-scoped read-only API key with IP restriction where available;
- Pionex through an API key restricted to `Read` permission;
- Ledger through Ledger Wallet API `account.list` capability only.

`financial-data-steward` normalizes those observations for internal finance specialists. Raw passwords, PINs, MFA secrets, API secrets, Ledger private keys, seed phrases, recovery codes and signing secrets remain outside Profile-visible context.

Read access does not include payment initiation, order placement/cancellation, trading, withdrawals, transfers, transaction signing, custody changes or account administration.

See `FINANCIAL_ACCESS.md` for the provider-specific contract.

## Execution boundary

Registry v1.9 does **not** grant financial profiles transaction authority.

Default-denied capabilities include:

- securities order placement/modification/cancellation;
- broker or bank account administration;
- fund subscriptions/redemptions;
- money transfers;
- exchange trading;
- cryptocurrency swaps, staking, bridging or production transfers;
- production-wallet signing or custody changes;
- handling user private keys, seed phrases, recovery codes or signing secrets;
- property purchases/sales, deposits, financing, leases, title actions or contractual commitments.

`financial-execution-gateway@0.1.0` is a disabled placeholder with zero executable capabilities. A future execution integration must be published as a new reviewed version with explicit authorization, account scoping, confirmation policy, limits, audit trail, credential isolation, provider/jurisdiction review and clear distinction between recommendation and execution.

## Agent crypto sandbox exception

The execution boundary above applies to real economic value and production wallets. A separate `agent-sandbox-wallet` may sign and send transactions using faucet/test assets on explicitly approved public test networks only.

The sandbox currently permits Ethereum Sepolia and Solana Devnet. It rejects mainnet, real-value deposits, fiat on-ramps, production exchange funding, mainnet bridges, production wallet connections, and imported user wallet secrets.

Sandbox signing authority is not financial authority and must never be reused for the user's Ledger, Pionex, Trading 212, bank accounts, or any mainnet wallet.

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
- `financial-data-team` — read-only financial source aggregation plus wealth/portfolio/risk interpretation.
- `crypto-sandbox-team` — testnet-only wallet and blockchain experimentation.

Bundles are starting compositions, not recruitment ceilings. Orchestrator and Team Leader may create multiple analyst instances for parallel research when useful, subject to host/resource policy.
