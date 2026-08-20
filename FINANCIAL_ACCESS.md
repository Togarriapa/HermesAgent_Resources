# Financial Account Access Architecture

Hermes financial integrations are split into four deliberately separate layers:

1. **Read-only personal financial data** — `financial-data-hub`.
2. **Real-money execution** — `financial-execution-gateway`, technically write-capable but callable only from a one-shot explicit user order plus fresh confirmation.
3. **Agent live wallet** — `agent-live-wallet`, a dedicated real-value wallet with the same explicit-order confirmation gate.
4. **Agent experimentation wallet** — `agent-sandbox-wallet`, autonomous only on approved public test networks and faucet/test assets.

The separation is structural: analytical Profiles never receive raw credentials or implicit transaction authority, and a recommendation can never self-authorize its own execution.

## Authorization model for real money

Every bank payment, broker/exchange order, Ledger transaction, or dedicated agent-live-wallet mainnet transaction requires:

- an explicit user order routed through Hermes;
- a one-shot authorization envelope bound to the exact provider, account, operation and economic parameters;
- a fresh confirmation of the final normalized action payload;
- revalidation of current account/balance/position state before execution;
- simulation/fee/slippage estimation where supported;
- duplicate/replay protection;
- reconciliation and an immutable audit event after execution.

Authorization expires after five minutes and cannot be wildcarded, reused, inferred from a strategy, converted from a recommendation, or delegated as standing authority.

## Bank data and payments: Revolut, Banco BPI, moey

Read access uses a regulated PSD2 Account Information Service Provider (AISP) connection. Write/payment access uses a regulated Payment Initiation Service Provider (PISP) adapter when provider and institution coverage permit it. Hermes does not scrape banking credentials or impersonate an unlicensed TPP.

Target institutions are:

- Revolut
- Banco BPI
- moey

Banco BPI exposes account-information and payment-initiation APIs through SIBS API Market. moey documents PSD2 AIS and PIS/PISP support through the same Portuguese Open Banking ecosystem. Revolut's Open Banking API supports account information and payment initiation for regulated TPPs/approved partners. Actual coverage and available payment types are checked at connection time.

Read capabilities:

- accounts and metadata;
- balances;
- transaction history;
- consent/freshness state.

Write capability:

- initiate the exact payment explicitly ordered and confirmed by the user, through the regulated provider's consent/SCA flow.

Not granted:

- autonomous payments or transfers;
- beneficiary/account/card administration;
- standing or scheduled authority created by the agent;
- passwords, PINs or reusable MFA secrets.

## Trading 212

Trading 212's Public API supports live account/portfolio data and live Market, Limit, Stop and Stop-Limit order placement plus cancellation of pending orders. API keys have selectable permissions and can be IP-restricted.

Hermes therefore uses two separate credentials:

- `TRADING212_READONLY_CREDENTIALS` for observation;
- `TRADING212_EXECUTION_CREDENTIALS` with the minimum order permission required for explicitly ordered trades.

Execution rules:

- live order endpoints are callable only by `financial-execution-operator` after explicit user order + fresh confirmation;
- the gateway must add duplicate protection because the beta API warns that some order endpoints are not idempotent;
- funding/withdrawals and account administration remain denied;
- IP restriction is required in the Hermes policy.

## Pionex

Pionex separates `Read` and `Trade` permissions. Hermes therefore uses separate keys:

- `PIONEX_READONLY_API_CREDENTIALS` with `Read` only;
- `PIONEX_TRADE_API_CREDENTIALS` with the minimum `Trade` permission required for order placement/cancellation.

The Trade key may be invoked only by the execution gateway after explicit user order + fresh confirmation. Withdrawals, transfers and account administration remain denied.

## Ledger

Ledger Wallet API permissions are separated by capability. Read observation uses `account.list`. The execution gateway is configured for `transaction.sign` and `transaction.signAndBroadcast`, but each real transaction still requires the Hermes explicit-order gate and the Ledger user's hardware/on-device confirmation.

Allowed after explicit user order + confirmation:

- sign the exact confirmed transaction;
- sign and broadcast the exact confirmed transaction.

Still denied:

- arbitrary message signing by default;
- seed/recovery phrase access;
- private-key access;
- production signing without the explicit Hermes authorization envelope and Ledger confirmation.

The user's Ledger is never used as the agent-owned wallet.

## Normalized financial view

`financial-data-steward` consumes read sources through `financial-data-hub` and exposes a normalized, source-aware internal view to Portfolio Manager, Wealth Manager, Financial Advisor, analysts, accounting, and risk profiles when recruited.

The normalized data records provider, source-account alias/token, asset/currency, units/balance, valuation currency, observation timestamp, and freshness. Raw provider credentials are never handed to Profiles.

## Execution operator

`financial-execution-operator` is separate from advisors/managers/researchers. It executes exactly one confirmed action and may not optimize, resize, substitute, split, retry with changed parameters, or add follow-on actions without a new user order.

This preserves the architecture:

`Research/Manager -> recommendation -> Hermes -> explicit user order + confirmation -> Financial Execution Operator -> provider -> reconciliation -> Hermes`

## Dedicated agent live wallet

`agent-live-wallet` is a separate real-value wallet owned for Hermes use. It can receive real assets and is technically able to construct, sign and broadcast mainnet transactions on an explicit configured network allowlist.

Private keys are generated locally and stored in the host encrypted secret boundary. They are never exported to Profiles, logs, the repository, or the user's Ledger.

For real-value use, however, the wallet follows the same execution gate as all other production financial accounts: every transfer, swap, contract call, approval, bridge, staking action or other economic transaction requires a specific user order and fresh confirmation. The agent may autonomously research, monitor, simulate and prepare a proposed transaction, but it cannot autonomously commit real value.

## Agent-owned cryptocurrency sandbox

`agent-sandbox-wallet` remains available for autonomous experimentation on approved public test networks. Initial allowed networks are Ethereum Sepolia and Solana Devnet.

The sandbox may autonomously:

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
- expose secret material in logs or user-visible output.

This gives agents unrestricted operational learning in the sandbox while keeping real economic execution tied to the user's explicit order.
