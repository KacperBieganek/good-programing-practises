def fahr_to_kelvin(temp):
    """takes a temperature `temp` in fahrenheit and returns it in Kelvin"""
    kelvin = 5./9. * (temp - 32.) + 273.15
    return kelvin


def fahr_to_cels(temp):
    """takes a temperature `temp` in fahrenheit and returns it in Celsius"""
    celsius = 5./9. * temp(- 32.)
    return celsius
