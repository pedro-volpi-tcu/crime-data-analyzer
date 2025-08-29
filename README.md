# Ferramenta de Análise de Dados de Criminalidade

Ferramenta projetada para auxiliar na escolha de um objeto de auditoria na área de segurança pública. Ela oferece um conjunto de funcionalidades para analisar dados de criminalidade, ajudando os usuários a identificar tendências, padrões e áreas que podem exigir uma investigação mais aprofundada.

## Funcionalidades

-   **Processamento de Dados**: Lê e processa dados de criminalidade de várias fontes.

-   **Análise**: Aplica diferentes métodos analíticos para destacar as principais percepções.

-   **Visualização**: Gera gráficos para tornar dados complexos mais fáceis de entender.

-   **Geração de Relatórios**: Exporta os resultados da análise para um formato utilizável, como uma planilha Excel.

## Instalação

Este projeto requer Python 3.12 ou superior. Para instalar as dependências necessárias, use pip:

```bash
python -m pip install -e .
```

## Uso

Após a instalação, você pode executar a ferramenta usando o seguinte comando:

```bash
analyze-crime-data
```

Ou como módulo:
```bash
python -m crime_data_analizer.main --args
```

Para instruções mais detalhadas e opções disponíveis, consulte a documentação da ferramenta.

# Metodologia
O presente módulo tem por objetivo calcular índice de estresse de políticas de segurança pública.

Cada política $P_i$, $i \in \mathbb{N}$ possui um determinado orçamento $B_i$, e cobre um conjunto de crimes $c_{ij}$, $j \in \mathbb{N}$.

Os crimes analisados com base nos dados da [plataforma VDE](https://www.gov.br/mj/pt-br/assuntos/sua-seguranca/seguranca-publica/estatistica/dados-nacionais-1/base-de-dados-e-notas-metodologicas-dos-gestores-estaduais-sinesp-vde-2022-e-2023) possuem essencialmente três categorias relevantes: número de vítimas, peso e quantidade de apreensões.

Assim, o crime $c_{ij}$ é o vetor $(\alpha_{ij}, \beta_{ij}, \gamma_{ij})$.

Cada categoria $X$ é então normalizada segundo a fórmula:
$$Z = \frac{X - \mu}{\sigma}$$

Cada crime possui um escore de seriedade, que é uma média ponderada das três categorias, com base nos seguintes pesos:
$$\Omega = \{\omega_1, \omega_2, \omega_3\}$$

Assim, o escore de seriade de um crime $c_{ij}$ é a média ponderada abaixo:
$$S(c_{ij}) = \omega_1 \alpha_{ij} + \omega_2 \Beta_{ij} + \omega_3 \gamma_{ij}$$


## Licença

Este projeto é licenciado sob a Licença MIT.
