def numplaces(num, uncert=False):
    if uncert:
        l, r = '{}'.format(num).split('+/-')
        a, b = l.split('.')
        c, d = r.split('.')
        return len(a), len(b), len(d)
    else:
        # TODO temporary hack
        a, b = '{:.1f}'.format(num).split('.')
        return len(a), len(b)

def is_uncert(num):
    uncert = True
    try:
        num.nominal_value
        num.std_dev
    except:
        uncert = False
    return uncert

def genspec(col):
    amax = 0
    bmax = 0
    cmax = 0
    for v in col:
        if is_uncert(v):
            a, b, c = numplaces(v, uncert=True)
            if a > amax:
                amax = a
            if b > bmax:
                bmax = b
            if c > cmax:
                cmax = c
        else:
            a, b = numplaces(v)
            if a > amax:
                amax = a
            if b > bmax:
                bmax = b
    if cmax:
        return 'S[table-format={}.{}({})]'.format(amax, bmax, cmax)
    else:
        return 'S[table-format={}.{}]'.format(amax, bmax)

def table(toprow, cols, leftcol=None):
    '''
    Generates LaTeX tables from numpy arrays.

    Parameters
    ----------
    toprow : array_like
        A row at the top used to label the columns.
    cols : array_like
        Your Data.
    leftcol : array_like, optional
        First column used to label the rows.

    Returns
    ----------
    str
        LaTeX table.

    Example
    ----------
    x = array([1., 2., 3.])
    y = array([ufloat(2, 0.1), ufloat(4, 0.5), ufloat(2, 0.04)])
    table(['x', 'y'], [x, y], ['a', 'b', 'c'])
    '''

    result = []

    if leftcol is not None:
        spec = 'l {}'.format(' '.join(map(genspec, cols)))
    else:
        spec = ' '.join(map(genspec, cols))

    result.append(r'\begin{{tabular}}{{{}}}'.format(spec))
    result.append(r'\toprule')
    if leftcol is not None:
        result.append(' & ' + ' & '.join(map(r'\multicolumn{{1}}{{c}}{{{}}}'.format, toprow)) + r'\\')
    else:
        result.append(' & '.join(map(r'\multicolumn{{1}}{{c}}{{{}}}'.format, toprow)) + r'\\')
    result.append(r'\midrule')

    line = []
    maxlen = 0
    for c in cols:
        maxlen = max(len(c), maxlen)
    for i in range(maxlen):
        if leftcol is not None:
            line.append(leftcol[i])
        for c in cols:
            try:
                if is_uncert(c[i]):
                    line.append('{:L}'.format(c[i]))
                else:
                    line.append('{}'.format(c[i]))
            except:
                line.append('')
        result.append(' & '.join(line) + r' \\')
        line = []

    result.append(r'\bottomrule')
    result.append(r'\end{tabular}')

    return '\n'.join(result)

def write_table(filename, toprow, cols, leftcol=None):
    '''
    Writes LaTeX tables from numpy arrays to .tex file.

    Parameters
    ----------
    filename : str
    toprow : array_like
        A row at the top used to label the columns.
    cols : array_like
        Your Data.
    leftcol : array_like, optional
        First column used to label the rows.

    Returns
    ----------
    .tex file
        ready to import in your main LaTeX document.

    Example
    ----------
    x = array([1., 2., 3.])
    y = array([ufloat(2, 0.1), ufloat(4, 0.5), ufloat(2, 0.04)])
    write_table('testtable', ['x', 'y'], [x, y], ['a', 'b', 'c'])
    '''

    f = open(filename + '.tex', 'w')
    f.write(table(toprow, cols, leftcol))
    f.close()
