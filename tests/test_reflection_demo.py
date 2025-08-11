import base64
import json
import os
import sys
import pathlib
import hashlib
import pytest

from fastapi.testclient import TestClient

# Ensure repo root on path for direct test invocation without install
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from resonance_demos.app import app, DATA_DIR

client = TestClient(app)

def test_list_reflections_has_samples():
    r = client.get('/api/reflection/list')
    assert r.status_code == 200
    data = r.json()
    files = {f['name']: f for f in data['files']}
    # Expect at least one known sample
    assert 'sample1.txt' in files or 'sample2.md' in files

@pytest.mark.parametrize('filename', ['sample1.txt', 'sample2.md'])
def test_compress_and_roundtrip_local(filename):
    target = DATA_DIR / filename
    if not target.exists():
        pytest.skip(f"{filename} missing")
    raw = target.read_bytes()
    # Compress
    r = client.get(f'/api/reflection/get?name={filename}')
    assert r.status_code == 200
    payload = r.json()
    assert payload['original_size'] == len(raw)
    assert payload['compressed_size'] > 0
    assert 'gzip_size' in payload
    assert payload['sha256_raw'] == hashlib.sha256(raw).hexdigest()
    # Decode preview
    decode_r = client.post('/api/reflection/decode', json={'b64_phicomp': payload['b64_phicomp']})
    assert decode_r.status_code == 200
    decoded = decode_r.json()
    assert decoded['sha256_raw'] == payload['sha256_raw']
    assert 'file_type' in decoded
    # Full file download
    dl_r = client.post('/api/reflection/decode_file', json={'b64_phicomp': payload['b64_phicomp'], 'name': filename})
    assert dl_r.status_code == 200
    assert dl_r.content == raw

def test_fetch_github_rejects_non_raw():
    r = client.get('/api/reflection/fetch_github?raw_url=https://example.com/file.txt')
    assert r.status_code == 200
    j = r.json()
    assert 'error' in j

def test_fetch_github_readme_has_file_type():
    url = 'https://raw.githubusercontent.com/bclonan/project-resonance/main/README.md'
    r = client.get('/api/reflection/fetch_github', params={'raw_url': url})
    assert r.status_code == 200
    j = r.json()
    assert 'compressed_size' in j and j['compressed_size'] > 0
    assert j.get('file_type') in ('markdown','text','json','csv','binary')
