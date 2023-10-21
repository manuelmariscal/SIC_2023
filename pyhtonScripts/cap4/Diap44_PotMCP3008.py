import spidev
import time

# Configura la conexión SPI con el MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus SPI 0, Dispositivo SPI 0

def read_potentiometer(channel):
    # Lee el valor del potenciómetro en el canal especificado (0-7)
    if channel < 0 or channel > 7:
        raise ValueError("El canal debe estar en el rango 0-7")
    
    adc_data = spi.xfer2([1, (8 + channel) << 4, 0])
    pot_value = ((adc_data[1] & 3) << 8) + adc_data[2]
    return pot_value

try:
    while True:
        channel = 0  # Canal del MCP3008 al que está conectado el potenciómetro
        pot_value = read_potentiometer(channel)
        print(f"Valor del potenciómetro: {pot_value}")
        time.sleep(0.5)  # Puedes ajustar el tiempo de espera según tus necesidades

except KeyboardInterrupt:
    pass

finally:
    spi.close()
