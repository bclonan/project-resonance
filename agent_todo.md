# TODO for AI Agents

1. [ ] Fuse RGBD smoothing tensor into Codec::encode_bytes and decode_bytes.
2. [ ] Apply soft φ-weighted frequency bias from GridCtx at (x, y, t).
3. [ ] Update RGBD tensor with per-symbol posteriors at runtime.
4. [ ] Add smooth_once() every 8 symbols during encode.
5. [ ] Plot GridCtx usage heatmaps as PNG/GIFs.
6. [ ] Validate determinism: hash compressed output.
7. [ ] Extend benchmark: include new bpb, runtime, memory stats.
