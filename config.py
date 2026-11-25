class Pins:
    PPG_SENSOR_ADC = 26
    OLED_SDA = 14
    OLED_SCL = 15
    HEARTBEAT_LED = 20
    ENCODER_A = 10
    ENCODER_B = 11
    ENCODER_BUTTON = 12
    BUTTON_SW_0 = 9
    BUTTON_SW_1 = 8
    BUTTON_SW_2 = 7

class Encoder:
    FIFO_SIZE = 30
    FIFO_TYPECODE = 'i'
    TURN_LEFT = -1
    TURN_RIGHT = 1
    BUTTON_DEBOUNCE_MS = 200

class Sampling:
    RATE_HZ = 250
    FIFO_DEPTH = 64          # how many samples you read per batch
    BUTTON_DEBOUNCE_MS = 200
    FIFO_SIZE = 256

class Analysis:
    MIN_PLAUSIBLE_BPM = 30
    MAX_PLAUSIBLE_BPM = 240
    BPM_UPDATE_INTERVAL_S = 3        # criteria: at least once per 5 s
    PEAK_THRESHOLD_RATIO = 0.7       # tune against real data
    MIN_PEAK_DISTANCE_MS = 250
    HRV_WINDOW_S = 30                # criteria: at least 30 s
    SMOOTHING_WINDOW = 5
    THRESHOLD_WINDOW_S = 2          
    THRESHOLD_UPDATE_SAMPLES = 25   
    MIN_SIGNAL_AMPLITUDE = 700      
    BEATS_TO_AVERAGE = 5
    MAX_PPI_CHANGE_RATIO = 0.3

class Display:
    WIDTH = 128
    HEIGHT = 64
    COLOR_ON = 1
    LINE_HEIGHT = 8
    GRAPH_TOP = 16
    GRAPH_HEIGHT = 40
    I2C_ID = 1
    I2C_FREQ = 400000
    I2C_ADDRESS = 0x3C

class Network:
    WIFI_CONNECT_TIMEOUT_S = 15
    WIFI_RETRY_COUNT = 3
    MQTT_PORT = 1883
    MQTT_BROKER_HOST = "http://kmd652g11.asuscomm.com"
    MQTT_TOPIC_REQ = "kubios/request"
    MQTT_TOPIC_RES = "kubios/response"
    TOPIC_DEVICES_ADD = "database/devices/add"
    TOPIC_PATIENTS_ADD = "database/patients/add"
    TOPIC_PATIENTS_LIST = "database/patients/list"
    TOPIC_RECORDS_ADD = "database/records/add"
    TOPIC_DB_RESPONSE = "database/response"
    KUBIOS_DATA_TYPE = "RRI"
    KUBIOS_ANALYSIS_TYPE = "readiness"
    NTP_HOST = "pool.ntp.org"
    MQTT_KEEPALIVE_S = 60
    KUBIOS_TIMEOUT_S = 30

class Storage:
    HISTORY_FILE = "history.json"
    HISTORY_MAX_ENTRIES = 5          # criteria: at least 3

class Input:
    LEFT = "left"
    RIGHT = "right"
    PRESS = "press"

class ScreenId:
    STARTUP = "startup"
    MENU = "menu"
    HEART_RATE = "heart_rate"
    HRV = "hrv"
    KUBIOS = "kubios"
    HISTORY = "history"

class Ui:
    START_SCREEN = ScreenId.STARTUP
    ERROR_RETURN_TIMEOUT_S = 3       # from the error screen in the criteria
    MENU_ITEMS = ("Measure HR", "HRV analysis", "Kubios", "History")
    MENU_TARGETS = (ScreenId.HEART_RATE, ScreenId.HRV, ScreenId.KUBIOS, ScreenId.HISTORY)
    MENU_X = 0
    MENU_CURSOR = ">"
    FRAME_INTERVAL_MS = 50
    PATIENT_NAME = "Patient"         # level 4: sent with MQTT data

class StartupAnim:
    HEART_SCALE = 1.4
    HEART_GAP = 0.6              # bottom opening width
    HEART_STEPS = 48
    HEART_Y_OFFSET = 2.5
    PULSES_PER_SIDE = 2
    MARGIN = 6                   # clear space between pulses and the heart
    INTERPOLATION_STEP = 4       # keeps the drawing speed even
    PULSE_WIDTH = 6
    PULSE_SLOT_MARGIN = 2
    PULSE_MIN_HEIGHT = 5
    PULSE_MAX_HEIGHT = 12
    SEGMENTS_PER_FRAME = 4       # segments revealed per App frame
    HOLD_MS = 1000               # pause on the finished drawing
