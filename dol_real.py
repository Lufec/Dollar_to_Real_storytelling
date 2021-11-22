#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 22:11:32 2021

@author: lufec
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style

exchange_rates = pd.read_csv('euro-daily-hist_1999_2020.csv')

exchange_rates.rename(columns={'[Brazilian real ]': 'BR_real',
                               '[US dollar ]':'US_dollar',
                               'Period\\Unit:': 'Time'},
                      inplace=True)
exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)
exchange_rates.reset_index(drop=True, inplace=True)

exchange_rates = exchange_rates[exchange_rates['BR_real'] != '-']
exchange_rates = exchange_rates[exchange_rates['US_dollar'] != '-']

exchange_rates['US_dollar'] = exchange_rates['US_dollar'].astype(float)
exchange_rates['BR_real'] = exchange_rates['BR_real'].astype(float)

exchange_rates['US_dollar_to_BR_real'] = exchange_rates['BR_real']/exchange_rates['US_dollar']

dollar_to_real = exchange_rates[['Time','US_dollar_to_BR_real']]

dollar_to_real['rolling_mean'] = dollar_to_real['US_dollar_to_BR_real'].rolling(30).mean()

dollar_to_real.dropna(inplace = True)

pres_brasil = dollar_to_real.copy()
fhc = pres_brasil.copy()[pres_brasil['Time'].dt.year < 2002]
lula = pres_brasil.copy()[(pres_brasil['Time'].dt.year >= 2002)&
			   (pres_brasil['Time'].dt.year < 2010)]
dilma = pres_brasil.copy()[(pres_brasil['Time'].dt.year >= 2010)&
                           (pres_brasil['Time'] < '2016-09-01')]
temer = pres_brasil.copy()[(pres_brasil['Time'] >= '2016-09-01')&
                           (pres_brasil['Time'].dt.year < 2018)]
bolso = pres_brasil.copy()[(pres_brasil['Time'].dt.year >= 2018)]

style.use('fivethirtyeight')
### Adding the subplots
plt.figure(figsize=(16, 6))
ax1 = plt.subplot(2,5,1)
ax2 = plt.subplot(2,5,2)
ax3 = plt.subplot(2,5,3)
ax4 = plt.subplot(2,5,4)
ax5 = plt.subplot(2,5,5)
ax6 = plt.subplot(2,1,2)

axes = [ax1, ax2, ax3, ax4, ax5, ax6]

for ax in axes:
    ax.set_ylim(1.00, 6.00)
    ax.set_yticks([1.0, 1.5, 2.0,2.5, 3.0,3.5, 4.0,4.5, 5.0,5.5, 6.0])
    ax.set_yticklabels(['','1.5', '2.0','2.5','3.0','3.5','4.0','4.5','5.0','5.5','6.0'],alpha=0.3)
    ax.grid(alpha=0.5)

### Ax1: FHC
ax1.plot(fhc['Time'], fhc['rolling_mean'],
        color='#BF5FFF')
ax1.set_xticklabels(['jan-00','','','jan-01','','','dez-01'],
                   alpha=0.3)
ax1.text(11230, 7, 'FHC', fontsize=18, weight='bold',
        color='#BF5FFF')
ax1.text(11120, 6.5, '(2000-2001)', weight='bold',
        alpha=0.3)

### Ax2: Lula
ax2.plot(lula['Time'], lula['rolling_mean'],
        color='#ffa500')
ax2.set_xticks([11734,12145,12556,12966,13377,13788,14199,14610])
ax2.set_xticklabels(['','2003','','2005','','2007','','2009'],
                   alpha=0.3)
ax2.text(12650, 7, 'LULA', fontsize=18, weight='bold',
        color='#ffa500')
ax2.text(12250, 6.5, '(2002-2010)', weight='bold',
        alpha=0.3)

### Ax3: Dilma
ax3.plot(dilma['Time'], dilma['rolling_mean'],
        color='#00B2EE')
ax3.set_xticks([14610,14975,15340,15705,16070,16436,16801])
ax3.set_xticklabels(['10','11','12','13','14','15','16'],
                   alpha=0.3)
ax3.text(15300, 7, 'DILMA', fontsize=18, weight='bold',
        color='#00B2EE')
ax3.text(15000, 6.5, '(2010-08/2016)', weight='bold',
        alpha=0.3)

### Ax4: Temer
ax4.plot(temer['Time'], temer['rolling_mean'],
        color='#3cb043')
ax4.set_xticks([17045,17142,17240,17337,17434,17532])
ax4.set_xticklabels(['sep-16','','jan-17','','sep-17',''],
                   alpha=0.3)
ax4.text(17200, 7, 'TEMER', fontsize=18, weight='bold',
        color='#3cb043')
ax4.text(17100, 6.5, '(09/2016 - 2018)', weight='bold',
        alpha=0.3)

### Ax5: Bolso
ax5.plot(bolso['Time'], bolso['rolling_mean'],
        color='#990f02')
ax5.set_xticks([17532,17669,17806,17943,18080,18217,18354,18491,18628])
ax5.set_xticklabels(['','2018','','2019','','2020','','2021',''],
                alpha=0.3)
ax5.text(17650, 7, 'BOLSONARO', fontsize=18, weight='bold',
        color='#990f02')
ax5.text(17700, 6.5, '(2018 - 2021)', weight='bold',
        alpha=0.3)

#Todos

ax6.plot(fhc['Time'], fhc['rolling_mean'],
        color='#BF5FFF')
ax6.plot(lula['Time'], lula['rolling_mean'],
        color='#ffa500')
ax6.plot(dilma['Time'], dilma['rolling_mean'],
        color='#00B2EE')
ax6.plot(temer['Time'], temer['rolling_mean'],
        color='#3cb043')
ax6.plot(bolso['Time'], bolso['rolling_mean'],
        color='#990f02')
ax6.grid(alpha=0.5)
ax6.set_xticks([])

### Adding a title and a subtitle
ax1.text(11500.0, 9.35, 'BRL-USD rate averaged 2.68 under the last five BR presidents',
         fontsize=20, weight='bold')
ax1.text(11700.0, 8.14, '''BR-USD exchange rates under FHC, Lula, Dilma, Temer and Bolsonaro''',
        fontsize=16)

plt.savefig('fig.png')
