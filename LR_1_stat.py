"""
Задание 5. Статистическая обработка измерений газоразрядного счетчика
и сцинтиляционного. Построение диаграмм и вычисление вероятности попадания
в каждый из интервалов измерений.

"""
import pltinit as ini

import os
import math as m
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import scipy.special as special
import pickle

#===================================================
# Настройка графиков
#===================================================

ini.init_matplotlib(plt, IsReport=True)

#===================================================
# Используемые функции
#===================================================

# Считает количество ненулевых элементов в столбце 2-х массива
def Count_not_zer(Array,M,N):
    Count = np.zeros([M])
    for j in range (M): # По столбцам
        for i in range (N): # По строкам
            if Array[i,j] != 0:
                Count[j] += 1
    return Count

# Считаем среднее для каждого интервала
def Ave_interval(Array,n,M):
    Ave = np.zeros([M])
    for j in range (M):
        Ave[j] = np.sum(Array[:,j]) / n[j]
    return Ave

# Считаем общее среднее
def Ave_ave_interval(Array,n,num,M):
    Sum = 0
    for j in range (M):
        Sum += Array[j] * n[j]
    Ave_ave = Sum/num
    return Ave_ave

# Считаем СКО
def SKO(Array,AVR,n,num,M,H):
    Sum = 0
    for j in range(M):
        Sum += n[j] * (Array[j] - AVR)**2
    SKO_2 = (1/(num-1)) * Sum - (H**2)/12
    return SKO_2

# Расчет вероятностей
def Probability_int(Bord,sko_2,sko,avr,M):
    prob = np.zeros([M,2])
    INT = np.zeros([M,2])
    for j in range (M):
        INT = integrate.quad(lambda H : np.exp(-0.5 * (H-avr)**2 /sko_2 ),Bord[j,0],Bord[j,1])
        prob[j] = INT / ((2*np.pi)**0.5 * sko)
    return prob*100

# Формирование массива без ошибки вычисления
def only_prob(Array_err,M):
    only_prob = np.zeros([M])
    only_prob = Array_err[:,0]
    return only_prob

def Crit_Pirs(num,M,NUM,prob):
    hi_2 = 0
    prob /= 100
    for j in range(M):
        hi_2 += (num[j] - NUM*prob[j])**2 /(NUM*prob[j])
    return hi_2

#===================================================
# Исходные данные
#===================================================

num_int = 12        # Количество интервалов
N_meas  = 118       # Количество измерений
h_SN    = 0.00325   # Шаг интервала СЦ
h_GZ    = 0.01725   # Шаг интервала ГР

# Загружаем интервалы сцинтиляционного датчика (12 интервалов)
SN_int = np.loadtxt("SN_stat.txt", delimiter='\t', dtype=np.float)
n_max_SN = 32   #Максимальное количество эл-ов в столбце

# Загружаем интервалы газоразрядного датчика (12 интервалов)
GZ_int = np.loadtxt("GZ_stat.txt", delimiter='\t', dtype=np.float)
n_max_GZ = 23   #Максимальное количество эл-ов в столбце

# Левая и правая границы интервалов СЦ датчика
SN_bord = np.loadtxt("LR_1_dat_stat_bord_SN.txt", delimiter='\t', dtype=np.float)

# Левая и правая границы интервалов ГР датчика
GZ_bord = np.loadtxt("LR_1_dat_stat_bord_GZ.txt", delimiter='\t', dtype=np.float)


num_SN = Count_not_zer(SN_int,num_int,n_max_SN)
num_GZ = Count_not_zer(GZ_int,num_int,n_max_GZ)

#===================================================
# Определение статистических параметров
#===================================================

# Средние для каждого из интервалов
SN_int_ave = Ave_interval(SN_int,num_SN,num_int)
GZ_int_ave = Ave_interval(GZ_int,num_GZ,num_int)

# Среднее по измерениям
SN_ave = Ave_ave_interval(SN_int_ave,num_SN,N_meas,num_int)
GZ_ave = Ave_ave_interval(GZ_int_ave,num_GZ,N_meas,num_int)

# СКО  в квадрате
SKO_2_SN = SKO(SN_int_ave,SN_ave,num_SN,N_meas,num_int,h_SN)
SKO_2_GZ = SKO(GZ_int_ave,GZ_ave,num_GZ,N_meas,num_int,h_GZ)

