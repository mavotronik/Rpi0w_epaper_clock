import systemd.journal
import re

def render(draw, fonts, config):

    data = watch_miner()
    hs_pos = config.get("hs_pos", (170, 25))
    accepted_pos = config.get("accepted_pos", (170, 40))
    percentage_pos = config.get("percentage_pos", (170, 55))

    draw.text(hs_pos, data[0], font=fonts["res"], fill=0)
    draw.text(accepted_pos, f"{data[1]}", font=fonts["res"], fill=0)
    draw.text(percentage_pos, f"{data[2]}%", font=fonts["res"], fill=0)
    print("CPUMINER MULTI SYSLOG", data)


def watch_miner():
    j = systemd.journal.Reader()
    j.log_level(systemd.journal.LOG_INFO)
    j.add_match(SYSLOG_IDENTIFIER="cpuminer")
    j.seek_tail()
    
    hashrate = None
    accepted_info = None
    percentage = None
    found = False
    
    for entry in reversed(list(j)):
        msg = entry.get("MESSAGE", "")
        if not msg:
            continue
        
        # Searching string looks like: accepted: 48/48 (100.00%), 240.44 khash/s (yay!!!)
        match = re.search(r'accepted:\s+(\d+)/(\d+)\s+\(([\d.]+)%\),\s+([\d.]+)\s+([kmgt]?hash/s)', msg, re.IGNORECASE)
        
        if match:
            accepted_current = int(match.group(1))
            accepted_total = int(match.group(2))
            percentage = float(match.group(3))
            hashrate_value = float(match.group(4))
            hashrate_unit = match.group(5)
            hashrate = f"{hashrate_value} {hashrate_unit}"
            accepted_info = f"{accepted_current}/{accepted_total}"
            found = True
            break
    
    if found:
        return hashrate, accepted_info, percentage
    else:
        hashrate = "-"
        accepted_info = "-"
        percentage ="-"
        return hashrate, accepted_info, percentage