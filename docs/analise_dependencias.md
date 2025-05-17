# Análise de Dependências Nativas e Incompatibilidades

## Dependências Incompatíveis Identificadas
- psycopg2-binary: Conector PostgreSQL com código nativo compilado
- numpy: Biblioteca de computação numérica com código C
- lxml: Parser XML/HTML com código C
- pandas: Biblioteca de análise de dados que depende de numpy e outros componentes nativos

## Impacto no Sistema
1. **psycopg2-binary**: Usado para conexão com PostgreSQL
   - Impacto: Alto (core do sistema)
   - Alternativas: sqlite3 (puro Python), pg8000 (puro Python)

2. **pandas**: Usado para processamento da tabela SIGTAP
   - Impacto: Médio (apenas no módulo de importação)
   - Alternativas: csv (módulo padrão), processamento manual

3. **lxml**: Usado para parsing de XML na importação SIGTAP
   - Impacto: Médio (apenas no módulo de importação)
   - Alternativas: xml.etree.ElementTree (módulo padrão)

4. **numpy**: Usado indiretamente via pandas
   - Impacto: Baixo (dependência indireta)
   - Alternativas: Não necessário se pandas for substituído

## Estratégia de Substituição
1. Substituir psycopg2-binary por pg8000 (mantém compatibilidade PostgreSQL)
2. Substituir pandas+lxml por processamento manual com módulos padrão (csv, xml.etree)
3. Simplificar o módulo de importação SIGTAP para versão demonstrativa
4. Manter a estrutura geral do sistema e todas as interfaces

## Próximos Passos
1. Atualizar requirements.txt removendo dependências incompatíveis
2. Modificar código de conexão ao banco de dados para usar pg8000
3. Simplificar processamento de importação SIGTAP
4. Testar localmente antes de tentar novo deploy
