import re
import json
import os
from getpass import getpass

import oracledb   


# -------------------------
# CONFIGURAÇÃO ORACLE
# -------------------------
ORACLE_CONFIG = {
    "user": "**",
    "password": "***",
    "dsn": "oracle.fiap.com.br:1521/ORCL"
}

USE_ORACLE = True  


# -------------------------
# Conexão Oracle
# -------------------------
def conectar():
    try:
        conn = oracledb.connect(
            user=ORACLE_CONFIG['user'],
            password=ORACLE_CONFIG['password'],
            dsn=ORACLE_CONFIG['dsn']
        )
        return conn
    except Exception as e:
        print("Erro ao conectar Oracle:", e)
        return None



# ========================
# FUNÇÕES DE SUPORTE
# ========================
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPressione ENTER para continuar...")


def cabecalho(titulo):
    limpar_tela()
    print(f"\n{'=' * 10} {titulo} {'=' * 10}\n")



# -------------------------
# Validações
# -------------------------
def validar_idade(valor):
    try:
        idade = int(valor)
        if idade <= 0 or idade > 120:
            print("Idade fora do intervalo permitido.")
            return None
        return idade
    except:
        print("Digite um número válido.")
        return None


def validar_sim_nao(valor):
    v = valor.lower().strip()
    if v in ("sim", "s", "1"):
        return "sim"
    if v in ("nao", "não", "n", "0"):
        return "não"
    print("Digite 'sim' ou 'não'.")
    return None


def validar_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(regex, email.strip()):
        return email.strip()
    print("E-mail inválido.")
    return None


def validar_telefone(tel):
    só_digitos = re.sub(r'\D', '', tel)
    if 8 <= len(só_digitos) <= 13:
        return só_digitos
    print("Telefone inválido.")
    return None


def validar_cpf(cpf):
    """
    Corrigido: retorna o CPF (string) se válido (11 dígitos numéricos),
    ou None se inválido. Isso garante que o CPF real seja salvo
    em vez de True/False.
    """
    if cpf is None:
        return None
    cpf_str = str(cpf).strip()
    if cpf_str.isdigit() and len(cpf_str) == 11:
        return cpf_str
    print("CPF inválido. Digite exatamente 11 dígitos numéricos.")
    return None



# -------------------------
# CRUD 
# -------------------------
def cadastrar_aluno():
    conn = conectar()
    cabecalho("Cadastrar Aluno")

    if conn is None:
        return

    try:
        nome = input("Nome completo: ").strip()
        if not nome:
            print("Nome é obrigatório.")
            return

        idade = None
        while idade is None:
            idade = validar_idade(input("Idade: "))

        cpf = None
        while cpf is None:
            cpf = validar_cpf(input("CPF (11 dígitos): "))

        email = None
        while email is None:
            email = validar_email(input("E-mail: "))

        telefone = None
        while telefone is None:
            telefone = validar_telefone(input("Telefone: "))

        bairro = input("Bairro: ")

        acesso = None
        while acesso is None:
            acesso = validar_sim_nao(input("Acesso à internet? (sim/não): "))

        dispositivo = input("Dispositivo principal (): ")
        trilha = input("Trilha atual (python, IA, java, frontend, dados): ")
        parceiro = input("Parceiro indicado (opcional): ")

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO alunotech 
            (nome, idade, cpf, email, telefone, bairro, acesso_internet, dispositivo, trilha_atual, parceiro_indicado)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
        """, (nome, idade, cpf, email, telefone, bairro, acesso, dispositivo, trilha, parceiro))

        conn.commit()
        print("Aluno cadastrado com sucesso.")

    except Exception as e:
        print("Erro ao cadastrar aluno:", e)
    finally:
        conn.close()

def formatar_tabela(dados, colunas):
    # Calcula tamanho máximo por coluna
    larguras = []
    for i in range(len(colunas)):
        maior = len(colunas[i])
        for linha in dados:
            tamanho = len(str(linha[i])) if linha[i] is not None else 0
            if tamanho > maior:
                maior = tamanho
        larguras.append(maior + 2)

    # Linha separadora
    separador = "+" + "+".join("-" * w for w in larguras) + "+"

    # Cabeçalho
    header = "|" + "|".join(colunas[i].center(larguras[i]) for i in range(len(colunas))) + "|"

    print(separador)
    print(header)
    print(separador)

    # Linhas
    for linha in dados:
        print("|" + "|".join(str(linha[i]).center(larguras[i]) for i in range(len(colunas))) + "|")

    print(separador)


def listar_alunos():
    conn = conectar()
    cabecalho("Lista de Alunos")

    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_aluno, nome, idade, cpf, email, telefone, bairro, 
                   acesso_internet, dispositivo, trilha_atual, parceiro_indicado
            FROM alunotech
        """)

        rows = cur.fetchall()

        if not rows:
            print("Nenhum aluno cadastrado.")
            return

        colunas = [
            "ID", "Nome", "Idade", "CPF", "Email", "Telefone",
            "Bairro", "Internet", "Dispositivo", "Trilha", "Parceiro"
        ]

        formatar_tabela(rows, colunas)

    except Exception as e:
        print("Erro ao listar alunos:", e)
    finally:
        conn.close()



