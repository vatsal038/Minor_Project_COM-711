# Week 3 Multi-Source Integration & Standardization Report

- **Execution Timestamp**: 2026-10-12T18:08:25.908811+00:00
- **Total Integrated Records**: 1200
- **Total Integrated Variables**: 49

## 1. Join Coverage Across Datasets

| Source Dataset | Join Key | Matched Records | Coverage Rate |
| :--- | :--- | :--- | :--- |
| JDA Layout Approvals | `locality` | 1200 / 1200 | 100.0% |
| J&K RERA Registers | `builder_name` | 1200 / 1200 | 100.0% |
| JMC Civic Infrastructure | `locality` | 1200 / 1200 | 100.0% |
| Revenue Circle Rates | `locality` | 1200 / 1200 | 100.0% |

## 2. Market vs Statutory Circle Rate Valuation

- Min Ratio (Bargain / At Circle Rate): `0.82x`
- Median Ratio: `2.925x`
- Max Ratio (Speculative Market Premium): `10.25x`

## 3. Builder Credibility Reconciliation (Claimed vs RERA Synthesized)

- Mean Claimed Credibility Score: `6.84`
- Mean Statutory RERA Score: `6.81`
- Max Discrepancy Observed: `2.1` points
