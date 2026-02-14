def FormatAge(age, suffix=""):
    """Takes a time (age) in seconds, and returns a string that describes it with the largest unit that
    is smaller than the time. ex: age = 119, returns 'one minute', age = 95000, returns 'one day.'
    Suffix is used to append some phrase after the unit, such as 'ago.' The suffix is not applied to the
    just now unit (ages less than 60 seconds)

    Args:
        age (): The time in seconds to be converted to a string
        suffix (): String to be placed after the time

    Returns: {count} {word}(s) {suffix}. Ex: age = 400 and suffix = "ago". Returns: "6 minutes ago"

    """

    MINUTE = 60
    HOUR = 3600  # 3,600 (60*60)
    DAY = 86400  # 86,400 (60*60*24)
    MONTH = 2592000  # 2,592,000  (60*60*24*30) (30 days in a month)
    YEAR = 31536000  # 31,536,000 (60*60*24*30*365)

    try:
        age + 1
    except TypeError:
        return f"{age}"

    ticker = 0
    word = ""

    if age > YEAR:  # Years
        while age > YEAR:
            age -= YEAR
            ticker += 1
        word = "year"

    elif age > MONTH:  # Months
        while age > MONTH:
            age -= MONTH
            ticker += 1
        word = "month"

    elif age > DAY:  # Days
        while age > DAY:
            age -= DAY
            ticker += 1
        word = "day"

    elif age > HOUR:  # Hours
        while age > HOUR:
            age -= HOUR
            ticker += 1
        word = "hour"

    elif age > MINUTE:  # Minutes
        while age > MINUTE:
            age -= MINUTE
            ticker += 1
        word = "minute"

    else:  # Times less than 60 seconds (1 minute)
        return "just now"

    # Need to make word plural
    if ticker > 1:
        word += "s"

    return f"{ticker} {word} {suffix}"
