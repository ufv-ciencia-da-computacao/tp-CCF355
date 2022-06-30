# Projeto de Álbum de Figurinhas
Projeto desenvolvido para sistemas distribuídos e paralelos

## Instalando dependências
Inicialmente algumas dependências devem ser instaladas para a executação correta do sistema

```
pip install -r requirements.txt
```

## Criando o banco de dados
Em seguida o banco de dados deve ser criado através do comando a seguir

```
python3 create_db.py
```

## Executando o processo servidor
Um único processo servidor deve ser executado para a utilização do sistema

```
python3 server.py
```

## Executando processos clientes
Múltiplos processos clientes podem ser executados 

```
python3 client.py
```