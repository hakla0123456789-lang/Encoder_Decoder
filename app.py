# from flask import Flask,render_template,request
# import base64

# app = Flask(__name__)



# @app.route('/',methods=['GET','POST'])
# def home():
#     result=None

#     if request.method=='POST':
#         message = request.form['message']
#         key  = request.form['key']
#         operation = request.form['operation']


#         if operation =='encode':
#             result = encode_msg(message,key)
#         else:
#             result= decode_msg(message,key)
#     return render_template('index.html',result=result)

# def encode_msg(msg,key):
#   encoded_list = []
#   for i in range(len(msg)):
#       message = msg[i]
#       key_char = key[i% len(key)]
      
#       value = (ord(message)+ord(key_char))%256
#       encoded_list.append(chr(value))

#   encoded_text = ''.join(encoded_list)
#   return str(base64.b64encode(encoded_text.encode())).split('b')[1]


# def decode_msg(encoded_msg,key):
#   decoded = base64.b64decode(encoded_msg).decode()
#   result=[]
#   for i in range(len(decoded)):
#       encoded_msg=decoded[i]
#       key_msg = key[i % len(key)]

#       value = (256+ord(encoded_msg)-ord(key_msg))%256
#       result.append(chr(value))

#   return ''.join(result)


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request
import base64
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    
    if request.method == 'POST':
        message = request.form['message']
        key = request.form['keys']  # HTML se 'keys' naam se aayega
        operation = request.form['operation']
        
        if operation == 'encode':
            result = encode_msg(message, key)  # CORRECTED: 'key' pass karo
        else:
            result = decode_msg(message, key)  # CORRECTED: 'key' pass karo
    
    return render_template('index.html', result=result)

def encode_msg(msg, key):  # CORRECTED: 'key' parameter
    encoded_list = []
    for i in range(len(msg)):
        message_char = msg[i]
        key_char = key[i % len(key)]  # CORRECTED: 'key' use karo
        
        value = (ord(message_char) + ord(key_char)) % 256
        encoded_list.append(chr(value))
    
    encoded_text = ''.join(encoded_list)
    
    # CORRECTED: Proper base64 encoding
    base64_encoded = base64.b64encode(encoded_text.encode()).decode('utf-8')
    return base64_encoded

def decode_msg(encoded_msg, key):  # CORRECTED: 'key' parameter
    try:
        # Remove base64 wrapper if present
        if encoded_msg.startswith("b'") and encoded_msg.endswith("'"):
            encoded_msg = encoded_msg[2:-1]
        
        decoded_base64 = base64.b64decode(encoded_msg).decode('utf-8')
        result = []
        
        for i in range(len(decoded_base64)):
            encoded_char = decoded_base64[i]
            key_char = key[i % len(key)]  # CORRECTED: 'key' use karo
            
            value = (256 + ord(encoded_char) - ord(key_char)) % 256
            result.append(chr(value))
        
        return ''.join(result)
    except Exception as e:
        return f"Error in decoding: {str(e)}. Make sure it's a valid encoded message."

if __name__ == "__main__":
      port = int(os.environ.get("PORT", 5000))
      app.run(host="0.0.0.0", port=port)
