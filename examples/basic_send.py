"""
Basic send example for TouchDesigner.
Run this in a Text DAT Execute or Script CHOP.
"""

from veilmail_td import VeilMailTD


def onStart():
    """Called when the project starts (or paste into a Script CHOP callback)."""

    def on_success(key, result):
        print(f"[VeilMail] Success ({key}): {result}")
        # Optionally update a Text TOP or DAT with the result
        # op('status_text').text = f"Email sent: {result.get('id', '')}"

    def on_error(key, error):
        print(f"[VeilMail] Error ({key}): {error}")

    vm = VeilMailTD(
        api_key="veil_live_xxxxx",  # Replace with your API key
        on_success=on_success,
        on_error=on_error,
    )

    # Send an email (non-blocking)
    vm.send_email(
        from_addr="hello@yourdomain.com",
        to="user@example.com",
        subject="Hello from TouchDesigner!",
        html="<h1>Sent from TD</h1><p>This email was triggered by a TouchDesigner network.</p>",
    )


# For use in a Text DAT with "Run" button:
if __name__ != "__main__":
    onStart()
