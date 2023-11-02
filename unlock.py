import os

def get_unlock_count(date):
    times = os.popen(f"grep -e 'gdm-password]: pam_unix(gdm-password:session)' -e 'gdm-password]: gkr-pam: unlocked login keyring' /var/log/auth.log | grep -i '{date}' | cut -c 8-15").read()
    
    times_list = times.split("\n")[:-1]

    return len(times_list)