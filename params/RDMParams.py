"""RDM Defined Parameters"""


"""Command Class Defines"""
DISCOVERY_COMMAND = 0x10
DISCOVERY_COMMAND_RESPONSE = 0x11
GET_COMMAND = 0x20
GET_COMMAND_RESPONSE = 0x21
SET_COMMAND = 0x30
SET_COMMAND_RESPONSE = 0x31


"""Response Type Defines"""
RESPONSE_TYPE_ACK = 0x00
RESPONSE_TYPE_ACK_TIMER = 0x01
RESPONSE_TYPE_NACK_REASON = 0x02  # See Table A-17
RESPONSE_TYPE_ACK_OVERFLOW = 0x03  # Additional Response Data available beyond single response length.


"""Network Management Defines"""
DISC_UNIQUE_BRANCH = 0x0001
DISC_MUTE = 0x0002
DISC_UN_MUTE = 0x0003
PROXIED_DEVICES = 0x0010
PROXIED_DEVICE_COUNT = 0x0011
COMMS_STATUS = 0x0015

"""Status Collection Defines"""
QUEUED_MESSAGE = 0x0020  # See Table A-4
STATUS_MESSAGES = 0x0030  # See Table A-4
STATUS_ID_DESCRIPTION = 0x0031
CLEAR_STATUS_ID = 0x0032
SUB_DEVICE_STATUS_REPORT_THRESHOLD = 0x0033  # See Table A-4

"""RDM Information Defines"""
SUPPORTED_PARAMETERS = 0x0050  # Support required only if supporting Parameters beyond the minimum required set.
PARAMETER_DESCRIPTION = 0x0051  # Support required for Manufacturer-Specific PIDs exposed in SUPPORTED_PARAMETERS msg.

"""Product Information Defines"""
DEVICE_INFO = 0x0060
PRODUCT_DETAIL_ID_LIST = 0x0070
DEVICE_MODEL_DESCRIPTION = 0x0080
MANUFACTURER_LABEL = 0x0081
DEVICE_LABEL = 0x0082
FACTORY_DEFAULTS = 0x0090
LANGUAGE_CAPABILITIES = 0x00A0
LANGUAGE = 0x00B0
SOFTWARE_VERSION_LABEL = 0x00C0
BOOT_SOFTWARE_VERSION_ID = 0x00C1
BOOT_SOFTWARE_VERSION_LABEL = 0x00C2

"""DMX512 Setup Defines"""
DMX_PERSONALITY = 0x00E0
DMX_PERSONALITY_DESCRIPTION = 0x00E1
DMX_START_ADDRESS = 0x00F0  # Support required if device uses a DMX512 Slot.
SLOT_INFO = 0x0120
SLOT_DESCRIPTION = 0x0121
DEFAULT_SLOT_VALUE = 0x0122

"Sensors Defines (0x02xx)"""
SENSOR_DEFINITION = 0x0200
SENSOR_VALUE = 0x0201
RECORD_SENSORS = 0x0202

"""Dimmer Settings Defines (0x03xx)"""
# Future

"""Power/Lamp Settings Defines (0x04xx)"""
DEVICE_HOURS = 0x0400
LAMP_HOURS = 0x0401
LAMP_STRIKES = 0x0402
LAMP_STATE = 0x0403  # See Table A-8
LAMP_ON_MODE = 0x0404 # See Table A-8
DEVICE_POWER_CYCLES = 0x0405

"""Display Settings Defines (0x05xx)"""
DISPLAY_INVERT = 0x0500
DISPLAY_LEVEL = 0x0501

"""Configuration Defines (0x06xx)"""
PAN_INVERT = 0x0600
TILT_INVERT = 0x0601
PAN_TILT_SWAP = 0x0602
REAL_TIME_CLOCK = 0x0603

"""Control Defines (0x10xx)"""
IDENTIFY_DEVICE = 0x1000
RESET_DEVICE = 0x1001
POWER_STATE = 0x1010  # See Table A-11
PERFORM_SELFTEST = 0x1020  # See Table A-10
SELF_TEST_DESCRIPTION = 0x1021
CAPTURE_PRESET = 0x1030
PRESET_PLAYBACK = 0x1031  # See Table A-7

"""ESTA Reserved Future RDM Development"""
# 0x7FE0-0x7FFF

"""Manufacturer-Specific PIDs"""
# 0x8000-0xFFDF

"""ESTA Reserved Future RDM Development"""
# 0xFFE0-0xFFFF

