# Schema, Mathematical Formulations & Discrepancy Reconciliation Methodology

## 1. SQL Warehouse Schema (`SQL Joins & CTEs`)

- `fct_retail_omnichannel_orders` (`64,000` rows): Customer-level randomized experiment assignments mapped to `48` regional market cohorts (`MKT_01`–`MKT_48`) and `4` retail checkout surfaces (`Brick_And_Mortar_POS`, `Amazon_Marketplace`, `Walmart_Connect_POS`, `DTC_Brand_Site`).
- `fct_social_content_velocity` (`39,644` rows): Content-level video count, image count, search keyword velocity index, sentiment polarity, subjectivity, and viral shares mapped to CPG/retail verticals and `48` regional markets.
- `fct_creator_video_engagement` (`1,956` rows): Creator stream interactions and affiliate promotional link flags mapped across the `48` regional markets.

## 2. Causal Incrementality & Halo Measurement Formulations

1. **Matched-Market Pre/Post Difference-in-Differences (DiD):**
   $$\hat{\tau}_{\text{DiD}} = \frac{1}{M}\sum_{m=1}^{M}\left[\left(\bar{Y}_{m,T,\text{post}} - \bar{Y}_{m,T,\text{pre}}\right) - \left(\bar{Y}_{m,C,\text{post}} - \bar{Y}_{m,C,\text{pre}}\right)\right]$$
2. **Simplex-Constrained Synthetic Control:**
   $$\min_{\mathbf{w} \in \Delta^{J-1}} \left\|\mathbf{Y}_{1,\text{pre}} - \sum_{j=1}^{J} w_j \mathbf{Y}_{0j,\text{pre}}\right\|_2^2 \quad \text{s.t.} \quad w_j \ge 0, \quad \sum_{j=1}^{J} w_j = 1$$
3. **Omnichannel Retail & Marketplace Halo Multiplier:**
   $$\text{Halo Multiplier} = \frac{\Delta \text{GMV}_{\text{DTC}} + \Delta \text{GMV}_{\text{Brick-and-Mortar POS}} + \Delta \text{GMV}_{\text{Amazon}} + \Delta \text{GMV}_{\text{Walmart Connect}}}{\Delta \text{GMV}_{\text{DTC}}}$$
4. **Geometric Adstock & Hill Saturation MMM:**
   $$A_{m,t} = X_{m,t} + \lambda A_{m,t-1}, \qquad H(A_{m,t}) = \frac{A_{m,t}^{\gamma}}{\kappa^{\gamma} + A_{m,t}^{\gamma}}$$

## 3. Native Social Shop vs. Third-Party Discrepancy Taxonomy

- **Attribution Window Delta (`+2.65%` Native vs. Canonical):** Native social shop Seller/Affiliate Center credits 7-day click + 1-day view conversions, whereas third-party last-touch POS/web trackers use 1-day click.
- **Return & Cancellation Settlement Lag (`+1.50%` Native vs. Canonical):** Unshipped cancellations and post-settlement returns remain in gross native order logs until settlement batch closure.
- **UTC vs. Local Store Timezone Cutoff (`-1.45%` 3P vs. Canonical):** Third-party intelligence tools cut daily partitions at `00:00 UTC` versus local retailer POS register close.
- **Unmapped Affiliate Sample SKUs (`-1.24%` 3P vs. Canonical):** Creator sample bundle SKUs lacking parent-child GTIN/UPC crosswalks in third-party scrapers.
