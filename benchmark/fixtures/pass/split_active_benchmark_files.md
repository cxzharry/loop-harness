## Transcript

Before actioning on checkout, I ran:

`select_benchmarks.py --repo /tmp/product-repo --profile ux-product --intent UX_OPTIMIZE --surface checkout-web-route --metric activation --require`

Discovery loaded `.loop-harness/PRODUCT_LOOP_BENCHMARK.md` as the compact active index and also read full active cases from `.loop-harness/benchmarks/active/`.

## Selected Active Case

- Case id: checkout-visible-flow
- Source: .loop-harness/benchmarks/active/checkout-visible-flow.md
- Matching rule: checkout web-route ux-product activation
- Owner profile: ux-product
- Status: active
- Benchmark verdict: PASS before optimization

The selected benchmark ran before optimization and blocks forward actioning if it regresses. Retired cases stay in `.loop-harness/benchmarks/archive/` and are not selected as active cases.
