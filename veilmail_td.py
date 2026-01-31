"""
Veil Mail TouchDesigner Integration
Thin wrapper around the Veil Mail Python SDK for use inside TouchDesigner.
"""

import threading
from typing import Optional, Callable, Any

try:
    import veilmail
except ImportError:
    raise ImportError(
        "veilmail package not found. Install it into TouchDesigner's Python:\n"
        "  <TD Python path>/python -m pip install veilmail"
    )


class VeilMailTD:
    """TouchDesigner-friendly wrapper around the Veil Mail Python SDK."""

    def __init__(self, api_key: str, base_url: str = "https://api.veilmail.xyz",
                 on_success: Optional[Callable] = None,
                 on_error: Optional[Callable] = None):
        self.client = veilmail.VeilMail(api_key, base_url=base_url)
        self._on_success = on_success
        self._on_error = on_error

    def _run_threaded(self, func: Callable, callback_key: str = "result"):
        """Run an API call on a background thread to avoid blocking TD's cook."""
        def _worker():
            try:
                result = func()
                if self._on_success:
                    # Use run() to post back to main thread on next frame
                    import td  # type: ignore
                    td.run(lambda: self._on_success(callback_key, result), delayFrames=1)
            except Exception as e:
                if self._on_error:
                    import td  # type: ignore
                    td.run(lambda: self._on_error(callback_key, e), delayFrames=1)
                else:
                    print(f"[VeilMail] Error: {e}")

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        return t

    def send_email(self, from_addr: str, to: str, subject: str,
                   html: str = "", text: str = "",
                   template_id: str = "", template_data: Optional[dict] = None):
        """Send an email in a background thread."""
        def _do():
            params: dict[str, Any] = {
                "from_": from_addr,
                "to": to,
                "subject": subject,
            }
            if html:
                params["html"] = html
            if text:
                params["text"] = text
            if template_id:
                params["template_id"] = template_id
            if template_data:
                params["template_data"] = template_data
            return self.client.emails.send(**params)

        return self._run_threaded(_do, "send_email")

    def list_templates(self):
        """Fetch templates in a background thread."""
        return self._run_threaded(
            lambda: self.client.templates.list(),
            "list_templates"
        )

    def check_connection(self):
        """Test the API connection in a background thread."""
        return self._run_threaded(
            lambda: self.client.domains.list(),
            "check_connection"
        )

    def send_email_sync(self, from_addr: str, to: str, subject: str,
                        html: str = "", text: str = "",
                        template_id: str = "", template_data: Optional[dict] = None):
        """Send an email synchronously (blocks the cook thread — use only in scripts)."""
        params: dict[str, Any] = {
            "from_": from_addr,
            "to": to,
            "subject": subject,
        }
        if html:
            params["html"] = html
        if text:
            params["text"] = text
        if template_id:
            params["template_id"] = template_id
        if template_data:
            params["template_data"] = template_data
        return self.client.emails.send(**params)
