import sys
import os
import re
from datetime import datetime

README_FILE = 'README.md'

def update_leaderboard(score, user):
    if not os.path.exists(README_FILE):
        with open(README_FILE, 'w') as f:
            f.write("# Line Follower Challenge\n\n## Leaderboard\n| User | Time | Date |\n|---|---|---|\n")
    
    with open(README_FILE, 'r') as f:
        content = f.read()
        
    # Check if Leaderboard section exists
    if "## Leaderboard" not in content:
        content += "\n\n## Leaderboard\n| Rank | User | Time | Date |\n|---|---|---|---|\n"
        
    lines = content.splitlines()
    leaderboard_start = -1
    
    for i, line in enumerate(lines):
        if "## Leaderboard" in line:
            leaderboard_start = i
            break
            
    if leaderboard_start == -1:
        return

    # Extract entries
    entries = []
    # format: {'user': str, 'time': float, 'date': str}
    
    # Rows start after header and separator (start + 2 usually)
    table_start = leaderboard_start + 3
    
    table_end = table_start
    while table_end < len(lines) and lines[table_end].strip().startswith('|'):
        table_end += 1

    # Read existing entries
    for i in range(table_start, table_end):
        line = lines[i].strip()
        parts = [p.strip() for p in line.split('|') if p.strip()]
        
        # Handle both old format (3 columns) and new format (4 columns)
        if len(parts) == 3: # Old: User | Time | Date
            u, t, d = parts[0], parts[1], parts[2]
        elif len(parts) >= 4: # New: Rank | User | Time | Date
            u, t, d = parts[1], parts[2], parts[3]
        else:
            continue
            
        try:
            t_val = float(t.replace('s', ''))
            entries.append({'user': u, 'time': t_val, 'date': d})
        except ValueError:
            pass
                
    # Update or Add
    current_time = float(score)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    updated = False
    new_entry_added = False
    
    # Find if user exists
    user_exists = False
    for entry in entries:
        if entry['user'] == user:
            user_exists = True
            if current_time < entry['time']:
                entry['time'] = current_time
                entry['date'] = date_str
                updated = True
                print(f"Updated Personal Best for {user}: {current_time}s")
            else:
                print(f"Score {current_time}s is not better than existing {entry['time']}s for {user}.")
            break
            
    if not user_exists:
        entries.append({'user': user, 'time': current_time, 'date': date_str})
        updated = True
        new_entry_added = True

    # Always rewrite table if format changed or new entry
    # But strictly we only need if updated or if we want to enforces rank format
    # Let's enforce rank format always
    
    # Sort entries by time (asc)
    entries.sort(key=lambda x: x['time'])
    
    # Reconstruct Table with Rank
    new_table_lines = []
    new_table_lines.append("| Rank | User | Time | Date |")
    new_table_lines.append("|---|---|---|---|")
    
    for i, e in enumerate(entries):
        rank = i + 1
        # Add medal emojis for fun
        if rank == 1:
            rank_str = "🥇 1"
        elif rank == 2:
            rank_str = "🥈 2"
        elif rank == 3:
            rank_str = "🥉 3"
        else:
            rank_str = str(rank)
            
        new_table_lines.append(f"| {rank_str} | {e['user']} | {e['time']:.4f}s | {e['date']} |")
        
    # Reconstruct File Content
    # We replace everything from header to end of table
    # This overwrites the old header too
    
    # Lines before Leaderboard header
    pre_lines = lines[:leaderboard_start+1] 
    
    # Lines after table
    post_lines = lines[table_end:]
    
    # We need to act carefully. The 'pre_lines' includes "## Leaderboard"
    # Then we append our new table (header + body)
    # Then post lines
    
    final_lines = pre_lines + new_table_lines + post_lines
    
    with open(README_FILE, 'w') as f:
        f.write("\n".join(final_lines))
        
    print(f"Leaderboard updated for {user}.")

if __name__ == "__main__":
    print("Leaderboard will not be updated in the main")
