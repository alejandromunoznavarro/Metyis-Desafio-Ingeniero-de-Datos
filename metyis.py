#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 14:13:09 2021

@author: Alejandro Muñoz Navarro
"""

# Importamos librerias
import pandas as pd
from matplotlib import pyplot as plt
import sqlite3
from sqlite3 import Error

class Metyis:
    # Definimos el rango de años
    minimo = 0
    maximo = 0
    # Realizamos la conexión a la Base de Datos
    con = 0
    conectado = 0
    
    def __init__(self):
        self.minimo = 2014
        self.maximo = 2017
        self.connect()

    """
    Conexión a la base de datos
    """
    def connect(self):
        try:
            self.con = sqlite3.connect('Metyis.db')
            self.conectado = 1
            pass
        except Error:
            print("Error de conexión con la Base de Datos")
     
    """
    Desconexión de la base de datos
    """
    def disconnect(self):
        try:
            if self.conectado == 1:
                self.con.close()
            pass
        except Exception:
            print("Error de desconexión con la Base de Datos")
            
    """
    Creación de las tablas en la base de datos'
    """
    
    def create_Tables(self):
        years = range(self.minimo,self.maximo+1)
    
        cursorObj = self.con.cursor()

        # Leemos archivos
        for i in years:
            # Leemos OD por cada año
            df = pd.read_csv("dataset/OD_"+ str(i) +".csv")
        
            cursorObj.execute('''CREATE TABLE OD_'''+str(i)+''' ([Unnamed: 0] 
                              INTEGER PRIMARY KEY, [start_date] date, 
                              [start_station_code] integer, [end_date] date, 
                              [end_station_code] integer, [duration_sec] 
                              integer, [is_member] integer)''')
            df.to_sql('OD_'+str(i), self.con, 
                      if_exists='append', index = False)
            print(df.columns)
    
            # Leemos Stations por cada año
            df = pd.read_csv("dataset/Stations_"+ str(i) +".csv")
            
            
            if(i == 2017):
                cursorObj.execute('''CREATE TABLE Stations_'''+str(i)+''' 
                                  ([code] INTEGER PRIMARY KEY, [name] text, 
                                   [latitude] integer, [longitude] integer, 
                                   [is_public] integer)''')
            else:
                cursorObj.execute('''CREATE TABLE Stations_'''+str(i)+''' 
                                  ([code] INTEGER PRIMARY KEY, [name] text, 
                                   [latitude] integer, [longitude] integer)''')
            df.to_sql('Stations_'+str(i), self.con, 
                      if_exists='append', index = False)
            print(df.columns)
    
        self.con.commit()
    

    def combinar(self, row1, row2, N:int):
        # Combinamos ambas listas
        aux = [[i[0],i[1]] for i in row1]
        for i in row2:
            encontrado = 0
            for j in aux:
                if i[0] == j[0] and not encontrado:
                    encontrado = 1
                    j[1] +=i [1]
            if encontrado == 0:
                aux.append(i)
          
        # Ordenamos la lista y devolvemos el top N
        aux.sort(key = lambda x: x[1], reverse=True)
        lista_combinada = aux[0:N]
        return lista_combinada
    
    """
    EJERCICIOS OBLIGATORIOS
    """

    """ 
    1.  Histograma de tiempos de viaje para un año dado
    """
    def get_hist(self, year:int):
        if not type(year) == int or year < self.minimo or year > self.maximo:
            raise ValueError('Valor del año incorrecto. Debe ser un número entre ')
        try:
            cursorObj = self.con.cursor()

            cursorObj.execute('SELECT duration_sec FROM OD_'+str(year))

            rows = cursorObj.fetchall()
        
            tiempos = [i[0] for i in rows]
        
            # Calculamos los extremos de los intervalos
            intervalos = range(min(tiempos), max(tiempos) + 2) 

            plt.hist(x=tiempos, bins=intervalos, color='#F2AB6D')
            plt.title('Histograma de tiempos en '+str(year))
            plt.xlabel('Tiempos')
            plt.ylabel('Frecuencia')
            # Dibujamos el histograma
            plt.show()  
            pass

        except Error:
            print("Error en la Base de Datos")
    
    """
    2.  Listado del Top N de estaciones más utilizadas para un año dado.
        Dividirlo en:
        1. Estaciones de salida
        2. Estaciones de llegada
        3. En general
    """
    def get_TopN(self, N:int, year:int, option:int):
        if not type(N) == int or N <= 0:
            raise ValueError('Valor de N incorrecto. Debe ser un número positivo')
        elif not type(year) == int or year < self.minimo or year > self.maximo:
            raise ValueError('Valor del año incorrecto. Debe ser un número entre '
                             + str(self.minimo)+' y '+ str(self.maximo))
        elif not type(option) == int or option < 1 or option > 3:
            raise ValueError('Opción incorrecta. Seleccione 1, 2 o 3')
        try:
            cursorObj = self.con.cursor()

            if option == 3:
                # Caso 3 - SIMPLIFICAR
                cursorObj.execute('''SELECT st.name, 
                                  count(od.start_station_code) AS total 
                                  FROM OD_'''+str(year)+''' od 
                                  INNER JOIN Stations_'''+str(year)+''' st 
                                  ON od.start_station_code = st.code 
                                  GROUP BY st.code''')
                row1 = cursorObj.fetchall()
                
                cursorObj.execute('''SELECT st.name, count(od.end_station_code)
                                  AS total FROM OD_'''+str(year)+''' od 
                                  INNER JOIN Stations_'''+str(year)+''' st 
                                  ON od.end_station_code = st.code 
                                  GROUP BY st.code ''')
                row2 = cursorObj.fetchall()
                rows = self.combinar(row1,row2,N)
                
                
            else:
                if option == 2:
                    # Caso 2
                    cursorObj.execute('''SELECT st.name, 
                                      count(od.end_station_code) AS total 
                                      FROM OD_'''+str(year)+''' od 
                                      INNER JOIN Stations_'''+str(year)+''' st 
                                      ON od.end_station_code = st.code 
                                      GROUP BY st.code ORDER BY total DESC 
                                      LIMIT '''+str(N))
               
                else:
                    # Caso 1
                    cursorObj.execute('''SELECT st.name, 
                                      count(od.start_station_code) AS total 
                                      FROM OD_'''+str(year)+''' od 
                                      INNER JOIN Stations_'''+str(year)+''' st 
                                      ON od.start_station_code = st.code 
                                      GROUP BY st.code ORDER BY total DESC 
                                      LIMIT '''+str(N))
                
               
                rows = cursorObj.fetchall()
            stations = [i[0] for i in rows]
            for i in range(0,N):
                print(i+1,stations[i])
            pass
        except Error:
            print('Error en la base de datos')
        

    """
    3.  Listado del Top N de viajes más comunes para un año dado. 
        Donde un viaje se define por su estación de salida y de llegada
    """
    def get_TopNViajes(self, N:int, year:int):
        if not type(N) == int or N <= 0:
            raise ValueError('Valor de N incorrecto. Debe ser un número positivo')
        elif not type(year) == int or year < self.minimo or year > self.maximo:
            raise ValueError('Valor del año incorrecto. Debe ser un número entre '
                             + str(self.minimo)+' y '+ str(self.maximo))

        try:
            cursorObj = self.con.cursor()
            cursorObj.execute('''SELECT st1.name AS name1, st2.name AS name2,
                              od.start_station_code, od.end_station_code, 
                              count(*) AS total FROM OD_'''+str(year)+'''
                              od INNER JOIN Stations_'''+str(year)+'''
                              st1, Stations_'''+str(year)+''' st2 
                              ON st1.code = od.start_station_code AND 
                              st2.code = od.end_station_code GROUP BY 
                              od.start_station_code, od.end_station_code 
                              ORDER BY total DESC LIMIT '''+str(N))
                
               
            rows = cursorObj.fetchall()
            stations = [[i[0],i[1]] for i in rows]
                
            for i in range(0,N):
                print(i+1,'Salida:',stations[i][0], 
                      '\n\tLlegada:',stations[i][1])
            pass
        except Error:
            print('Error en la base de datos')
    
    """
    4.  Identificación de horas punta para un año determinado sin tener en 
        cuenta el día.
        Es decir, si es día de semana, fin de semana, festivo o temporada del 
        año.
    """
    def get_NHoraPunta(self,N:int,year:int):
        if not type(N) == int or N <= 0:
            raise ValueError('Valor de N incorrecto. Debe ser un número positivo')
        elif not type(year) == int or year < self.minimo or year > self.maximo:
            raise ValueError('Valor del año incorrecto. Debe ser un número entre '
                             + str(self.minimo)+' y '+ str(self.maximo))
            
        try:
            cursorObj = self.con.cursor()
            cursorObj.execute('''SELECT time(o1.start_date), count(*) AS total
                              FROM OD_'''+str(year)+''' o1 
                              GROUP BY time(o1.start_date)''') 
            salidas = cursorObj.fetchall()
            cursorObj.execute('''SELECT time(o1.end_date), count(*) AS total
                              FROM OD_'''+str(year)+''' o1 
                              GROUP BY time(o1.end_date)''')
            llegadas = cursorObj.fetchall()
                
            hora = self.combinar(salidas,llegadas,N)
             
            for i in range(0,N):
                print(i+1,'Hora:',hora[i][0])
            pass
        except Error:
            print('Error en la base de datos')
    
            
    """
    EJERCICIOS DESEABLES:
    
    1.  Pruebas unitarias sobre los distintos módulos/objetos/funciones
        - ver modulo test_metyis.py
        
    2.  Comparación de utilización del sistema entre dos años cualesquiera. 
        La utilización del sistema se puede medir como:
        1. Cantidad de viajes totales
        2. Tiempo total de utilización del sistema
        3. Cantidad de viajes por estaciones/bicicletas disponibles
    """
    def get_comparar(self, year1:int, year2:int, option:int):
        if (not type(year1) == int or year1 < self.minimo or year1 > self.maximo) or (not type(year2) == int or year2 < self.minimo or year2 > self.maximo):
            raise ValueError('Valor del año incorrecto. Debe ser un número entre '
                             + str(self.minimo)+' y '+ str(self.maximo))
        elif not type(option) == int or option < 1 or option > 3:
            raise ValueError('Opción incorrecta. Seleccione 1, 2 o 3')
        try:
            cursorObj = self.con.cursor()
            
            if option == 1:
                cursorObj.execute('''SELECT count(*) FROM OD_'''+str(year1))
                cyear1 = cursorObj.fetchall()
                cursorObj.execute('''SELECT count(*) FROM OD_'''+str(year2))
                cyear2 = cursorObj.fetchall()
                resultado = [cyear1[0][0],cyear2[0][0]]
                print('Cantidad de viajes:\n\t'+str(year1)+': '+
                      str(resultado[0]) + '\n\t'+str(year2)+': '+str(resultado[1]))
            elif option == 2:
                cursorObj.execute('''SELECT sum(julianday(od.end_date)-
                                  julianday(od.start_date)) FROM OD_'''+str(year1)+''' od''')
                cyear1 = cursorObj.fetchall()
                cursorObj.execute('''SELECT sum(julianday(od.end_date)-
                                  julianday(od.start_date)) FROM OD_'''+str(year2)+''' od''')
                cyear2 = cursorObj.fetchall()
                resultado = [cyear1[0][0],cyear2[0][0]]
                print('Tiempo del sistema (días):\n\t'+str(year1)+': '+
                      str(resultado[0]) + '\n\t'+str(year2)+': '+str(resultado[1]))
                
            else:
                cursorObj.execute('''SELECT st.name, 
                                  count(od2.start_station_code), T.total 
                                  FROM OD_'''+str(year1)+''' od2 
                                  INNER JOIN (SELECT od.start_station_code, 
                                              count(*) as total 
                                              FROM OD_'''+str(year2)+''' od
                                              GROUP By od.start_station_code) 
                                  AS T 
                                  ON od2.start_station_code = T.start_station_code
                                  INNER JOIN Stations_'''+str(year1)+''' st 
                                  ON st.code = od2.start_station_code
                                  GROUP BY od2.start_station_code''')
                cyear1 = cursorObj.fetchall()
                
                print('Comparación de viajes en estaciones entre los años '+
                      str(year1)+ ' y '+str(year2))
                for i in cyear1:
                    print('Estación: ' +i[0]+'\n\t'+str(year1)+': '+ str(i[1])
                          +'\n\t'+str(year2)+': '+ str(i[2]))
            
            pass
        except Error:
            print('Error en la base de datos')




    """
    3.  Capacidad instalada total (suma de la capacidad total de cada 
        estación)
        NOTA: No entiendo a qué se refiere en cuanto a la capacidad de una estación
    
    4.  Cambio en la capacidad instalada entre dos años puntuales
        NOTA: No entiendo a qué se refiere en cuanto a la capacidad
    """
    
    
    """
    EJERCICIOS IDEALES
    
    1.  Ampliación de la cobertura de la red entre dos años puntuales.
        La misma se puede medir como el área total que generan las estaciones
    """
    def get_area(self,x:list,y:list):
        
        n = len(x)-1
        #Algoritmo para la determinación del área
        for i in range(n):
            suma=(x[i]*(y[i+1]-y[i-1])) # Formula del área Gauss

        area=(1/2)*abs(suma)
 
        return area
     
    def get_ampliacion(self,year1:int,year2:int):
        if (not type(year1) == int or year1 < self.minimo or year1 > self.maximo) or (not type(year2) == int or year2 < self.minimo or year2 > self.maximo):
            raise ValueError('Valor del año incorrecto. Debe ser un número entre '
                             + str(self.minimo)+' y '+ str(self.maximo))
        try:
            cursorObj = self.con.cursor()
            
            cursorObj.execute('''SELECT latitude, longitude FROM Stations_'''+str(year1))
            cyear = cursorObj.fetchall()
            x = [i[0] for i in cyear]  
            y = [i[1] for i in cyear]
            area1 = self.get_area(x, y)
            cursorObj.execute('''SELECT latitude, longitude FROM Stations_'''+str(year2))
            cyear = cursorObj.fetchall()
            x = [i[0] for i in cyear]  
            y = [i[1] for i in cyear]
            area2 = self.get_area(x, y)
            print('Ampliación entre el año '+str(year1)+' y '+str(year2)+ ': '+str(area2-area1))
            pass
        except Error:
            print('Error en la base de datos')
            
    """
    2.  Comparación de densidad de la red para un par de años puntuales. 
        La densidad de la red se mide como el área que abarcan todas las 
        estaciones, dividida la cantidad de estaciones
    """
    def get_densidad(self,year1:int,year2:int):
        if (not type(year1) == int or year1 < self.minimo or year1 > self.maximo) or (not type(year2) == int or year2 < self.minimo or year2 > self.maximo):
            raise ValueError('Valor del año incorrecto. Debe ser un número entre '
                             + str(self.minimo)+' y '+ str(self.maximo))
        try:
            cursorObj = self.con.cursor()
            
            cursorObj.execute('''SELECT latitude, longitude FROM Stations_'''+str(year1))
            cyear = cursorObj.fetchall()
            x = [i[0] for i in cyear]  
            y = [i[1] for i in cyear]
            area1 = self.get_area(x, y)
            cursorObj.execute('''SELECT latitude, longitude FROM Stations_'''+str(year2))
            cyear = cursorObj.fetchall()
            x = [i[0] for i in cyear]  
            y = [i[1] for i in cyear]
            area2 = self.get_area(x, y)
            cursorObj.execute('''SELECT count(st1.code) AS total1, T.total2
                              FROM Stations_'''+str(year1)+''' st1, 
                              (SELECT count(st2.code) AS total2
                               FROM Stations_'''+str(year2)+''' st2) AS T''')
            cestaciones = cursorObj.fetchall()
            densidad1 =   area1/cestaciones[0][0]
            densidad2 =   area2/cestaciones[0][1]
            print('Densidad entre el año '+str(year1)+' y '+str(year2)+ ': \n\t'+
                  str(year1)+': '+str(densidad1) + ': \n\t'+
                  str(year2)+': '+str(densidad2))
            pass
        except Error:
            print('Error en la base de datos')
    """
    EJERCICIOS CON BICICLETAS (?)
    3.  Velocidad promedio de los ciclistas para un año determinado
    
    4.  Cantidad de bicicletas totales para un momento dado. Considerando la
        misma como la cantidad de bicicletas que hay en todas las estaciones 
        activas para ese momento, más todos los viajes que se estén realizando
    """
    