def consultar_aluno_por_id():
    cabecalho("Consultar por ID")
    conn = conectar()

    if conn is None:
        return

    try:
        idp = input("ID do aluno: ")
        if not idp.isdigit():
            print("ID inválido.")
            return

        cur = conn.cursor()
        cur.execute("""
            SELECT id_aluno, nome, idade, cpf, email, telefone, bairro, 
                   acesso_internet, dispositivo, trilha_atual, parceiro_indicado
            FROM alunotech
            WHERE id_aluno = :1
        """, (int(idp),))

        row = cur.fetchone()

        if not row:
            print("Aluno não encontrado.")
            return

        colunas = [
            "ID", "Nome", "Idade", "CPF", "Email", "Telefone",
            "Bairro", "Internet", "Dispositivo", "Trilha", "Parceiro"
        ]

        formatar_tabela([row], colunas)

    except Exception as e:
        print("Erro na consulta:", e)
    finally:
        conn.close()




def atualizar_aluno():
    conn = conectar()
    cabecalho("Atualizar Aluno")

    if conn is None:
        return

    try:
        idp = input("ID do aluno: ")
        if not idp.isdigit():
            print("ID inválido.")
            return

        idp = int(idp)

        cur = conn.cursor()
        cur.execute("SELECT * FROM alunotech WHERE id_aluno = :1", (idp,))
        row = cur.fetchone()

        if not row:
            print("Aluno não encontrado.")
            return

        print("Deixe vazio para manter o valor atual.\n")

        nome = input(f"Nome [{row[1]}]: ") or row[1]
        idade = input(f"Idade [{row[2]}]: ") or row[2]
        cpf = input(f"CPF [{row[3]}]: ") or row[3]
        email = input(f"E-mail [{row[4]}]: ") or row[4]
        telefone = input(f"Telefone [{row[5]}]: ") or row[5]
        bairro = input(f"Bairro [{row[6]}]: ") or row[6]
        acesso = input(f"Acesso internet [{row[7]}]: ") or row[7]
        dispositivo = input(f"Dispositivo [{row[8]}]: ") or row[8]
        trilha = input(f"Trilha [{row[9]}]: ") or row[9]
        parceiro = input(f"Parceiro [{row[10]}]: ") or row[10]

        cur.execute("""
            UPDATE alunotech SET
                nome = :1, idade = :2, cpf = :3, email = :4,
                telefone = :5, bairro = :6, acesso_internet = :7,
                dispositivo = :8, trilha_atual = :9, parceiro_indicado = :10
            WHERE id_aluno = :11
        """, (nome, idade, cpf, email, telefone, bairro, acesso, dispositivo, trilha, parceiro, idp))

        conn.commit()
        print("Aluno atualizado com sucesso.")

    except Exception as e:
        print("Erro ao atualizar:", e)
    finally:
        conn.close()



def excluir_aluno():
    cabecalho("Excluir Aluno")
    conn = conectar()

    if conn is None:
        return

    try:
        idp = input("ID do aluno: ")
        if not idp.isdigit():
            print("ID inválido.")
            return

        cur = conn.cursor()
        cur.execute("DELETE FROM alunotech WHERE id_aluno = :1", (int(idp),))
        conn.commit()

        print("Aluno excluído.")

    except Exception as e:
        print("Erro ao excluir:", e)
    finally:
        conn.close()



# -------------------------
# CONSULTAS (OBRIGATÓRIAS)
# -------------------------
def consulta_alunos_sem_internet(): 
    cabecalho("Alunos sem Internet")
    conn = conectar()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("SELECT nome, bairro FROM alunotech WHERE acesso_internet = 'não'")
        rows = cur.fetchall()

        if not rows:
            print("Nenhum aluno sem internet encontrado.")
            return []

        colunas = ["Nome", "Bairro"]
        formatar_tabela(rows, colunas)

        # Retorna em formato estruturado para exportação JSON
        resultado = [{"nome": r[0], "bairro": r[1]} for r in rows]
        return resultado

    except Exception as e:
        print("Erro:", e)
        return []
    finally:
        conn.close()



def consulta_alunos_por_bairro():
    cabecalho("Alunos por Bairro")
    conn = conectar()

    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute("SELECT bairro, COUNT(*) FROM alunotech GROUP BY bairro")
        rows = cur.fetchall()

        if not rows:
            print("Nenhum dado encontrado.")
            return []

        colunas = ["Bairro", "Total"]
        formatar_tabela(rows, colunas)

        # Retorno estruturado para exportação JSON
        resultado = [{"bairro": r[0], "total": r[1]} for r in rows]
        return resultado

    except Exception as e:
        print("Erro:", e)
        return []
    finally:
        conn.close()



