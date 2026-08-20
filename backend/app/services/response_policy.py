
SAFE_ACTIONS = {"notify", "create_incident", "add_tag", "quarantine_file"}
HIGH_IMPACT_ACTIONS = {"isolate_endpoint", "disable_account", "block_network_destination"}

def requires_approval(action: str, mode: str = "approval_required") -> bool:
    if action in HIGH_IMPACT_ACTIONS:
        return mode != "automatic"
    return False
