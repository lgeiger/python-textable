def numplaces(num, fprec, uncert=False):
    if uncert:
        l, r = '{}'.format(num).split('+/-')
        a, b = l.split('.')
        c, d = r.split('.')
        return len(a), len(b), len(d)
    else:
        a, b = '{}'.format(round(num, fprec)).split('.')
        return len(a), len(b)


def is_uncert(num):
    uncert = True
    try:
        num.nominal_value
        num.std_dev
    except:
        uncert = False
    return uncert


def genspec(col, fprec):
    amax = 0
    bmax = 0
    cmax = 0
    for v in col:
        if is_uncert(v):
            a, b, c = numplaces(v, fprec, uncert=True)
            if a > amax:
                amax = a
            if b > bmax:
                bmax = b
            if c > cmax:
                cmax = c
        else:
            a, b = numplaces(v, fprec)
            if a > amax:
                amax = a
            if b > bmax:
                bmax = b
    if cmax:
        return 'S[table-format={}.{}({})]'.format(amax, bmax, cmax)
    else:
        return 'S[table-format={}.{}]'.format(amax, bmax)


def table(cols, headerrow=None, headercol=None, filename=None, fprec=3,
          caption=None, label=None, env=True, loc='h'):
    '''
    Generates LaTeX tables from arrays.

    Parameters
    ----------
    cols : array_like
        Your Data.
    headerrow : array_like, optional
        A row at the top used to label the columns.
    headercol : array_like, optional
        First column used to label the rows.
    filename: str, optional
        If set .tex file is saved.
    fprec: int
        Round floats to given precision. Defaults to 3 decimal places.
    caption: str, optional
        Adds a LaTeX caption.
    label: str, optional
        Adds a LaTeX label.
    env: bool, optional
        If True (default) everything is wrapped in the LaTeX table environment.
    loc: str, optional
        Specifies the position of the table environment. Defaults to 'h'.

    Example
    ----------
    x = array([1., 2., 3.])
    y = array([ufloat(2, 0.1), ufloat(4, 0.5), ufloat(2, 0.04)])
    table([x, y], ['x', 'y'])
    '''

    result = []
    spec = ' '.join([genspec(col, fprec) for col in cols])
    if headerrow is not None:
        head = ' & '.join(map(r'\multicolumn{{1}}{{c}}{{{}}}'.format,
                              headerrow)) + r'\\'
    else:
        head = ''
    if headercol is not None:
        spec = 'l ' + spec
        head = ' & ' + head
    if env is True:
        result.append(r'\begin{{table}}[{}]'.format(loc))
        result.append(r'\centering')
    result.append(r'\begin{{tabular}}{{{}}}'.format(spec))
    result.append(r'\toprule')
    if headerrow is not None:
        result.append(head)
        result.append(r'\midrule')

    line = []
    maxlen = 0
    for c in cols:
        maxlen = max(len(c), maxlen)
    for i in range(maxlen):
        if headercol is not None:
            line.append(headercol[i])
        for c in cols:
            try:
                if is_uncert(c[i]):
                    line.append('{:L}'.format(c[i]))
                else:
                    line.append('{}'.format(round(c[i], fprec)))
            except:
                line.append('')
        result.append(' & '.join(line) + r' \\')
        line = []

    result.append(r'\bottomrule')
    result.append(r'\end{tabular}')
    if caption is not None:
        result.append(r'\caption{{{}}}'.format(caption))
    if label is not None:
        result.append(r'\label{{{}}}'.format(label))
    if env is True:
        result.append(r'\end{table}')

    if filename is not None:
        f = open(filename + '.tex', 'w')
        f.write('\n'.join(result))
        f.close()
    else:
        return '\n'.join(result)
