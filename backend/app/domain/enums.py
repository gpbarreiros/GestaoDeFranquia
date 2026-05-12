from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    GERENTE = "GERENTE"
    CLIENTE = "CLIENTE"
    COZINHA = "COZINHA"
    ATENDENTE = "ATENDENTE"


class BaseLegalEnum(str, Enum):
    CONSENTIMENTO = "CONSENTIMENTO"
    CONTRATO = "CONTRATO"
    OBRIGACAO_LEGAL = "OBRIGACAO_LEGAL"


class CanalPedidoEnum(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"


class StatusPedidoEnum(str, Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGO = "PAGO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


class FormaPagamentoEnum(str, Enum):
    PIX = "PIX"
    CARTAO = "CARTAO"
    DINHEIRO = "DINHEIRO"
    MOCK = "MOCK"


class StatusPagamentoEnum(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"
    ESTORNADO = "ESTORNADO"


class TipoMovimentacaoEstoqueEnum(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    AJUSTE = "AJUSTE"


class TipoMovimentacaoFidelidadeEnum(str, Enum):
    CREDITO = "CREDITO"
    DEBITO = "DEBITO"


# Transições de status permitidas — regra de negócio central
TRANSICOES_STATUS_PEDIDO: dict[StatusPedidoEnum, list[StatusPedidoEnum]] = {
    StatusPedidoEnum.AGUARDANDO_PAGAMENTO: [
        StatusPedidoEnum.PAGO,
        StatusPedidoEnum.CANCELADO,
    ],
    StatusPedidoEnum.PAGO: [
        StatusPedidoEnum.EM_PREPARO,
        StatusPedidoEnum.CANCELADO,
    ],
    StatusPedidoEnum.EM_PREPARO: [
        StatusPedidoEnum.PRONTO,
    ],
    StatusPedidoEnum.PRONTO: [
        StatusPedidoEnum.ENTREGUE,
    ],
    StatusPedidoEnum.ENTREGUE: [],
    StatusPedidoEnum.CANCELADO: [],
}