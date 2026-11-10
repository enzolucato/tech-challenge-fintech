import pandera as pa
from pandera.typing import Series


class CreditDataContract(pa.DataFrameModel):
    """Contrato de Qualidade de Dados para Ingestão de Risco de Crédito."""

    age: Series[int] = pa.Field(
        ge=18,
        le=120,
        nullable=False,
        description="Idade do cliente deve ser entre 18 e 120 anos.",
    )

    income: Series[float] = pa.Field(
        gt=0,
        nullable=False,
        description="Renda mensal deve ser estritamente maior que 0 e não nula.",
    )

    credit_score: Series[int] = pa.Field(
        ge=300,
        le=850,
        nullable=False,
        description="Score de crédito padrão entre 300 e 850.",
    )

    loan_amount: Series[float] = pa.Field(
        gt=0,
        nullable=False,
        description="Valor do empréstimo solicitado.",
    )

    target: Series[int] = pa.Field(
        isin=[0, 1],
        nullable=True,  # Pode ser Nulo no lote de predição em produção
        description="Inadimplência: 1 para Default, 0 para Bom Pagador.",
    )

    class Config:
        strict = True  # Rejeita colunas não especificadas no esquema
        coerce = True  # Converte tipos compatíveis