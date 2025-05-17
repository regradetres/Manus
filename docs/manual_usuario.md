# Manual do Usuário - Sistema de Produção SUS

## Introdução

Bem-vindo ao Sistema de Produção SUS, uma ferramenta desenvolvida para auxiliar técnicos e digitadores de secretarias de saúde na geração de arquivos válidos de produção ambulatorial e hospitalar do SUS (BPA, FPO, RAAS e AIH), com base na tabela SIGTAP.

Este manual fornece instruções detalhadas sobre como utilizar o sistema, desde o acesso inicial até a exportação dos arquivos para envio ao DATASUS.

## Acesso ao Sistema

### Requisitos Mínimos

- Navegador web atualizado (Chrome, Firefox, Edge ou Safari)
- Conexão com a internet
- Credenciais de acesso fornecidas pelo administrador

### Login

1. Acesse o endereço do sistema fornecido pelo administrador
2. Na tela de login, insira seu nome de usuário e senha
3. Clique no botão "Entrar"

![Tela de Login](../docs/images/login.png)

### Perfis de Acesso

O sistema possui quatro perfis de acesso, cada um com permissões específicas:

- **Administrador**: Acesso completo a todas as funcionalidades, incluindo gerenciamento de usuários
- **Supervisor**: Acesso à maioria das funcionalidades, com ênfase em validação e aprovação de lotes
- **Digitador**: Foco no cadastro e edição de produção, com acesso limitado a relatórios
- **Auditor**: Acesso somente leitura à maioria das funcionalidades, com foco em relatórios e logs

## Dashboard Principal

Após o login, você será direcionado para o Dashboard principal, que oferece uma visão geral do sistema:

![Dashboard](../docs/images/dashboard.png)

O Dashboard apresenta:

1. **Menu lateral**: Acesso às principais funcionalidades do sistema
2. **Resumo de Status**: Cards com contadores de BPA, RAAS e AIH
3. **Atividade Recente**: Lista das últimas ações realizadas
4. **Status de Exportação**: Gráfico com o status dos registros (pendentes, validados, exportados, rejeitados)

## Importação da Tabela SIGTAP

A importação da tabela SIGTAP é o primeiro passo para utilizar o sistema, pois todos os procedimentos cadastrados dependem desta tabela.

### Como Importar

1. No menu lateral, clique em "SIGTAP"
2. Clique em "Importar"
3. Baixe o arquivo ZIP da tabela SIGTAP do site oficial do DATASUS
4. Clique em "Escolher arquivo" e selecione o arquivo ZIP baixado
5. Marque a caixa de confirmação
6. Clique em "Importar"

![Importação SIGTAP](../docs/images/importar_sigtap.png)

O sistema processará o arquivo e importará os procedimentos para o banco de dados. Este processo pode levar alguns minutos, dependendo do tamanho do arquivo.

### Consulta de Procedimentos

Após a importação, você pode consultar os procedimentos:

1. No menu lateral, clique em "SIGTAP"
2. Clique em "Procedimentos"
3. Utilize os filtros para buscar procedimentos específicos
4. Clique em um procedimento para ver detalhes

![Consulta de Procedimentos](../docs/images/procedimentos.png)

## Cadastro de Produção

O sistema permite o cadastro de diferentes tipos de produção: BPA, RAAS e AIH.

### Novo Cadastro

1. No menu lateral, clique em "Produção"
2. Clique em "Nova Produção"
3. Selecione o tipo de produção (BPA, RAAS ou AIH)

![Seleção de Tipo](../docs/images/selecionar_tipo.png)

### Formulário BPA

O formulário de BPA (Boletim de Produção Ambulatorial) contém os seguintes campos:

1. **Dados do Estabelecimento**:
   - CNES (obrigatório)
   - Competência (obrigatório, formato AAAAMM)

2. **Dados do Profissional**:
   - CNS do Profissional (obrigatório)
   - CBO (obrigatório)

3. **Dados do Paciente**:
   - CNS do Paciente
   - Nome do Paciente
   - Data de Nascimento
   - Sexo

4. **Dados do Atendimento**:
   - Data do Atendimento (obrigatório)
   - Tipo de BPA (Consolidado ou Individualizado)
   - CID (para BPA-I)
   - Caráter do Atendimento

5. **Dados do Procedimento**:
   - Procedimento (obrigatório, selecione da tabela SIGTAP)
   - Quantidade (obrigatório)

![Formulário BPA](../docs/images/formulario_bpa.png)

Preencha todos os campos obrigatórios e clique em "Salvar".

### Formulário RAAS

O formulário de RAAS (Registro das Ações Ambulatoriais de Saúde) contém campos específicos para este tipo de produção, incluindo:

- Tipo de RAAS (Psicossocial, AD, etc.)
- CID Principal e Secundário
- CNS do Cuidador (quando aplicável)

### Formulário AIH

O formulário de AIH (Autorização de Internação Hospitalar) contém campos específicos para internações:

- Número da AIH
- Data de Internação e Alta
- CID Principal e Secundário
- Caráter da Internação

### Listagem e Edição

Para visualizar, editar ou excluir registros:

