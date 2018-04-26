from cieloApi3 import *
from app import app_config
# from run import config_name
import json


class Creditcard(object):
  merchantid = app_config['development'].MERCHANT_ID
  mercantkey = app_config['development'].MERCHANT_KEY
  # Configure o ambiente
  environment = Environment(sandbox=True)
  # Configure seu merchant, para gerar acesse: https://cadastrosandbox.cieloecommerce.cielo.com.br/
  merchant = Merchant(merchantid, mercantkey)

  def __init__(self, value, order_id, name, cvc, brand, expr_date, card_n, card_holder):
    self.value = value
    self.order_id = order_id
    self.name = name
    self.cvc = cvc
    self.brand = brand
    self.expr_date = expr_date
    self.card_n = card_n
    self.card_holder = card_holder

  def createTransaction(self):
    # Crie uma instancia de Sale informando o ID do pagamento
    self.sale = Sale(self.order_id) # order_id = id da transacao

    # Crie uma instancia de Customer informando o nome do cliente
    self.customer = Customer(self.name) # name = nome do cliente

    # Crie uma instancia de Credit Card utilizando os dados de teste
    # esses dados estao disponiveis no manual de integracao
    self.credit_card = CreditCard(self.cvc, self.brand) # cvc = 123 ; brand = 'Visa'
    self.credit_card.expiration_date = self.expr_date # expr_date = MM/YYYY
    self.credit_card.card_number = self.card_n # card_n = '0000000000000001'
    self.credit_card.holder = self.card_holder # card_holder = nome no cartao

    # Crie uma instancia de Payment informando o valor do pagamento
    self.sale.payment = Payment(self.value) # value = 15000
    self.sale.payment.credit_card = self.credit_card

    # Cria instancia do controlador do ecommerce
    self.cielo_ecommerce = CieloEcommerce(self.merchant, self.environment)

    # Criar a venda
    response_create_sale = self.cielo_ecommerce.create_sale(self.sale)

    # Verifica se a venda foi criada com sucesso
    if(response_create_sale['Payment']['Status'] == 1):
      # Com a venda criada na Cielo, ja temos o ID do pagamento, TID e demais
      # dados retornados pela Cielo
      self.payment_id = self.sale.payment.payment_id

      # Com o ID do pagamento, podemos fazer sua captura,
      # se ela nao tiver sido capturada ainda
      response_capture_sale = self.cielo_ecommerce.capture_sale(self.payment_id, self.value, 0)

      # Retorna o Status e as Mensagens de retorno
      response = {
        'Status': response_capture_sale['Status'],
        'ReturnMessage': response_capture_sale['ReturnMessage'],
        'ReasonMessage': response_capture_sale['ReasonMessage']
      }
      # response = response_capture_sale
    else: # Venda nao foi criada. Imprime o Status e a Mensagem de retorno
      # response = response_create_sale
      response = {
        'Status': response_create_sale['Payment']['Status'],
        'ReturnMessage': response_create_sale['Payment']['ReturnMessage']
      }
    return response

