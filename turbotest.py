import arweave

wallet = arweave.Wallet('wallet.json')

ardrive_url = "https://upload.ardrive.dev"

print(wallet.address, wallet.balance)

#######################

# uploadTxn = arweave.Transaction(
#     # wallet=wallet, data=open('captures/IMG_20240403_123647.png', "rb").read())
#     wallet=wallet, data=b'ok')
# # uploadTxn.api_url = ardrive_url

# uploadTxn.add_tag("Content-Type", "image/png")

# uploadTxn.sign()
# price = uploadTxn.get_price()
# print(price)
# r = uploadTxn.send()

# print(r)

####################

tx = arweave.Transaction(
    wallet, id="UaLQWnAntwORw8xOkDYDV4J6kRSXi0L3707iFzbi3CxfLQ5ogLlLRoujUOlWAEKN")
print(tx.data)
print(tx.get_status())

# UaLQWnAntwORw8xOkDYDV4J6kRSXi0L3707iFzbi3CxfLQ5ogLlLRoujUOlWAEKN
