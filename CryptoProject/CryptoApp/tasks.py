from CryptoApp.scripts.get_coins import run, call_api

def update_coins():
    if run() == True:
        print('Database updated')
    else:
        print('Database not updated')
    
