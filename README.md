# VeilMail TouchDesigner Integration

TouchDesigner integration for Veil Mail using the Python SDK. This package provides a thin wrapper, extension class, callback scripts, and parameter definitions for building VeilMail-powered TouchDesigner components.

TouchDesigner runs Python 3.11 natively, so the existing Veil Mail Python SDK works as-is. This integration adds TouchDesigner-specific conveniences: threaded API calls that won't block the cook thread, a COMP extension with custom parameters, and callback wiring for UI-driven workflows.

## Prerequisites

- **TouchDesigner 2023+** (Python 3.11 environment)
- **Veil Mail Python SDK** installed into TouchDesigner's Python
- A Veil Mail account with an API key (`veil_live_xxx` or `veil_test_xxx`)

## Installation

### 1. Install the Python SDK into TouchDesigner's Python

Locate your TouchDesigner Python executable and install the `veilmail` package:

**macOS:**
```bash
/Applications/TouchDesigner.app/Contents/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pip install veilmail
```

**Windows:**
```cmd
"C:\Program Files\Derivative\TouchDesigner\bin\python.exe" -m pip install veilmail
```

Verify the installation by opening a Text DAT in TouchDesigner and running:
```python
import veilmail
print(veilmail.__version__)
```

### 2. Copy integration files to your project

Copy these files into your TouchDesigner project folder (or add them to TD's Python search path):

- `veilmail_td.py` -- Thin wrapper with threaded API calls
- `VeilMailExt.py` -- COMP extension class
- `VeilMailCallbacks.py` -- DAT execute callbacks (optional)
- `VeilMailPars.json` -- Parameter definitions reference

## Component Setup

### Create the VeilMail COMP

1. **Create a Base COMP** and name it `veilmail`.

2. **Add a custom parameter page** named `VeilMail`.

3. **Create the following parameters** on that page (see `VeilMailPars.json` for full definitions):

   | Name           | Type   | Description                        |
   |----------------|--------|------------------------------------|
   | Apikey         | Str    | Your Veil Mail API key             |
   | Baseurl        | Str    | API base URL (default provided)    |
   | From           | Str    | Sender email address               |
   | To             | Str    | Recipient email address            |
   | Subject        | Str    | Email subject line                 |
   | Body           | Str    | Email HTML body content            |
   | Templateid     | Str    | Optional template ID               |
   | Send           | Pulse  | Trigger email send                 |
   | Testconnection | Pulse  | Test the API connection            |
   | Refresh        | Pulse  | Re-initialize the client           |
   | Status         | Str    | Last operation status (read-only)  |

4. **Attach the extension:** In the COMP's Extensions parameter, add `VeilMailExt.py` and set the Extension Object to `VeilMailExt`.

5. **Place Python files** (`veilmail_td.py`, `VeilMailExt.py`) in your project folder or TouchDesigner's Python path.

6. **(Optional)** Wire `VeilMailCallbacks.py` to a DAT Execute for button-driven interactions.

## Usage Examples

### Quick send (script)

```python
from veilmail_td import VeilMailTD

vm = VeilMailTD(api_key="veil_live_xxxxx")

# Non-blocking send (safe for cook thread)
vm.send_email(
    from_addr="hello@yourdomain.com",
    to="user@example.com",
    subject="Hello from TouchDesigner!",
    html="<h1>Sent from TD</h1>",
)
```

### Using the COMP

Once you have the `veilmail` Base COMP set up with the extension:

1. Fill in **API Key**, **From**, **To**, **Subject**, and **Body** parameters.
2. Click the **Send Email** pulse button.
3. Watch the **Status** parameter for confirmation or errors.

### With callbacks

```python
def on_success(key, result):
    op('status_text').text = f"Done: {result}"

def on_error(key, error):
    op('status_text').text = f"Error: {error}"

vm = VeilMailTD(
    api_key="veil_live_xxxxx",
    on_success=on_success,
    on_error=on_error,
)

vm.send_email(
    from_addr="hello@yourdomain.com",
    to="user@example.com",
    subject="Event triggered!",
    html="<p>Something happened in the network.</p>",
)
```

### Template email

```python
vm.send_email(
    from_addr="hello@yourdomain.com",
    to="user@example.com",
    subject="Weekly Report",
    template_id="tmpl_abc123",
    template_data={"name": "Operator", "week": "2025-01"},
)
```

## API Reference

### VeilMailTD

| Method                | Blocking | Description                          |
|-----------------------|----------|--------------------------------------|
| `send_email()`        | No       | Send email on a background thread    |
| `send_email_sync()`   | Yes      | Send email synchronously             |
| `send_template_email()`| No      | Send using a template (background)   |
| `list_templates()`    | No       | Fetch templates (background)         |
| `check_connection()`  | No       | Test API connectivity (background)   |

### VeilMailExt (COMP Extension)

| Method             | Description                              |
|--------------------|------------------------------------------|
| `SendEmail()`      | Send email using COMP parameters         |
| `TestConnection()` | Test API connection                      |
| `Refresh()`        | Re-create the client                     |

## Security Note

TouchDesigner installations are operator-controlled environments. Direct API key usage in parameters and scripts is safe in this context, as the keys remain local to the machine running the TouchDesigner project. For shared projects, consider using environment variables or a separate configuration file that is excluded from version control.

## File Reference

| File                    | Purpose                                      |
|-------------------------|----------------------------------------------|
| `veilmail_td.py`        | Thin wrapper with threaded API calls         |
| `VeilMailExt.py`        | COMP extension class                         |
| `VeilMailCallbacks.py`  | DAT execute callback scripts                 |
| `VeilMailPars.json`     | Parameter definitions for the component      |
| `requirements.txt`      | Python dependencies                          |
| `examples/`             | Example scripts                              |
