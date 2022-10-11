import pandas as pd


def __report_production (prod, writer):
    prod['journal'][['ABNT', 'Ano da produção', 'Periódico', 'qualis']].to_excel(writer, sheet_name='Journal')
    prod['journal_student'][['ABNT', 'Ano da produção', 'Periódico', 'qualis']].to_excel(writer, sheet_name='Student-Journal')
    prod['proc'][['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis']].to_excel(writer, sheet_name='Proceedings')
    prod['proc_student'][['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis']].to_excel(writer, sheet_name='Student-Proceedings')
    prod['tec'][['ABNT', 'Tipo da produção', 'Ano da produção']].to_excel(writer, sheet_name='Tec')
    prod['tec_student'][['ABNT', 'Tipo da produção', 'Ano da produção']].to_excel(writer, sheet_name='Student-Tec')
    prod['master'][['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='Graduate')
    prod['ic'][['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='IC')
    prod['tcc'][['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='TCC')

def summary (report_folder, prod):
    with pd.ExcelWriter('./output/%s/program-report.xlsx' % (report_folder)) as writer:
        __report_production(prod, writer)

def by_professor (report_folder, prod_docente):
    for professor in prod_docente.keys():
        name = ''.join(professor.split(' '))
        with pd.ExcelWriter('./output/%s/report-%s.xlsx' % (report_folder, name)) as writer:
            __report_production(prod_docente[professor], writer)


def summary_by_professor (report_folder, prod_docente):
    with pd.ExcelWriter('./output/%s/professor-report.xlsx' % (report_folder)) as writer:
        journal_all = None

        for professor in prod_docente.keys():
            if journal_all is None:
                journal_all = prod_docente[professor]['journal'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'qualis', 'docente']]
                proc_all = prod_docente[professor]['proc'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis', 'docente']]
                master_all = prod_docente[professor]['master'].loc[:, ['ABNT', 'Ano da produção', 'docente']]
                ic_all = prod_docente[professor]['ic'].loc[:, ['ABNT', 'Ano da produção', 'docente']]
                tcc_all = prod_docente[professor]['tcc'].loc[:, ['ABNT', 'Ano da produção', 'docente']]
                tec_all = prod_docente[professor]['tec'].loc[:, ['ABNT', 'Tipo da produção', 'Ano da produção', 'docente']]
                journal_student_all = prod_docente[professor]['journal_student'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'qualis', 'docente']]
                proc_student_all = prod_docente[professor]['proc_student'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis', 'docente']]
                tec_student_all = prod_docente[professor]['tec_student'].loc[:, ['ABNT', 'Tipo da produção', 'Ano da produção', 'docente']]
            else:
                journal_all = pd.concat([journal_all, prod_docente[professor]['journal'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'qualis', 'docente']]])
                proc_all = pd.concat([proc_all, prod_docente[professor]['proc'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis', 'docente']]])
                master_all = pd.concat([master_all, prod_docente[professor]['master'].loc[:, ['ABNT', 'Ano da produção', 'docente']]])
                ic_all = pd.concat([ic_all, prod_docente[professor]['ic'].loc[:, ['ABNT', 'Ano da produção', 'docente']]])
                tcc_all = pd.concat([tcc_all, prod_docente[professor]['tcc'].loc[:, ['ABNT', 'Ano da produção', 'docente']]])
                tec_all = pd.concat([tec_all, prod_docente[professor]['tec'].loc[:, ['ABNT', 'Tipo da produção', 'Ano da produção', 'docente']]])
                journal_student_all = pd.concat([journal_student_all, prod_docente[professor]['journal_student'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'qualis', 'docente']]])
                proc_student_all = pd.concat([proc_student_all, prod_docente[professor]['proc_student'].loc[:, ['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis', 'docente']]])
                tec_student_all = pd.concat([tec_student_all, prod_docente[professor]['tec_student'].loc[:, ['ABNT', 'Tipo da produção', 'Ano da produção', 'docente']]])

        journal_all.to_excel(writer, sheet_name='Journal')
        journal_student_all.to_excel(writer, sheet_name='Journal Student')
        proc_all.to_excel(writer, sheet_name='Proceedings')
        proc_student_all.to_excel(writer, sheet_name='Proceedings Student')
        tec_all.to_excel(writer, sheet_name='Tec')
        tec_student_all.to_excel(writer, sheet_name='Tec Student')
        master_all.to_excel(writer, sheet_name='Graduate')
        ic_all.to_excel(writer, sheet_name='IC')
        tcc_all.to_excel(writer, sheet_name='TCC')




