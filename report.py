import os, sys, pandas as pd

from utils import filter_interval, select_authors, report_journal, report_proc, prod_by_docente, get_students, prod_of_students

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
prod_docente = prod_by_docente({ 'journal': journal, 'proc': proc, 'master': master, 'ic': ic, 'tcc': tcc, 'tec': tec, 'journal_student': prod_student['journal'], 'proc_student': prod_student['proc'], 'tec_student': prod_student['tec'] }, docentes)


# general report
with pd.ExcelWriter('./output/%s/program-report.xlsx' % (report_folder)) as writer:
    journal[['ABNT', 'Ano da produção', 'Periódico', 'qualis']].to_excel(writer, sheet_name='Journal')
    proc[['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis']].to_excel(writer, sheet_name='Proceedings')
    master[['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='Graduate')
    ic[['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='IC')
    tcc[['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='TCC')
    tec[['ABNT', 'Subtipo da produção', 'Ano da produção']].to_excel(writer, sheet_name='Tec')
    prod_student['journal'][['ABNT', 'Ano da produção', 'Periódico', 'qualis']].to_excel(writer, sheet_name='Student-Journal')
    prod_student['proc'][['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis']].to_excel(writer, sheet_name='Student-Proceedings')
    prod_student['tec'][['ABNT', 'Subtipo da produção', 'Ano da produção']].to_excel(writer, sheet_name='Student-Tec')


for professor in prod_docente.keys():
    name = ''.join(professor.split(' '))
    with pd.ExcelWriter('./output/%s/report-%s.xlsx' % (report_folder, name)) as writer:
        prod_docente[professor]['journal'][['ABNT', 'Ano da produção', 'Periódico', 'qualis']].to_excel(writer, sheet_name='Journal')
        prod_docente[professor]['proc'][['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis']].to_excel(writer, sheet_name='Proceedings')
        prod_docente[professor]['master'][['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='Graduate')
        prod_docente[professor]['ic'][['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='IC')
        prod_docente[professor]['tcc'][['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='TCC')
        prod_docente[professor]['tec'][['ABNT', 'Subtipo da produção', 'Ano da produção']].to_excel(writer, sheet_name='Tec')
        prod_docente[professor]['journal_student'][['ABNT', 'Ano da produção', 'Periódico', 'qualis']].to_excel(writer, sheet_name='Student-Journal')
        prod_docente[professor]['proc_student'][['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis']].to_excel(writer, sheet_name='Student-Proceedings')
        prod_docente[professor]['tec_student'][['ABNT', 'Subtipo da produção', 'Ano da produção']].to_excel(writer, sheet_name='Student-Tec')


with pd.ExcelWriter('./output/%s/professor-report.xlsx' % (report_folder)) as writer:
    journal_all = None

    for professor in prod_docente.keys():
        if journal_all is None:
            journal_all = prod_docente[professor]['journal'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'qualis', 'docente']]
            proc_all = prod_docente[professor]['proc'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis', 'docente']]
            master_all = prod_docente[professor]['master'].loc[:, ['ABNT', 'Ano da produção', 'docente']]
            ic_all = prod_docente[professor]['ic'].loc[:, ['ABNT', 'Ano da produção', 'docente']]
            tcc_all = prod_docente[professor]['tcc'].loc[:, ['ABNT', 'Ano da produção', 'docente']]
            tec_all = prod_docente[professor]['tec'].loc[:, ['ABNT', 'Subtipo da produção', 'Ano da produção', 'docente']]
            journal_student_all = prod_docente[professor]['journal_student'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'qualis', 'docente']]
            proc_student_all = prod_docente[professor]['proc_student'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis', 'docente']]
            tec_student_all = prod_docente[professor]['tec_student'].loc[:, ['ABNT', 'Subtipo da produção', 'Ano da produção', 'docente']]
        else:
            journal_all = pd.concat([journal_all, prod_docente[professor]['journal'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'qualis', 'docente']]])
            proc_all = pd.concat([proc_all, prod_docente[professor]['proc'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis', 'docente']]])
            master_all = pd.concat([master_all, prod_docente[professor]['master'].loc[:, ['ABNT', 'Ano da produção', 'docente']]])
            ic_all = pd.concat([ic_all, prod_docente[professor]['ic'].loc[:, ['ABNT', 'Ano da produção', 'docente']]])
            tcc_all = pd.concat([tcc_all, prod_docente[professor]['tcc'].loc[:, ['ABNT', 'Ano da produção', 'docente']]])
            tec_all = pd.concat([tec_all, prod_docente[professor]['tec'].loc[:, ['ABNT', 'Subtipo da produção', 'Ano da produção', 'docente']]])
            journal_student_all = pd.concat([journal_student_all, prod_docente[professor]['journal_student'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'qualis', 'docente']]])
            proc_student_all = pd.concat([proc_student_all, prod_docente[professor]['proc_student'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis', 'docente']]])
            tec_student_all = pd.concat([tec_student_all, prod_docente[professor]['tec_student'].loc[:, ['ABNT', 'Subtipo da produção', 'Ano da produção', 'docente']]])

    journal_all.to_excel(writer, sheet_name='Journal')
    proc_all.to_excel(writer, sheet_name='Proceedings')
    master_all.to_excel(writer, sheet_name='Graduate')
    ic_all.to_excel(writer, sheet_name='IC')
    tcc_all.to_excel(writer, sheet_name='TCC')
    journal_student_all.to_excel(writer, sheet_name='Journal Student')
    proc_student_all.to_excel(writer, sheet_name='Proceedings Student')
    tec_student_all.to_excel(writer, sheet_name='Tec Student')




