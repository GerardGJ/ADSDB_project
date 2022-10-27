from tkinter import *
from TrustedAtp_V2 import trustedATP_V2
from TrustedBet_V1 import trustedBet_V1
from TrustedBet_V2 import trustedBet_V2
from TrustedAtp_V1 import trustedAtp_V1
from Exploitation import exploitation
from TrustedAtp_V3 import trustedAtp_V3
from Formated_Zone import formated


def main():

    #First execute the formated zone

    formated()
    label = Label(window, text= "Data inserted to the formated Zone")
    label.pack()

    #Second will do all the Trusted zone regarding the ATP data
    
    trustedAtp_V1()
    trustedATP_V2()
    trustedAtp_V3()
    label = Label(window, text= "Finished Trusted Zone regarding ATP data")
    label.pack()

    #Then we execute the trusted zone regarding the Bet data

    trustedBet_V1()
    trustedBet_V2()
    label = Label(window, text= "Finished Trusted Zone regarding Bet data")
    label.pack()

    #Finally will execute the exploitation zone:
    exploitation()
    label = Label(window, text= "Exploitation zone and Data Backbone finished and executed correctly ")
    label.pack()




if __name__ == '__main__':
    
    window=Tk()
    window.title('ADSDB Project')
    window.geometry("300x200+10+20")
    button = Button(window, text="Run Data Backbone", command=main) 
    button.pack()
    window.mainloop()
