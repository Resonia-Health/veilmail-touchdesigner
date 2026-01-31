# VeilMail TouchDesigner Examples

## basic_send.py

Demonstrates sending an email from a TouchDesigner script. Can be used in:
- A Text DAT with Run Script
- A Script CHOP callback
- A Timer CHOP callback

### Setup

1. Install the `veilmail` Python package into TouchDesigner's Python:
   ```
   /path/to/TouchDesigner/python/bin/python -m pip install veilmail
   ```

2. Copy `veilmail_td.py` to your project folder or TouchDesigner's Python path.

3. Update the API key and email addresses in the script.

4. Run the script from TouchDesigner.

## Using the Component

For a full UI-driven experience:
1. Follow the setup instructions in `VeilMailPars.json`
2. Create the Base COMP with parameters
3. Attach the `VeilMailExt` extension
4. Use the custom parameters to configure and send emails
