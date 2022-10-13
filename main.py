import os, sys, pandas as pd, datetime

from utils import filter_interval, select_authors, report_journal, report_proc, prod_by_docente, get_students
from utils.report import summary, by_professor, summary_by_linha

START = 2017
INTERVAL = 4
QUALIS_PER_FILENAME = './data/qualis-periodicos.csv'
QUALIS_CONF_FILENAME = './data/qualis-conferencias.csv'
DOCENTES_FILENAME = './data/docentes.txt'

if len(sys.argv) < 2:
    print('Deve ser passado como argumento um arquivo de produções gerado pelo programa Stella (https://www.stelaexperta.com.br/utfpr/index.html#main), início e fim do período de avaliação')
    sys.exit(1)

if len(sys.argv) < 3:
    print('Deve ser passado como argumento um início e fim do período de avaliação')
    sys.exit(1)

if len(sys.argv) < 4:
    print('Deve ser passado como argumento um fim do período de avaliação')
    sys.exit(1)

_, prod_filename, start, end = sys.argv
start, end = int(start), int(end)
report_folder = '%d-%d' % (start, end)

try:
    os.mkdir('./output/%s' % (report_folder))
    print('report folder generated...')
except:
    print('directory not created')
    sys.exit(1)

df = pd.read_csv(prod_filename)
docentes_df = pd.read_csv(DOCENTES_FILENAME, index_col='Nome')
docentes = docentes_df.index.tolist()
linhas_map = docentes_df.to_dict()['Linha']
qualis_journal_df = pd.read_csv(QUALIS_PER_FILENAME)
qualis_proc_df = pd.read_csv(QUALIS_CONF_FILENAME)

prod_df = filter_interval(df, start, end)

ppgi_df = select_authors(prod_df, docentes)
journal = report_journal(ppgi_df, qualis_journal_df)
proc = report_proc(ppgi_df, qualis_proc_df)

total_df = filter_interval(df, 2016, datetime.datetime.now().year + 1)
total_ppgi_df = select_authors(df, docentes)
total_journal = report_journal(total_ppgi_df, qualis_journal_df)
total_proc = report_proc(total_ppgi_df, qualis_proc_df)
total_tec = total_ppgi_df.loc[total_ppgi_df['Tipo agrupador da produção'] == 'Produção técnica']

ic = ppgi_df.loc[(ppgi_df['Tipo agrupador da produção'] == 'Orientação concluída') & (ppgi_df['Tipo da produção'] == 'Iniciação Científica')]
tcc = ppgi_df.loc[(ppgi_df['Tipo agrupador da produção'] == 'Orientação concluída') & (ppgi_df['Tipo da produção'] == 'Trabalho de conclusão de curso de graduação')]
tec = ppgi_df.loc[ppgi_df['Tipo agrupador da produção'] == 'Produção técnica']

(master, prod_student) = get_students(ppgi_df, { 'journal': total_journal, 'proc': total_proc, 'tec': total_tec })

all_prod = { 'journal': journal, 'proc': proc, 'master': master, 'ic': ic, 'tcc': tcc, 'tec': tec, 'journal_student': prod_student['journal'], 'proc_student': prod_student['proc'], 'tec_student': prod_student['tec'] }
prod_docente = prod_by_docente(all_prod, docentes)

# reporting
summary(report_folder, all_prod, start=start, end=end)
by_professor(report_folder, prod_docente, start=start, end=end)
summary_by_linha(report_folder, prod_docente, linhas_map, start=start, end=end)
