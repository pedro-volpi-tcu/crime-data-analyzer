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

A presente metodologia destina-se ao cálculo de um Índice de Estresse para políticas de segurança pública. O modelo parte da premissa de que cada política $P_i$, com $i \in ℕ$, dispõe de um orçamento específico $B_i$ e se aplica a um conjunto determinado de crimes, aqui denotados por $c_{ij}$, onde $j \in ℕ$.

A análise fundamenta-se nos dados da plataforma [Sinesp VDE](https://www.gov.br/mj/pt-br/assuntos/sua-seguranca/seguranca-publica/estatistica/dados-nacionais-1/base-de-dados-e-notas-metodologicas-dos-gestores-estaduais-sinesp-vde-2022-e-2023), a partir dos quais os crimes são caracterizados por três dimensões primárias: o número de vítimas ($\alpha$), um fator de peso ou relevância da ocorrência ($\beta$) e a quantidade de apreensões ($\gamma$). Desta forma, cada crime $c_{ij}$ é formalmente representado por um vetor tridimensional:

$$c_{ij} = (\alpha_{ij}, \beta_{ij}, \gamma_{ij})$$

Para garantir a comparabilidade entre as distintas dimensões, cada uma dessas variáveis ($X \in \\{\alpha, \beta, \gamma\\}$) é submetida a um processo de normalização. Utiliza-se a normalização por escore Z, conforme a equação:

$$Z = \frac{X - \mu}{\sigma}$$

onde $\mu$ representa a média e $\sigma$ o desvio padrão da respectiva variável no conjunto de dados.

Após a normalização, calcula-se um escore de gravidade ($G$) para cada crime. Este escore é definido como a média ponderada das três dimensões normalizadas, com base em um conjunto de pesos $\Omega = \\{\omega_1, \omega_2, \omega_3\\}$ que reflete a importância relativa de cada dimensão. O escore de gravidade para um crime $c_{ij}$ é, portanto, dado por:

$$G(c_{ij}) = \omega_1 \alpha_{ij} + \omega_2 \beta_{ij} + \omega_3 \gamma_{ij}$$

Finalmente, o Índice de Estresse ($\mathrm{IE}$) para uma política $P_i$ é estabelecido pela razão entre a soma da gravidade de todos os crimes que ela abrange e o seu respectivo orçamento:

$$\mathrm{IE}(P_i) = \frac{\sum_{j} G(c_{ij})}{B_i}$$

Este índice expressa, portanto, a gravidade criminal agregada que uma política aborda por unidade monetária investida. Políticas com um índice de estresse elevado são aquelas que enfrentam desafios criminais de maior magnitude com um orçamento proporcionalmente menor, sinalizando a necessidade de uma análise prioritária e, potencialmente, de uma readequação de recursos.

## Licença

Este projeto é licenciado sob a Licença MIT.
