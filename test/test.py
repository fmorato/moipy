import unittest
from moipy.moip import Moip
import random

class MoipTestCase(unittest.TestCase):

    def setUp(self):
        self.moip = Moip('Razao do Pagamento')
        self.moip.set_credenciais(token='PUMLYQSCI0JNCFGQQWGGKJNMG4QRX5DH',key='PHMLUTXWEJ0D5VJZDBFUFZYPZ4IWIC2AGUWMVRWE')
        self.moip.set_ambiente('sandbox')


    def test_set_pagador(self):

        self.moip.set_checkout_transparente()
        self.moip.set_valor('12345')
        self.moip.set_data_vencimento('yyyy-mm-dd')
        self.moip.set_id_proprio(str(random.randrange(500000)))

        endereco = dict(Logradouro='Rua santa ceia',Numero='222',Bairro='Buritis',Cidade='Belo Horizonte',Estado='MG',CEP='30850170',TelefoneFixo='3125124444')

        self.moip.set_pagador(Nome='Victor',Email='vitalbh@gmail.com',Apelido='vitalbh',IdPagador='1',EnderecoCobranca=endereco)

        self.moip.envia()

        resposta = self.moip.get_resposta()

        self.assertEqual(resposta['sucesso'],'Sucesso')
        self.assertIsInstance(resposta['token'],str)



    if __name__ == '__main__':
        unittest.main()