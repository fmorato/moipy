MoIPy
=====

Camada de abstração para integração via API com o MoIP em Python.

 - Author: Hebert Amaral
 - Contributor: Ale Borba
 - Contributor: Igor Hercowitz
 - Contributor: Victor Hugo
 - Contributor: Felipe Gubert Cruz
 - Contributor: Felipe Morato

 - Version: v0.4.1

Dependências
------------

O MoIPy tem as seguintes dependências:

 - lxml
 - requests

Instalação
----------

Pelo repositório do Github:

    git clone git://github.com/fmorato/moipy.git
    cd moipy
    python moipy/moip.py # executa os testes
    python setup.py build
    sudo python setup.py install

Uso
----

Basta importar a classe do MoIP e sair brincando :-)

    from moipy import Moip

    moip = Moip('Razao do Pagamento')

    moip.set_credenciais(token='seu_token',key='sua_key')
    moip.set_ambiente('sandbox')
    moip.set_valor('12345')
    moip.set_data_vencimento('yyyy-mm-dd')
    moip.set_id_proprio('abc123')
    moip.envia()

    print(moip.get_resposta()) # {sucesso:'Sucesso','token':'KJHSDASKD392847293AHFJKDSAH'}


Para checkout transparente basta chamar:

     self.moip.set_checkout_transparente()

neste caso é obrigatorio passar os dados do pagador:

     endereco = dict(Logradouro='Rua xxxxx',Numero='222',Bairro='xxxx',Cidade='xxxx',Estado='xx',CEP='xxxxxx',TelefoneFixo='xxxxxxxxxx')
     self.moip.set_pagador(Nome='xxxx',Email='xxxxxx',Apelido='vitalbh',IdPagador='x',EnderecoCobranca=endereco)


ChangeLog
----------

v0.4.1
 - Troca do httplib para requests
 - Suporte para python3

v0.4
 - Troca do pyCurl por httplib
 - Melhorias no código/documentação
 - Adiciona arquivo de teste na raiz do projeto.

v0.3
 - Suporte a checkout transparente
 - Adição dos dados do Pagador
 - Teste do envio de intrução para checkout transparente

v0.2
 - Refatorações de código
 - Retirada dos DocTests

v0.1
 - First version

ToDo
------

 - Aplicar testes automatizados usando unittest
 - Validar campos


Licença
------

MoIPy Copyright (C) 2010 Herberth Amaral

This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
