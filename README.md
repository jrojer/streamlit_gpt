### `run gpt chat with text and pictures using streamlit and openai`
## Getting started:
1. Install packages.
```bash
pip install -r requirements.txt
```

2. Set up `config.json`.
```bash
cp config.json_ex config.json
```

3. Set your `openai_api_key` in `config.json`.

4. Run.
```python
python entrypoint.py
```

## Further steps:
You can enable authorisation by setting `enable_auth` and `password_hash` in `config.json`.

### How to generate password hash:
```python
hashlib.sha256(password.encode("utf-8")).hexdigest()
```