def consulta_por_faixa_idade():
    cabecalho("Faixa Etária")
    conn = conectar()

    try:
        cur = conn.cursor()
        cur.execute("SELECT idade FROM alunotech WHERE idade IS NOT NULL")
        rows = cur.fetchall()

        if not rows:
            print("Nenhum dado de idade encontrado.")
            return

        total = len(rows)

        faixas = {"<18": 0, "18-24": 0, "25-34": 0, "35+": 0}

        for r in rows:
            idade = r[0]
            if idade < 18:
                faixas["<18"] += 1
            elif 18 <= idade <= 24:
                faixas["18-24"] += 1
            elif 25 <= idade <= 34:
                faixas["25-34"] += 1
            else:
                faixas["35+"] += 1

        # Calcula porcentagem
        p_menor18 = (faixas["<18"] / total) * 100
        p_18_24 = (faixas["18-24"] / total) * 100
        p_25_34 = (faixas["25-34"] / total) * 100
        p_35mais = (faixas["35+"] / total) * 100

        # Imprime tudo em UMA única linha
        print(
            f"<18: {p_menor18:.1f}% | "
            f"18-24: {p_18_24:.1f}% | "
            f"25-34: {p_25_34:.1f}% | "
            f"35+: {p_35mais:.1f}%"
        )

    except Exception as e:
        print("Erro:", e)
    finally:
        conn.close()



# -------------------------
# EXPORTAÇÃO JSON
# -------------------------

def exportar_json_completo():
    conn = conectar()
    if conn is None:
        print("Erro ao conectar ao banco para exportar.")
        return

    try:
        cur = conn.cursor()

        # 1. Buscar todos os alunos
        cur.execute("""
            SELECT id_aluno, nome, idade, cpf, email, telefone, bairro, 
                   acesso_internet, dispositivo, trilha_atual, parceiro_indicado
            FROM alunotech
        """)
        alunos_rows = cur.fetchall()

        alunos = []
        for r in alunos_rows:
            alunos.append({
                "id": r[0],
                "nome": r[1],
                "idade": r[2],
                "cpf": r[3],
                "email": r[4],
                "telefone": r[5],
                "bairro": r[6],
                "acesso_internet": r[7],
                "dispositivo": r[8],
                "trilha_atual": r[9],
                "parceiro_indicado": r[10]
            })

        # 2. Consultas obrigatórias
        # ------------------------

        # Alunos sem internet
        cur.execute("SELECT nome, bairro FROM alunotech WHERE acesso_internet = 'não'")
        sem_internet_rows = cur.fetchall()
        sem_internet = [{"nome": r[0], "bairro": r[1]} for r in sem_internet_rows]

        # Quantidade por bairro
        cur.execute("SELECT bairro, COUNT(*) FROM alunotech GROUP BY bairro")
        bairro_rows = cur.fetchall()
        por_bairro = [{"bairro": r[0], "total": r[1]} for r in bairro_rows]

        # Faixa etária
        cur.execute("SELECT idade FROM alunotech WHERE idade IS NOT NULL")
        idade_rows = cur.fetchall()
        faixas = {"<18": 0, "18-24": 0, "25-34": 0, "35+": 0}

        for r in idade_rows:
            idade = r[0]
            if idade < 18:
                faixas["<18"] += 1
            elif 18 <= idade <= 24:
                faixas["18-24"] += 1
            elif 25 <= idade <= 34:
                faixas["25-34"] += 1
            else:
                faixas["35+"] += 1

        
        # ----------------------------
        dados_exportacao = {
            "alunos": alunos,
            "consultas": {
                "alunos_sem_internet": sem_internet,
                "quantidade_por_bairro": por_bairro,
                "faixa_etaria": faixas
            }
        }

        # Gravar em arquivo único
        with open("tech_de_bairro_export.json", "w", encoding="utf-8") as f:
            json.dump(dados_exportacao, f, indent=2, ensure_ascii=False)

        print("\nArquivo gerado: tech_de_bairro_export.json")

    except Exception as e:
        print("Erro ao exportar JSON completo:", e)

    finally:
        conn.close()



