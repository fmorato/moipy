from moipy import Moip

moip = Moip('Razao do Pagamento')

moip.set_credenciais(token='seu_token',key='sua_key')
moip.set_ambiente('sandbox')
moip.set_valor('12345')
moip.set_data_vencimento('yyyy-mm-dd')
moip.set_id_proprio('abc1234')
moip.envia()

print moip.get_resposta()