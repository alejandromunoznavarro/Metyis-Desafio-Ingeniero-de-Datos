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
            print("\x1b[1;31m"+"Error de conexión con la Base de Datos")
     
    """
    Desconexión de la base de datos
    """
    def disconnect(self,con):
        try:
            if self.conectado == 1:
                self.con.close()
            pass
        except Exception:
            print("\x1b[1;31m"+"Error de desconexión con la Base de Datos")
            
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
    EJERCICIOS
    """

    """ 
    1.  Histograma de tiempos de viaje para un año dado
    """
    def get_hist(self, year:int):
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

        except Exception:
            print("\x1b[1;31m"+"ERROR! Año no encontrado")
    
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
            print("\x1b[1;31m"+"ERROR! Año no encontrado")
        

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
        except Exception:
            print("\x1b[1;31m"+"ERROR! Año no encontrado")
    
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
        except Exception:
            print("\x1b[1;31m"+"ERROR! Año no encontrado")
            
    
if __name__ == "__main__":  
    user = Metyis()
    #user.create_Tables()
    #user.get_hist(2016)
    user.get_TopN(2, 2014, 4)
    #user.get_TopNViajes(6, 2014)
    #user.get_NHoraPunta(6, 2014)