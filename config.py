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

class Display:
    WIDTH = 128
    HEIGHT = 64
    LINE_HEIGHT = 8
    GRAPH_TOP = 16
    GRAPH_HEIGHT = 40

class Network:
    WIFI_CONNECT_TIMEOUT_S = 15
    WIFI_RETRY_COUNT = 3
    MQTT_PORT = 1883
    MQTT_TOPIC_REQ = "kubios/request"
    MQTT_TOPIC_RES = "kubios/response"
    MQTT_KEEPALIVE_S = 60
    NTP_HOST = "http://kmd652g11.asuscomm.com/"
    KUBIOS_TIMEOUT_S = 30

class Storage:
    HISTORY_FILE = "history.json"
    HISTORY_MAX_ENTRIES = 5          # criteria: at least 3

class Ui:
    ERROR_RETURN_TIMEOUT_S = 3       # from the error screen in the criteria
    MENU_ITEMS = ("Measure HR", "HRV analysis", "Kubios", "History")
    FRAME_INTERVAL_MS = 50
    PATIENT_NAME = "Patient"         # level 4: sent with MQTT data
