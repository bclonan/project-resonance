import random
import os, sys
# Ensure we import the local workspace package first
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import phiresearch_compression as phicomp
import importlib
import phiresearch_compression.core_bindings as core_bindings
if not hasattr(core_bindings, "reset_rgbd_state"):
    # Attempt reload if running in a long-lived interpreter with stale symbol table
    core_bindings = importlib.reload(core_bindings)

def maybe_reset():
    if hasattr(core_bindings, 'reset_rgbd_state'):
        core_bindings.reset_rgbd_state()

def maybe_set_rgbd(on: bool, weight: float = 0.0):
    if hasattr(core_bindings, 'set_rgbd_options'):
        if weight > 0:
            core_bindings.set_rgbd_options(on, weight)
        else:
            core_bindings.set_rgbd_options(on)


def test_roundtrip_baseline():
    maybe_reset()
    maybe_set_rgbd(False)
    samples = [b"", b"a", b"The quick brown fox", b"0123456789" * 10,
               bytes([random.randint(0, 255) for _ in range(512)])]
    for sample in samples:
        comp = phicomp.compress(sample)
        decomp = phicomp.decompress(comp)
        assert decomp == sample


def test_roundtrip_with_rgbd():
    maybe_reset()
    maybe_set_rgbd(True, 0.2)
    sample = b"RGBD test payload" * 5
    comp = phicomp.compress(sample)
    maybe_reset()
    decomp = phicomp.decompress(comp)
    assert decomp == sample


def test_header_integrity():
    maybe_reset()
    data = b"header integrity test" * 3
    c = phicomp.compress(data)
    assert c.startswith(b"PHIC") and len(c) >= 14
    sz = 0
    for i in range(8):
        sz |= c[6 + i] << (i * 8)
    assert sz == len(data)
    core_bindings.reset_rgbd_state()
    d = phicomp.decompress(c)
    assert d == data
