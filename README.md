# DCA3507 - INTRODUÇÃO À ROBÓTICA - T01 (2025.1)

## Trabalho: Cinemática Direta e Espaço de Trabalho de Braço Robótico

Este projeto realiza a calibração dos servos, cálculo dos ângulos das juntas, cinemática direta e visualização do espaço de trabalho de um braço robótico.

---

### Funcionalidades

- Conversão de valores PWM para ângulos das juntas
- Cálculo da posição do atuador via cinemática direta
- Visualização 3D do workspace (tetraedro)
- Geração de relatório em Markdown e PDF

### Requisitos

- Python 3.8+
- Bibliotecas: numpy, matplotlib, pandas

### Instalação

```bash
pip install -r requirements.txt
```

### Como usar

1. Edite os valores PWM dos pontos de teste no arquivo `robotica.py` conforme sua coleta.
2. Execute o script principal:

   ```bash
   python robotica.py
   ```

   Isso irá mostrar o gráfico 3D e imprimir a tabela de validação dos pontos.


### Estrutura dos arquivos

- `robotica.py`: Script principal de cálculos e visualização
- `relatorio.md`: Relatório em Markdown
- `imgs/`: Imagens dos pontos coletados e do resultado

### Créditos

- Professor: Pablo Javier Alsina
- Alunos: Cesar Henrique Tittoto Melo, Eduardo Lira da Silva Filho, Henrique Antônio Guanais Corneau, Rutileno Gabriel Camilo da Silva, Rinaldo Tavares da Silva Filho

---

*Projeto acadêmico para a disciplina DCA3507 - Introdução à Robótica (UFRN)*
