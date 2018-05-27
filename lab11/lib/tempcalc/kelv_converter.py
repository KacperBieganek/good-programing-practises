def kelv_to_cels(temp):
    """takes a temperature `temp` in Kelvin and returns it in Celsius"""
    celsius = temp - 273.15
    return celsius


def kelv_to_fahr(temp):
    """takes a temperature `temp` in Kelvin and returns it in Fahrenheit"""
    fahrenheit = (temp - 273.15) * (9/5) + 32
    return fahrenheit
