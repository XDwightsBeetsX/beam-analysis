

def getAbsMax(list, roundTo=None):
    """
    `list` - the list/array to find the absolute maximum

    `roundTo` - the number of digits to round the result to.

    returns the absolute maximum of a list.
    """
    x = max(max(list), abs(min(list)))
    if roundTo:
        x = round(x, roundTo)
    return x
