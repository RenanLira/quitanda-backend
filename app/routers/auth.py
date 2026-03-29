

from typing import Annotated
from fastapi import APIRouter, Body, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.dependencies import get_auth_service
from app.domain.auth.auth_errors import TokenNotFoundError
from app.domain.auth.auth_service import AuthService
from app.domain.auth.dto.completar_cadastro_simplificado_dto import CompletarCadastroSimplificadoDTO
from app.domain.usuarios.dto.criar_usuario import CriarUsuarioDTO
from app.http.cookies import Cookies
from app.http.mappers.usuarios import map_usuario_publico
from app.http.schemas.auth import CompletarCadastroResponse, TokenAuthResponse



class AuthRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, prefix="/auth", tags=["auth"], **kwargs)
        
        self.registrar_rotas()
    
    def registrar_rotas(self):
        
        @self.post("/signup")
        async def signup(
            response: Response,
            body: Annotated[CriarUsuarioDTO, Body()],
            auth_service: Annotated[AuthService, Depends(get_auth_service)]
        ):
            
            result = await auth_service.signup(body)
            response.set_cookie(key="refresh_token", value=result.refresh_token, httponly=True, secure=True)
            
            return TokenAuthResponse(access_token=result.access_token, token_type=result.token_type)
        
        @self.post("/signin")
        async def login(
            response: Response,
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
            auth_service: Annotated[AuthService, Depends(get_auth_service)],
        ):
            
            result = await auth_service.login(form_data.username, form_data.password)
            
            response.set_cookie(key="refresh_token", value=result.refresh_token, httponly=True, secure=True)
            
            return TokenAuthResponse(access_token=result.access_token, token_type=result.token_type)
        
        @self.post("/refresh")
        async def refresh_token(
            cookies: Annotated[Cookies, Cookie()],
            auth_service: Annotated[AuthService, Depends(get_auth_service)],
        ):
            if not cookies.refresh_token:
                raise TokenNotFoundError()
            
            res = await auth_service.refresh_access_token(cookies.refresh_token)
            
            cookies.refresh_token = res.refresh_token
            
            return TokenAuthResponse(access_token=res.access_token, token_type=res.token_type)

        @self.post("/completar-cadastro")
        async def completar_cadastro(
            body: Annotated[CompletarCadastroSimplificadoDTO, Body()],
            auth_service: Annotated[AuthService, Depends(get_auth_service)],
        ):
            usuario = await auth_service.completar_cadastro_simplificado(body)

            return CompletarCadastroResponse(
                message="Cadastro completo com sucesso",
                usuario=map_usuario_publico(usuario)
            )
        
        @self.delete("/logout")
        async def logout(
            response: Response,
            cookies: Annotated[Cookies, Cookie()],
            token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/signin", refreshUrl="/auth/refresh"))],
            auth_service: Annotated[AuthService, Depends(get_auth_service)]
        ):
            refresh_token = cookies.refresh_token
            if not refresh_token:
                raise TokenNotFoundError()

            await auth_service.logout(refresh_token=refresh_token, access_token=token)
            response.delete_cookie(key="refresh_token")

            return {"message": "Logout bem-sucedido"}