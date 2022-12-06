def PantallaDades():
    OLED.clear()
    OLED.write_string_new_line("TDR")
    OLED.new_line()
    OLED.write_string_new_line("Temperatura: " + ("" + str(temperatura)) + " C")
    OLED.write_string_new_line("Humitat: " + ("" + str(Humitat)) + "%")
    OLED.write_string_new_line("Pressio: " + ("" + str(Pressió)) + " hPa")
    OLED.write_string_new_line("Intensitat: " + ("" + str(intensitat)) + " mA")

def on_button_pressed_a():
    global pantalla
    pantalla += 1
input.on_button_pressed(Button.A, on_button_pressed_a)

def LlegirDades():
    global temperatura, Humitat, Pressió, intensitat
    temperatura = BME280.temperature(BME280_T.T_C)
    Humitat = BME280.humidity()
    Pressió = BME280.pressure(BME280_P.H_PA)
    intensitat = pins.analog_read_pin(AnalogPin.P1)
def VoltatgeBateria():
    global batvolt
    batvolt = 0
    for index in range(100):
        batvolt += pins.analog_read_pin(AnalogPin.P1)
    batvolt = batvolt / 100 * 3.187 / 1023 * 110 / 10
def PercentatgeBat():
    global PercBat
    if batvolt == 4.2:
        PercBat = 100
    if batvolt < 4.2 and batvolt >= 4:
        PercBat = 80
    if batvolt < 4 and batvolt >= 3.9:
        PercBat = 60
    if batvolt < 3.9 and batvolt >= 3.8:
        PercBat = 40
    if batvolt < 3.8 and batvolt >= 3.7:
        PercBat = 20
    if batvolt < 3.7:
        PercBat = 0
PercBat = 0
batvolt = 0
intensitat = 0
Pressió = 0
Humitat = 0
temperatura = 0
OLED.init(128, 64)
OLED.write_string_new_line("TDR")
OLED.new_line()
VoltatgeBateria()
PercentatgeBat()
basic.pause(5000)
ESP8266_IoT.init_wifi(SerialPin.P8, SerialPin.P12, BaudRate.BAUD_RATE115200)
ESP8266_IoT.connect_wifi("MAZINGERZ", "letsthesunshine")
if ESP8266_IoT.wifi_state(True):
    OLED.write_string_new_line("Connectat")
else:
    OLED.write_string_new_line("No connectat")
basic.pause(1000)
pantalla = 1

def on_forever():
    ESP8266_IoT.connect_thing_speak()
    if ESP8266_IoT.thing_speak_state(True):
        VoltatgeBateria()
        PercentatgeBat()
        ESP8266_IoT.set_data("8OUGW8MHUV093H5B",
            temperatura,
            Humitat,
            Pressió,
            PercBat,
            batvolt)
        ESP8266_IoT.upload_data()
    else:
        OLED.clear()
        OLED.write_string_new_line("TDR")
        OLED.new_line()
        OLED.write_string_new_line("ERROR DADES")
    basic.pause(300000)
basic.forever(on_forever)

def on_forever2():
    global pantalla
    LlegirDades()
    if pantalla == 1:
        PantallaDades()
        basic.pause(2000)
    if pantalla == 2:
        VoltatgeBateria()
        PercentatgeBat()
        OLED.clear()
        OLED.write_string_new_line("TDR")
        OLED.new_line()
        OLED.write_string_new_line("BATERIA:" + ("" + str(PercBat)) + "%")
        basic.pause(2000)
    if pantalla > 2:
        pantalla = 1
basic.forever(on_forever2)
