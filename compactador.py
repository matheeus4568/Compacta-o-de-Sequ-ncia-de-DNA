import struct
DnaToBit = {'A': 0b00, 'C': 0b01, 'G': 0b10, 'T': 0b11}
BitToDna = {0b00: 'A', 0b01: 'C', 0b10: 'G', 0b11: 'T'}
IntToBit = {0: 0b00, 1: 0b01, 2: 0b10, 3: 0b11}

def compactar(sequencia: str) -> bytes:
    resultado = bytearray()
    n_bases_ultimo_byte = (len(sequencia) + 1) % 4
    
    byte = (0b00000000 << 2) | IntToBit[n_bases_ultimo_byte]
    n_bits = 2
    
    for base in sequencia:
        byte = (byte << 2) | DnaToBit[base]
        n_bits += 2
        
        if (n_bits == 8):
            resultado.append(byte)
            byte = 0b00000000
            n_bits = 0
    
    if (n_bits > 0):
        byte <<= (8 - n_bits)
        resultado.append(byte)
        
    return bytes(resultado)


def descompactar(sequencia: bytes) -> str:
    duplas_bits = []
    
    for byte in sequencia:
        for deslocamento in (6, 4, 2, 0):
            duplas_bits.append((byte >> deslocamento) & 0b11)
    
    cabecario = duplas_bits[0]
    bases = duplas_bits[1:-cabecario]
    
    resultado = ''
    for base in bases:
        resultado = resultado + BitToDna[base]
    
    return resultado


while True:
    opc = input("ESCOLHA A AÇÃO\n=-=-=-=-=-=-=-=-=\n(1) Compactar\n(2) Descompactar\n(0) Sair\n")
    match opc:
        case '1':
            nome_arquivo = input("Digite o nome do arquivo: ")
            with open(nome_arquivo, 'r') as arquivo:
                seq = arquivo.read()

            seq_compactada = compactar(seq)

            nome_saida = f"{nome_arquivo.removesuffix('.txt')}_cmpct.bin"
            with open(nome_saida, 'wb') as arquivo:
                arquivo.write(seq_compactada)

            print("COMPACTAÇÃO REALIZADA\n=-=-=-=-=-=-=-=")

        case '2':
            nome_arquivo = input("Digite o nome do arquivo: ")
            with open(nome_arquivo, 'rb') as arquivo:
                seq = arquivo.read()
            
            seq_descompactada = descompactar(seq)

            nome_saida = f"{nome_arquivo.removesuffix('_cmpct.bin')}_dcmpct.txt"
            with open(nome_saida, 'w') as arquivo:
                arquivo.write(seq_descompactada)

            print("DESCOMPACTAÇÃO REALIZADA\n=-=-=-=-=-=-=-=")

        case '0':
            break