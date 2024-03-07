from datetime import date, datetime, timedelta
import os
import pandas as pd
import requests
import sys


# Fecha inicial considerada: año:2021 mes:08 dia:21

API_TOKEN = "..."

url_recaudacion = "https://toteatglobal.appspot.com/mw/or/1.0/collection"
params = {
    "xir" : "6502106216529920", # Identificador del restaurante
    "xil" : "2",                # Identificador del local asociado al restaurante
    "xiu" : "1002",             # Identificador del usuario
    "xapitoken" : API_TOKEN,    # Token habilitado (ver credenciales)
    #"date" : ""                # Deben ser enviados como un string en formato YYYYMMDD
}


def obtener_recaudacion_fecha(fecha:str=None, url=url_recaudacion, params=params) -> dict:
    if not fecha:
        fecha = datetime.today() - timedelta(days= 1)
        fecha = fecha.strftime("%Y%m%d")
    params["date"] = fecha
    print(f"Conectando a la API por consulta recaudacion {fecha}...")
    response = requests.get(url, params)
    if response.status_code == 200:
        data = response.json()
        print("Procesando respuesta...")
    else:
        print("Error en la solicitud:", response["msg"])
        return None

    recaudacion = {"Fecha": "","Dia semana": "", "Monto total": 0}
    modos_de_pago_id = [1000, 2000, 3000, 5000, 5012, 5013, 5015, 5103, 5119, 9001, 50002, 50004]
    modos_de_pago = ["Efectivo", "Tarjeta Credito", "Tarjeta Debito", "Web Pay", "PedidosYa", "PedidosYa Vouchers",
                    "Rappi", "UberEats", "Mercat", "Transferencia", "PedidosYa Efectivo", "Uber eats"]
    recaudacion.update(dict.fromkeys(modos_de_pago_id, 0))
    tabla_modos_de_pago = dict(zip(modos_de_pago_id, modos_de_pago))
    recaudacion["Fecha"] = datetime.strptime(params["date"], "%Y%m%d").strftime("%Y/%m/%d")
    recaudacion["Dia semana"] = datetime.strptime(params["date"], "%Y%m%d").strftime("%A")

    for turno in data["data"]["shifts"].keys():
        for caja in data["data"]["shifts"][turno]["registers"].keys():
            for item in data["data"]["shifts"][turno]["registers"][caja]:
                recaudacion["Monto total"] += item["finalAmount"] 
                for sub_item in item["paymentMethods"]:
                    if sub_item["amount"] is not None:
                        recaudacion[sub_item["paymentMethodID"]] += sub_item["amount"]

    for id, nombre in tabla_modos_de_pago.items():
        recaudacion[nombre] = recaudacion.pop(id) 

    return recaudacion


def generar_csv(data:dict, nombre_archivo:str="./recaudacion_historica.csv"):
    # abrir archivo si existe, sino devolver error? generar desde inicio?
    df = pd.DataFrame.from_dict([data.values()])
    df.columns=data.keys()
    fecha = data["Fecha"]
    nombre = nombre_archivo
    if os.path.exists(nombre):
        df.to_csv(nombre, mode="a", index=False, header=False)
        return f"archivo {nombre} actualizado al {fecha}"
    else:
        nombre = f"./recaudacion_{fecha[0:4]}_{fecha[5:7]}_{fecha[8:]}"
        df.to_csv(f"{nombre}.csv", index=False)
        return f"archivo {nombre}.csv generado"


def obtener_recaudacion_historica_completa():
    """Actualiza archivo recaudacion_historica.csv"""
    fecha_ini = date(2021, 8, 21) # primer registro en toteat 2021 08 03, connsidero desde 21/08/2021
    fecha_fin = date.today() - timedelta(days= 1)  # ayer
    fecha_consulta = fecha_ini # fecha comienzo de periodo de consulta
    while (fecha_consulta <= fecha_fin):
        print(generar_csv(obtener_recaudacion_fecha(fecha_consulta.strftime("%Y%m%d"))))
        fecha_consulta += timedelta (days= 1)
    return


#if len(sys.argv) != 1:
#    print(generar_csv(obtener_recaudacion_fecha(fecha=sys.argv[1])))
#else:
#    print(generar_csv(obtener_recaudacion_fecha()))


obtener_recaudacion_historica_completa()
