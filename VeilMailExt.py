"""
VeilMail TouchDesigner Extension
Attach this to a Base COMP with custom parameters to create a VeilMail component.
See VeilMailPars.json for the parameter definitions.
"""

import threading
from typing import Any


class VeilMailExt:
    """
    COMP extension for VeilMail integration.

    Attach to a Base COMP and configure custom parameters on the 'VeilMail' page:
      - Apikey (str): Your Veil Mail API key
      - Baseurl (str): API base URL (default: https://api.veilmail.xyz)
      - From (str): Default sender address
      - To (str): Recipient address
      - Subject (str): Email subject
      - Body (str): Email HTML body
      - Templateid (str): Optional template ID
      - Send (pulse): Trigger email send
      - Status (str, read-only): Last operation status
    """

    def __init__(self, ownerComp):  # noqa: N803
        self.ownerComp = ownerComp
        self._client = None

    @property
    def Client(self):
        """Lazy-initialize the VeilMail client from component parameters."""
        api_key = self.ownerComp.par.Apikey.eval()
        if not api_key:
            self._set_status("Error: API key not set")
            return None

        if self._client is None:
            try:
                from veilmail_td import VeilMailTD
                base_url = self.ownerComp.par.Baseurl.eval() or "https://api.veilmail.xyz"
                self._client = VeilMailTD(
                    api_key=api_key,
                    base_url=base_url,
                    on_success=self._on_success,
                    on_error=self._on_error,
                )
                self._set_status("Client initialized")
            except ImportError as e:
                self._set_status(f"Error: {e}")
                return None
        return self._client

    def _set_status(self, msg: str):
        """Update the Status parameter (read-only display)."""
        try:
            self.ownerComp.par.Status = msg
        except Exception:
            print(f"[VeilMail] {msg}")

    def _on_success(self, key: str, result: Any):
        """Callback when an API call succeeds."""
        if key == "send_email":
            email_id = result.get("id", "unknown") if isinstance(result, dict) else str(result)
            self._set_status(f"Sent: {email_id}")
        elif key == "check_connection":
            self._set_status("Connected")
        elif key == "list_templates":
            count = len(result.get("data", [])) if isinstance(result, dict) else 0
            self._set_status(f"Found {count} templates")
        else:
            self._set_status(f"OK: {key}")

    def _on_error(self, key: str, error: Exception):
        """Callback when an API call fails."""
        self._set_status(f"Error ({key}): {error}")

    def SendEmail(self):
        """Triggered by the Send pulse parameter."""
        client = self.Client
        if not client:
            return

        from_addr = self.ownerComp.par.From.eval()
        to = self.ownerComp.par.To.eval()
        subject = self.ownerComp.par.Subject.eval()
        body = self.ownerComp.par.Body.eval()
        template_id = self.ownerComp.par.Templateid.eval()

        if not from_addr or not to:
            self._set_status("Error: From and To are required")
            return

        self._set_status("Sending...")
        client.send_email(
            from_addr=from_addr,
            to=to,
            subject=subject or "(no subject)",
            html=body,
            template_id=template_id or "",
        )

    def TestConnection(self):
        """Test the API connection."""
        client = self.Client
        if client:
            self._set_status("Testing connection...")
            client.check_connection()

    def Refresh(self):
        """Re-create the client (e.g., after changing API key)."""
        self._client = None
        self._set_status("Client reset")
