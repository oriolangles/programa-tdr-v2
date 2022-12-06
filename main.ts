function PantallaDades () {
    OLED.clear()
    OLED.writeStringNewLine("TDR")
    OLED.newLine()
    OLED.writeStringNewLine("Temperatura: " + ("" + temperatura) + " C")
    OLED.writeStringNewLine("Humitat: " + ("" + Humitat) + "%")
    OLED.writeStringNewLine("Pressio: " + ("" + Pressió) + " hPa")
    OLED.writeStringNewLine("Bateria: " + ("" + PercBat) + "%")
    OLED.writeStringNewLine("Voltatge:  " + ("" + batvolt) + " V")
}
function Wifi () {
    botoapretat = 0
    while (botoapretat == 0) {
        if (pins.digitalReadPin(DigitalPin.P2) == 0) {
            botoapretat += 1
            SSID = "MAZINGERZ"
            WIFI_PASSWORD = "letsthesunshine"
        }
        if (pins.digitalReadPin(DigitalPin.P16) == 0) {
            botoapretat += 1
            SSID = "orioloneplusnord"
            WIFI_PASSWORD = "bondia1234"
        }
    }
    OLED.clear()
    OLED.writeStringNewLine("...")
    ESP8266_IoT.initWIFI(SerialPin.P8, SerialPin.P12, BaudRate.BaudRate115200)
    ESP8266_IoT.connectWifi(SSID, WIFI_PASSWORD)
    OLED.clear()
    OLED.writeStringNewLine("Connectat")
}
function LlegirDades () {
    temperatura = BME280.temperature(BME280_T.T_C)
    Humitat = BME280.humidity()
    Pressió = BME280.pressure(BME280_P.hPa)
}
function EnviarDades () {
    ESP8266_IoT.connectThingSpeak()
    ESP8266_IoT.setData(
    "8OUGW8MHUV093H5B",
    temperatura,
    Humitat,
    Pressió,
    PercBat,
    batvolt,
    sos
    )
    ESP8266_IoT.uploadData()
}
function Sos () {
    OLED.clear()
    OLED.writeStringNewLine("SOS")
    OLED.newLine()
    OLED.writeStringNewLine("Enviant...")
    basic.pause(15000)
    sos = 1
    EnviarDades()
    sos = 0
    basic.pause(15000)
    EnviarDades()
    basic.pause(2000)
    pins.digitalWritePin(DigitalPin.P2, 1)
}
function VoltatgeBateria () {
    batvolt = 0
    for (let index = 0; index < 10; index++) {
        batvolt += pins.analogReadPin(AnalogPin.P1) * 3.148 / 1023 * 11
    }
    batvolt = batvolt / 10 + 0.02
    PercentatgeBat()
}
function PercentatgeBat () {
    if (batvolt >= 4.2) {
        PercBat = 100
    }
    if (batvolt < 4.2 && batvolt >= 4.02) {
        PercBat = 80
    }
    if (batvolt < 4.02 && batvolt >= 3.87) {
        PercBat = 60
    }
    if (batvolt < 3.87 && batvolt >= 3.8) {
        PercBat = 40
    }
    if (batvolt < 3.8 && batvolt >= 3.73) {
        PercBat = 20
    }
    if (batvolt < 3.73) {
        PercBat = 10
    }
}
let WIFI_PASSWORD = ""
let SSID = ""
let botoapretat = 0
let batvolt = 0
let PercBat = 0
let Pressió = 0
let Humitat = 0
let temperatura = 0
let sos = 0
pins.digitalWritePin(DigitalPin.P2, 1)
pins.digitalWritePin(DigitalPin.P16, 1)
OLED.init(128, 64)
OLED.writeStringNewLine("TDR")
OLED.newLine()
OLED.writeStringNewLine("A - WIFI CASA")
OLED.writeStringNewLine("B - WIFI MOBIL")
OLED.newLine()
Wifi()
basic.pause(1000)
LlegirDades()
VoltatgeBateria()
sos = 0
basic.forever(function () {
    LlegirDades()
    VoltatgeBateria()
    if (pins.digitalReadPin(DigitalPin.P2) == 0) {
        Sos()
    } else {
        PantallaDades()
        basic.pause(2000)
    }
})
basic.forever(function () {
    EnviarDades()
    basic.pause(900000)
})
