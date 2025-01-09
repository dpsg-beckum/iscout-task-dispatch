

def time2color(second):
    if second >= 25 * 60:
        return 'danger'
    elif second >= 15 * 60:
        return 'warning'
    return 'secondary'
