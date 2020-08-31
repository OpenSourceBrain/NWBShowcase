
import matplotlib.pyplot as plt
import numpy

figsizeA=(12, 5)
plt.rc_context({'xtick.color':'white', 'ytick.color':'white'})
tr_fig, tr_ax = plt.subplots(figsize=figsizeA)
all_traces = None
for acq in nwbfile.acquisition.values():
    max_points = 10000
    if 'traces corrected' in acq.description and '' in acq.description:
        cell = acq.description.split(': ')[-1]
        ca = acq.data[:max_points]
        times = acq.timestamps[:max_points]

        tr_ax.plot(times, ca, lw=.5, label='%s'%cell)
        if all_traces is None:
            all_traces = numpy.array([ca])
        else:
            all_traces = numpy.concatenate((all_traces,[ca]), axis=0)

hm_fig, hm_ax = plt.subplots(figsize=figsizeA)
im = hm_ax.pcolormesh(all_traces, cmap='jet')
hm_fig.colorbar(im, ax=hm_ax)
plt.show()



!pip install sklearn


num_traces = all_traces.shape[0]

from sklearn import decomposition

n_components=10
pca = decomposition.PCA(n_components=n_components)
pca.fit(all_traces)
X = pca.transform(all_traces)


def to_dat(ts, xss, filename):
    f = open(filename, 'w')
    for i in range(len(ts)):
        f.write('%s'%(ts[i]))
        for xs in xss:
            f.write('\t%s'%(xs[i]))
        f.write('\n')
    f.close()
    
plt.figure()
pca_fig, pca_ax = plt.subplots(figsize=figsizeA)

pcomps = []
for trace_i in range(num_traces):
    #print('trace_i: %s, %s'%(trace_i,X[trace_i]))
    for comp_i in range(n_components):
        #print('  comp_i: %s, %s'%(comp_i, X[trace_i][comp_i]))
        trace = all_traces[trace_i]
        if trace_i ==0 :
            pcomps.append([0 for rr in trace])
        for t in range(len(trace)):
            pcomps[comp_i][t] += X[trace_i][comp_i] * trace[t]

for comp_i in range(n_components):                
    pca_ax.plot(times, pcomps[comp_i], lw=.5, label='PC%s'%(comp_i+1))
        
plt.legend()  
plt.show()
        
to_dat(times,pcomps,'split.dat')
            



# Import dependencies
import plotly
import plotly.graph_objs as go

# Configure Plotly to be rendered inline in the notebook.
plotly.offline.init_notebook_mode()

# Configure the trace.
trace = go.Scatter3d(
    x=pcomps[0],  # <-- Put your data instead
    y=pcomps[1],  # <-- Put your data instead
    z=pcomps[2],  # <-- Put your data instead
    mode='lines'
)

# Configure the layout.
layout = go.Layout(
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0},    
    scene = dict(
    xaxis = dict(
        title='PC1'),
    yaxis = dict(
        title='PC2'),
    zaxis = dict(
        title='PC3'),),
)
data = [trace]

plot_figure = go.Figure(data=data, layout=layout)

# Render the plot.
plotly.offline.iplot(plot_figure)