"""Status Type Defines"""
STATUS_NONE = 0x00  # Not allowed for use with GET: QUEUED_MESSAGE
STATUS_GET_LAST_MESSAGE = 0x01
STATUS_ADVISORY = 0x02
STATUS_WARNING = 0x03
STATUS_ERROR = 0x04
STATUS_ADVISORY_CLEARED = 0x12
STATUS_WARNING_CLEARED = 0x13
STATUS_ERROR_CLEARED = 0x14

"""Product Category Defines"""
PRODUCT_CATEGORY_NOT_DECLARED = (0x00, 0x00)

# Fixtures – intended as source of illumination
PRODUCT_CATEGORY_FIXTURE = (0x01, 0x00)  # No Fine Category declared
PRODUCT_CATEGORY_FIXTURE_FIXED = (0x01, 0x01)  # No pan / tilt / focus style functions
PRODUCT_CATEGORY_FIXTURE_MOVING_YOKE = (0x01, 0x02)
PRODUCT_CATEGORY_FIXTURE_MOVING_MIRROR = (0x01, 0x03)
PRODUCT_CATEGORY_FIXTURE_OTHER = (0x01, 0xFF)  # For example, focus but no pan/tilt.

# Fixture Accessories – add-ons to fixtures or projectors
PRODUCT_CATEGORY_FIXTURE_ACCESSORY = (0x02, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_FIXTURE_ACCESSORY_COLOR = (0x02, 0x01)  # Scrollers / Color Changers
PRODUCT_CATEGORY_FIXTURE_ACCESSORY_YOKE = (0x02, 0x02)  # Yoke add-on
PRODUCT_CATEGORY_FIXTURE_ACCESSORY_MIRROR = (0x02, 0x03)  # Moving mirror add-on
PRODUCT_CATEGORY_FIXTURE_ACCESSORY_EFFECT = (0x02, 0x04)  # Effects Discs
PRODUCT_CATEGORY_FIXTURE_ACCESSORY_BEAM = (0x02, 0x05)  # Gobo Rotators / Iris / Shutters / Dousers / Beam modifiers.
PRODUCT_CATEGORY_FIXTURE_ACCESSORY_OTHER = (0x02, 0xFF)

# Projectors - light src capable of producing realistic images from another media Video / Slide / Oil Wheel / Film / LCD
PRODUCT_CATEGORY_PROJECTOR = (0x03, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_PROJECTOR_FIXED = (0x03, 0x01)  # No pan / tilt functions.
PRODUCT_CATEGORY_PROJECTOR_MOVING_YOKE = (0x03, 0x02)
PRODUCT_CATEGORY_PROJECTOR_MOVING_MIRROR = (0x03, 0x03)
PRODUCT_CATEGORY_PROJECTOR_OTHER = (0x03, 0xFF)

# Atmospheric Effect – earth/wind/fire
PRODUCT_CATEGORY_ATMOSPHERIC = (0x04, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_ATMOSPHERIC_EFFECT = (0x04, 0x01)  # Fogger / Hazer / Flame, etc.
PRODUCT_CATEGORY_ATMOSPHERIC_PYRO = (0x04, 0x02)  # See Note 2.
PRODUCT_CATEGORY_ATMOSPHERIC_OTHER = (0x04, 0xFF)

# Intensity Control (specifically Dimming equipment)
PRODUCT_CATEGORY_DIMMER = (0x05, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_DIMMER_AC_INCANDESCENT = (0x05, 0x01)  # AC > 50VAC
PRODUCT_CATEGORY_DIMMER_AC_FLUORESCENT = (0x05, 0x02)
PRODUCT_CATEGORY_DIMMER_AC_COLDCATHODE = (0x05 0x03)  # High Voltage outputs such as Neon or other cold cathode.
PRODUCT_CATEGORY_DIMMER_AC_NONDIM = (0x05, 0x04)  # Non-Dim module in dimmer rack.
PRODUCT_CATEGORY_DIMMER_AC_ELV = (0x05, 0x05)  # AC <= 50V such as 12/24V AC Low voltage lamps.
PRODUCT_CATEGORY_DIMMER_AC_OTHER = (0x05, 0x06)
PRODUCT_CATEGORY_DIMMER_DC_LEVEL = (0x05, 0x07)  # Variable DC level output.
PRODUCT_CATEGORY_DIMMER_DC_PWM = (0x05, 0x08)  # Chopped (PWM) output.
PRODUCT_CATEGORY_DIMMER_CS_LED = (0x05, 0x09)  # Specialized LED dimmer.
PRODUCT_CATEGORY_DIMMER_OTHER = (0x05, 0xFF)

# Power Control (other than Dimming equipment)
PRODUCT_CATEGORY_POWER = (0x06, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_POWER_CONTROL = (0x06, 0x01)  # Contactor racks, other forms of Power Controllers.
PRODUCT_CATEGORY_POWER_SOURCE = (0x06, 0x02)  # Generators
PRODUCT_CATEGORY_POWER_OTHER = (0x06, 0xFF)

# Scenic Drive – including motorized effects unrelated to light source.
PRODUCT_CATEGORY_SCENIC = (0x07, 0x00)  # No Fine Category declared
PRODUCT_CATEGORY_SCENIC_DRIVE = (0x07, 0x01)  # Rotators / Kabuki drops, etc. See Note 2.
PRODUCT_CATEGORY_SCENIC_OTHER = (0x07, 0xFF)

# DMX Infrastructure, conversion and interfaces
PRODUCT_CATEGORY_DATA = (0x08, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_DATA_DISTRIBUTION = (0x08, 0x01)  # Splitters / repeaters / data patch / Ethernet products used
                                                   # to distribute DMX universes.
PRODUCT_CATEGORY_DATA_CONVERSION = (0x08, 0x02)  # Protocol Conversion analog decoders.
PRODUCT_CATEGORY_DATA_OTHER = (0x08, 0xFF)

# Audio-Visual Equipment
PRODUCT_CATEGORY_AV = (0x09, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_AV_AUDIO = (0x09, 0x01)  # Audio controller or device.
PRODUCT_CATEGORY_AV_VIDEO = (0x09, 0x02)  # Video controller or display device.
PRODUCT_CATEGORY_AV_OTHER = (0x09, 0xFF)

# Parameter Monitoring Equipment. See Note 3.
PRODUCT_CATEGORY_MONITOR = (0x0A, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_MONITOR_ACLINEPOWER = (0x0A, 0x01)  # Product that monitors AC line voltage, current or power.
PRODUCT_CATEGORY_MONITOR_DCPOWER = (0x0A, 0x02)  # Product that monitors DC line voltage, current or power.
PRODUCT_CATEGORY_MONITOR_ENVIRONMENTAL = (0x0A, 0x03)  # Temperature or other environmental parameter.
PRODUCT_CATEGORY_MONITOR_OTHER = (0x0A, 0xFF)

# Controllers, Backup devices
PRODUCT_CATEGORY_CONTROL = (0x70, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_CONTROL_CONTROLLER = (0x70, 0x01)
PRODUCT_CATEGORY_CONTROL_BACKUPDEVICE = (0x70, 0x02)
PRODUCT_CATEGORY_CONTROL_OTHER = (0x70, 0xFF)

# Test Equipment
PRODUCT_CATEGORY_TEST = (0x71, 0x00)  # No Fine Category declared.
PRODUCT_CATEGORY_TEST_EQUIPMENT = (0x71, 0x01)
PRODUCT_CATEGORY_TEST_EQUIPMENT_OTHER = (0x71, 0xFF)

# Miscellaneous
PRODUCT_CATEGORY_OTHER = (0x7F, 0xFF)  # For devices that aren’t described within this table.

#Manufacturer Specific Categories
# (0x80-0xDF, 0x00-0xFF)

# Note 1: A fixture in this context is defined as a light source intended as a means of illumination. A
# projector is a light source capable of producing realistic images from another media. A light
# source intended for use with Fiber Optics should be classified as a fixture.
# Note 2: The DMX512 standard specifically states that, as there is no mandatory error checking,
# DMX512 is not an appropriate control protocol for hazardous applications. RDM may, however,
# be appropriate for configuration and monitoring purposes.
# Note 3: This category is for equipment that has no DMX512 control capability, but uses RDM to
# provide a data logging or monitoring function.

"""Product Detail Defines"""
PRODUCT_DETAIL_NOT DECLARED = 0x0000

# Generally applied to fixtures
PRODUCT_DETAIL_ARC = 0x0001  # Intended for constant light output.
PRODUCT_DETAIL_METAL_HALIDE = 0x0002
PRODUCT_DETAIL_INCANDESCENT = 0x0003
PRODUCT_DETAIL_LED = 0x0004
PRODUCT_DETAIL_FLUROESCENT = 0x0005
PRODUCT_DETAIL_COLDCATHODE = 0x0006  # includes Neon/Argon
PRODUCT_DETAIL_ELECTROLUMINESCENT = 0x0007
PRODUCT_DETAIL_LASER = 0x0008
PRODUCT_DETAIL_FLASHTUBE = 0x0009  # Strobes or other flashtubes

# Generally applied to fixture accessories
PRODUCT_DETAIL_COLORSCROLLER = 0x0100
PRODUCT_DETAIL_COLORWHEEL = 0x0101
PRODUCT_DETAIL_COLORCHANGE = 0x0102  # Semaphore or other type
PRODUCT_DETAIL_IRIS_DOUSER = 0x0103
PRODUCT_DETAIL_DIMMING_SHUTTER = 0x0104
PRODUCT_DETAIL_PROFILE_SHUTTER = 0x0105  # hard-edge beam masking
PRODUCT_DETAIL_BARNDOOR_SHUTTER = 0x0106  # soft-edge beam masking
PRODUCT_DETAIL_EFFECTS_DISC = 0x0107
PRODUCT_DETAIL_GOBO_ROTATOR = 0x0108

# Generally applied to Projectors
PRODUCT_DETAIL_VIDEO = 0x0200
PRODUCT_DETAIL_SLIDE = 0x0201
PRODUCT_DETAIL_FILM = 0x0202
PRODUCT_DETAIL_OILWHEEL = 0x0203
PRODUCT_DETAIL_LCDGATE = 0x0204

# Generally applied to Atmospheric Effects
PRODUCT_DETAIL_FOGGER_GLYCOL = 0x0300  # Glycol/Glycerin hazer
PRODUCT_DETAIL_FOGGER_MINERALOIL = 0x0301  # White Mineral oil hazer
PRODUCT_DETAIL_FOGGER_WATER = 0x0302  # Water hazer
PRODUCT_DETAIL_C02 = 0x0303  # Dry Ice/Carbon Dioxide based
PRODUCT_DETAIL_LN2 = 0x0304  # Nitrogen based
PRODUCT_DETAIL_BUBBLE = 0x0305  # including foam
PRODUCT_DETAIL_FLAME_PROPANE = 0x0306
PRODUCT_DETAIL_FLAME_OTHER = 0x0307
PRODUCT_DETAIL_OLEFACTORY_STIMULATOR = 0x0308  # Scents
PRODUCT_DETAIL_SNOW = 0x0309
PRODUCT_DETAIL_WATER_JET = 0x030A  # Fountain controls etc
PRODUCT_DETAIL_WIND = 0x030B  # Air Mover
PRODUCT_DETAIL_CONFETTI = 0x030C
PRODUCT_DETAIL_HAZARD = 0x030D  # Any form of pyrotechnic control or device.

# Generally applied to Dimmers/Power controllers See Note 1
PRODUCT_DETAIL_PHASE_CONTROL = 0x0400
PRODUCT_DETAIL_REVERSE_PHASE_CONTROL = 0x0401  # includes FET/IGBT
PRODUCT_DETAIL_SINE = 0x0402
PRODUCT_DETAIL_PWM = 0x0403
PRODUCT_DETAIL_DC = 0x0404  # Variable voltage
PRODUCT_DETAIL_HFBALLAST = 0x0405  # for Fluroescent
PRODUCT_DETAIL_HFHV_NEONBALLAST = 0x0406  # for Neon/Argon and other coldcathode.
PRODUCT_DETAIL_HFHV_EL = 0x0407  # for Electroluminscent
PRODUCT_DETAIL_MHR_BALLAST = 0x0408  # for Metal Halide
PRODUCT_DETAIL_BITANGLE_MODULATION = 0x0409
PRODUCT_DETAIL_FREQUENCY_MODULATION = 0x040A
PRODUCT_DETAIL_HIGHFREQUENCY_12V = 0x040B  # as commonly used with MR16 lamps
PRODUCT_DETAIL_RELAY_MECHANICAL = 0x040C  # See Note 1
PRODUCT_DETAIL_RELAY_ELECTRONIC = 0x040D  # See Note 1, Note 2
PRODUCT_DETAIL_SWITCH_ELECTRONIC = 0x040E  # See Note 1, Note 2
PRODUCT_DETAIL_CONTACTOR = 0x040F  # See Note 1

# Generally applied to Scenic drive
PRODUCT_DETAIL_MIRRORBALL_ROTATOR = 0x0500
PRODUCT_DETAIL_OTHER_ROTATOR = 0x0501  # includes turntables
PRODUCT_DETAIL_KABUKI_DROP = 0x0502
PRODUCT_DETAIL_CURTAIN = 0x0503  # flown or traveller
PRODUCT_DETAIL_LINESET = 0x0504
PRODUCT_DETAIL_MOTOR_CONTROL = 0x0505
PRODUCT_DETAIL_DAMPER_CONTROL = 0x0506  # HVAC Damper

# Generally applied to Data Distribution
PRODUCT_DETAIL_SPLITTER = 0x0600  # Includes buffers/repeaters
PRODUCT_DETAIL_ETHERNET_NODE = 0x0601  # DMX512 to/from Ethernet
PRODUCT_DETAIL_MERGE = 0x0602  # DMX512 combiner
PRODUCT_DETAIL_DATAPATCH = 0x0603  # Electronic Datalink Patch
PRODUCT_DETAIL_WIRELESS_LINK = 0x0604  # radio/infrared

# Generally applied to Data Conversion and Interfaces
PRODUCT_DETAIL_PROTOCOL_CONVERTOR = 0x0701  # D54/AMX192/Non DMX serial links, etc to/from DMX512
PRODUCT_DETAIL_ANALOG_DEMULTIPLEX = 0x0702 # DMX to DC voltage
PRODUCT_DETAIL_ANALOG_MULTIPLEX = 0x0703  # DC Voltage to DMX
PRODUCT_DETAIL_SWITCH_PANEL = 0x0704  # Pushbuttons to DMX or polled using RDM

# Generally applied to Audio or Video (AV) devices
PRODUCT_DETAIL_ROUTER = 0x0800  # Switching device
PRODUCT_DETAIL_FADER = 0x0801  # Single channel
PRODUCT_DETAIL_MIXER = 0x0802  # Multi-channel
# Generally applied to Controllers, Backup devices and Test Equipment
PRODUCT_DETAIL_CHANGEOVER_MANUAL = 0x0900 # requires manual intervention to assume control of DMX line
PRODUCT_DETAIL_CHANGEOVER_AUTO = 0x0901  # may automatically assume control of DMX line
PRODUCT_DETAIL_TEST = 0x0902  # test equipment

# Could be applied to any category
PRODUCT_DETAIL_GFI_RCD = 0x0A00  # device includes GFI/RCD trip
PRODUCT_DETAIL_BATTERY = 0x0A01  # device is battery operated
PRODUCT_DETAIL_CONTROLLABLE_BREAKER = 0x0A02

# Manufacturer Specific Types
# 0x8000-0xDFFF
PRODUCT_DETAIL_OTHER = 0x7FFF  # for use where the Manufacturer believes that none of the defined details apply.

# Note 1: Products intended for switching 50V AC / 120V DC or greater should be declared with a
# Product Category of PRODUCT_CATEGORY_POWER_CONTROL.
# Products only suitable for extra low voltage switching (typically up to 50VAC / 30VDC) at currents
# less than 1 ampere should be declared with a Product Category of
# PRODUCT_CATEGORY_DATA_CONVERSION.
# Please refer to GET: DEVICE_INFO and Table A-5 for an explanation of Product Category
# declaration.
# Note 2: Products with TTL, MOSFET or Open Collector Transistor Outputs or similar non-isolated
# electronic outputs should be declared as PRODUCT_DETAIL_SWITCH_ELECTRONIC. Use of
# PRODUCT_DETAIL_RELAY_ELECTRONIC shall be restricted to devices whereby the switched
# circuits are electrically isolated from the control signals.

"""Preset Playback Defines"""
PRESET_PLAYBACK_OFF = 0x0000  # Returns to Normal DMX512 Input
PRESET_PLAYBACK_ALL = 0xFFFF  # Plays Scenes in Sequence if supported.
#PRESET_PLAYBACK_SCENE 0x0001-0xFFFE  # Plays individual Scene

"""Lamp State Defines"""
LAMP_OFF = 0x00  # No demonstrable light output
LAMP_ON = 0x01
LAMP_STRIKE = 0x02  # Arc-Lamp ignite
LAMP_STANDBY = 0x03  # Arc-Lamp Reduced Power Mode
LAMP_NOT_PRESENT = 0x04  # Lamp not installed
LAMP_ERROR = 0x7F
# Manufacturer-Specific States  # 0x80 – 0xDF

"""Lamp On Mode Defines"""
LAMP_ON_MODE_OFF = 0x00  # Lamp Stays off until directly instructed to Strike.
LAMP_ON_MODE_DMX = 0x01  # Lamp Strikes upon receiving a DMX512 signal.
LAMP_ON_MODE_ON = 0x02  # Lamp Strikes automatically at Power-up.
LAMP_ON_MODE_AFTER_CAL = 0x03  # Lamp Strikes after Calibration or Homing procedure.
# Manufacturer-Specific Modes  # 0x80 – 0xDF

"""Self Test Defines"""
SELF_TEST_OFF = 0x00  # Turns Self Tests Off
# Manufacturer Tests = 0x01 – 0xFE  # Various Manufacturer Self Tests
SELF_TEST_ALL = 0xFF  # Self Test All, if applicable

"""Sensor Type Defines"""
SENS_TEMPERATURE = 0x00
SENS_VOLTAGE = 0x01
SENS_CURRENT = 0x02
SENS_FREQUENCY = 0x03
SENS_RESISTANCE = 0x04  # Eg: Cable resistance
SENS_POWER = 0x05
SENS_MASS = 0x06  # Eg: Truss load Cell
SENS_LENGTH = 0x07
SENS_AREA = 0x08
SENS_VOLUME = 0x09  # Eg: Smoke Fluid
SENS_DENSITY = 0x0A
SENS_VELOCITY = 0x0B
SENS_ACCELERATION = 0x0C
SENS_FORCE = 0x0D
SENS_ENERGY = 0x0E
SENS_PRESSURE = 0x0F
SENS_TIME = 0x10
SENS_ANGLE = 0x11
SENS_POSITION_X = 0x12  # E.g.: Lamp position on Truss
SENS_POSITION_Y = 0x13
SENS_POSITION_Z = 0x14
SENS_ANGULAR_VELOCITY = 0x15  # E.g.: Wind speed
SENS_LUMINOUS_INTENSITY = 0x16
SENS_LUMINOUS_FLUX = 0x17
SENS_ILLUMINANCE = 0x18
SENS_CHROMINANCE_RED = 0x19
SENS_CHROMINANCE_GREEN = 0x1A
SENS_CHROMINANCE_BLUE = 0x1B
SENS_CONTACTS = 0x1C  # E.g.: Switch inputs.
SENS_MEMORY = 0x1D  # E.g.: ROM Size
SENS_ITEMS = 0x1E  # E.g.: Scroller gel frames.
SENS_HUMIDITY = 0x1F
SENS_COUNTER_16BIT = 0x20
SENS_OTHER = 0x7F
# Manufacturer-Specific Sensors  # 0x80 – 0xFF

"""Sensor Unit Defines Value"""
UNITS_NONE = 0x00  # CONTACTS
UNITS_CENTIGRADE = 0x01  # TEMPERATURE
UNITS_VOLTS_DC = 0x02  # VOLTAGE
UNITS_VOLTS_AC_PEAK = 0x03  # VOLTAGE
UNITS_VOLTS_AC_RMS = 0x04  # VOLTAGE
UNITS_AMPERE_DC = 0x05  # CURRENT
UNITS_AMPERE_AC_PEAK  =0x06  # CURRENT
UNITS_AMPERE_AC_RMS = 0x07  # CURRENT
UNITS_HERTZ = 0x08  # FREQUENCY / ANG_VEL
UNITS_OHM = 0x09  # RESISTANCE
UNITS_WATT = 0x0A  # POWER
UNITS_KILOGRAM = 0x0B  # MASS
UNITS_METERS = 0x0C  # LENGTH / POSITION
UNITS_METERS_SQUARED = 0x0D  # AREA
UNITS_METERS_CUBED = 0x0E  # VOLUME
UNITS_KILOGRAMMES_PER_METER_CUBED = 0x0F  # DENSITY
UNITS_METERS_PER_SECOND = 0x10  # VELOCITY
UNITS_METERS_PER_SECOND_SQUARED = 0x11  # ACCELERATION
UNITS_NEWTON = 0x12  # FORCE
UNITS_JOULE = 0x13  # ENERGY
UNITS_PASCAL = 0x14  # PRESSURE
UNITS_SECOND = 0x15  # TIME
UNITS_DEGREE = 0x16  # ANGLE
UNITS_STERADIAN = 0x17  # ANGLE
UNITS_CANDELA = 0x18  # LUMINOUS_INTENSITY
UNITS_LUMEN = 0x19  # LUMINOUS_FLUX
UNITS_LUX = 0x1A  # ILLUMINANCE
UNITS_IRE = 0x1B  # CHROMINANCE
UNITS_BYTE = 0x1C  # MEMORY
# Manufacturer-Specific Units #  0x80 – 0xFF

"""Sensor Unit Prefix Defines"""
PREFIX_NONE = 0x00  # Multiply by 1
PREFIX_DECI = 0x01  # Multiply by 10^-1
PREFIX_CENTI = 0x02  # Multiply by 10^-2
PREFIX_MILLI = 0x03  # Multiply by 10^-3
PREFIX_MICRO = 0x04  # Multiply by 10^-6
PREFIX_NANO = 0x05  # Multiply by 10^-9
PREFIX_PICO = 0x06  # Multiply by 10^-12
PREFIX_FEMPTO = 0x07  # Multiply by 10^-15
PREFIX_ATTO = 0x08  # Multiply by 10^-18
PREFIX_ZEPTO = 0x09  # Multiply by 10^-21
PREFIX_YOCTO = 0x0A  # Multiply by 10^-24
PREFIX_DECA = 0x11  # Multiply by 10^+1
PREFIX_HECTO = 0x12  # Multiply by 10^+2
PREFIX_KILO = 0x13  # Multiply by 10^+3
PREFIX_MEGA = 0x14  # Multiply by 10^+6
PREFIX_GIGA = 0x15  # Multiply by 10^+9
PREFIX_TERRA = 0x16  # Multiply by 10^+12
PREFIX_PETA = 0x17  # Multiply by 10^+15
PREFIX_EXA = 0x18  # Multiply by 10^+18
PREFIX_ZETTA = 0x19  # Multiply by 10^+21
PREFIX_YOTTA = 0x1A  # Multiply by 10^+24

"""Data Type Defines"""
DS_NOT_DEFINED = 0x00  # Data type is not defined
DS_BIT_FIELD = 0x01  # Data is bit packed
DS_ASCII = 0x02  # Data is a string
DS_UNSIGNED_BYTE = 0x03  # Data is an array of unsigned bytes
DS_SIGNED_BYTE = 0x04  # Data is an array of signed bytes
DS_UNSIGNED_WORD = 0x05  # Data is an array of unsigned 16-bit words
DS_SIGNED_WORD = 0x06  # Data is an array of signed 16-bit words
DS_UNSIGNED_DWORD = 0x07  # Data is an array of unsigned 32-bit words
DS_SIGNED_DWORD = 0x08  # Data is an array of signed 32-bit words
# Manufacturer-Specific Data Types  # 0x80 – 0xDF

"""Command Class Defines"""
CC_GET = 0x01  # PID supports GET only
CC_SET = 0x02  # PID supports SET only
CC_GET_SET = 0x03  # PID supports GET & SET

"""Response NACK Reason Codes"""
NR_UNKNOWN_PID = 0x0000  # The responder cannot comply with request because the message is not implemented in responder.
NR_FORMAT_ERROR = 0x0001  # The responder cannot interpret request as controller data was not formatted correctly.
NR_HARDWARE_FAULT = 0x0002  # The responder cannot comply due to an internal hardware fault.
NR_PROXY_REJECT = 0x0003  # Proxy is not the RDM line master and cannot comply with message.
NR_WRITE_PROTECT = 0x0004  # SET Command normally allowed but being blocked currently.
NR_UNSUPPORTED_COMMAND_CLASS = 0x0005  # Not valid for Command Class attempted. May be used where GET allowed but SET is
                                       # not supported.
NR_DATA_OUT_OF_RANGE = 0x0006  # Value for given Parameter out of allowable range or not supported.
NR_BUFFER_FULL = 0x0007  # Buffer or Queue space currently has no free space to store data.
NR_PACKET_SIZE_UNSUPPORTED = 0x0008  # Incoming message exceeds buffer capacity.
NR_SUB_DEVICE_OUT_OF_RANGE = 0x0009  # Sub-Device is out of range or unknown.
NR_PROXY_BUFFER_FULL = 0x000A  # The proxy buffer is full and can not store any more Queued Message or Status Message
                               # responses.

"""Status Message ID Definitions"""
STS_CAL_FAIL = 0x0001  # Slot Label Code “%L failed calibration”
STS_SENS_NOT_FOUND = 0x0002  # Slot Label Code “%L sensor not found”
STS_SENS_ALWAYS_ON = 0x0003  # Slot Label Code “%L sensor always on”
STS_LAMP_DOUSED = 0x0011  # N/A “Lamp doused”
STS_LAMP_STRIKE = 0x0012  # N/A “Lamp failed to strike”
STS_OVERTEMP = 0x0021  # Sensor Number Temperature “Sensor %d over temp at %d degrees C”
STS_UNDERTEMP = 0x0022  # Sensor Temperature “Sensor %d under temp at %d degrees C”
STS_SENS_OUT_RANGE = 0x0023  # Sensor Number “Sensor %d out of range”
STS_OVERVOLTAGE_PHASE = 0x0031  # Phase Number Voltage “Phase %d over voltage at %d V.”
STS_UNDERVOLTAGE_PHASE = 0x0032  # Phase Number Voltage “Phase %d under voltage at %d V.”
STS_OVERCURRENT = 0x0033  # Phase Number Current “Phase %d over current at %d A.”
STS_UNDERCURRENT = 0x0034  # Phase Number Current “Phase %d under current at %d A.”
STS_PHASE = 0x0035  # Phase Number Phase Angle “Phase %d is at %d degrees”
STS_PHASE_ERROR = 0x0036  # Phase Number “Phase %d Error.”
STS_AMPS = 0x0037  # Current “%d Amps”
STS_VOLTS = 0x0038  # Volts “%d Volts”
STS_DIMSLOT_OCCUPIED = 0x0041  # N/A “No Dimmer”
STS_BREAKER_TRIP = 0x0042  # N/A “Tripped Breaker”
STS_WATTS = 0x0043  # Wattage “%d Watts”
STS_DIM_FAILURE = 0x0044  # N/A “Dimmer Failure”
STS_DIM_PANIC = 0x0045  # N/A “Panic Mode”
STS_READY = 0x0050  # Slot Label Code “%L ready”
STS_NOT_READY = 0x0051  # Slot Label Code “%L not ready”
STS_LOW_FLUID = 0x0052  # Slot Label Code “%L low fluid”

"""Slot ID Type"""
ST_PRIMARY = 0x00  # Slot directly controls parameter (represents Coarse for 16-bit parameters)
ST_SEC_FINE = 0x01  # Fine, for 16-bit parameters
ST_SEC_TIMING = 0x02  # Slot sets timing value for associated parameter
ST_SEC_SPEED = 0x03  # Slot sets speed/velocity for associated parameter
ST_SEC_CONTROL = 0x04  # Slot provides control/mode info for parameter
ST_SEC_INDEX = 0x05  # Slot sets index position for associated parameter
ST_SEC_ROTATION = 0x06  # Slot sets rotation speed for associated parameter
ST_SEC_INDEX_ROTATE = 0x07  # Combined index/rotation control
ST_SEC_UNDEFINED = 0xFF  # Undefined secondary type

"""Slot Category/ID"""
# Intensity Functions (0x00xx)
SD_INTENSITY = 0x0001  # Intensity
SD_INTENSITY_MASTER = 0x0002  # Intensity Master

# Movement Functions (0x01xx)
SD_PAN = 0x0101  # Pan
SD_TILT = 0x0102  # Tilt

# Color Functions (0x02xx)
SD_COLOR_WHEEL = 0x0201  # Color Wheel
SD_COLOR_SUB_CYAN = 0x0202  # Subtractive Color Mixer – Cyan/Blue
SD_COLOR_SUB_YELLOW = 0x0203  # Subtractive Color Mixer – Yellow/Amber
SD_COLOR_SUB_MAGENTA = 0x0204  # Subtractive Color Mixer - Magenta
SD_COLOR_ADD_RED = 0x0205  # Additive Color Mixer - Red
SD_COLOR_ADD_GREEN = 0x0206  # Additive Color Mixer - Green
SD_COLOR_ADD_BLUE = 0x0207  # Additive Color Mixer - Blue
SD_COLOR_CORRECTION = 0x0208  # Color Temperature Correction
SD_COLOR_SCROLL = 0x0209  # Color Scroll
SD_COLOR_SEMAPHORE = 0x0210  # Color Semaphore

# Image Functions (0x03xx)
SD_STATIC_GOBO_WHEEL = 0x0301  # Static gobo wheel
SD_ROTO_GOBO_WHEEL = 0x0302  # Rotating gobo wheel
SD_PRISM_WHEEL = 0x0303  # Prism wheel
SD_EFFECTS_WHEEL = 0x0304  # Effects wheel

# Beam Functions (0x04xx)
SD_BEAM_SIZE_IRIS = 0x0401  # Beam size iris
SD_EDGE = 0x0402  # Edge/Lens focus
SD_FROST = 0x0403  # Frost/Diffusion
SD_STROBE = 0x0404  # Strobe/Shutter
SD_ZOOM = 0x0405  # Zoom lens
SD_FRAMING_SHUTTER = 0x0406  # Framing shutter
SD_SHUTTER_ROTATE = 0x0407  # Framing shutter rotation
SD_DOUSER = 0x0408  # Douser
SD_BARN_DOOR = 0x0409  # Barn Door

# Control Functions (0x05xx)
SD_LAMP_CONTROL = 0x0501  # Lamp control functions
SD_FIXTURE_CONTROL = 0x0502  # Fixture control channel
SD_FIXTURE_SPEED = 0x0503  # Overall speed setting applied to multiple or all parameters
SD_MACRO = 0x0504  # Macro control

SD_UNDEFINED = 0xFFFF  # No definition