#! /usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import httplib
from lxml import etree


class Moip():

    def __init__(self, razao, xml_node="EnviarInstrucao"):

        if xml_node:
            self.xml_node = etree.Element(xml_node)

            self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(Razao=razao))

    def _monta_xml(self, parent, unique=False, **kwargs):
        """Metodo interno que monta o XML utilizando os parametros passados
        por outros metodos."""

        if isinstance(parent, etree._Element):
            node_parent = parent
        else:
            node_parent = etree.Element(parent)

        for k, v in kwargs.items():
            if unique and node_parent.find(k) is not None:
                node = node_parent.find(k)
            else:
                node = etree.SubElement(node_parent, k)

            if isinstance(v, dict):
                self._monta_xml(node, **v)
            else:
                node.text = v

        return node_parent

    def set_credenciais(self, token, key):
        """Define as credenciais utilizadas para autenticar a chamada aos webservices
        """

        self.token = token
        self.key = key

        return self

    def set_ambiente(self, ambiente):
        """Define se o ambiente é o de homologação (sandbox) ou de produção
        """

        if ambiente == "sandbox":
            self.host = 'desenvolvedor.moip.com.br'
            self.post_url = '/sandbox/ws/alpha/EnviarInstrucao/Unica'
            self.url = "https://desenvolvedor.moip.com.br/sandbox/ws/alpha/EnviarInstrucao/Unica"
        elif ambiente == "producao":
            self.host = 'www.moip.com.br'
            self.post_url = '/ws/alpha/EnviarInstrucao/Unica'
            self.url = "https://www.moip.com.br/ws/alpha/EnviarInstrucao/Unica"
        else:
            raise ValueError("Ambiente inválido")

    def set_valor(self, valor):
        """Define o valor a ser enviado
        """

        self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(Valores=dict(Valor=valor)))

        return self

    def set_id_proprio(self, id):
        """Define o ID proprio da transação
        """

        self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(IdProprio=id))

        return self

    def set_data_vencimento(self, data):
        """Define a data de vencimento
        """

        self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(DataVencimento=data))

        return self

    def set_recebedor(self, login_moip, email, apelido):
        """Define o recebedor
        """

        self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(Recebedor=dict(LoginMoip=login_moip, Email=email, Apelido=apelido)))

        return self

    def set_pagador(self, **pagador):
        """Define o pagador e endereço de cobrança
        """

        if not 'EnderecoCobranca' in pagador:
            return False

        if not 'Pais' in pagador['EnderecoCobranca']:
            pagador['EnderecoCobranca']['Pais'] = 'BRA'

        self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(Pagador=pagador))

        return self

    def set_checkout_transparente(self):
        """Define que o checkout sera transparente
        """

        instrucao = self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict())
        instrucao.find('InstrucaoUnica').set('TipoValidacao', 'Transparente')

    def envia(self):
        """Comunica com o webservice e envia a transação
        """
        # base64 encode the username and password
        auth = base64.encodestring('%s:%s' % (self.token, self.key)).replace('\n', '')

        webservice = httplib.HTTPSConnection(self.host)
        # headers
        webservice.putrequest("POST", self.post_url)
        webservice.putheader("Host", self.host)
        webservice.putheader("User-Agent", "Mozilla/4.0")
        webservice.putheader("Content-type", "text/html; charset=\"UTF-8\"")
        webservice.putheader("Content-length", "%d" % len(self._get_xml()))
        webservice.putheader("Authorization", "Basic %s" % auth)

        webservice.endheaders()
        webservice.send(self._get_xml())

        resposta = webservice.getresponse()

        self.status = resposta.status
        self.retorno = resposta.read()

        return self

    def _get_xml(self):
        """Metodo interno que retorna o objeto etree em formato string"""

        return etree.tostring(self.xml_node)

    def get_resposta(self):
        """Trata o retorno
        """
        if self.status == 200:
            resposta = etree.XML(self.retorno)
            return {'sucesso': resposta[0][1].text, 'token': resposta[0][2].text}
        else:
            return {'sucesso': u'Falha', 'token': u'Não autorizado. Verifique seu Token/key'}
