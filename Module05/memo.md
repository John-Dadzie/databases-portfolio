# Module 5 recommendation memo

**To:** Lea Winter and Yasmin Kaya  
**Subject:** Choosing the dashboard design

Keep the operational tables normalized to 3NF: `machine`, `part`, `job`, and
`job_part` store each fact once and preserve foreign-key integrity. The
denormalized `report_jobpart` is a useful read model only when the dashboard
workload makes its extra storage and maintenance worthwhile. In this run both
designs returned the same grouped rows, while one site change touched 1
normalized row versus 4,000 report rows; the benchmark output records the
measured timings, plans, and storage. The report copy should therefore be
rebuilt by a scheduled job after operational changes rather than edited as an
independent source of truth. The refresh should verify row counts and a
price-sum checksum before publication, and a failed check should mark the
dashboard stale and alert its owner. If the dashboard becomes join-heavy or
larger than memory, rerun the benchmark before changing the design.
