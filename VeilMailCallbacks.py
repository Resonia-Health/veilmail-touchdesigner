"""
VeilMail DAT Execute Callbacks
Wire these callbacks to a DAT or Button COMP to trigger VeilMail actions.

Usage:
  1. Create a DAT Execute DAT
  2. Set the DAT to watch your button/panel
  3. Paste this script (or reference it)
"""


def onPulse(par):
    """Called when a pulse parameter is triggered."""
    name = par.name

    # Find the VeilMail COMP (assumes it's a sibling or parent)
    vm = par.owner.parent().op('veilmail')
    if vm is None:
        print("[VeilMail] Could not find 'veilmail' COMP")
        return

    ext = vm.ext.VeilMailExt

    if name == 'Send':
        ext.SendEmail()
    elif name == 'Testconnection':
        ext.TestConnection()
    elif name == 'Refresh':
        ext.Refresh()


def onValueChange(par, prev):
    """Called when a parameter value changes."""
    name = par.name

    # Reset client when API key or base URL changes
    if name in ('Apikey', 'Baseurl'):
        vm = par.owner
        if hasattr(vm, 'ext') and hasattr(vm.ext, 'VeilMailExt'):
            vm.ext.VeilMailExt.Refresh()
