# ------------------------------------------------------------------------------------------------
#
# Solution to the "Sum and Product Puzzle"
#
# First Version
#
# X and Y are two different whole numbers greater than 1. Their sum is not greater than 100, and 
# Y is greater than X. S and P are two mathematicians (and consequently perfect logicians);
# S knows the sum X + Y and P knows the product X * Y. Both S and P know all the information
# in this paragraph.
#
# The following conversation occurs:
#
# S says "P does not know X and Y."
# P says "Now I know X and Y."
# S says "Now I also know X and Y."
#
# What are X and Y?
#
# Links: 
#  https://en.wikipedia.org/wiki/Sum_and_Product_Puzzle
#
# Also, find more versions on the "versions" list below
# ------------------------------------------------------------------------------------------------

class SparseList(list):
  def __setitem__(self, index, value):
    missing = index - len(self) + 1
    if missing > 0:
      self.extend([[]] * missing)
    return list.__setitem__(self, index, value)
  def __getitem__(self, index):
    missing = index - len(self) + 1
    if missing > 0:
      self.extend([[]] * missing)
    return list.__getitem__(self, index)

class knowledge:
  codebook = { 'I dont know' : lambda x,K: len(x&K) >  1,
               'I knew that' : lambda x,K:       x  <= K,
               'Thanks fyi'  : lambda x,K: len(x&K)  > 1,
               'Now I know'  : lambda x,K: len(x&K) == 1,
               '<Skip>'      : lambda x,K:          True,
               '<Silence>'   : lambda x,K: len(x&K) >  1 }
  def __init__(self, K, dialog):
    self.o, self.U, self.V = set([]), SparseList([[]]), SparseList([[]])
    for e in K:
      self.o.add( e )
      self.U[e[1][0]] = self.U[e[1][0]] + [e]
      self.V[e[1][1]] = self.V[e[1][1]] + [e]
    self.U = [frozenset( U ) for U in self.U if U]
    self.V = [frozenset( V ) for V in self.V if V]
    from itertools import cycle
    self.D = [[ who, what, self.codebook[what]] for who, what in zip( cycle([self.V, self.U]), dialog)]
  def step(self, X, cond):
    self.o = set.union( *( [set(x&self.o) for x in X if cond(x,self.o)]+[set([])] ))
    return self.o
  def solve(self):
    self.trace = [self.step(k[0],k[2]) for k in self.D]
    return self.o
  def get_trace(self):
    return { 'trace' : zip( [[self.o, 'Initial', self.codebook['<Skip>']]] + self.D, self.trace),
             'U'     : self.U,
             'V'     : self.V }

versions = [[[ ((x,y),(x+y,x*y)) for y in range(3, 800) for x in range(2,min(y, 800-y+1))], # ok
             ['<Silence>', 'I knew that', 'Now I know', 'Now I know']],
            [[ ((x,y),(x+y,x*x+y*y)) for y in range(1,50) for x in range(1,y+1)], # ok
             ['I dont know']*5 + ['Now I know']],
            [[ ((x,y),(x+y,x*x+y*y)) for y in range(1,50) for x in range(1,y+1)], # ok
             ['I dont know']*6 + ['Now I know']],
            [[ ((x,y),(x+y,x*y)) for y in range(1,10) for x in range(1,10) if y >= x], # ok
             ['I dont know']*8 + ['Now I know']],
            [[ ((x,y),(x+y,x*y)) for y in range(3,100) for x in range(2,min(y, 100-y+1))], # ok
             ['<Silence>', 'I knew that', 'I dont know', 'Now I know']],
            [[ ((x,y),(x+y,x*y)) for y in range(2,100) for x in range(2,100) if y >= x ], # ok (x3)
             ['<Skip>', 'I dont know', 'I dont know', 'Now I know', 'Now I know']],
            [[ ((x,y),(x+y,x*y)) for y in range(2,100) for x in range(2,100) if y >=x ], # semi-ok (x2)
             ['I dont know', 'Thanks fyi', 'I dont know', 'Now I know', 'Now I know']],
            [[ ((x,y),(x+y,x*y)) for y in range(2,100) for x in range(2,100) if y >= x], # ok? (x2)
             ['I dont know', 'Thanks fyi', 'I dont know', 'Thanks fyi', 'Thanks fyi', 'Now I know', 'Now I know']],
            [[ ((x,y),(x+y,x*y)) for y in range(1,100) for x in range(1,100) if y >= x], # ok? probably but no solution provided
             ['<Skip>', 'I dont know'] + ['I knew that']*4 + ['I dont know', 'Now I know', 'Now I know']]]

K = None

if 0:
    K = knowledge( *versions[0] )
    print K.solve()
else:
    for i in versions:
        K = knowledge( *i )
        print K.solve()

# Plotting
if 0:
    import plotly.graph_objs as go
    import plotly.offline as offline
    from plotly import tools
    
    log = K.get_trace()
    Aplane = []
    Bplane = []
    for i,e in enumerate(log['trace']):
        trace = go.Scattergl(
            x = [ k[1][0] for k in e[1]],
            y = [ k[1][1] for k in e[1]],
            mode = 'markers',
            name = e[0][1],
            legendgroup = 'Iter' + str(i),
            showlegend=True
        )
        Bplane.append(trace)
        trace = go.Scattergl(
            x = [ k[0][0] for k in e[1]],
            y = [ k[0][1] for k in e[1]],
            mode = 'markers',
            name = e[0][1],
            legendgroup = 'Iter' + str(i),
            showlegend=False
        )
        Aplane.append(trace)

    fig = tools.make_subplots(rows=1, cols=2, subplot_titles=('A-plane','B-plane'))
    [fig.append_trace(A, 1, 1) for A in Aplane]
    [fig.append_trace(B, 1, 2) for B in Bplane]
    fig['layout'].update(title  ='Sum and Product puzzle',
                         hovermode = 'closest',
                         xaxis1 = {'title':'X', 'range': [0, 1001], 'spikemode' : "across", 'showspikes': True, 'spikedash': 'solid', 'spikethickness': 1},
                         yaxis1 = {'title':'Y', 'range': [0, 1001], 'spikemode' : "across", 'showspikes': True, 'spikedash': 'solid', 'spikethickness': 1},
                         xaxis2 = {'title':'U', 'range': [0, 2001], 'spikemode' : "across", 'showspikes': True, 'spikedash': 'solid', 'spikethickness': 1},
                         yaxis2 = {'title':'V', 'range': [0, 1000001], 'spikemode' : "across", 'showspikes': True, 'spikedash': 'solid', 'spikethickness': 1})
    offline.plot( fig, filename='solved.html')
