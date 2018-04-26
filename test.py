from cieloApi3 import *

import json

# Configure o ambiente
environment = Environment(sandbox=True)

# Configure seu merchant, para gerar acesse: https://cadastrosandbox.cieloecommerce.cielo.com.br/
merchant = Merchant('d47006eb-ad3d-4686-9958-e99e97eecfba', 'CWVYKSZVHVHLZJYYHHSOLZXBATTZASLVPQXPPEIW')

# Crie uma instancia de Sale informando o ID do pagamento
sale = Sale('123')

# Crie uma instancia de Customer informando o nome do cliente
sale.customer = Customer('Fulano de Tal')

# Crie uma instancia de Credit Card utilizando os dados de teste
# esses dados estao disponiveis no manual de integracao
credit_card = CreditCard('123', 'Visa')
credit_card.expiration_date = '12/2018'
credit_card.card_number = '0000000000000001'
credit_card.holder = 'Fulano de Tal'

# Crie uma instancia de Payment informando o valor do pagamento
sale.payment = Payment(15700)
sale.payment.credit_card = credit_card

# Cria instancia do controlador do ecommerce
cielo_ecommerce = CieloEcommerce(merchant, environment)

# Criar a venda e imprime o retorno
response_create_sale = cielo_ecommerce.create_sale(sale)
print '----------------------response_create_sale----------------------'
print json.dumps(response_create_sale, indent=2)
print '----------------------response_create_sale----------------------'

# Com a venda criada na Cielo, ja temos o ID do pagamento, TID e demais
# dados retornados pela Cielo
payment_id = sale.payment.payment_id

# Com o ID do pagamento, podemos fazer sua captura,
# se ela nao tiver sido capturada ainda
response_capture_sale = cielo_ecommerce.capture_sale(payment_id, 15700, 0)
print '----------------------response_capture_sale----------------------'
print json.dumps(response_capture_sale, indent=2)
print '----------------------response_capture_sale----------------------'