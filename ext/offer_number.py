# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:33:18 2022

@author: ph1g0
"""

"""This module deals with reading, updating and storing the offer number"""



def readOfferNumber():
    """
    Read the offer number from offer_number.txt
    """
    with open('offer_number.txt', 'r') as file:
        offer_number = int(file.read())
        file.close()
  
    return offer_number
    
def storeOfferNumber(offer_number):
    """
    Store the offer number from offer_number.txt
    """
    with open('offer_number.txt', 'w') as file:
        file.write(str(offer_number))
        file.close()
        
def updateOfferNumber():
    """
    Update the offer number from offer_number.txt
    """
    offer_number = readOfferNumber()
    offer_number += 1
    storeOfferNumber(offer_number)