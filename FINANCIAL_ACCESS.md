# Financial Account Access Architecture

Hermes financial integrations are split into three deliberately separate layers:

1. **Read-only personal financial data** — enabled through `financial-data-hub`.
2. **Future real-money execution** — represented only by the disabled `financial-execution-gateway` contract.
3. **Agent experimentation wallet** — enabled only through `agent-sandbox-wallet` on approved public test networks.

The separation is structural: adding data access must not silently create payment, trading, signing, transfer, or custody authority.

## Bank data: Revolut, Banco BPI, moey

Bank access uses a regulated PSD2 Account Information Service Provider (AISP) integration rather than making the Hermes host behave as an unlicensed TPP.

The initial provider contract is GoCardless Bank Account Data because it operates as an AISP in the EEA and exposes account, balance, and transaction information. Institution coverage is checked during connection because availability can change by institution, account type, country, or provider maintenance.

Target institutions are:

- Revolut
- Banco BPI
- moey

BPI and moey expose PSD2/Open-Banking connectivity through the Portuguese/SIBS ecosystem; Revolut also exposes Open Banking to regulated TPPs/partners. If the selected aggregator cannot currently connect a target institution, the connection stays unavailable rather than falling back to credential scraping or browser automation.

Allowed bank capabilities:

- list connected accounts;
- account metadata/IBAN where returned by the provider;
- balances;
- transaction history;
- freshness/consent status.

Denied bank capabilities:

- payment initiation;
- transfers;
- beneficiary management;
- card/account administration;
- password/PIN/MFA collection.

## Trading 212

Trading 212 supports permission-scoped API keys and separate demo/live API environments. Hermes uses a live-account key configured for read-only account/portfolio/history permissions, with provider-side IP restrictions required when available.

Allowed:

- account summary;
- positions;
- dividends/history;
- cash transactions and portfolio observations.

Denied:

- order placement;
- order modification;
- order cancellation.

Any future trading capability must use a different credential and a new reviewed execution resource. A read-only key must never be upgraded in place.

## Pionex

Pionex API endpoints declare permissions such as `Read` and `Trade`. Hermes uses a key with `Read` only.

Allowed:

- balances;
- open-order observation;
- order history;
- fills/history.

Denied:

- `Trade` permission;
- new orders;
- cancellations;
- withdrawals or transfers.

## Ledger

Ledger access uses the Ledger Wallet API with read-only account-list capability. The integration may learn which accounts/public assets the user has chosen to expose, but it cannot request signatures or receive secret key material.

Allowed:

- `account.list`;
- public account metadata needed for portfolio observation.

Denied:

- transaction signing;
- message signing;
- transaction broadcasting;
- private keys;
- seed/recovery phrases;
- production wallet custody changes.

User Ledger assets are observation-only and are never used as the agent experimentation wallet.

## Normalized financial view

`financial-data-steward` consumes these sources through `financial-data-hub` and exposes a normalized, source-aware internal view to Portfolio Manager, Wealth Manager, Financial Advisor, analysts, accounting, and risk profiles when recruited.

The normalized data records provider, source-account alias/token, asset/currency, units/balance, valuation currency, observed timestamp, and freshness. Raw provider credentials are never handed to Profiles.

## Future write access

`financial-execution-gateway@0.1.0` is deliberately disabled and has zero executable capabilities. Future bank payments, securities orders, crypto transfers, wallet signing, or other real-money actions require a new reviewed version with explicit user authority, account scoping, limits, fresh confirmation, audit trail, credential isolation, idempotency, and provider/jurisdiction review.

Recommendation and execution remain separate responsibilities.

## Agent-owned cryptocurrency sandbox

`agent-sandbox-wallet` gives Hermes an agent-controlled wallet only on approved public test networks. Initial allowed networks are Ethereum Sepolia and Solana Devnet.

The sandbox may:

- create resettable testnet accounts;
- receive faucet/test tokens;
- sign and send testnet transactions;
- deploy test contracts;
- interact with reviewed testnet dApps;
- simulate transactions and inspect receipts/events.

It must never:

- connect to mainnet;
- receive real-value assets;
- use a fiat on-ramp;
- receive production exchange withdrawals;
- bridge value to mainnet;
- import the user's Ledger/private wallet material;
- expose its own secret material in logs or user-visible output.

`crypto-sandbox-operator` owns sandbox execution. Cryptocurrency Manager and Blockchain Researcher may recruit it for experiments, but their production/user portfolio permissions do not flow into the sandbox and sandbox signing authority does not flow back into production wallets.
