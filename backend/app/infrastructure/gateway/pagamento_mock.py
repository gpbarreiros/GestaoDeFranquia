import uuid
import random
from datetime import datetime, timezone
from app.core.config import settings


def processarPagamento(
    pedidoId: uuid.UUID,
    valor: float,
    forma: str,
) -> dict:
    aprovado = random.random() < settings.pagamentoMockTaxaAprovacao

    gatewayId = str(uuid.uuid4())
    processadoEm = datetime.now(timezone.utc).isoformat()

    if aprovado:
        return {
            "aprovado": True,
            "gatewayId": gatewayId,
            "status": "APROVADO",
            "valor": float(valor),
            "forma": forma,
            "pedidoId": str(pedidoId),
            "processadoEm": processadoEm,
            "mensagem": "Pagamento aprovado com sucesso.",
            "codigoAutorizacao": str(uuid.uuid4())[:8].upper(),
        }
    else:
        return {
            "aprovado": False,
            "gatewayId": gatewayId,
            "status": "RECUSADO",
            "valor": float(valor),
            "forma": forma,
            "pedidoId": str(pedidoId),
            "processadoEm": processadoEm,
            "mensagem": "Pagamento recusado pela operadora.",
            "codigoErro": "SALDO_INSUFICIENTE",
        }