# СКО
SKO_SN = (SKO_2_SN)**(0.5)
SKO_GZ = (SKO_2_GZ)**(0.5)

# Вычисление вероятностей
prob_err_SN = Probability_int(SN_bord,SKO_2_SN,SKO_SN,SN_ave,num_int)
prob_SN = only_prob(prob_err_SN,num_int)
prob_err_GZ = Probability_int(GZ_bord,SKO_2_GZ,SKO_GZ,GZ_ave,num_int)
prob_GZ = only_prob(prob_err_GZ,num_int)

#Критерий Пирсона
pirs_2_SN = Crit_Pirs(num_SN,num_int,N_meas,prob_SN)
pirs_2_GZ = Crit_Pirs(num_GZ,num_int,N_meas,prob_GZ)

#===================================================
# Построение графиков и вывод результатов
#===================================================

f = open("stat_and_prob_SN.txt","w")
f.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CЦИНТИЛЯЦИОННЫЙ СЧЕТЧИК ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
f.write("\n")
f.write("Разбиваем диапазон измеренных значений на 12.\n")
f.write("Количество измерений для каждого интервала")
for j in range(0,num_int):
    f.write(str(num_SN[j]))
f.write("\n\n")
f.write("Шаг интервала\t")
f.write(str(h_SN))
f.write("\n\n")
f.write("Среднее значение на i-м интервале\n")
f.write("H =")
for j in range(0,num_int):
    f.write("\t %.3f" % (SN_int_ave[j]))
f.write("\n\n")
f.write("Среднее значение H = ")
f.write("\t %.3f" %(SN_ave))
f.write("\n\n")
f.write("Среднеквадратичное отклонение S =")
f.write("\t %.5f" % (SKO_SN))
f.write("\n\n")
f.write("Теоретические вероятности попадания в каждый из i интервал\n")
f.write("p =")
for j in range(0,num_int):
    f.write("\t %.3f" % (prob_SN[j]*100))
f.write("\n\n")
f.write("Критерий Пирсона hi =\t")
f.write("\t %.2f" %(pirs_2_SN))
f.write("\n\n")
f.write("При уровне значимости  0.05 , при заданном f = 12 – 3 = 9 (число степеней свободы)\n \
 табличное значение критерия Пирсона: 16.9. Распределение является нормальным.")


f = open("stat_and_prob_GZ.txt","w")
f.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ГАЗОРАЗРЯДНЫЙ СЧЕТЧИК ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
f.write("\n")
f.write("Разбиваем диапазон измеренных значений на 12.\n")
f.write("Количество измерений для каждого интервала")
for j in range(0,num_int):
    f.write(str(num_GZ[j]))
f.write("\n\n")
f.write("Шаг интервала\t")
f.write(str(h_GZ))
f.write("\n\n")
f.write("Среднее значение на i-м интервале\n")
f.write("H =")
for j in range(0,num_int):
    f.write("\t %.3f" % (GZ_int_ave[j]))
f.write("\n\n")
f.write("Среднее значение H = ")
f.write("\t %.3f" %(GZ_ave))
f.write("\n\n")
f.write("Среднеквадратичное отклонение S =")
f.write("\t %.5f" % (SKO_GZ))
f.write("\n\n")
f.write("Теоретические вероятности попадания в каждый из i интервал\n")
f.write("p =")
for j in range(0,num_int):
    f.write("\t %.3f" % (prob_GZ[j]*100))
f.write("\n\n")
f.write("Критерий Пирсона hi =\t")
f.write("\t %.2f" %(pirs_2_GZ))
f.write("\n\n")
f.write("При уровне значимости  0.05 , при заданном f = 12 – 3 = 9 (число степеней свободы)\n \
 табличное значение критерия Пирсона: 16.9. Распределение не является нормальным.")

x = np.linspace(1,12,12)

fig_1 = plt.figure()
plt.bar(x,prob_SN)
plt.title('Сцинтиляционный счетчик')
plt.grid(True)
plt.savefig("pic/Сцинт_сч",fnt='png')

fig_2 = plt.figure()
plt.bar(x,prob_GZ)
plt.title('Газоразрядный счетчик')
plt.grid(True)
plt.savefig("pic/Газоразр_сч",fnt='png')

axes = plt.gca()
axes.set_xlim([0,13])
axes.set_ylim([0,0.25])
plt.ylabel(r"$H,мкзВ/ч$")
plt.xlabel(r"$интервал$")
plt.tight_layout()
plt.show()
f.close()