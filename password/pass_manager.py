import pymysql.cursors 
import secrets
import string

def randomPass(size=20):
	letters = string.ascii_letters + string.digits
	return ''.join(secrets.choice(letters) for i in range(size))

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',#The MySQL password
                             db='db',#The database
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
sql = "SELECT `senha` FROM pass WHERE plataforma='manager'"
cursor.execute(sql)
result = cursor.fetchone()

enter = input("Digite a senha mestre: ")
if result["senha"] == enter:
	comand = ""
	while comand!="exit":
		comand = input("\nOperações:\nConsultar - para consultar uma senha existem\nInserir - para inserir uma nova senha\nAlterar- para alterar uma senha\nDeletar - para deletar uma plataforma\nExit - para sair do sistema\nDigite a operacao: ")
		if comand.lower()=="inserir":
			plat = ""
			while True:
				plat = input("Digite o nome da plataforma (exit para sair):")
				if plat.lower()=="exit":
					break
				sql = "SELECT `senha` FROM pass WHERE plataforma=%s"
				cursor.execute(sql,(plat.lower(),))
				result = cursor.fetchone()
				if result==None:
					senha = input("Digite a senha ou random - para um senha randomica: ")
					s = ""
					if senha.lower() == "random":
						s = randomPass()				
					else:
						s = senha
					p = plat.lower()
					sql = "INSERT INTO pass (plataforma,senha) VALUES(%s,%s)"
					cursor.execute(sql,(p,s))
					connection.commit()
				else:
					print("Plataforma ja cadastrada")
		elif comand.lower()=="consultar":
			plat = ""
			while True:
				plat = input("Digite o nome da plataforma (exit para sair): ")
				if plat.lower()=="exit":
					break
				sql = "SELECT `senha` FROM pass WHERE plataforma=%s"
				cursor.execute(sql,(plat.lower(),))
				result = cursor.fetchone()
				if result==None:
					print("\nPlataforma nao cadastrada\n")
				else:
					print("\nA senha para a plataforma "+plat.lower()+" é: "+result["senha"]+"\n")
		elif comand.lower()=="alterar":
			plat = ""
			while True:
				plat = input("Digite o nome da plataforma (exit para sair): ")
				if plat.lower()=="exit":
					break
				sql = "SELECT `senha` FROM pass WHERE plataforma=%s"
				cursor.execute(sql,(plat.lower(),))
				result = cursor.fetchone()
				if result==None:
					print("\nPlataforma nao cadastrada\n")
				else:
					new_senha = input("Digite a nova senha ou random - para um senha randomica: ")
					s = ""
					if new_senha.lower() == "random":
						s = randomPass()				
					else:
						s = new_senha
					sql = "UPDATE pass SET senha=%s WHERE plataforma=%s"
					cursor.execute(sql,(s,plat.lower()))
					connection.commit()
					print("\nSenha atualizada\n")
		elif comand.lower()=="deletar":
			plat = ""
			while True:
				plat = input("Digite o nome da plataforma (exit para sair): ")
				if plat.lower()=="exit":
					break
				sql = "SELECT `plataforma` FROM pass WHERE plataforma=%s"
				cursor.execute(sql,(plat.lower(),))
				result = cursor.fetchone()
				if result == None:
					print("\nPlataforma nao cadastrada\n")
				else:
					sql = "DELETE FROM pass WHERE plataforma=%s"
					cursor.execute(sql,(plat.lower(),))
					connection.commit()
					print("\nPlataforma deletada\n")
		elif comand.lower()!="exit":
			print("\nComando invalido\n")
else:
	print("Senha incorreta")
