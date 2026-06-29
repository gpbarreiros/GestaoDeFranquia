from fastapi import APIRouter
from app.api.v1 import auth, usuarios, unidades, produtos, cardapios, estoque, pedidos, pagamentos, fidelidade, auditoria

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(usuarios.router)
router.include_router(unidades.router)
router.include_router(produtos.router)
router.include_router(cardapios.router)
router.include_router(estoque.router)
router.include_router(pedidos.router)
router.include_router(pagamentos.router)
router.include_router(fidelidade.router)
router.include_router(auditoria.router)
