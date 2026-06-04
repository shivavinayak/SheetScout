#!/usr/bin/env python3
import os
import csv

def print_banner():
    banner = r"""
  ╔══════════════════════════════════════════════════════════════╗
  ║                                                              ║
  ║   ███████╗██╗  ██╗███████╗███████╗████████╗                 ║
  ║   ██╔════╝██║  ██║██╔════╝██╔════╝╚══██╔══╝                 ║
  ║   ███████╗███████║█████╗  █████╗     ██║                    ║
  ║   ╚════██║██╔══██║██╔══╝  ██╔══╝     ██║                    ║
  ║   ███████║██║  ██║███████╗███████╗   ██║                    ║
  ║   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝                    ║
  ║                                                              ║
  ║    ███████╗ ██████╗ ██████╗ ██╗   ██╗████████╗              ║
  ║    ██╔════╝██╔════╝██╔═══██╗██║   ██║╚══██╔══╝              ║
  ║    ███████╗██║     ██║   ██║██║   ██║   ██║                 ║
  ║    ╚════██║██║     ██║   ██║██║   ██║   ██║                 ║
  ║    ███████║╚██████╗╚██████╔╝╚██████╔╝   ██║                 ║
  ║    ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝                 ║
  ║                                                              ║
  ║          🔍  CSV Keyword Search Tool  📄                     ║
  ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def get_search_directory():
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │              📁  Set Search Directory                │")
    print("  └─────────────────────────────────────────────────────┘")
    print()
    path = input("  Enter folder path to search (or press Enter for current dir): ").strip()
    if not path:
        path = "."
    # Strip surrounding quotes in case user drag-drops a path
    path = path.strip('"').strip("'")
    if not os.path.isdir(path):
        print(f"\n  ⚠  Path '{path}' not found or is not a directory.")
        print("     Falling back to current directory.\n")
        path = "."
    print(f"\n  ✔  Search directory set to: {os.path.abspath(path)}\n")
    return path


def find_csv_files(folder):
    csv_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    return csv_files


def search_in_csv(filepath, term):
    results = []
    total_cells = 0
    try:
        with open(filepath, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row_idx, row in enumerate(reader, start=2):  # row 1 = header
                for col, value in row.items():
                    total_cells += 1
                    if value and term.lower() in value.lower():
                        results.append({
                            "row"     : row_idx,
                            "column"  : col,
                            "value"   : value.strip(),
                            "full_row": dict(row),
                        })
    except Exception as e:
        print(f"  [error reading {filepath}]: {e}")
    return results, total_cells


def highlight(text, term):
    import re
    return re.sub(re.escape(term), f"[{term.upper()}]", text, flags=re.IGNORECASE)


def print_full_row(row_data, matched_col, term):
    col_width = max((len(k) for k in row_data.keys()), default=10)
    print(f"     {'─' * (col_width + 36)}")
    for col, val in row_data.items():
        val = val.strip() if val else ""
        marker = " ◄" if col == matched_col else ""
        if col == matched_col:
            val = highlight(val, term)
        print(f"     {col:<{col_width}}  :  {val}{marker}")
    print(f"     {'─' * (col_width + 36)}")


def run_search():
    print_banner()

    search_dir = get_search_directory()

    csv_files = find_csv_files(search_dir)
    if not csv_files:
        print(f"  ✖  No CSV files found in '{search_dir}'")
        return

    print(f"  ✔  Found {len(csv_files)} CSV file(s):\n")
    for f in csv_files:
        print(f"      • {f}")
    print()

    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │                  🔎  Keyword Search                  │")
    print("  └─────────────────────────────────────────────────────┘\n")

    while True:
        term = input("  Enter keyword to search (or press Enter to exit): ").strip()
        if not term:
            print("\n  👋  Goodbye! Thanks for using SheetScout.\n")
            break

        total_matches = 0
        total_cells   = 0
        print()

        for filepath in csv_files:
            results, cells = search_in_csv(filepath, term)
            total_cells   += cells
            total_matches += len(results)

            if results:
                print(f"  ── {filepath}  ({len(results)} match(es))\n")
                for r in results:
                    print(f"  Row {r['row']}  |  Match in column: \"{r['column']}\"")
                    print_full_row(r["full_row"], r["column"], term)
                    print()

        pct = (total_matches / total_cells * 100) if total_cells > 0 else 0.0
        print("  ── Summary ─────────────────────────────────────────")
        print(f"     Keyword     : '{term}'")
        print(f"     Directory   : {os.path.abspath(search_dir)}")
        print(f"     Files       : {len(csv_files)}")
        print(f"     Total cells : {total_cells:,}")
        print(f"     Matches     : {total_matches}")
        print(f"     Match rate  : {pct:.2f}%")
        print("  ────────────────────────────────────────────────────\n")


run_search()
