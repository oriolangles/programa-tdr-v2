def PantallaDades():
    OLED.clear()
    OLED.write_string_new_line("TDR")
    OLED.new_line()
    OLED.write_string_new_line("Temperatura: " + ("" + str(temperatura)) + " C")
    OLED.write_string_new_line("Humitat: " + ("" + str(Humitat)) + "%")
    OLED.write_string_new_line("Pressio: " + ("" + str(Pressió)) + " hPa")
    OLED.write_string_new_line("Bateria: " + ("" + str(PercBat)) + "%")
    OLED.write_string_new_line("Voltatge:  " + ("" + str(batvolt)) + " V")
def Wifi():
    global botoapretat, SSID, WIFI_PASSWORD
    botoapretat = 0
    while botoapretat == 0:
        if pins.digital_read_pin(DigitalPin.P2) == 0:
            botoapretat += 1
            SSID = "MAZINGERZ"
            WIFI_PASSWORD = "letsthesunshine"
        if pins.digital_read_pin(DigitalPin.P16) == 0:
            botoapretat += 1
            SSID = "orioloneplusnord"
            WIFI_PASSWORD = "bondia1234"
    OLED.clear()
    OLED.write_string_new_line("...")
    ESP8266_IoT.init_wifi(SerialPin.P8, SerialPin.P12, BaudRate.BAUD_RATE115200)
    ESP8266_IoT.connect_wifi(SSID, WIFI_PASSWORD)
    OLED.clear()
    OLED.write_string_new_line("Connectat")
def LlegirDades():
    global temperatura, Humitat, Pressió
    temperatura = BME280.temperature(BME280_T.T_C)
    Humitat = BME280.humidity()
    Pressió = BME280.pressure(BME280_P.H_PA)
def EnviarDades():
    ESP8266_IoT.connect_thing_speak()
    ESP8266_IoT.set_data("8OUGW8MHUV093H5B",
        temperatura,
        Humitat,
        Pressió,
        PercBat,
        batvolt,
        sos)
    ESP8266_IoT.upload_data()
def Sos():
    global sos
    OLED.clear()
    OLED.write_string_new_line("SOS")
    OLED.new_line()
    OLED.write_string_new_line("Enviant...")
    basic.pause(15000)
    sos = 1
    EnviarDades()
    sos = 0
    basic.pause(15000)
    EnviarDades()
    basic.pause(2000)
    pins.digital_write_pin(DigitalPin.P2, 1)
def VoltatgeBateria():
    global batvolt
    batvolt = 0
    for index in range(10):
        batvolt += pins.analog_read_pin(AnalogPin.P1) * 3.148 / 1023 * 11
    batvolt = batvolt / 10 + 0.02
    PercentatgeBat()
def PercentatgeBat():
    global PercBat
    if batvolt >= 4.2:
        PercBat = 100
    if batvolt < 4.2 and batvolt >= 4.02:
        PercBat = 80
    if batvolt < 4.02 and batvolt >= 3.87:
        PercBat = 60
    if batvolt < 3.87 and batvolt >= 3.8:
        PercBat = 40
    if batvolt < 3.8 and batvolt >= 3.73:
        PercBat = 20
    if batvolt < 3.73:
        PercBat = 10
WIFI_PASSWORD = ""
SSID = ""
botoapretat = 0
batvolt = 0
PercBat = 0
Pressió = 0
Humitat = 0
temperatura = 0
sos = 0
pins.digital_write_pin(DigitalPin.P2, 1)
pins.digital_write_pin(DigitalPin.P16, 1)
OLED.init(128, 64)
OLED.write_string_new_line("TDR")
OLED.new_line()
OLED.write_string_new_line("A - WIFI CASA")
OLED.write_string_new_line("B - WIFI MOBIL")
OLED.new_line()
Wifi()
basic.pause(1000)
LlegirDades()
VoltatgeBateria()
sos = 0

def on_forever():
    LlegirDades()
    VoltatgeBateria()
    if pins.digital_read_pin(DigitalPin.P2) == 0:
        Sos()
    else:
        PantallaDades()
        basic.pause(2000)
basic.forever(on_forever)

def on_forever2():
    EnviarDades()
    basic.pause(900000)
basic.forever(on_forever2)