1. No menu lateral, clique em "Produção"
2. Selecione o tipo de produção na aba superior
3. Utilize os filtros para encontrar registros específicos
4. Clique nos ícones de ação para visualizar, editar ou excluir

![Lista de Produção](../docs/images/lista_producao.png)

## Validação de Produção

A validação é um passo importante para garantir que os registros estejam corretos antes da exportação.

### Como Validar

1. Na lista de produção, localize o registro a ser validado
2. Clique no ícone de validação (✓)
3. Revise os dados do registro
4. Clique em "Validar" para confirmar

![Validação](../docs/images/validacao.png)

O sistema realizará verificações automáticas, como:

- Validação de CNS contra a base do CADSUS (quando disponível)
- Verificação de CBO contra tabela de ocupações válidas
- Validação de compatibilidade entre procedimentos, CBO e estabelecimento
- Verificação de limites de idade, sexo e quantidade para procedimentos

Se alguma inconsistência for encontrada, o sistema exibirá alertas ou erros que devem ser corrigidos antes da validação.

## Exportação para Formato DATASUS

Após validar os registros, você pode exportá-los para o formato exigido pelo DATASUS.

### Como Exportar

1. No menu lateral, clique em "Exportação"
2. Clique em "Nova Exportação"
3. Selecione o tipo de arquivo (BPA, RAAS, AIH)
4. Informe a competência (AAAAMM)
5. Marque a opção "Incluir apenas registros validados" (recomendado)
6. Clique em "Exportar"

![Configuração de Exportação](../docs/images/configurar_exportacao.png)

O sistema gerará o arquivo no formato exigido pelo DATASUS e exibirá uma tela de resultado com informações sobre a exportação.

### Download do Arquivo

Para baixar o arquivo gerado:

1. Na tela de resultado da exportação, clique em "Download"
2. Ou acesse "Exportação" no menu lateral e clique no ícone de download na lista de exportações

![Resultado da Exportação](../docs/images/resultado_exportacao.png)

O arquivo baixado estará pronto para ser enviado através dos sistemas oficiais do DATASUS.

## Histórico e Logs

O sistema mantém um histórico detalhado de todas as operações realizadas.

### Histórico de Exportações

Para visualizar o histórico de exportações:

1. No menu lateral, clique em "Exportação"
2. A lista exibirá todas as exportações realizadas, com informações como tipo, competência, quantidade de registros e status

![Histórico de Exportações](../docs/images/historico_exportacoes.png)

## Dicas e Boas Práticas

### Importação SIGTAP

- Atualize a tabela SIGTAP mensalmente, conforme o calendário de publicação do Ministério da Saúde
- Verifique os procedimentos importados após a conclusão da importação

### Cadastro de Produção

- Utilize a busca de procedimentos para encontrar rapidamente o código correto
- Verifique a compatibilidade entre procedimento e CBO antes de cadastrar
- Salve frequentemente para evitar perda de dados

### Validação

- Valide os registros em lotes pequenos para facilitar a correção de erros
- Priorize a validação de registros mais antigos para evitar acúmulo

### Exportação

- Exporte os arquivos por tipo e competência
- Verifique o arquivo gerado antes de enviar ao DATASUS
- Mantenha um backup dos arquivos exportados

## Solução de Problemas

### Problemas Comuns

1. **Erro ao importar SIGTAP**:
   - Verifique se o arquivo ZIP está íntegro
   - Confirme se é o arquivo oficial do DATASUS
   - Tente novamente com uma conexão mais estável

2. **Procedimento não encontrado**:
   - Verifique se a tabela SIGTAP foi importada corretamente
   - Confirme o código do procedimento
   - Verifique se o procedimento está vigente na competência atual

3. **Erro de validação**:
   - Verifique os campos obrigatórios
   - Confirme a compatibilidade entre procedimento, CBO e estabelecimento
   - Verifique as regras específicas do procedimento (idade, sexo, quantidade)

4. **Erro ao exportar**:
   - Verifique se há registros validados para a competência selecionada
   - Confirme se o tipo de arquivo selecionado é compatível com os registros

### Suporte Técnico

Se você encontrar problemas que não consegue resolver, entre em contato com o suporte técnico:

- Email: suporte@exemplo.com
- Telefone: (00) 1234-5678
- Horário de atendimento: Segunda a sexta, das 8h às 18h

## Glossário

- **BPA**: Boletim de Produção Ambulatorial
- **RAAS**: Registro das Ações Ambulatoriais de Saúde
- **AIH**: Autorização de Internação Hospitalar
- **SIGTAP**: Sistema de Gerenciamento da Tabela de Procedimentos, Medicamentos e OPM do SUS
- **CNES**: Cadastro Nacional de Estabelecimentos de Saúde
- **CNS**: Cartão Nacional de Saúde
- **CBO**: Classificação Brasileira de Ocupações
- **CID**: Classificação Internacional de Doenças
- **DATASUS**: Departamento de Informática do SUS

## Atualizações e Novidades

O sistema é constantemente atualizado para melhorar a experiência do usuário e adicionar novas funcionalidades. Fique atento às notificações e comunicados sobre atualizações.

Para sugestões de melhorias ou relato de problemas, entre em contato com o administrador do sistema ou com o suporte técnico.
