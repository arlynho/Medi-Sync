import mysql.connector

# Mega trashy code - Wellcome to Hell
class BDConection:
    # Conectar ao banco de dados
    def conectar_bd():
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456789",
                database="clinica",
                port=3306
            )
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            return None, f"Erro ao conectar ao banco de dados: {err}"

class BDHandler:
    # Função para adicionar um novo paciente
    def adicionar_paciente(entry_nome, entry_data_nascimento, entry_tel, entry_email, entry_cpf):
        nome = entry_nome
        data_nascimento = entry_data_nascimento
        telefone = entry_tel
        email = entry_email
        cpf = entry_cpf

        print("Adicionando paciente:", nome, data_nascimento, telefone, email, cpf)  # Debug info

        conexao = BDConection.conectar_bd()
        if conexao is None:
            return False

        try:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO pacientes (nome, data_nascimento, telefone, email, cpf) VALUES (%s, %s, %s, %s, %s)",
                        (nome, data_nascimento, telefone, email, cpf))
            conexao.commit()
            return True, "Paciente adicionado com sucesso!"
        except mysql.connector.Error as err:
            print(f"Erro ao adicionar paciente: {err}")  # Imprime o erro
            return False, f"Erro ao adicionar paciente: {err}"
        finally:
            conexao.close()

    # Função para adicionar um novo médico       
    def adicionar_medico(entry_nome, entry_email, entry_tel, entry_crm, entry_data_nascimento, entry_cpf):
        nome = entry_nome
        email = entry_email
        telefone = entry_tel
        crm = entry_crm
        data_nascimento = entry_data_nascimento
        cpf = entry_cpf

        print("Adicionando medico:", nome, email, telefone, crm, data_nascimento, cpf)  # Debug info

        conexao = BDConection.conectar_bd()
        if conexao is None:
            return False, "Deu ruim"

        try:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO medicos (nome, email, tel, crm, d_nasc, cpf) VALUES (%s, %s, %s, %s, %s, %s)",
                        (nome, email, telefone, crm, data_nascimento, cpf))
            conexao.commit()
            return True, "Medico adicionado com sucesso!"
        except mysql.connector.Error as err:
            print(f"Erro ao adicionar medico: {err}")  # Imprime o erro
            return False, f"Erro ao adicionar medico: {err}"
        finally:
            conexao.close()

    # Função para agendar uma nova consulta
    def agendar_consulta(entry_paciente_id, entry_medico_id, entry_data, entry_horario, entry_descricao, entry_val):
        paciente_id = entry_paciente_id
        medico_id = entry_medico_id
        data = entry_data
        horario = entry_horario
        descricao = entry_descricao
        valor = entry_val

        print("Tentando adicionando nova consulta")  # Debug info

        conexao = BDConection.conectar_bd()
        if conexao is None:
            return False

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(horario) FROM consultas WHERE (horario = %s AND data = %s AND medico_id = %s)", 
                        (horario, data, medico_id))
            timeCheck = cursor.fetchone()[0]
            if (timeCheck > 0):
                return False, "Este horario já esta agendado!"
            else:
                cursor.execute("INSERT INTO consultas (paciente_id, medico_id, data, horario, descricao, val_cons) VALUES (%s, %s, %s, %s, %s, %s)",
                            (paciente_id, medico_id, data, horario, descricao, valor))
                conexao.commit()
                return True, "Consulta agendada com sucesso!"
        except mysql.connector.Error as err:
            print(f"Erro ao agendar consulta: {err}")  # Imprime o erro
            return None, f"Erro ao agendar consulta: {err}"
        finally:
            conexao.close()

    # Função para visualizar a lista de pacientes
    def visualizar_pacientes():
        conexao = BDConection.conectar_bd()
        if conexao is None:
            return False

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone, cpf, data_nascimento FROM pacientes")
            pacientes = cursor.fetchall()
            return pacientes
        except mysql.connector.Error as err:
            print(f"Erro ao buscar pacientes: {err}")
            return False,  f"Erro ao buscar pacientes: {err}"
        finally:
            conexao.close()

    # Função para visualizar a lista de medicos
    def visualizar_medicos():
        conexao = BDConection.conectar_bd()
        if conexao is None:
            return False

        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, tel, crm, d_nasc, cpf FROM medicos")
            medicos = cursor.fetchall()
            return medicos
        except mysql.connector.Error as err:
            print(f"Erro ao buscar ,edicos: {err}")
            return None, f"Erro ao buscar medicos: {err}"
        finally:
            conexao.close()
            
    # Função para visualizar a agenda de consultas
    def visualizar_agenda():
        conexao = BDConection.conectar_bd()
        if conexao is None:
            return False

        try:
            cursor = conexao.cursor()
            cursor.execute(""" 
                SELECT consultas.id, medicos.nome AS medico, pacientes.nome AS paciente, consultas.val_cons, consultas.descricao, consultas.data, consultas.horario
                FROM consultas 
                JOIN pacientes ON consultas.paciente_id = pacientes.id 
                JOIN medicos ON consultas.medico_id = medicos.id
                ORDER BY consultas.data ASC, consultas.horario ASC;
            """)
            consultas = cursor.fetchall()
            return consultas
        except mysql.connector.Error as err:
            print(f"Erro ao buscar agenda: {err}")
            return None, f"Erro ao buscar agenda: {err}"
        finally:
            conexao.close()

class BDDataRemovers:
    #Função de remoção de linhas na tabela pacientes
    def removedor_pacientes(aux, checkOpc):
        conexao = BDConection.conectar_bd()
        
        if conexao is None:
            return False
        
        try:
            cursor = conexao.cursor()
            if (checkOpc):
                cursor.execute("DELETE FROM pacientes WHERE id = %s", (aux,))
                conexao.commit()
                print(f"Dados deletados! ID = {aux}")
                return True, "Dados deletados com exito!"
            else:
                print("Deleção cancelada pelo usuario")
        except mysql.connector.Error as err:
            print(f"Erro ao deletar paciente: {err}")
            return False, f"Erro ao deletar paciente: {err}"
        finally:
            cursor.close()

    #Função de remoção de linhas na tabela medicos
    def removedor_medicos(aux, checkOpc):
        conexao = BDConection.conectar_bd()
        
        if conexao is None:
            return False
        
        try:
            cursor = conexao.cursor()
            if (checkOpc):
                cursor.execute("DELETE FROM medicos WHERE id = %s", (aux,))
                conexao.commit()
                print(f"Dados deletados! ID = {aux}")
                return True, "Dados deletados com exito!"
            else:
                print("Deleção cancelada pelo usuario")
        except mysql.connector.Error as err:
            print(f"Erro ao deletar medico: {err}")
            return False, f"Erro ao deletar o funcionario: {err}"
        finally:
            cursor.close()
            
    #Função de remoção de linhas na tabela consultas
    def removedor_consultas(aux, checkOpc):
        conexao = BDConection.conectar_bd()
        
        if conexao is None:
            return False
        
        try:
            cursor = conexao.cursor()
            if (checkOpc):
                cursor.execute("DELETE FROM consultas WHERE id = %s", (aux,))
                conexao.commit()
                print(f"Dados deletados! ID = {aux}")
                return True, "Dados deletados com exito!"
            else:
                print("Deleção cancelada pelo usuario")
        except mysql.connector.Error as err:
            print(f"Erro ao deletar consulta: {err}")
            return False, f"Erro ao deletar consulta: {err}"
        finally:
            cursor.close()
    

