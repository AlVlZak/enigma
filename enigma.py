def enigma(text, ref, rot1, shift1, rot2, shift2, rot3, shift3, pairs = ''):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    text_without = ''
    for symbol in text:
        if symbol.upper() in alphabet:
            text_without += symbol.upper()
            
    rot_shift = [0, 17, 5, 22, 10, 0, [0, 13], [0, 13], [0, 13]]     
    
    res = ''
    
    flag_rot = False
    
    pairs = pairs.upper()
    for symbol in pairs.upper():
        if symbol == ' ':
            continue
        elif pairs.count(symbol) > 1:
            return "Извините, невозможно произвести коммутацию"
        
    #pairs = pairs.upper().split()    

    
    for symbol in text_without:
        if symbol in pairs:
            symbol = commute(pairs, symbol)
            
        shift3 = (shift3 + 1) % len(alphabet)
        
        if flag_rot: 
            shift2 = (shift2 + 1) % len(alphabet)
            shift1 = (shift1 + 1) % len(alphabet)
            flag_rot = False
            
        if shift3 == rot_shift[rot3]:
            shift2 = (shift2 + 1) % len(alphabet)
            
            if shift2 == (rot_shift[rot2] - 1):
                flag_rot = True
            else: flag_rot = False
            
            if shift2 == rot_shift[rot2]:
                shift1 = (shift1 + 1) % len(alphabet)
                
        #print(f'{shift1},{shift2},{shift3}')
                
        text_3 = rotor(caesar(symbol, shift3), rot3, False)
        #print(text_3)
        text_2 = rotor(caesar(text_3, -shift3 + shift2), rot2, False)
        #print(text_2)
        text_1 = rotor(caesar(text_2, -shift2 + shift1), rot1, False)
        #print(text_1)
    
        text_ref1 = reflector(caesar(text_1,-shift1), ref)
        #print(text_ref1)      
        
        text_1 = rotor(caesar(text_ref1, shift1), rot1, True)
        #print(text_1)
        text_2 = rotor(caesar(text_1, -shift1 + shift2), rot2, True)
        #print(text_2)
        text_3 = rotor(caesar(text_2, -shift2 + shift3), rot3, True)
        #print(text_3)
        
        text_3 = caesar(text_3, -shift3)
        
        if text_3 in pairs:
            text_3 = commute(pairs, text_3)
            
        res += text_3
        
    return res
 

def commute(pairs, symbol):
    index = pairs.index(symbol)
    if index % 3 == 0:
        return pairs[index + 1]
    elif index % 3 == 1:
        return pairs[index - 1]
    else:
        return "Извините, невозможно произвести коммутацию"

def caesar(text, key, alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    text_new = ""
    for i in range(len(text)):
        text_new +=  alphabet[(alphabet.index(text[i]) + key) % len(alphabet)]
    return text_new 
    
def rotor(symbol, to_rot, reverse=False):
    ROTORS = {\
          0: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
          1: 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
          2: 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
          3: 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
          4: 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
          5: 'VZBRGITYUPSDNHLXAWMJQOFECK',
          6: 'JPGVOUMFYQBENHZRDKASXLICTW',
          7: 'NZJHGRCXMYSWBOUFAIVLPEKQDT', 
          8: 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
          'beta': 'LEYJVCNIXWPBQMDRTAKZGFUHOS',
          'gamma': 'FSOKANUERHMBTIYCWLQPZXVGJD'
          }
    return ROTORS[0][ROTORS[to_rot].index(symbol)] if reverse \
        else ROTORS[to_rot][ROTORS[0].index(symbol)]

def reflector(symbol, n):
    REFLECTORS = {\
              0: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
              1: 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
              2: 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
              3: 'ENKQAUYWJICOPBLMDXZVFTHRGS',
              4: 'RDOBJNTKVEHMLFCWZAXGYIPSUQ',
              }
    return REFLECTORS[0][REFLECTORS[n].index(symbol)]

