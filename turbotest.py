import arweave
from arweave.arweave_lib import Wallet, Transaction
from arweave.transaction_uploader import get_uploader

wallet = Wallet('wallet.json')
print(wallet.address, wallet.balance)

with open("captures/compressed.png", "rb", buffering=0) as file_handler:
    print("file opened")
    tx = Transaction(wallet, file_handler=file_handler,
                     file_path="captures/compressed.png")
    # tx.api_url = "https://turbo.ardrive.io"
    tx.add_tag('Content-Type', 'image/png')
    tx.add_tag("Type", "image")
    tx.add_tag("App-Name", "InfinityCam")
    print("signing")
    tx.sign()
    print("signed, price: ", tx.get_price())

    uploader = get_uploader(tx, file_handler)

    print("xyz")
    while not uploader.is_complete:
        uploader.upload_chunk()

        print("{}% complete, {}/{}".format(
            uploader.pct_complete, uploader.uploaded_chunks, uploader.total_chunks
        ))
    print("done uploading", tx.id)


# ardrive_url = "https://turbo.ardrive.io"

# print(wallet.address, wallet.balance)

#######################

# uploadTxn = arweave.Transaction(
#     wallet=wallet, data=open('captures/IMG_20240403_123647.png', "rb").read())
# wallet=wallet, data=b'ok')
# uploadTxn.api_url = ardrive_url

# uploadTxn.add_tag("Content-Type", "image/png")

# uploadTxn.sign()
# price = uploadTxn.get_price()
# print(price)
# r = uploadTxn.send()

# print(r)

####################

# tx = arweave.Transaction(
#     wallet, id="UaLQWnAntwORw8xOkDYDV4J6kRSXi0L3707iFzbi3CxfLQ5ogLlLRoujUOlWAEKN")
# print(tx.data)
# print(tx.get_status())

# UaLQWnAntwORw8xOkDYDV4J6kRSXi0L3707iFzbi3CxfLQ5ogLlLRoujUOlWAEKN
