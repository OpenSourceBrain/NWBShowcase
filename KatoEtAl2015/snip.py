
import matplotlib.pyplot as plt
import numpy
plt.rc_context({'xtick.color':'white', 'ytick.color':'white'})
tr_fig, tr_ax = plt.subplots()
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

hm_fig, hm_ax = plt.subplots()
im = hm_ax.pcolormesh(all_traces, cmap='jet')
hm_fig.colorbar(im, ax=hm_ax)
plt.show()