from typing import List, Dict, Any

def print_teaching_log(logs: List[Dict[str, Any]], max_rows: int = 20) -> None:
    if not logs:
        print("No teaching logs available.")
        return

    print("\n==================== TEACHING LOG ====================")
    print("Index | Timestamp           | Action | Sig | Price    | Shares     | PnL        | Equity")
    print("-------------------------------------------------------")

    for i, entry in enumerate(logs[:max_rows]):
        timestamp = entry.get("timestamp", "")
        action = entry.get("action", "")
        signal = entry.get("signal", 0.0)
        price = entry.get("price", 0.0)
        shares = entry.get("shares", 0.0)
        equity = entry.get("equity", 0.0)
        pnl = entry.get("pnl", 0.0)

        print(
            f"{i+1:5d} | "
            f"{str(timestamp):19} | "
            f"{action:6} | "
            f"{int(signal):+3d} | "      # <-- FIXED HERE
            f"{price:8.2f} | "
            f"{shares:10.2f} | "
            f"{pnl:10.2f} | "
            f"{equity:10.2f}"
        )

    print("=======================================================\n")
