from numpy import round, shape


def numplaces(num, fprec, uncert=False):
    if uncert:
        l, r = '{}'.format(num).split('+/-')
        a, b = l.split('.')
        c, d = r.split('.')
        return len(a), len(b), len(d)
    else:
        try:
            a, b = '{}'.format(round(num, fprec)).split('.')
        except:
            a = '{}'.format(round(num, fprec))
            b = ''

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
    addsys = ''
    if len(shape(col)) == 2:
        col1 = col[0]
        col2 = col[1]
        dmax = 0
        for sys in col2:
            d = round(sys, fprec)
            if len(str(d)) > dmax:
                dmax = len(str(d))
                addsys = r', table-space-text-post=$\, \pm \, {}$'.format(d)
    else:
        col1 = col

    for v in col1:
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
        return 'S[table-format={}.{}({}){}]'.format(amax, bmax, cmax, addsys)
    else:
        return 'S[table-format={}.{}{}]'.format(amax, bmax, addsys)


def table(cols, headerrow=None, headercol=None, filename=None, fprec=3,
          caption=None, label=None, env=True, loc='h'):
    '''
    Generates LaTeX tables from arrays.

    Parameters
    ----------
    cols : array_like
        Your Data. Input cols=[x, y] where x and y are 1-d arrays or lists.
        If x is two dimensional x[0] should be your data and x[1] the
        systematic uncertainty.
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

    |  x  |       y       |
    |:---:|:-------------:|
    | 1.0 | 2.00 \pm 0.10 |
    | 2.0 | 4.0 \pm 0.5   |
    | 3.0 | 2.00 \pm 0.04 |
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
        if len(shape(c)) == 2:
            c1 = c[0]
        else:
            c1 = c
        maxlen = max(len(c1), maxlen)
    for i in range(maxlen):
        if headercol is not None:
            line.append(headercol[i])
        for c in cols:
            if len(shape(c)) == 2:
                try:
                    if is_uncert(c[0][i]):
                        line.append(r'{:L} {{$\, \pm \, {}$}}'.format(
                                    c[0][i], round(c[1][i], fprec)))
                    else:
                        line.append(r'{} {{$\, \pm \, {}$}}'.format(round(
                                    c[0][i], fprec), round(c[1][i], fprec)))
                except:
                    line.append('')
            else:
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
