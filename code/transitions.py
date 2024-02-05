import music21
import pickle
import pathlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable 
from mpl_toolkits.axes_grid1 import ImageGrid

palestrina_dir = pathlib.Path('data/midi/')
generated_dir = pathlib.Path('gen_midis/')

def matrix(x, y):

    m = []
    for iy in range(y):
        m.append([])
        for ix in range(x):
            m[iy].append(0)

    return m

def normalize(histogram:list):

    histogram = np.array(histogram)
    hist_max = np.max(histogram)
    return histogram / np.full(histogram.shape, hist_max) if hist_max > 0 else histogram
    
def get_transition_matrix(directory:pathlib.Path):

    NOTES = np.array(matrix(12,12))
    DURATIONS = np.array(matrix(16,16))

    for path in directory.iterdir():

        print('Processing:', path)

        pc_matrix = matrix(12,12) # create matrix 12 x 12 for all pitch classes.
        duration_matrix = matrix(16,16) # create matrix 16 x 16 for all durations (maxima, longa, brevis, semibrevis, minima, semiminima, fusa, semifusa AND their dotted versions)

        if path.suffix == '.mid' or path.suffix == '.midi':

            score = music21.converter.parse(path)
            pc_prev:list[int] = None
            dur_prev:int = None

            for note in score.flatten().notes: # or chord!

                # make heatmap
                pc:list = [pitch.pitchClass for pitch in note.pitches]
                dur = note.duration.ordinal * 2 - note.duration.dots - 1 if note.duration.ordinal != 'complex' else 0

                if pc_prev:
                    for pitch_class_prev in pc_prev:
                        for pitch_class in pc:
                            pc_matrix[pitch_class_prev][pitch_class] += 1

                if dur_prev:
                    duration_matrix[dur_prev][dur] += 1

                pc_prev = pc
                dur_prev = dur

        NOTES = NOTES + normalize(pc_matrix)
        DURATIONS = DURATIONS + normalize(duration_matrix)

    return normalize(NOTES), normalize(DURATIONS)

save_dir = pathlib.Path('data/statistics/transition_matrices')
heatmaps = pathlib.Path('data/statistics/transition_matrices.npz')
# notes1, durations1, histo1 = get_transition_matrix(palestrina_dir)
# notes2, durations2, histo2 = get_transition_matrix(generated_dir)
# np.savez(heatmaps, notes1, durations1, notes2, durations2)
# np.save(save_dir/'notes_palestrina', notes1)
# np.save(save_dir/'notes_model', notes2)
# np.save(save_dir/'durations_palestrina', durations1)
# np.save(save_dir/'durations_model', durations2)

# fig, axs = plt.subplots(ncols=6, gridspec_kw=dict(width_ratios=[4,4,0.2,4,4,0.2]))
# # fig.tight_layout(pad=0)

# h1 = sns.heatmap(notes1, cbar=False, ax=axs[0])
# h1.set_title('Palestrina')
# # h1.set_xticks(range(len(notes2)), pc_labels)
# # h1.set_yticks(range(len(notes2)), pc_labels)
# h2 = sns.heatmap(notes2, yticklabels=False, cbar=False, ax=axs[1])
# h2.set_title('Model')
# # h2.set_xticks(range(len(notes2)), pc_labels)
# # h2.set_yticks(range(len(notes2)), pc_labels)

# fig.colorbar(axs[1].collections[0], cax=axs[2])

# h3 = sns.heatmap(durations1, cbar=False, ax=axs[3])
# h3.set_title('Palestrina')
# # h3.set_xticks(range(len(durations2)), duration_labels)
# # h3.set_yticks(range(len(durations2)), duration_labels)
# h4 = sns.heatmap(durations2, yticklabels=False, cbar=False, ax=axs[4])
# h4.set_title('Model')
# # h4.set_xticks(range(len(durations2)), duration_labels)
# # h4.set_yticks(range(len(durations2)), duration_labels)

# fig.colorbar(axs[4].collections[0], cax=axs[5])

'''
    Create graph
'''

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Helvetica",
    'font.size': 4
})

pc_labels = ['C','','D','','E','F','','G','','A','','B']
# duration_labels = ['','','','','','','semibreveDotted','semibreve','minim','minimDotted','crotchetDotted','crotchet','quaverDotted','quaver','semiquaverDotted','semiquaver']
duration_labels = ['-2.','-2','-1.','-1','0.','0','1.','1','2.','2','4.','4','8.','8','16.', '16']

notes1, durations1, notes2, durations2 = np.load(heatmaps).values()

heatmaps = [notes1, notes2, durations1, durations2]
labels = [pc_labels, pc_labels, duration_labels, duration_labels]
titles = ["Palestrina's PCTM", "Model's PCTM", "Palestrina's NLTM", "Model's NLTM"]

fig, h = plt.subplots(1,4)

for ax, heatmap, label, title in zip(h.flat, heatmaps, labels, titles):
    im = ax.imshow(heatmap, vmin=0, vmax=1)
    ax.set_xticks(range(len(heatmap)), label)
    ax.set_yticks(range(len(heatmap)), label)
    ax.set_title(title)

cb = fig.colorbar(im, ax=h.ravel().tolist(), shrink=0.33)
cb.set_label('Normalized histogram')

# !!! next time maybe save the plots separately !!!
# (doesn't work well with .gpf files for LaTeX).
# plt.savefig('graphs/transition_heatmap.pdf', dpi=100, backend='pgf')
plt.savefig('graphs/transition_heatmap.pdf', dpi=500, bbox_inches='tight')

plt.show()