#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 19:58:50 2021

@author: Alejandro Muñoz Navarro
"""

import metyis


def menu():
    print("Seleccione una opción:"+
          "\n\t1. Histograma de tiempos de viaje para un año dado"+
          "\n\t2. Listado del Top N de estaciones más utilizadas para un año dado (Estaciones de salida)"+
          "\n\t3. Listado del Top N de estaciones más utilizadas para un año dado (Estaciones de llegada)"+
          "\n\t4. Listado del Top N de estaciones más utilizadas para un año dado (En general)"+
          "\n\t5. Listado del Top N de viajes más comunes para un año dado."+
          "\n\t6. Identificación de horas punta para un año determinado sin tener en cuenta el día."+
          "\n\t7. Comparación de utilización del sistema entre dos años cualesquiera. (Cantidad de viajes totales )"+
          "\n\t8. Comparación de utilización del sistema entre dos años cualesquiera. (Tiempo total de utilización del sistema)"+
          "\n\t9. Comparación de utilización del sistema entre dos años cualesquiera. (Cantidad de viajes por estaciones/bicicletas disponibles)"+
          "\n\t10. Ampliación de la cobertura de la red entre dos años puntuales. "+
          "\n\t11. Comparación de densidad de la red para un par de años puntuales."+
          "\n\t12. Salir")
  
    
if __name__ == "__main__":  
    user = metyis.Metyis()
    entrada = -1
    
    while not entrada == 12:
        year = -1
        N = -1
        year1 = -1
        year2 = -1
        
        while entrada==-1:
            menu()
            aux = int(input())
            if aux>=1 and aux <= 12:
                entrada = aux
            else:
                print("Opción incorrecta, pruebe otra vez")
    
    
        """
        Crear tabla Base de Datos (está creada)
            - create_Tables()
        """
        #user.create_Tables()
        """
        Histograma de tiempos de viaje para un año dado 
            - get_hist(year)
            """
        if entrada == 1:
            print("Introduce un año entre "+ str(user.minimo) + " y " + str(user.maximo))
            while year == -1:
                aux = int(input())
                if aux >= user.minimo and aux <= user.maximo:
                    year = aux
                else:
                    print("Año incorrecto, pruebe otra vez")
            user.get_hist(year)
            entrada = -1
            """
            Listado del Top N de estaciones más utilizadas para un año dado 
            1. Estaciones de salida
                - get_TopN(N, year, option=1)
            2. Estaciones de llegada 
                - get_TopN(N, year, option=2)
            3. En general 
                - get_TopN(N, year, option=3)
            
            Listado del Top N de viajes más comunes para un año dado. 
                - get_TopNViajes(N, year)
                
            Identificación de horas punta para un año determinado sin tener en 
            cuenta el día. 
                - get_NHoraPunta(N, year)
            """
        elif entrada == 2 or entrada == 3 or entrada == 4 or entrada ==5 or entrada == 6:
            print("Introduce un N para el Top N")
            while N == -1:
                aux = int(input())
                if aux >0:
                    N = aux
                else:
                    print("N debe ser positiva, pruebe otra vez")
            print("Introduce un año entre "+ str(user.minimo) + " y " + str(user.maximo))
            while year == -1:
                aux = int(input())
                if aux >= user.minimo and aux <= user.maximo:
                    year = aux
                else:
                    print("Año incorrecto, pruebe otra vez")
            if entrada == 2:
                user.get_TopN(N, year, 1)
            elif entrada == 3:
                user.get_TopN(N, year, 2)
            elif entrada == 4:
                user.get_TopN(N, year, 3)
            elif entrada == 5:
                user.get_TopNViajes(N, year)
            else:
                user.get_NHoraPunta(N, year)
            entrada = -1
            1
            """
            Comparación de utilización del sistema entre dos años cualesquiera. La
            utilización del sistema se puede medir como:
            1. Cantidad de viajes totales 
                - get_comparar(year1, year2, option=1)
            2. Tiempo total de utilización del sistema 
                - get_comparar(year1, year2, option=2)
            3. Cantidad de viajes por estaciones/bicicletas disponibles 
                - get_comparar(year1, year2, option=3)
            
            
            Ampliación de la cobertura de la red entre dos años puntuales. 
                - get_ampliacion(year1, year2)
            
            
            Comparación de densidad de la red para un par de años puntuales.
                - get_densidad(year1, year2)
            """
        
    
        elif entrada == 7 or entrada == 8 or entrada == 9 or entrada ==10 or entrada == 11:
            print("Introduce un año entre "+ str(user.minimo) + " y " + str(user.maximo))
            while year1 == -1:
                aux = int(input())
                if aux >= user.minimo and aux <= user.maximo:
                    year1 = aux
                else:
                    print("Año incorrecto, pruebe otra vez")
            print("Introduce un año entre "+ str(user.minimo) + " y " + str(user.maximo))
            while year2 == -1:
                aux = int(input())
                if aux >= user.minimo and aux <= user.maximo:
                    year2 = aux
                else:
                    print("Año incorrecto, pruebe otra vez")
            if entrada == 7:
                user.get_comparar(year1, year2, 1)
            elif entrada == 8:
                user.get_comparar(year1, year2, 2)
            elif entrada == 9:
                user.get_comparar(year1, year2, 3)
            elif entrada == 10:
                user.get_ampliacion(year1, year2)
            else:
                user.get_densidad(year1, year2)
            entrada = -1
    user.disconnect()