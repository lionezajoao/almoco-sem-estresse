import textwrap
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.src.lib.auth import Auth
from app.src.lib.user import User
from app.src.lib.email_sender import EmailSender

class UserController:
    def __init__(self):
        self.user = User()
        self.auth = Auth()
        self.email = EmailSender()
        self.scope = ["admin"]

    def return_all_users(self, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            return JSONResponse(content=self.user.get_all_users(), status_code=200)
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    def handle_user(self, email, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            data = self.user.get_user(email)
            if data:
                return JSONResponse(content=data, status_code=200)
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    def handle_user_password(self, email, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            data = self.user.get_user_password(email)
            if data:
                return JSONResponse(content=data, status_code=200)
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    def handle_new_user(self, data, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            user_check = self.user.get_user(data.email)
            if user_check:
                raise HTTPException(status_code=400, detail="User already exists")
            
            hashed_password = self.auth.hash_password(data.password)
            self.user.insert_new_user(data.name, data.email, hashed_password, data.role)
            email_text = """
            <html>
                <body>
                    <p>Olá, {name}! Seja muito bem-vinda ao ALMOÇO SEM ESTRESSE! 🧡<br><br>
                    A partir de agora você pode planejar cardápios de forma rápida e simples.<br><br>
                    Vou te passar algumas informações importantes sobre seu acesso ok?<br><br><br>
                    Para acessar a ferramenta geradora de cardápios, basta clicar nesse link: <a href="{website}">Almoço Sem Estresse</a><br><br>
                    Uma senha será solicitada. Esta é sua senha provisória:<br><br>
                    Senha: {password}<br><br>
                    Recomendamos que você faça a alteração no primeiro acesso.<br><br>
                    Pronto, agora é só escolher os pratos e montar seus cardápios.<br><br>
                    Se tiver alguma dúvida ou precisar de suporte, você pode nos contactar pela área de membros nesse link: <a href="{whatsapp}">WhatsApp</a><br><br>
                    ou pelo email: suporte@almocosemestresse.com.br</p><br>
                    <p>Abraços,</p>
                    <p>Melina</p>
                    <p>Instagram | <a href="https://www.instagram.com/demaesparamaes/">@demaesparamaes</a></p>
                </body>
            </html>
            """.format(
                name=data.name,
                password=data.password,
                website="https://almoçosemestresse.app.br",
                whatsapp="https://api.whatsapp.com/send/?phone=5531972394438&app_absent=0"
            )
            
            self.email.send_text_email(subject="Senha provisória", recipients=[data.email], body=email_text, html=True)
            return JSONResponse(content={ "success": True, "message": "User added successfully"}, status_code=200)
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    def handle_new_password(self, data, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            if self.user.get_user(data.email):
                new_password = self.auth.hash_password(data.password)
                self.update_user_password(data.name, new_password)
                return JSONResponse(content={"message": "Password updated successfully"}, status_code=200)
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    def handle_delete_user(self, email, token_data):
        if self.user.verify_user_role(token_data.get("email"), token_data.get("role"), self.scope):
            if self.user.get_user(email):
                try:
                    self.user.delete_user(email)
                    return JSONResponse(content={"success": True, "message": "User deleted successfully"}, status_code=200)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Internal Server Error: { e }")
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=401, detail="Unauthorized")
