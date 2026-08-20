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

## Execution boundary

Registry v1.8 does **not** grant financial profiles transaction authority.

Default-denied capabilities include:

- securities order placement/modification/cancellation;
- broker or bank account administration;
- fund subscriptions/redemptions;
- money transfers;
- exchange trading;
- cryptocurrency swaps, staking, bridging or transfers;
- wallet signing or custody changes;
- handling private keys, seed phrases, recovery codes or signing secrets;
- property purchases/sales, deposits, financing, leases, title actions or contractual commitments.

A future execution integration must be a separate reviewed resource with explicit authorization, account scoping, confirmation policy, limits, audit trail, credential isolation, provider/jurisdiction review and clear distinction between recommendation and execution.

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

Bundles are starting compositions, not recruitment ceilings. Orchestrator and Team Leader may create multiple analyst instances for parallel research when useful, subject to host/resource policy.
