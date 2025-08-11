# Reflection Compression Demo

This demo shows how to use the `phiresearch_compression` (`phicomp`) library on both the backend (FastAPI) and frontend (vanilla JS) to:

1. Enumerate local reflection/metadata files stored under the `/data` folder.
2. Compress any file with `phicomp` (and compute a gzip baseline) returning sizes, savings, Base64 payload + hash.
3. Fetch an arbitrary public file from a GitHub raw URL, compress it, and stage it for later reconstruction.
4. Decode any Base64 `phicomp` payload back into its exact original bytes, verifying with SHA-256.

## Backend Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/reflection/list` | GET | List local files with size, SHA-256, preview. |
| `/api/reflection/get?name=FILENAME` | GET | Compress specified local file (phicomp + gzip baseline metrics) and return Base64 payload. |
| `/api/reflection/decode` | POST JSON `{ b64_phicomp }` | Decompress payload and return preview + hash. |
| `/api/reflection/fetch_github?raw_url=...` | GET | Fetch a raw GitHub file (only raw.githubusercontent.com), compress (phicomp + gzip metrics). |
| `/demo/reflection` | GET | HTML UI for interacting with the above. |

## Data Folder Structure

```text
project-resonance/
  data/
    sample1.txt
    sample2.md
    notes.json
```

Add any additional files to `data/` and they will automatically appear in the listing endpoint/UI.

## How It Works

1. Listing uses Python `pathlib` to iterate over `data/` and compute SHA-256 and a preview (first ~160 UTF-8 decodable bytes).
2. Compression uses `phicomp.compress(bytes)`; gzip (`zlib`) is also computed for a factual baseline; both sizes and savings percentages are reported; the phicomp bytes are Base64-encoded for transport.
3. Decoding reverses: Base64 decode -> `phicomp.decompress()` -> verify SHA-256.
4. External GitHub files are fetched via a raw URL (must start with `https://raw.githubusercontent.com/`). The same compression + Base64 packaging is applied.

## Export Format

The JSON structure returned by `/api/reflection/get` or `/api/reflection/fetch_github`:
 
```json
{
  "name": "sample1.txt",
  "original_size": 1234,
  "compressed_size": 456,
  "gzip_size": 612,
  "savings_vs_raw_phicomp_pct": 63.05,
  "savings_vs_raw_gzip_pct": 50.40,
  "savings_vs_gzip_phicomp_pct": 25.50,
  "sha256_raw": "...",
  "b64_phicomp": "BASE64_COMPRESSED_DATA"
}
```
Store only `b64_phicomp` and `sha256_raw` and you can later restore the original file and verify integrity.


## Frontend UI

The page `reflection_demo.html` provides:

- Table of local files with metadata.
- Button to compress a file (fills a textarea with `b64_phicomp`).
- Button to decode the current textarea payload back to raw preview.
- Input to fetch a GitHub raw URL and compress it.

All logic is plain JavaScript (`fetch`) for easy integration elsewhere.

## Example Workflow

1. Navigate to `http://127.0.0.1:8000/demo/reflection`.
2. Click "Refresh List" (auto-runs on load) to see local files.
3. Click "Compress" next to `sample2.md`.
4. Observe metadata and Base64 in the textarea.
5. Click "Decode This Payload" to reconstruct and verify hash.
6. Paste a GitHub raw URL (e.g., a LICENSE file) and click Fetch & Compress.
7. Optionally store the Base64 + hash somewhere (DB, file, ledger).

## Adding to Another Project

Minimal backend pseudo-code:
 
```python
raw = open(path, 'rb').read()
comp = phicomp.compress(raw)
package = {
  'sha256_raw': hashlib.sha256(raw).hexdigest(),
  'b64_phicomp': base64.b64encode(comp).decode('ascii')
}
```
Decoding:
 
```python
comp = base64.b64decode(package['b64_phicomp'])
raw = phicomp.decompress(comp)
assert hashlib.sha256(raw).hexdigest() == package['sha256_raw']
```

## Integrity & Verification

- SHA-256 ensures the restored bytes match the original exactly.
- If the hash mismatches, reject the artifact.
- You can chain this with an external signature or blockchain anchor for tamper evidence.

## Security Notes

- Only `raw.githubusercontent.com` URLs are allowed to mitigate SSRF risk.
- No file writes are performed; decoding endpoint returns data and preview only.
- Add rate limiting or authentication if exposing publicly.

## Next Improvements (Optional)

- Add streaming chunked compression for very large files.
- Provide an index manifest (JSON) listing stored reflections with timestamps.
- (Done) Provide a secondary codec baseline (gzip) for ratio comparison.
- Add download buttons to retrieve reconstructed file as an attachment.

## License

Follows the main project license. See `LICENSE` in repository root.
