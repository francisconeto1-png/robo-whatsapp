from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Sua chave da OpenWeather já configurada aqui:
API_KEY = "cbcf641f81eaeea33d0a56dbbf79ce2a"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # Pega a mensagem (nome da cidade) que o usuário mandou no WhatsApp
    cidade = request.values.get('Body', '').strip()
    
    # Prepara a resposta para o WhatsApp
    resposta_twilio = MessagingResponse()
    msg = resposta_twilio.message()

    if not cidade:
        msg.body("Por favor, digite o nome de uma cidade.")
        return str(resposta_twilio)

    # Link para buscar o clima na OpenWeather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric"
    
    try:
        dados = requests.get(url).json()
        
        if dados.get("cod") == 200:
            status = dados["weather"][0]["description"].capitalize()
            temp = dados["main"]["temp"]
            humidade = dados["main"]["humidity"]
            
            # Texto que o robô vai responder no WhatsApp
            texto_resposta = (
                f"🌍 *Previsão para {cidade.title()}:*\n"
                f"🌤️ Clima: {status}\n"
                f"🌡️ Temperatura: {temp}°C\n"
                f"💧 Umidade: {humidade}%"
            )
            msg.body(texto_resposta)
        else:
            msg.body(f"Desculpe, não consegui encontrar a cidade '{cidade}'. Verifique a grafia.")
            
    except Exception as e:
        msg.body("Ops, tive um problema para consultar a previsão agora. Tente novamente mais tarde.")

    return str(resposta_twilio)

# A porta 5000 que o ngrok vai procurar
if __name__ == "__main__":
    app.run(port=5000)