from utils import Eval
from sympy import *

class SymPyGamma(object):

    def eval(self, s):
        r = self.try_sympy(s)
        if r:
            return r
        return [
                {"title": "Input", "input": s,
                    "output": "Can't handle the input."},
                ]

    def try_sympy(self, s):
        namespace = {}
        exec "from sympy.interactive import *" in {}, namespace
        a = Eval(namespace)
        # change to True to spare the user from exceptions:
        r = a.eval(u'pprint(%s)' % s, use_none_for_exceptions=False)
        if r is not None:
            result = [
                    {"title": "Input", "input": s},
                    {"title": "SymPy", "input": s, "output": r},
                    ]
            code = """\
s = %s
a = s.atoms(Symbol)
if len(a) == 1:
    x = a.pop()
    result = %s
else:
    result = None
pprint(result)
"""
            line = "diff(%s, x)" % s
            r = a.eval(code % (s, line), use_none_for_exceptions=True)
            if r and r != "None":
                result.append(
                        {"title": "Derivative", "input": line,
                            "output": r})
            line = "integrate(%s, x)" % s
            r = a.eval(code % (s, line), use_none_for_exceptions=True)
            if r and r != "None":
                result.append(
                        {"title": "Indefinite integral", "input": line,
                            "output": r})
            line = "series(%s, x, 0, 10)" % s
            r = a.eval(code % (s, line), use_none_for_exceptions=True)
            if r and r != "None":
                result.append(
                        {"title": "Series expansion around 0", "input": line,
                            "output": r})
            try:
                for item in range(len(result)):
                    for k in result[item].keys():
                        if 'None' in result[item][k]:
                            result[item][k] = result[item][k].replace('None', '')
            except TypeError as e:
                pass
            return result
        else:
            return None
