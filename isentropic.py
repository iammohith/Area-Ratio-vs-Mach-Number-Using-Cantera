#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 13:21:16 2020

Author: Mohith Sai

Description:
This script calculates the area ratio versus Mach number curve for 
isentropic, adiabatic flow using Cantera. It allows for the analysis 
of different gas mixtures or defaults to a hydrogen/nitrogen mixture.
"""

import cantera as ct
import math
import numpy as np


def soundspeed(gas):
    """Calculate the speed of sound in an ideal gas."""
    gamma = gas.cp / gas.cv  # Heat capacity ratio
    return math.sqrt(gamma * ct.gas_constant * gas.T / gas.mean_molecular_weight)


def isentropic(gas=None):
    """
    Compute the area ratio vs. Mach number curve.

    If a gas object is provided, it will be used for calculations 
    with the stagnation state defined by the gas's state. If no gas 
    is provided, calculations are performed for a hydrogen/nitrogen 
    mixture with a stagnation temperature of 1200 K and a pressure of 10 atm.
    
    Returns:
        np.ndarray: An array containing the area ratios, Mach numbers, 
                    temperatures, and pressure ratios.
    """
    if gas is None:
        gas = ct.Solution('gri30.yaml')  # Default gas mixture in YAML format
        gas.TPX = 1200.0, 10.0 * ct.one_atm, 'H2:1,N2:0.1'

    # Get the stagnation state parameters
    s0 = gas.s  # Entropy
    h0 = gas.h  # Enthalpy
    p0 = gas.P  # Pressure

    mdot = 1  # Mass flow rate (arbitrary)
    amin = 1.e14  # Minimum area initialized to a large number

    # Initialize an array to store data for plotting
    data = np.zeros((200, 4))

    # Compute values for a range of pressure ratios
    for r in range(200):
        p = p0 * (r + 1) / 201.0  # Current pressure
        gas.SP = s0, p  # Set the state using (entropy, pressure)

        v2 = 2.0 * (h0 - gas.h)  # Calculate velocity from enthalpy difference
        v = math.sqrt(v2)  # Velocity
        area = mdot / (gas.density * v)  # Area calculation
        amin = min(amin, area)  # Update minimum area
        data[r, :] = [area, v / soundspeed(gas), gas.T, p / p0]  # Store results

    data[:, 0] /= amin  # Normalize area ratios

    return data


if __name__ == "__main__":
    print(isentropic.__doc__)  # Print documentation for the isentropic function
    data = isentropic()  # Perform the calculations

    try:
        import matplotlib.pyplot as plt  # Import matplotlib for plotting
        plt.plot(data[:, 1], data[:, 0])  # Plot area ratio vs. Mach number
        plt.ylabel('Area Ratio')
        plt.xlabel('Mach Number')
        plt.title('Isentropic Flow: Area Ratio vs. Mach Number')
        plt.grid()  # Add grid for better readability
        plt.show()  # Show the plot

    except ImportError:
        # Fallback for environments without matplotlib
        print('Area Ratio, Mach Number, Temperature, Pressure Ratio:')
        print(data)
