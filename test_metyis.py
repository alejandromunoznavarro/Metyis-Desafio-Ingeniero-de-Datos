#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 20:54:28 2021

@author: Alejandro Muñoz Navarro
"""

import unittest
import metyis

class TestMetyis(unittest.TestCase):
    
    def test_get_hist(self):
        with self.assertRaises(ValueError):
            metyis.Metyis().get_hist(2010)
            
    def test_get_TopN(self):
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopN(0, 2014, 1)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopN(-1, 2014, 1)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopN(1, 2000, 1)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopN(1, 2030, 1)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopN(1, 2014, 0)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopN(1, 2014, 4)
    
    def test_get_TopNViajes(self):
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopNViajes(0, 2014)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopNViajes(-1, 2014)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopNViajes(2, 2013)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_TopNViajes(2, 2020)

    def test_get_NHoraPunta(self):
        with self.assertRaises(ValueError):
            metyis.Metyis().get_NHoraPunta(0, 2014)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_NHoraPunta(-1, 2014)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_NHoraPunta(2, 2013)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_NHoraPunta(2, 2020)

    def test_get_comparar(self):
        with self.assertRaises(ValueError):
            metyis.Metyis().get_comparar(0, 2014, 1)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_comparar(-1, 2014, 1)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_comparar(1, 2000, 1)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_comparar(1, 2030, 1)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_comparar(1, 2014, 0)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_comparar(1, 2014, 4)
            
    def test_get_area(self):
        self.assertEquals(metyis.Metyis().get_area([0,0,1,1], [0,1,1,0]), 0.5)
     
    def test_get_ampliacion(self):
        with self.assertRaises(ValueError):
            metyis.Metyis().get_ampliacion(2013, 2014)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_ampliacion(2020, 2014)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_ampliacion(2015, 201)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_ampliacion(2015, 2020)
            
    def test_get_densidad(self):
        with self.assertRaises(ValueError):
            metyis.Metyis().get_densidad(2013, 2014)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_densidad(2020, 2014)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_densidad(2015, 201)
        with self.assertRaises(ValueError):
            metyis.Metyis().get_densidad(2015, 2020)
            
if __name__ == "__main__":
    unittest.main()