#--------------------------
#Trilha
#--------------------------
def obter_trilha_do_aluno(id_aluno):
    conn = conectar()
    if conn is None:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT trilha_atual 
            FROM alunotech 
            WHERE id_aluno = :1
        """, (id_aluno,))
        
        row = cur.fetchone()
        return row[0] if row else None

    except Exception as e:
        print("Erro ao buscar trilha:", e)
        return None
    finally:
        conn.close()



def mostrar_ebook(trilha):
    cabecalho("E-book da Trilha")
    if trilha is None:
        print("Trilha inválida.")
        return

    t = trilha.lower()
    if t == "python":
        print("E-book: Lógica de Programação em Python – Nível 1")
    elif t == "ia":
        print("E-book: Fundamentos de IA generativa, LLMs, Chatbots")    
    elif t == "java":
        print("E-book: Fundamentos Java, Orientação a objetos, Frameworks collections, Conexão Bd")
    elif t == "frontend":
        print("E-book: Fundamentos de HTML, CSS e JS")
    elif t == "dados":
        print("E-book: Introdução a Data Analytics")  
    else:
        print("Trilha sem e-book configurado.")


def mostrar_desafios(trilha):
    cabecalho("Desafios Mensais")
    if trilha is None:
        print("Trilha inválida.")
        return

    t = trilha.lower()
    if t == "python":
        print("Desafio: Criar um CRUD completo em Python.")
    elif t == "ia":
        print("Desafio: criar um agente de IA")    
    elif t == "java":
        print("Desafio: Fazer uma conexão ao bancos de dados")
    elif t == "frontend":
        print("Desafio: Criar uma landing page responsiva.")
    elif t == "dados":
        print("Desafio: Dashboard com análise de dataset.")
    else:
        print("Trilha sem desafios configurados.")


def mostrar_equipamentos(trilha):
    cabecalho("Equipamentos Recomendados")
    if trilha is None:
        print("Trilha inválida.")
        return

    t = trilha.lower()
    if t == "python":
        print("Recomendado: Notebook dual-core, 8GB RAM.")
    elif t == "frontend":
        print("Recomendado: Monitor secundário e 8GB RAM.")
    elif t == "dados":
        print("Recomendado: 16GB RAM + SSD para datasets.")
    elif t == "java":
        print("Recomendado: 8GB RAM e JDK instalado.")
    elif t == "ia":
        print("Recomendado: GPU opcional, 16GB RAM.")
    else:
        print("Trilha sem recomendações.")




    



# -------------------------
# MENUS
# -------------------------
def menu_trilha_ebook():
    cabecalho("Trilha do mês")

    try:
        id_aluno = input("Digite seu ID para carregar sua trilha: ")

        if not id_aluno.isdigit():
            print("ID inválido.")
            pausar()
            return

        trilha = obter_trilha_do_aluno(int(id_aluno))

        if not trilha:
            print("Nenhuma trilha encontrada para esse aluno.")
            pausar()
            return

        print(f"\nTrilha atual detectada: {trilha}\n")

        while True:
            print("1. E-book do mês")
            print("2. Desafios mensais")
            print("3. Equipamentos tech recomendados")
            print("4. Voltar")
            op = input("Escolha: ")

            if op == "1":
                mostrar_ebook(trilha)
            elif op == "2":
                mostrar_desafios(trilha)
            elif op == "3":
                mostrar_equipamentos(trilha)
            elif op == "4":
                break
            else:
                print("Opção inválida.")
            pausar()

    except Exception as e:
        print("Erro:", e)




def menu_crud():
    while True:
        cabecalho("Menu ")
        print("1. Cadastrar aluno")
        print("2. Listar alunos")
        print("3. Consultar por ID")
        print("4. Atualizar aluno")
        print("5. Excluir aluno")
        print("6. Voltar")
        op = input("Escolha: ")

        if op == "1":
            cadastrar_aluno()
        elif op == "2":
            listar_alunos()
        elif op == "3":
            consultar_aluno_por_id()
        elif op == "4":
            atualizar_aluno()
        elif op == "5":
            excluir_aluno()
        elif op == "6":
            break
        else:
            print("Opção inválida.")
        pausar()



def menu_consultas():
    while True:
        cabecalho("Consultas")
        print("1. Alunos sem internet")
        print("2. Quantidade por bairro")
        print("3. Faixa etária")
        print("4. Voltar")
        op = input("Escolha: ")

        if op == "1":
            exportar = consulta_alunos_sem_internet()
          
                

        elif op == "2":
            exportar = consulta_alunos_por_bairro()
            
              

        elif op == "3":
            exportar = consulta_por_faixa_idade()
               
                

        elif op == "4":
            break
        else:
            print("Opção inválida.")

        pausar()



def menu_principal():
    while True:
        cabecalho("TECH DE BAIRRO")
        print("1. cadastro de alunos")
        print("2. Trilha")
        print("3. Consultas")
        print("4. Exportar todas as consultas")
        print("5. Sair")
        op = input("Escolha: ")

      

        if op == "1":
            menu_crud()
        elif op == "2":
            menu_trilha_ebook()    
        elif op == "3":
            menu_consultas()
        elif op == "4":
            exportar_json_completo()
            pausar()
        elif op == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
            pausar()



# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    menu_principal()
