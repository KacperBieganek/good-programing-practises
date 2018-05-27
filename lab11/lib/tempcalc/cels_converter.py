def cels_to_kelvin(temp):
    """takes a temperature `temp` in Celsius and returns it in Kelvin"""
    kelvin = temp + 273.15
    return kelvin


def cels_to_fahr(temp):
    """takes a temperature `temp` in Celsius and returns it in fahrenheit"""
    fahrenheit = temp * (9/5) + 32
    return fahrenheit
