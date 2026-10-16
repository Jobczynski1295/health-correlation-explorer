# Verification (Pearson, full age range)

The pandas values below were independently calculated from the supplied CSV. **App shows** and **Match?** must be filled in after running the app; they have not been verified yet.

| # | Check | App shows | pandas gives | Match? |
|---|---|---|---|---|
| 1. All: age / systolic_bp | Not yet checked | r=0.463; n=4,433 | Pending |
| 2. All: bmi / waist_cm | Not yet checked | r=0.903; n=4,433 | Pending |
| 3. All: waist_cm / hdl_chol | Not yet checked | r=-0.335; n=4,433 | Pending |
| 4. Female: age / systolic_bp | Not yet checked | r=0.555; n=2,263 | Pending |
| 5. Male: age / systolic_bp | Not yet checked | r=0.351; n=2,170 | Pending |
| 6. Female heatmap: age / systolic_bp | Not yet checked | r=0.555; n=2,263 | Pending |

## M9 trap
A correlation near zero does not prove no relationship, because the relationship may be curved. Fix heatmap colors to −1 to 1 to avoid misleading comparisons.

## Code check
Inspect `app.py` to confirm sex and age filters feed every view; numeric columns exclude sex; pairwise correlations use complete pairs; and the heatmap has `vmin=-1, vmax=1`. Run and check the app yourself before marking verified.
