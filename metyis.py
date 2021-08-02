#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 14:13:09 2021

@author: alejandromunoz
"""

# Importamos librerias
import pandas as pd
from matplotlib import pyplot as plt
import sqlite3
from sqlite3 import Error

class BBDD:
    # Definimos el rango de años
    minimo = 0
    maximo = 0
    # Realizamos la conexión a la Base de Datos
    con = 0
    conectado = 0
    
    def __init__(self):
        self.minimo = 2014
        self.maximo = 2017
        
        try:
            self.connect()
            self.conectado = 1
        except Exception:
            self.conectado = 0

    # Conectamos a la Base de Datos
    def connect(self):

        try:
            self.con = sqlite3.connect('Metyis.db')

        except Error:
            print("Error de conexión con la Base de Datos")
        
    def disconnect(self,con):
        try:
            if self.conectado == 1:
                self.con.close()

        except Error:
            print("Error de desconexión con la Base de Datos")
            
    # Creamos las tablas y añadimos los datasets
    def create_Tables(self):
        years = range(self.minimo,self.maximo+1)
    
        cursorObj = self.con.cursor()

        # Leemos archivos
        for i in years:
            # Leemos OD por cada año
            df = pd.read_csv("dataset/OD_"+ str(i) +".csv")
        
            cursorObj.execute("CREATE TABLE OD_"+str(i)+" ([Unnamed: 0] INTEGER PRIMARY KEY, [start_date] date, [start_station_code] integer, [end_date] date, [end_station_code] integer, [duration_sec] integer, [is_member] integer)")
            df.to_sql('OD_'+str(i), self.con, if_exists='append', index = False)
            print(df.columns)
    
            # Leemos Stations por cada año
            df = pd.read_csv("dataset/Stations_"+ str(i) +".csv")
            
            
            if(i == 2017):
                cursorObj.execute("CREATE TABLE Stations_"+str(i)+" ([code] INTEGER PRIMARY KEY, [name] text, [latitude] integer, [longitude] integer, [is_public] integer)")
            else:
                cursorObj.execute("CREATE TABLE Stations_"+str(i)+" ([code] INTEGER PRIMARY KEY, [name] text, [latitude] integer, [longitude] integer)")
            df.to_sql('Stations_'+str(i), self.con, if_exists='append', index = False)
            print(df.columns)
    
        self.con.commit()
    

    '''
    EJERCICIOS
    '''

    ''' 
    1. Histograma de tiempos de viaje para un año dado
    '''
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

        except Exception:
            print("\x1b[1;31m"+"ERROR! Año no encontrado")
    
    '''
    2. Listado del Top N de estaciones más utilizadas para un año dado.
        Dividirlo en:
        1. Estaciones de salida
        2. Estaciones de llegada
        3. En general
    '''
    def get_TopN(self, N:int, year:int, option:int):
        
        try:
            cursorObj = self.con.cursor()

            if option == 1:
                cursorObj.execute("SELECT name, start_station_code, count(start_station_code) AS total FROM Stations_"+str(year)+", OD_"+str(year)+" WHERE code = start_station_code GROUP BY start_station_code ORDER BY total DESC LIMIT "+str(N))
                
            elif option == 2:
                cursorObj.execute("SELECT name, start_station_code, count(end_station_code) AS total FROM Stations_"+str(year)+", OD_"+str(year)+" WHERE code = end_station_code GROUP BY end_station_code ORDER BY total DESC LIMIT "+str(N))
               
            else:
                cursorObj.execute("SELECT name, start_station_code, count(start_station_code) AS total FROM Stations_"+str(year)+", OD_"+str(year)+" WHERE code = start_station_code GROUP BY start_station_code ORDER BY total DESC LIMIT "+str(N))
               
            rows = cursorObj.fetchall()
            stations = [i[0] for i in rows]
            print(stations)
            '''
            tiempos = [i[0] for i in rows]
        
            # Calculamos los extremos de los intervalos
            intervalos = range(min(tiempos), max(tiempos) + 2) 

            plt.hist(x=tiempos, bins=intervalos, color='#F2AB6D')
            plt.title('Histograma de tiempos en '+str(year))
            plt.xlabel('Tiempos')
            plt.ylabel('Frecuencia')
            # Dibujamos el histograma
            plt.show()     
            '''
        except Exception:
            print("\x1b[1;31m"+"ERROR! Año no encontrado")
        


# Listado del Top N de viajes más comunes para un año dado. Donde un viaje se define por su estación de salida y de llegada

# Identificación de horas punta para un año determinado sin tener en cuenta el día. Es decir, si es día de semana, fin de semana, festivo o temporada del año.

user = BBDD()
#user.create_Tables()
user.get_hist(2016)
user.get_TopN(5, 2014, 2)

