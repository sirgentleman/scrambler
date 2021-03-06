import csv
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns


data_path = sys.argv[1]
stats_file = sys.argv[2]

with open(data_path, 'r') as file:
    reader = csv.reader(file, delimiter=',')
    headers = next(reader)
    data = np.array(list(reader)).astype(int)

broken_packets = data[:, 0]

average = np.mean(broken_packets)
deviation = np.std(broken_packets)
quartiles = np.percentile(broken_packets, [25, 50, 75])
max_value = np.max(broken_packets)
min_value = np.min(broken_packets)

sns.set(style="ticks")

f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})

sns.boxplot(broken_packets, ax=ax_box)
sns.distplot(broken_packets, ax=ax_hist)

ax_box.set(yticks=[])
sns.despine(ax=ax_hist)
sns.despine(ax=ax_box, left=True)


#plt.set_title('Boxplot of broken packets')
#plt.boxplot(broken_packets)

# GENERATE HIStOGRAM
def function_model(x, mean, amplitude, std_deviation):
    return amplitude * np.exp( - ((x - mean) / std_deviation) ** 2)

n_points = int(headers[0])
n_bins = int(1 + np.floor(3.3*np.log(n_points)))


n, bins, patches = plt.hist(broken_packets, bins=n_bins)
bin_centers = bins[:-1] + np.diff(bins)/2
params, _ = curve_fit(function_model, bin_centers, n, p0=[average, 0, deviation])
x_interval_for_fit = np.linspace(bins[0], bins[-1], len(broken_packets))
plt.plot(x_interval_for_fit, function_model(x_interval_for_fit, *params), '--')

plt.title('Histogram of broken packets')
plt.ylabel('Repetitions')
plt.xlabel('Packets lost')

plt.savefig(sys.argv[2]+'.png')

with open(stats_file, 'w') as resultFile:
    resultFile.write('Measurments: ' + headers[0] + '\nPercentage of ones: ' + headers[1] + '\nPackets sent: ' + headers[2] + '\nPacket destroyed func: numberOfRepetitions * 2,5^(TypeOfRepetition -3)')
    resultFile.write('\nAverage packets broken: ' + str(average))
    resultFile.write('\nStandard deviation: ' + str(deviation))
    resultFile.write('\n\n\n\n\tFIVE-NUMBER SUMMARY\n')
    resultFile.write('\tQ0 (minimum) = ' + str(min_value))
    resultFile.write('\n\tQ1 = ' + str(quartiles[0]))
    resultFile.write('\n\tQ2 = ' + str(quartiles[1]))
    resultFile.write('\n\tQ3 = ' + str(quartiles[2]))
    resultFile.write('\n\tQ4 (maximum) = ' + str(max_value))
    #resultFile.write('\n\n\nFunction model\nMean = ' + str(params[0]) + '\nAmplitude = ' + str(params[1]) + '\nStandard deviation = ' + str(params[2]))
