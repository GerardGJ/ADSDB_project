from tkinter import *
from DataManagementBackbone.Persistent.Persistent_landing import persistent
from DataManagementBackbone.Trusted.ATP.TrustedAtp_V2 import trustedATP_V2
from DataManagementBackbone.Trusted.Bet.TrustedBet_V1 import trustedBet_V1
from DataManagementBackbone.Trusted.Bet.TrustedBet_V2 import trustedBet_V2
from DataManagementBackbone.Trusted.ATP.TrustedAtp_V1 import trustedAtp_V1
from DataManagementBackbone.Exploitation.Exploitation import exploitation
from DataManagementBackbone.Trusted.ATP.TrustedAtp_V3 import trustedAtp_V3
from DataManagementBackbone.Formated.Formated_Zone import formated
from DataAnalysisBackbone.AnalyticalSandbox.AnalyticalSandbox import analyticalSandbox
from DataAnalysisBackbone.FeatureGeneration.Feature_generation import fetaure_generation
from DataAnalysisBackbone.TrainingTest.TrainingTest_Insertion import trainingValidation
from subprocess import call
import os

def main():

    #Data Management Backbone
    ##Persistent Zone
    persistent()

    ##Formated zone

    formated()
    label = Label(window, text= "Data inserted to the formated Zone")
    label.pack()

    ##Trusted zone regarding the ATP data
    
    trustedAtp_V1()
    trustedATP_V2()
    trustedAtp_V3()
    label = Label(window, text= "Finished Trusted Zone regarding ATP data")
    label.pack()

    ##Trusted zone regarding the Bet data

    trustedBet_V1()
    trustedBet_V2()
    label = Label(window, text= "Finished Trusted Zone regarding Bet data")
    label.pack()

    ##Exploitation zone:
    exploitation()
    label = Label(window, text= "Exploitation zone and Data Backbone finished and executed correctly ")
    label.pack()

    #Data Analysis Backbone
    ##Analytical Sandbox
    analyticalSandbox()
    
    ##Feature Generation
    fetaure_generation()
    
    ##Fetaure Selection
    feature_selection = os.getcwd() + "\DataAnalysisBackbone\AdvancedTopic.R"
    call("Rscript %s" % (feature_selection), shell=True)
    
    ##Data Separation (Training and Validation)
    trainingValidation()
    
    #Model generation#
    
    

    
if __name__ == '__main__':
    
    window=Tk()
    window.title('ADSDB Project')
    window.geometry("300x200+10+20")
    button = Button(window, text="Execute project", command=main) 
    button.pack()
    window.mainloop()
