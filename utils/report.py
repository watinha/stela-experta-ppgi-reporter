import pandas as pd


def __report_bibliography (prod, writer):
    bibliographic = {}
    bibliographic['P'] = prod['journal']['qualis'].value_counts()
    bibliographic['PA'] = prod['journal_student']['qualis'].value_counts()
    bibliographic['C'] = prod['proc']['Proceedings qualis'].value_counts()
    bibliographic['CA'] = prod['proc_student']['Proceedings qualis'].value_counts()

    qualis = ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']
    summary = pd.DataFrame(columns=['P', 'PA', 'C', 'CA'])
    for p in summary.columns:
        k = bibliographic[p].keys().tolist()
        for q in qualis:
            if q in k: summary.loc[q, p] = bibliographic[p][q]
            else: summary.loc[q, p] = 0
    return summary


def __report_tec (prod, writer):
    tec = prod['tec']['Tipo da produção'].value_counts()
    tec_student = prod['tec_student']['Tipo da produção'].value_counts()
    student_columns = tec_student.keys().tolist()
    tec_summary = tec.to_frame().T
    tec_summary.index = ['Professor']
    for c in tec_summary.columns:
        if c in student_columns: tec_summary.loc['Aluno', c] = tec_student[c]
        else: tec_summary.loc['Aluno', c] = 0
    return tec_summary


def __report_students (prod, writer, start, end):
    master_count = prod['master']['Ano da produção'].value_counts()
    ic_count = prod['ic']['Ano da produção'].value_counts()
    tcc_count = prod['tcc']['Ano da produção'].value_counts()
    years = list(range(start, end))
    students_summary = pd.DataFrame(index=['Mestres', 'IC', 'TCC'], columns=years)
    for y in years:
        if str(y) in master_count.keys().tolist(): students_summary.loc['Mestres', y] = master_count[str(y)]
        else: students_summary.loc['Mestres', y] = 0
        if str(y) in ic_count.keys().tolist(): students_summary.loc['IC', y] = ic_count[str(y)]
        else: students_summary.loc['IC', y] = 0
        if str(y) in tcc_count.keys().tolist(): students_summary.loc['TCC', y] = tcc_count[str(y)]
        else: students_summary.loc['TCC', y] = 0

    total = students_summary.sum(axis=1)
    mean = students_summary.mean(axis=1)
    students_summary['Total'] = total
    students_summary['Média'] = mean

    return students_summary


def __report_production (prod, writer, start=0, end=0):
    summary = __report_bibliography(prod, writer)
    summary.to_excel(writer, sheet_name='Bibliografia')
    tec_summary = __report_tec(prod, writer)
    tec_summary.to_excel(writer, sheet_name='Técnica')
    students_summary = __report_students(prod, writer, start, end)
    students_summary.to_excel(writer, sheet_name='Orientações')

    prod['master'][['ABNT', 'Ano da produção', 'journal_count', 'proceedings_count', 'tec_count']].to_excel(writer, sheet_name='Graduate')

    prod['journal'][['ABNT', 'Ano da produção', 'Periódico', 'qualis']].to_excel(writer, sheet_name='Journal')
    prod['journal_student'][['ABNT', 'Ano da produção', 'Periódico', 'qualis']].to_excel(writer, sheet_name='Student-Journal')
    prod['proc'][['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis']].to_excel(writer, sheet_name='Proceedings')
    prod['proc_student'][['ABNT', 'Ano da produção', 'Periódico', 'Proceedings qualis']].to_excel(writer, sheet_name='Student-Proceedings')
    prod['tec'][['ABNT', 'Tipo da produção', 'Ano da produção']].to_excel(writer, sheet_name='Tec')
    prod['tec_student'][['ABNT', 'Tipo da produção', 'Ano da produção']].to_excel(writer, sheet_name='Student-Tec')
    prod['ic'][['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='IC')
    prod['tcc'][['ABNT', 'Ano da produção']].to_excel(writer, sheet_name='TCC')



def summary (report_folder, prod, start=0, end=0):
    with pd.ExcelWriter('./output/%s/program-report.xlsx' % (report_folder)) as writer:
        __report_production(prod, writer, start, end)


def by_professor (report_folder, prod_docente, start=0, end=0):
    for professor in prod_docente.keys():
        name = ''.join(professor.split(' '))
        with pd.ExcelWriter('./output/%s/report-%s.xlsx' % (report_folder, name)) as writer:
            __report_production(prod_docente[professor], writer, start, end)


def summary_by_linha (report_folder, prod_docente, linhas_map, start=0, end=0):
    results = {}
    for professor in prod_docente.keys():
        linha = linhas_map[professor]
        prod = prod_docente[professor]
        if linha not in results:
            results[linha] = prod
        else:
            results[linha]['journal'] = pd.concat([results[linha]['journal'], prod['journal']])
            results[linha]['proc'] = pd.concat([results[linha]['proc'], prod['proc']])
            results[linha]['tec'] = pd.concat([results[linha]['tec'], prod['tec']])
            results[linha]['master'] = pd.concat([results[linha]['master'], prod['master']])
            results[linha]['ic'] = pd.concat([results[linha]['ic'], prod['ic']])
            results[linha]['tcc'] = pd.concat([results[linha]['tcc'], prod['tcc']])
            results[linha]['journal_student'] = pd.concat([results[linha]['journal_student'], prod['journal_student']])
            results[linha]['proc_student'] = pd.concat([results[linha]['proc_student'], prod['proc_student']])
            results[linha]['tec_student'] = pd.concat([results[linha]['tec_student'], prod['tec_student']])

    for linha in results.keys():
        with pd.ExcelWriter('./output/%s/linhas-%s-report.xlsx' % (report_folder, linha)) as writer:
            __report_production(results[linha], writer, start, end)


