import sqlite3 # interface python pra base de dados sqlite3

def run_sql(sql: str): # função que tem como argumento uma string c um comando sql
    # analogia: create_users do fastapi é o garçom recebe o pedido (requisição), anota o que o cliente quer (dados do body) e leva o pedido pra cozinha
    # run_sql do sqlite3 recebe a comanda do garçom e faz a requisição na cozinha (banco de dados)
    con = sqlite3.connect("users.db")
    # conecta com o arquivo users.db, que, se não existir, o sqlite vai criar
    cur = con.cursor()
    # cursor permite executar comando na base de dados users.db (conectada através do con)
    res = cur.execute(sql)
    # envia a string passada na função e envia pra base de dados pra ser executada
    data = res.fetchall()
    # recolhe os resultados armazenados em res
    con.commit()
    # salva as alterações feitas no banco de dados
    return data
