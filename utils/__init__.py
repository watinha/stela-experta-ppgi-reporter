import math, pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

author_attrs = [('Autor %d' % (i)) for i in range(1, 45)]

def filter_interval (df, start, end):
    years = pd.to_numeric(df['Ano da produção'], errors='coerce')
    result = df.loc[(years < end) & (years >= start)] # filter by year
    return result

THRESHOLD = 0.8

def __search_author (authors, docente):
    authors_filtered = [ str(author) for author in authors]

    vectorizer = CountVectorizer(binary=True, strip_accents='unicode')
    docente_vec = vectorizer.fit_transform([docente])
    authors_vec = vectorizer.transform(authors_filtered)

    similarity_vec = cosine_similarity(docente_vec, authors_vec)
    max_similarity = max(similarity_vec[0])

    if max_similarity > THRESHOLD:
        return True
    return False


def select_authors (df, docentes):
    prod_authors = df[author_attrs].to_numpy().tolist()
    prod_ppgi = []
    for prod in prod_authors:
        selected = False

        for docente in docentes:
            if __search_author(prod, docente):
                selected = True
                break

        prod_ppgi.append(selected)

    return df.loc[prod_ppgi]


def report_journal (df, qualis_df):
    journal = df.loc[df['Tipo da produção'] == 'Artigo publicado em periódicos']
    qualis_dict = (pd.DataFrame(qualis_df['Qualis_Final'].to_numpy().tolist(), index=qualis_df['issn'])).to_dict()[0]
    journal.loc[:, 'qualis'] = [ qualis_dict[j] if j in qualis_dict else 'Sem classificação'
                            for j in journal['ISSN Periódico'].to_list() ]
    return journal


def report_proc (df, qualis_df):
    proc = df.loc[df['Tipo da produção'] == 'Trabalho publicado em anais de evento']
    proc = proc.loc[proc['Subtipo da produção'] == 'Completo']
    proc_text = proc['Periódico'].to_list()

    qualis_list = qualis_df[['sigla', 'conferencia', 'Qualis_Final']].to_numpy().tolist()
    qualis_text = [ ('%s %s' % (q[0], q[1])) for q in qualis_list ]

    vectorizer = CountVectorizer(binary=True, strip_accents='unicode')
    qualis_vec = vectorizer.fit_transform(qualis_text)
    proc_vec = vectorizer.transform(proc_text)

    similarity_vec = cosine_similarity(proc_vec, qualis_vec)
    qualis_index = [ row.index(max(row)) for row in similarity_vec.tolist() ]
    proc['Proceedings name'] = [ qualis_text[i] for i in qualis_index ]
    proc['Proceedings qualis'] = [ qualis_list[i] for i in qualis_index ]

    return proc


def prod_by_docente (dfs, docentes):
    result = {}

    for prod_type in dfs.keys():
        df = dfs[prod_type]
        prod_authors = df[author_attrs].to_numpy().tolist()
        for docente in docentes:
            for ind, authors in enumerate(prod_authors):
                if docente not in result:
                    result[docente] = {}

                if prod_type not in result[docente]:
                    result[docente][prod_type] = []

                if __search_author(authors, docente):
                    result[docente][prod_type].append(ind)

            result[docente][prod_type] = df.iloc[result[docente][prod_type], :]

    return result


def get_students (df):
    master = df.loc[(df['Tipo agrupador da produção'] == 'Orientação concluída') & (df['Tipo da produção'] == 'Dissertação de mestrado')]

    # removing bioinformatics
    titles = [ title.lower() for title in master['Periódico'].to_list() ]
    master = master.loc[[ (('bioinformática' not in t) and ('tecnológica' in t)) for t in titles ], :]

    students = df.loc[df['Tipo da produção'] == 'Dissertação de mestrado']
    titles = [ title.lower() for title in students['Periódico'].to_list() ]
    students = students.loc[[ (('bioinformática' not in t) and ('tecnológica' in t)) for t in titles ], :]
    students_map = {}
    for s in students['Periódico'].to_list():
        s_low = s.lower()
        name = s_low[:s_low.index(' universidade')]
        if name not in students_map:
            students_map[name] = True

    students = list(students_map.keys())

    return (master, students)


def prod_of_students (dfs, students):
    result = {}

    for prod_type in dfs.keys():
        df = dfs[prod_type]
        authors_list = df[author_attrs].to_numpy().tolist()
        result[prod_type] = []

        for ind, authors in enumerate(authors_list):
            for student in students:
                if __search_author(authors, student):
                    result[prod_type].append(ind)
                    break

        result[prod_type] = df.iloc[result[prod_type], :]

    return result





