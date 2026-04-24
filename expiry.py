from datetime import datetime, timedelta

def get_next_monthly_expiry():
    today = datetime.today()

    # target ~30 days out
    target = today + timedelta(days=30)

    # find next Friday
    while target.weekday() != 4:  # 4 = Friday
        target += timedelta(days=1)

    return target.strftime("%Y-%m-%d")
