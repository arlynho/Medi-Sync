from data import *

class Handler():
    def __init__(self):
        self.medicos = []
        self.medicos.append(Medico(1, "Kakaroto", "kakaroto@gmail.com", "19971366597", "4567989132", "10/5/2000", "456.789.123-01"))
        self.print()

    def carregarMedicos(): #retornar uma lista de médicos, nesse exemplo estamos retornando apenas um
        return Medico(1, "Kakaroto", "kakaroto@gmail.com", "19971366597", "4567989132", "10/5/2000", "456.789.123-01")
    
    def print(self):
        print(f"Nome: {self.medicos[0].nome}, Telefone: {self.medicos[0].telefone}, CRM: {self.medicos[0].crm}")

    def cadastrarMedico(self, nome, email, telefone, crm, nascimento, cpf):
        
        
Handler()