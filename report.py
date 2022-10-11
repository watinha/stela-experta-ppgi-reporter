import os, sys, pandas as pd

from utils import filter_interval, select_authors, report_journal, report_proc, prod_by_docente, get_students, prod_of_students
from utils.report import summary, by_professor, summary_by_professor

START = 2017
INTERVAL = 4
QUALIS_PER_FILENAME = './data/qualis-periodicos.csv'
QUALIS_CONF_FILENAME = './data/qualis-conferencias.csv'
DOCENTES_FILENAME = './data/docentes.txt'
PRODUCAO_FILENAME = './data/producao-29-06-2022.csv'

if len(sys.argv) < 2:
    print('Deve ser passado como argumento um arquivo de produções gerado pelo programa Stella (https://www.stelaexperta.com.br/utfpr/index.html#main), início e fim do período de avaliação')
    sys.exit(1)

if len(sys.argv) < 3:
    print('Deve ser passado como argumento um início e fim do período de avaliação')
    sys.exit(1)

if len(sys.argv) < 4:
    print('Deve ser passado como argumento um fim do período de avaliação')
    sys.exit(1)

_, _, start, end = sys.argv
start, end = int(start), int(end)
report_folder = '%d-%d' % (start, end)

try:
    os.mkdir('./output/%s' % (report_folder))
    print('report folder generated...')
except:
    print('directory not created')
    sys.exit(1)

prod_df = pd.read_csv(PRODUCAO_FILENAME)
docentes = open(DOCENTES_FILENAME).read().split('\n')[:-1] # remove last empty
qualis_journal_df = pd.read_csv(QUALIS_PER_FILENAME)
qualis_proc_df = pd.read_csv(QUALIS_CONF_FILENAME)

prod_df = filter_interval(prod_df, start, end)
ppgi_df = select_authors(prod_df, docentes)
journal = report_journal(ppgi_df, qualis_journal_df)
proc = report_proc(ppgi_df, qualis_proc_df)
(master, students) = get_students(ppgi_df)

ic = ppgi_df.loc[(ppgi_df['Tipo agrupador da produção'] == 'Orientação concluída') & (ppgi_df['Tipo da produção'] == 'Iniciação Científica')]
tcc = ppgi_df.loc[(ppgi_df['Tipo agrupador da produção'] == 'Orientação concluída') & (ppgi_df['Tipo da produção'] == 'Trabalho de conclusão de curso de graduação')]
tec = ppgi_df.loc[ppgi_df['Tipo agrupador da produção'] == 'Produção técnica']

prod_student = prod_of_students({ 'journal': journal, 'proc': proc, 'tec': tec }, students)

all_prod = { 'journal': journal, 'proc': proc, 'master': master, 'ic': ic, 'tcc': tcc, 'tec': tec, 'journal_student': prod_student['journal'], 'proc_student': prod_student['proc'], 'tec_student': prod_student['tec'] }
prod_docente = prod_by_docente(all_prod, docentes)

# reporting
summary(report_folder, all_prod)
by_professor(report_folder, prod_docente)
summary_by_professor(report_folder, prod_docente)
