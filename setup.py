from os import system

print("Install lib.")
system('pip install -r requirements.txt')
system('clear')

id = input("api_id: ")
hash = input("api_hash: ")

system('clear')
print('Configuration...')
with open('config', 'w') as f:
    f.write(id + "\n" + hash)
    
print("Finish!")
