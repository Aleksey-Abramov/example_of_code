# -*- coding: utf-8 -*-
"""
ANes20xe: Это общий модуль для настройки параметров графики

KBM 14.03.2019:   Создан
VIA 14.03.2019:   Добавил функцию init_matplotlib    

"""
#-------------------------------------------
# Шаблон для документа СТАТЬЯ
#-------------------------------------------

def init_matplotlib(name, IsReport = True):
  if IsReport:
     init_matplotlib_report(name)
  else:     
     init_matplotlib_article(name)
     

def init_matplotlib_article(name):
    import matplotlib.font_manager as font_manager
    import locale
    
    name.rcParams.update(name.rcParamsDefault)
    name.style.use('classic')
    prop = font_manager.FontProperties(fname='c:\\windows\\fonts\\times.ttf')
    name.rcParams['font.family'] = prop.get_name()
    name.rcParams['lines.linewidth'] = 1.5                         #     VIA , было 1
    name.rcParams["figure.figsize"] = (90.0/25.4,90.0/25.4) #mm to inch
    name.rcParams["figure.dpi"] = 1000
    name.rcParams["savefig.dpi"] = name.rcParams["figure.dpi"]
    name.rcParams["savefig.format"] = 'jpg'
    name.rcParams["font.size"] = 12
    name.rcParams["legend.fontsize"] = name.rcParams["font.size"]
    name.rcParams["axes.titlesize"] = name.rcParams["font.size"]
    name.rcParams["axes.labelsize"] = name.rcParams["font.size"]
    name.rcParams["xtick.labelsize"] = name.rcParams["font.size"]
    name.rcParams["ytick.labelsize"] = name.rcParams["font.size"]
    name.rcParams["legend.columnspacing"] = 0.0
    name.rcParams["markers.fillstyle"] = 'full' #full|left|right|bottom|top|none
    name.rcParams["lines.markersize"] = 5.0
    name.rcParams["axes.formatter.limits"] = (-7,7)
    name.rcParams["axes.formatter.use_locale"] = True
    #    locale.setlocale(locale.LC_NUMERIC, r"deu_Deu")
    #    name.rcParams["axes.formatter.use_locale"] = True   
    #   ======== Это для ANACONDA ==========================
    del font_manager.weight_dict['roman']
    font_manager._rebuild()
    # ======== Это для ANACONDA ==========================
    
#-------------------------------------------
# Шаблон для документа ОТЧЕТ
#-------------------------------------------
def init_matplotlib_report(name):
    import matplotlib.font_manager as font_manager

#    name.rcParams.update(plt.rcParamsDefault)
    name.rcParams.update(name.rcParamsDefault)

    name.style.use('classic')
    prop = font_manager.FontProperties(fname='c:\\windows\\fonts\\times.ttf')
    name.rcParams['font.family'] = prop.get_name()
    name.rcParams['lines.linewidth'] = 2
    name.rcParams['lines.markersize'] = 6.0                 
    name.rcParams['markers.fillstyle'] = 'none'

    name.rcParams['lines.markeredgewidth'] = 1.5

    name.rcParams["figure.figsize"] = (150.0/25.4,150.0/25.4) #mm to inch
    name.rcParams["figure.dpi"] = 160
    name.rcParams["savefig.dpi"] = name.rcParams["figure.dpi"]
    name.rcParams["savefig.format"] = 'png'
    name.rcParams["font.size"] = 18
    name.rcParams["legend.fontsize"] = 14
    name.rcParams["axes.titlesize"] = name.rcParams["font.size"]
    name.rcParams["axes.labelsize"] = name.rcParams["font.size"]
    name.rcParams["xtick.labelsize"] = name.rcParams["font.size"]
    name.rcParams["ytick.labelsize"] = name.rcParams["font.size"]
    name.rcParams["legend.columnspacing"] = 0.0
#    name.rcParams["axes.formatter.limits"] = (-2,2) #use scientific notation if log10 of the axis range is smaller than the first or larger than the second
#    locale.setlocale(locale.LC_NUMERIC, r"deu_Deu")
#    name.rcParams["axes.formatter.use_locale"] = True   
#   ======== Это для ANACONDA ==========================
    del font_manager.weight_dict['roman']
    font_manager._rebuild()
# ======== Это для ANACONDA ==========================

