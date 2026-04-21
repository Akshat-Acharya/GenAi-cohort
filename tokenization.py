import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

print("Vocab Size : ",encoder.n_vocab) #20019 (200K)

text = "The cat sat on the mat"
tokens = encoder.encode(text)
print("Tokens : ",tokens)
 
my_tokens =  [976, 9059, 10139, 402, 290, 2450]

decoder = encoder.decode(my_tokens)

print("Decoder : ",decoder)