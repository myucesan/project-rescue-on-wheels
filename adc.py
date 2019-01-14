import spi_dev as SPI

class adc(object):
    """Class to represent an Adafruit MCP3008 analog to digital converter.
    """

    def __init__(self, spi):
        """Initialize SPI
        """
        self._spi = spi # Serial communication
        self._spi.set_clock_hz(1000000)
        self._spi.set_mode(0) # Serial clock mode
        self._spi.set_bit_order(SPI.MSBFIRST) # numbering starts at 0, the most significan bit

    def read_adc(self, adc_number):
        """Read the current value of the specified ADC channel (0-7).  The values
        can range from 0 to 1023 (10-bits).
        """
        assert 0 <= adc_number <= 7, 'ADC number must be a value of 0-7!'
        # Build a single channel read command.
        # For example channel zero = 0b11000000
        command = 0b11 << 6                  # Start bit, single channel read
        command |= (adc_number & 0x07) << 3  # Channel number (in 3 bits)
        # Note the bottom 3 bits of command are 0, this is to account for the
        # extra clock to do the conversion, and the low null bit returned at
        # the start of the response.
        resp = self._spi.transfer([command, 0x0, 0x0])
        # Parse out the 10 bits of response data and return it.
        result = (resp[0] & 0x01) << 9
        result |= (resp[1] & 0xFF) << 1
        result |= (resp[2] & 0x80) >> 7
        return result & 0x3FF
