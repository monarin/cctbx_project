from __future__ import division

from libtbx.utils import null_out
from cStringIO import StringIO
from mmtbx.secondary_structure.find_ss_from_ca import find_secondary_structure
from libtbx import test_utils

def remove_blank(text):
  return text.replace(" ","").replace("\n","")

two_chain_helix_ss="""
HELIX    1   1 ALA A   15  LYS A   21  1                                   7
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  N  ILE B 280   O  ILE A  51
"""
bad_two_chain_helix_ss="""
HELIX    1   1 ALA A   15  LYS A   21  1                                   7
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  N  ILE B 278   O  ILE A  51
"""

bad_two_chain_helix_ss_correct_resname="""
HELIX    1   1 ALA A   15  LYS A   21  1                                   7
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  N  LEU B 278   O  ILE A  51
"""

antiparallel_text="""
ATOM      1  N   LEU A  95      19.823   2.447 -20.604  1.00  4.22           N
ATOM      2  CA  LEU A  95      19.411   3.491 -19.655  1.00  4.09           C
ATOM      3  C   LEU A  95      20.437   3.482 -18.522  1.00  4.12           C
ATOM      4  O   LEU A  95      20.764   2.410 -18.006  1.00  4.68           O
ATOM      5  CB  LEU A  95      18.007   3.186 -19.075  1.00  4.63           C
ATOM      9  N   LEU A  96      20.911   4.667 -18.125  1.00  4.11           N
ATOM     10  CA  LEU A  96      21.872   4.787 -17.025  1.00  4.27           C
ATOM     11  C   LEU A  96      21.308   5.812 -16.028  1.00  4.14           C
ATOM     12  O   LEU A  96      21.044   6.956 -16.404  1.00  4.78           O
ATOM     13  CB ALEU A  96      23.225   5.220 -17.574  0.50  4.58           C
ATOM     21  N   ARG A  97      21.144   5.374 -14.766  1.00  3.77           N
ATOM     22  CA  ARG A  97      20.820   6.284 -13.673  1.00  3.69           C
ATOM     23  C   ARG A  97      22.056   6.437 -12.774  1.00  3.41           C
ATOM     24  O   ARG A  97      22.651   5.441 -12.329  1.00  4.05           O
ATOM     25  CB  ARG A  97      19.612   5.796 -12.851  1.00  3.79           C
ATOM     32  N   PHE A  98      22.413   7.695 -12.516  1.00  3.36           N
ATOM     33  CA  PHE A  98      23.473   8.085 -11.601  1.00  3.42           C
ATOM     34  C   PHE A  98      22.827   8.597 -10.306  1.00  3.34           C
ATOM     35  O   PHE A  98      21.699   9.092 -10.321  1.00  3.88           O
ATOM     36  CB  PHE A  98      24.260   9.271 -12.203  1.00  3.74           C
ATOM     43  N   PHE A 117      25.991   3.957 -10.490  1.00  3.61           N
ATOM     44  CA  PHE A 117      26.196   3.832 -11.931  1.00  3.74           C
ATOM     45  C   PHE A 117      25.339   2.627 -12.381  1.00  3.68           C
ATOM     46  O   PHE A 117      25.850   1.516 -12.565  1.00  4.07           O
ATOM     47  CB  PHE A 117      27.700   3.629 -12.215  1.00  4.23           C
ATOM     54  N   ALA A 118      24.027   2.850 -12.466  1.00  3.64           N
ATOM     55  CA  ALA A 118      23.056   1.773 -12.686  1.00  3.60           C
ATOM     56  C   ALA A 118      22.714   1.712 -14.176  1.00  3.63           C
ATOM     57  O   ALA A 118      22.072   2.613 -14.700  1.00  4.10           O
ATOM     58  CB  ALA A 118      21.797   2.030 -11.857  1.00  4.08           C
ATOM     59  N   LEU A 119      23.182   0.650 -14.842  1.00  3.81           N
ATOM     60  CA  LEU A 119      23.136   0.560 -16.297  1.00  3.98           C
ATOM     61  C   LEU A 119      22.282  -0.621 -16.738  1.00  4.00           C
ATOM     62  O   LEU A 119      22.608  -1.781 -16.475  1.00  5.33           O
ATOM     63  CB  LEU A 119      24.577   0.411 -16.837  1.00  4.22           C
ATOM     67  N   ARG A 120      21.209  -0.315 -17.470  1.00  3.85           N
ATOM     68  CA  ARG A 120      20.357  -1.332 -18.102  1.00  3.95           C
ATOM     69  C   ARG A 120      20.680  -1.407 -19.584  1.00  3.95           C
ATOM     70  O   ARG A 120      20.778  -0.387 -20.282  1.00  4.48           O
ATOM     71  CB  ARG A 120      18.872  -0.947 -17.952  1.00  4.12           C
"""
antiparallel_ss="""
SHEET    1   1 2 LEU A  95  PHE A  98  0
SHEET    2   1 2 PHE A 117  ARG A 120 -1  N  ARG A 120   O  LEU A  95
"""
ss_text="""
HELIX    1   1 ALA A   15  LYS A   21  1                                   7
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  N  ILE B 280   O  ILE A  51
"""

std_text="""
ATOM      2  CA  THRAa   3     186.743 125.884 251.259  1.00100.00           C
ATOM      5  CA  ASNAa   4     189.629 123.742 252.763  1.00100.00           C
ATOM      8  CA  SERAa   5     191.072 126.112 255.320  1.00100.00           C
ATOM     11  CA  ASPAa   6     192.080 124.928 258.848  1.00100.00           C
ATOM     14  CA  PHEAa   7     189.384 124.585 261.530  1.00100.00           C
ATOM     17  CA  VALAa   8     189.248 124.466 265.315  1.00100.00           C
ATOM     20  CA  VALAa   9     187.059 122.294 267.547  1.00100.00           C
ATOM     23  CA  ILEAa  10     185.534 123.893 270.679  1.00100.00           C
ATOM     26  CA  LYSAa  11     183.570 122.134 273.450  1.00100.00           C
ATOM     29  CA  ALAAa  12     181.897 124.298 276.085  1.00100.00           C
ATOM     32  CA  LEUAa  13     182.733 123.145 279.601  1.00100.00           C
ATOM     35  CA  GLUAa  14     180.241 125.609 281.156  1.00100.00           C
ATOM     38  CA  ASPAa  15     177.155 127.540 279.985  1.00100.00           C
ATOM     41  CA  GLYAa  16     177.637 130.843 278.162  1.00100.00           C
ATOM     44  CA  VALAa  17     180.958 130.212 276.395  1.00100.00           C
ATOM     47  CA  ASNAa  18     181.477 132.715 273.547  1.00100.00           C
ATOM     50  CA  VALAa  19     183.320 131.753 270.320  1.00100.00           C
ATOM     53  CA  ILEAa  20     184.043 135.156 268.674  1.00100.00           C
ATOM     56  CA  GLYAa  21     185.054 135.558 264.994  1.00100.00           C
ATOM     59  CA  LEUAa  22     187.345 138.529 264.419  1.00100.00           C
ATOM     62  CA  THRAa  23     187.310 140.218 261.033  1.00100.00           C
ATOM     65  CA  ARGAa  24     189.831 139.523 258.335  1.00100.00           C
ATOM     68  CA  GLYAa  25     191.359 142.673 256.805  1.00100.00           C
ATOM     71  CA  ALAAa  26     192.794 146.041 257.837  1.00100.00           C
ATOM     74  CA  ASPAa  27     190.126 146.289 260.564  1.00100.00           C
ATOM     77  CA  THRAa  28     189.912 143.928 263.570  1.00100.00           C
ATOM     80  CA  ARGAa  29     186.413 143.856 265.033  1.00100.00           C
ATOM     83  CA  PHEAa  30     183.873 141.240 266.091  1.00100.00           C
ATOM     86  CA  HISAa  31     181.625 140.079 263.343  1.00100.00           C
ATOM     89  CA  HISAa  32     179.931 137.209 265.203  1.00100.00           C
ATOM     92  CA  SERAa  33     179.805 135.702 268.677  1.00100.00           C
ATOM     95  CA  GLUAa  34     178.501 132.109 268.857  1.00100.00           C
ATOM     98  CA  CYSAa  35     177.222 131.284 272.342  1.00100.00           C
ATOM    101  CA  LEUAa  36     177.646 127.700 273.502  1.00100.00           C
ATOM    104  CA  ASPAa  37     175.969 125.990 276.438  1.00100.00           C
ATOM    107  CA  LYSAa  38     177.682 123.298 278.488  1.00100.00           C
ATOM    110  CA  GLYAa  39     178.623 120.300 276.385  1.00100.00           C
ATOM    113  CA  GLUAa  40     177.892 121.761 272.941  1.00100.00           C
ATOM    116  CA  VALAa  41     180.597 121.439 270.276  1.00100.00           C
ATOM    119  CA  LEUAa  42     181.492 123.998 267.594  1.00100.00           C
ATOM    122  CA  ILEAa  43     183.793 123.155 264.645  1.00100.00           C
ATOM    125  CA  ALAAa  44     184.701 126.388 262.889  1.00100.00           C
ATOM    128  CA  GLNAa  45     186.987 127.209 259.959  1.00100.00           C
ATOM    131  CA  PHEAa  46     189.115 130.161 259.157  1.00100.00           C
ATOM    134  CA  THRAa  47     187.356 131.901 256.203  1.00100.00           C
ATOM    137  CA  GLUAa  48     187.180 134.953 253.965  1.00100.00           C
ATOM    140  CA  HISAa  49     185.578 136.805 256.905  1.00100.00           C
ATOM    143  CA  THRAa  50     187.343 135.292 259.938  1.00100.00           C
ATOM    146  CA  SERAa  51     191.129 135.327 260.339  1.00100.00           C
ATOM    149  CA  ALAAa  52     191.231 135.094 264.170  1.00100.00           C
ATOM    152  CA  ILEAa  53     188.989 133.390 266.744  1.00100.00           C
ATOM    155  CA  LYSAa  54     188.770 134.368 270.428  1.00100.00           C
ATOM    158  CA  VALAa  55     187.303 131.970 273.016  1.00100.00           C
ATOM    161  CA  ARGAa  56     185.817 133.382 276.214  1.00100.00           C
ATOM    164  CA  GLYAa  57     184.672 131.065 278.997  1.00100.00           C
ATOM    167  CA  LYSAa  58     185.698 127.553 280.004  1.00100.00           C
ATOM    170  CA  ALAAa  59     186.172 125.294 276.966  1.00100.00           C
ATOM    173  CA  TYRAa  60     188.258 122.444 275.620  1.00100.00           C
ATOM    176  CA  ILEAa  61     189.863 123.277 272.265  1.00100.00           C
ATOM    179  CA  GLNAa  62     191.492 121.098 269.577  1.00100.00           C
ATOM    182  CA  THRAa  63     193.550 122.431 266.653  1.00100.00           C
ATOM    185  CA  ARGAa  64     196.271 121.116 264.358  1.00100.00           C
ATOM    188  CA  HISAa  65     198.826 122.305 266.995  1.00100.00           C
ATOM    191  CA  GLYAa  66     197.443 120.330 269.914  1.00100.00           C
ATOM    194  CA  VALAa  67     194.865 120.679 272.646  1.00100.00           C
ATOM    197  CA  ILEAa  68     194.232 123.486 275.120  1.00100.00           C
ATOM    200  CA  GLUAa  69     191.576 124.693 277.564  1.00100.00           C
ATOM    203  CA  SERAa  70     190.301 128.219 277.907  1.00100.00           C
ATOM    206  CA  GLUAa  71     189.167 129.249 281.377  1.00100.00           C
ATOM    209  CA  GLYAa  72     186.003 131.073 282.428  1.00100.00           C
"""

helices_text="""
ATOM      2  CA  ALA A   1      11.323  32.055  11.635  1.00 40.00           C
ATOM      7  CA  ALA A   2       8.288  29.768  10.916  1.00 40.00           C
ATOM     12  CA  ALA A   3      10.313  27.854   8.231  1.00 40.00           C
ATOM     17  CA  ALA A   4      13.089  27.116  10.822  1.00 40.00           C
ATOM     22  CA  ALA A   5      10.573  25.488  13.298  1.00 40.00           C
ATOM     27  CA  ALA A   6       9.258  23.514  10.260  1.00 40.00           C
ATOM     32  CA  ALA A   7      12.788  22.543   8.962  1.00 40.00           C
ATOM     37  CA  ALA A   8      13.846  21.459  12.515  1.00 40.00           C
ATOM     42  CA  ALA A   9      10.716  19.261  12.994  1.00 40.00           C
ATOM     47  CA  ALA A  10      11.063  17.985   9.357  1.00 40.00           C
ATOM     52  CA  ALA A  11      14.754  17.018   9.967  1.00 40.00           C
ATOM     57  CA  ALA A  12      13.721  15.483  13.371  1.00 40.00           C
ATOM     62  CA  ALA A  13      10.821  13.516  11.708  1.00 40.00           C
ATOM     67  CA  ALA A  14      13.246  12.367   8.939  1.00 40.00           C
ATOM     72  CA  ALA A  15      15.847  11.407  11.629  1.00 40.00           C
ATOM     77  CA  ALA A  16      13.099   9.317  13.370  1.00 40.00           C
ATOM      2  CA  ALA B   2       1.733  -3.620  -2.296  1.00  1.00
ATOM      7  CA  ALA B   3      -1.902  -4.065  -1.341  1.00  1.00
ATOM     12  CA  ALA B   4      -2.941  -0.441  -1.685  1.00  1.00
ATOM     17  CA  ALA B   5      -0.320   0.578  -4.218  1.00  1.00
ATOM     22  CA  ALA B   6       0.221  -2.836  -5.759  1.00  1.00
ATOM     27  CA  ALA B   7      -3.192  -4.271  -4.973  1.00  1.00
ATOM     32  CA  ALA B   8      -5.081  -0.993  -4.849  1.00  1.00
ATOM     37  CA  ALA B   9      -2.802   0.969  -7.148  1.00  1.00
ATOM     42  CA  ALA B  10      -1.460  -1.967  -9.123  1.00  1.00
ATOM     47  CA  ALA B  11      -4.418  -4.277  -8.632  1.00  1.00
ATOM     52  CA  ALA B  12      -7.044  -1.601  -8.116  1.00  1.00
ATOM     57  CA  ALA B  13      -5.323   1.151 -10.064  1.00  1.00
ATOM     62  CA  ALA B  14      -3.322  -1.073 -12.383  1.00  1.00
ATOM     67  CA  ALA B  15      -5.629  -4.072 -12.291  1.00  1.00
ATOM     72  CA  ALA B  16      -8.822  -2.205 -11.488  1.00  1.00
ATOM     77  CA  ALA B  17      -7.833   1.122 -12.996  1.00  1.00
ATOM     82  CA  ALA B  18      -5.368  -0.211 -15.540  1.00  1.00
ATOM     87  CA  ALA B  19      -6.878  -3.661 -15.920  1.00  1.00
ATOM     92  CA  ALA B  20     -10.423  -2.748 -14.958  1.00  1.00
ATOM     97  CA  ALA B  21     -10.280   0.896 -15.972  1.00  1.00
ATOM    102  CA  ALA B  22      -7.582   0.562 -18.606  1.00  1.00
ATOM      2  CA  ALA C   2       1.202  -3.661  -1.646  1.00  1.00           C
ATOM      7  CA  ALA C   3      -1.466  -2.408  -4.020  1.00  1.00           C
ATOM     12  CA  ALA C   4       1.288  -2.503  -6.614  1.00  1.00           C
ATOM     17  CA  ALA C   5       0.312  -6.139  -7.010  1.00  1.00           C
ATOM     22  CA  ALA C   6      -2.284  -4.816  -9.426  1.00  1.00           C
ATOM     27  CA  ALA C   7       0.502  -5.008 -11.981  1.00  1.00           C
ATOM     32  CA  ALA C   8      -0.579  -8.614 -12.375  1.00  1.00           C
ATOM     37  CA  ALA C   9      -3.100  -7.225 -14.833  1.00  1.00           C
ATOM     42  CA  ALA C  10      -0.285  -7.514 -17.347  1.00  1.00           C
ATOM     47  CA  ALA C  11      -1.470 -11.087 -17.740  1.00  1.00           C
ATOM     52  CA  ALA C  12      -3.913  -9.634 -20.239  1.00  1.00           C
ATOM     57  CA  ALA C  13      -1.074 -10.021 -22.713  1.00  1.00           C
ATOM     62  CA  ALA C  14      -2.362 -13.558 -23.106  1.00  1.00           C
ATOM     67  CA  ALA C  15      -4.725 -12.045 -25.646  1.00  1.00           C
ATOM     72  CA  ALA C  16      -1.865 -12.529 -28.077  1.00  1.00           C
ATOM     77  CA  ALA C  17      -3.254 -16.028 -28.473  1.00  1.00           C
ATOM     82  CA  ALA C  18      -5.534 -14.456 -31.052  1.00  1.00           C
ATOM     87  CA  ALA C  19      -2.657 -15.038 -33.442  1.00  1.00           C
ATOM     92  CA  ALA C  20      -4.146 -18.495 -33.840  1.00  1.00           C
ATOM     97  CA  ALA C  21      -6.342 -16.867 -36.458  1.00  1.00           C
ATOM    102  CA  ALA C  22      -3.451 -17.549 -38.805  1.00  1.00           C
"""

one_full_helix_text="""
ATOM      1  N   ALA A  15      29.207  -2.952  12.868  1.00 16.39           N
ATOM      2  CA  ALA A  15      27.822  -3.418  12.724  1.00 17.10           C
ATOM      3  C   ALA A  15      27.023  -3.016  13.951  1.00 16.98           C
ATOM      4  O   ALA A  15      25.872  -2.551  13.769  1.00 16.78           O
ATOM      5  N   LEU A  16      27.570  -3.117  15.127  1.00 15.97           N
ATOM      6  CA  LEU A  16      26.958  -2.649  16.351  1.00 18.20           C
ATOM      7  C   LEU A  16      26.614  -1.169  16.344  1.00 20.28           C
ATOM      8  O   LEU A  16      25.599  -0.734  16.933  1.00 18.32           O
ATOM      9  N   ILE A  17      27.514  -0.365  15.791  1.00 20.97           N
ATOM     10  CA  ILE A  17      27.343   1.056  15.618  1.00 20.41           C
ATOM     11  C   ILE A  17      26.081   1.392  14.758  1.00 18.17           C
ATOM     12  O   ILE A  17      25.380   2.240  15.282  1.00 16.46           O
ATOM     13  N   SER A  18      25.930   0.759  13.657  1.00 16.97           N
ATOM     14  CA  SER A  18      24.825   0.827  12.744  1.00 19.98           C
ATOM     15  C   SER A  18      23.499   0.405  13.438  1.00 18.89           C
ATOM     16  O   SER A  18      22.557   1.165  13.352  1.00 18.37           O
ATOM     17  N   TRP A  19      23.512  -0.661  14.161  1.00 17.71           N
ATOM     18  CA  TRP A  19      22.492  -1.085  15.081  1.00 15.72           C
ATOM     19  C   TRP A  19      22.083   0.004  16.012  1.00 18.02           C
ATOM     20  O   TRP A  19      20.820   0.244  16.160  1.00 16.93           O
ATOM     21  N   ILE A  20      22.930   0.594  16.823  1.00 14.82           N
ATOM     22  CA  ILE A  20      22.628   1.633  17.766  1.00 15.67           C
ATOM     23  C   ILE A  20      21.917   2.819  17.080  1.00 17.51           C
ATOM     24  O   ILE A  20      20.942   3.365  17.655  1.00 17.70           O
ATOM     25  N   LYS A  21      22.464   3.177  15.957  1.00 16.61           N
ATOM     26  CA  LYS A  21      21.888   4.236  15.157  1.00 19.84           C
ATOM     27  C   LYS A  21      20.436   3.910  14.752  1.00 21.02           C
ATOM     28  O   LYS A  21      19.685   4.899  14.971  1.00 22.80           O
"""
one_helix_beginning_text="""
ATOM      2  CA  ALA A   1      11.323  32.055  11.635  1.00 40.00           C
ATOM      7  CA  ALA A   2       8.288  29.768  10.916  1.00 40.00           C
ATOM     12  CA  ALA A   3      10.313  27.854   8.231  1.00 40.00           C
ATOM     17  CA  ALA A   4      13.089  27.116  10.822  1.00 40.00           C
ATOM     22  CA  ALA A   5      10.573  25.488  13.298  1.00 40.00           C
ATOM     27  CA  ALA A   6       9.258  23.514  10.260  1.00 40.00           C
ATOM     32  CA  ALA A   7      12.788  22.543   8.962  1.00 40.00           C
ATOM     37  CA  ALA A   8      13.846  21.459  12.515  1.00 40.00           C
"""
one_helix_end_text="""
ATOM     42  CA  ALA A   9      10.716  19.261  12.994  1.00 40.00           C
ATOM     47  CA  ALA A  10      11.063  17.985   9.357  1.00 40.00           C
ATOM     52  CA  ALA A  11      14.754  17.018   9.967  1.00 40.00           C
ATOM     57  CA  ALA A  12      13.721  15.483  13.371  1.00 40.00           C
ATOM     62  CA  ALA A  13      10.821  13.516  11.708  1.00 40.00           C
ATOM     67  CA  ALA A  14      13.246  12.367   8.939  1.00 40.00           C
ATOM     72  CA  ALA A  15      15.847  11.407  11.629  1.00 40.00           C
ATOM     77  CA  ALA A  16      13.099   9.317  13.370  1.00 40.00           C
"""
one_helix_middle_text="""
ATOM     22  CA  ALA A   5      10.573  25.488  13.298  1.00 40.00           C
ATOM     27  CA  ALA A   6       9.258  23.514  10.260  1.00 40.00           C
ATOM     32  CA  ALA A   7      12.788  22.543   8.962  1.00 40.00           C
ATOM     37  CA  ALA A   8      13.846  21.459  12.515  1.00 40.00           C
ATOM     42  CA  ALA A   9      10.716  19.261  12.994  1.00 40.00           C
ATOM     47  CA  ALA A  10      11.063  17.985   9.357  1.00 40.00           C
ATOM     52  CA  ALA A  11      14.754  17.018   9.967  1.00 40.00           C
ATOM     57  CA  ALA A  12      13.721  15.483  13.371  1.00 40.00           C
ATOM     62  CA  ALA A  13      10.821  13.516  11.708  1.00 40.00           C
"""
one_helix_text="""
ATOM      2  CA  ALA A   1      11.323  32.055  11.635  1.00 40.00           C
ATOM      7  CA  ALA A   2       8.288  29.768  10.916  1.00 40.00           C
ATOM     12  CA  ALA A   3      10.313  27.854   8.231  1.00 40.00           C
ATOM     17  CA  ALA A   4      13.089  27.116  10.822  1.00 40.00           C
ATOM     22  CA  ALA A   5      10.573  25.488  13.298  1.00 40.00           C
ATOM     27  CA  ALA A   6       9.258  23.514  10.260  1.00 40.00           C
ATOM     32  CA  ALA A   7      12.788  22.543   8.962  1.00 40.00           C
ATOM     37  CA  ALA A   8      13.846  21.459  12.515  1.00 40.00           C
ATOM     42  CA  ALA A   9      10.716  19.261  12.994  1.00 40.00           C
ATOM     47  CA  ALA A  10      11.063  17.985   9.357  1.00 40.00           C
ATOM     52  CA  ALA A  11      14.754  17.018   9.967  1.00 40.00           C
ATOM     57  CA  ALA A  12      13.721  15.483  13.371  1.00 40.00           C
ATOM     62  CA  ALA A  13      10.821  13.516  11.708  1.00 40.00           C
ATOM     67  CA  ALA A  14      13.246  12.367   8.939  1.00 40.00           C
ATOM     72  CA  ALA A  15      15.847  11.407  11.629  1.00 40.00           C
ATOM     77  CA  ALA A  16      13.099   9.317  13.370  1.00 40.00           C
"""

two_helix_text="""
ATOM      2  CA  GLY A   1      43.603 -11.488  24.325  1.00 35.57
ATOM      6  CA  ILE A   2      44.200  -8.183  22.475  1.00 27.55
ATOM     14  CA  GLY A   3      43.999 -10.264  19.329  1.00 21.05
ATOM     18  CA  ALA A   4      40.378 -11.260  20.106  1.00 21.80
ATOM     23  CA  VAL A   5      39.355  -7.658  21.083  1.00 19.34
ATOM     30  CA  LEU A   6      41.062  -6.432  17.957  1.00 17.59
ATOM     38  CA  LYS A   7      39.079  -8.646  15.636  1.00 22.55
ATOM     47  CA  VAL A   8      35.792  -7.369  17.211  1.00 20.52
ATOM     69  CA  THR A  11      34.132  -6.405  12.343  1.00 24.14
ATOM     76  CA  GLY A  12      31.584  -6.595  15.140  1.00 24.17
ATOM     80  CA  LEU A  13      31.923  -2.919  16.364  1.00 23.24
ATOM     88  CA  PRO A  14      31.026  -1.278  13.030  1.00 17.52
ATOM     95  CA  ALA A  15      27.822  -3.418  12.724  1.00 17.10
ATOM    100  CA  LEU A  16      26.958  -2.649  16.351  1.00 18.20
ATOM    108  CA  ILE A  17      27.343   1.056  15.618  1.00 20.41
ATOM    116  CA  SER A  18      24.825   0.827  12.744  1.00 19.98
ATOM    122  CA  TRP A  19      22.492  -1.085  15.081  1.00 15.72
ATOM    136  CA  ILE A  20      22.628   1.633  17.766  1.00 15.67
ATOM    144  CA  LYS A  21      21.888   4.236  15.157  1.00 19.84
ATOM    153  CA  ARG A  22      18.740   2.273  14.020  1.00 20.38
ATOM    164  CA  LYS A  23      17.500   1.928  17.550  1.00 22.62
ATOM    173  CA  ARG A  24      18.059   5.674  18.276  1.00 27.11
ATOM    184  CA  GLN A  25      15.836   6.730  15.339  1.00 37.50
ATOM    193  CA  GLN A  26      13.132   4.360  16.583  1.00 46.66
"""

two_chain_text="""
ATOM    375  N   TYR A  50       6.211 -13.569   8.292  1.00 10.98           N
ATOM    376  CA  TYR A  50       7.318 -12.627   8.487  1.00 10.61           C
ATOM    377  C   TYR A  50       6.766 -11.320   9.020  1.00  9.44           C
ATOM    378  O   TYR A  50       5.608 -10.952   8.800  1.00 10.44           O
ATOM    379  CB  TYR A  50       8.112 -12.427   7.166  1.00 11.77           C
ATOM    380  CG  TYR A  50       8.994 -13.649   6.910  1.00 14.04           C
ATOM    381  CD1 TYR A  50       8.495 -14.805   6.394  1.00 14.79           C
ATOM    382  CD2 TYR A  50      10.334 -13.645   7.280  1.00 15.78           C
ATOM    383  CE1 TYR A  50       9.309 -15.912   6.201  1.00 16.35           C
ATOM    384  CE2 TYR A  50      11.185 -14.715   7.104  1.00 17.74           C
ATOM    385  CZ  TYR A  50      10.649 -15.862   6.545  1.00 17.61           C
ATOM    386  OH  TYR A  50      11.444 -16.974   6.380  1.00 22.90           O
ATOM    387  N   ILE A  51       7.626 -10.601   9.716  1.00  9.43           N
ATOM    388  CA  ILE A  51       7.269  -9.357  10.407  1.00  8.71           C
ATOM    389  C   ILE A  51       7.916  -8.211   9.657  1.00  8.94           C
ATOM    390  O   ILE A  51       9.112  -7.923   9.789  1.00  9.49           O
ATOM    391  CB  ILE A  51       7.636  -9.391  11.898  1.00  9.57           C
ATOM    392  CG1 ILE A  51       6.877 -10.489  12.634  1.00 11.51           C
ATOM    393  CG2 ILE A  51       7.340  -8.025  12.509  1.00  9.99           C
ATOM    394  CD1 ILE A  51       7.189 -11.913  12.447  1.00 13.04           C
ATOM    395  N   TYR A  52       7.103  -7.549   8.818  1.00  8.87           N
ATOM    396  CA  TYR A  52       7.523  -6.401   8.024  1.00  8.95           C
ATOM    397  C   TYR A  52       7.566  -5.196   8.933  1.00  8.79           C
ATOM    398  O   TYR A  52       6.546  -4.870   9.560  1.00  9.43           O
ATOM    399  CB  TYR A  52       6.599  -6.227   6.809  1.00  9.82           C
ATOM    400  CG  TYR A  52       6.769  -7.352   5.826  1.00  9.77           C
ATOM    401  CD1 TYR A  52       6.171  -8.583   6.037  1.00 10.04           C
ATOM    402  CD2 TYR A  52       7.581  -7.227   4.699  1.00 11.49           C
ATOM    403  CE1 TYR A  52       6.330  -9.627   5.177  1.00 11.90           C
ATOM    404  CE2 TYR A  52       7.751  -8.274   3.800  1.00 12.84           C
ATOM    405  CZ  TYR A  52       7.116  -9.468   4.045  1.00 12.86           C
ATOM    406  OH  TYR A  52       7.270 -10.516   3.193  1.00 14.57           O
ATOM    407  N   THR A  53       8.737  -4.586   9.055  1.00  8.30           N
ATOM    408  CA  THR A  53       8.996  -3.643  10.133  1.00  8.29           C
ATOM    409  C   THR A  53       9.384  -2.299   9.550  1.00  8.26           C
ATOM    410  O   THR A  53      10.386  -2.196   8.794  1.00 10.05           O
ATOM    411  CB  THR A  53      10.098  -4.225  11.054  1.00  9.01           C
ATOM    412  OG1 THR A  53       9.695  -5.497  11.548  1.00  9.73           O
ATOM    413  CG2 THR A  53      10.340  -3.320  12.250  1.00 10.75           C
ATOM    414  N   TYR A  54       8.595  -1.292   9.883  1.00  8.50           N
ATOM    415  CA  TYR A  54       8.688   0.046   9.368  1.00  8.54           C
ATOM    416  C   TYR A  54       9.130   0.977  10.480  1.00  9.00           C
ATOM    417  O   TYR A  54       8.469   1.106  11.537  1.00  9.89           O
ATOM    418  CB  TYR A  54       7.350   0.517   8.786  1.00  9.33           C
ATOM    419  CG  TYR A  54       6.866  -0.378   7.660  1.00  9.22           C
ATOM    420  CD1 TYR A  54       6.113  -1.523   7.899  1.00  9.26           C
ATOM    421  CD2 TYR A  54       7.207  -0.083   6.368  1.00  9.45           C
ATOM    422  CE1 TYR A  54       5.683  -2.351   6.899  1.00  9.56           C
ATOM    423  CE2 TYR A  54       6.783  -0.929   5.368  1.00 10.19           C
ATOM    424  CZ  TYR A  54       6.039  -2.054   5.609  1.00  9.31           C
ATOM    425  OH  TYR A  54       5.593  -2.884   4.606  1.00 10.62           O
ATOM    426  N   ARG A  55      10.273   1.635  10.317  1.00  8.99           N
ATOM    427  CA  ARG A  55      10.779   2.540  11.331  1.00  9.30           C
ATOM    428  C   ARG A  55      10.006   3.855  11.284  1.00  9.04           C
ATOM    429  O   ARG A  55       9.809   4.438  10.215  1.00 10.80           O
ATOM    430  CB  ARG A  55      12.255   2.778  11.090  1.00  9.60           C
ATOM    431  CG  ARG A  55      13.089   1.503  11.251  1.00 11.09           C
ATOM    432  CD  ARG A  55      14.531   1.724  10.963  1.00 12.60           C
ATOM    433  NE  ARG A  55      15.393   0.536  10.991  1.00 12.79           N
ATOM    434  CZ  ARG A  55      15.853  -0.067   9.907  1.00 11.24           C
ATOM    435  NH1 ARG A  55      15.601   0.267   8.635  1.00 13.70           N
ATOM    436  NH2 ARG A  55      16.683  -1.110  10.084  1.00 12.83           N
ATOM    437  N   VAL A  56       9.574   4.315  12.463  1.00  9.17           N
ATOM    438  CA  VAL A  56       8.706   5.468  12.645  1.00  9.47           C
ATOM    439  C   VAL A  56       9.399   6.439  13.577  1.00  9.55           C
ATOM    440  O   VAL A  56       9.819   6.065  14.671  1.00 11.35           O
ATOM    441  CB  VAL A  56       7.334   5.020  13.148  1.00 10.23           C
ATOM    442  CG1 VAL A  56       6.464   6.185  13.566  1.00 13.31           C
ATOM    443  CG2 VAL A  56       6.623   4.148  12.100  1.00 11.48           C
ATOM    444  N   SER A  57       9.486   7.688  13.122  1.00 10.07           N
ATOM    445  CA  SER A  57      10.220   8.739  13.797  1.00 11.56           C
ATOM    446  C   SER A  57       9.413  10.020  13.948  1.00 10.72           C
ATOM    447  O   SER A  57       8.594  10.296  13.076  1.00 10.93           O
ATOM    448  CB  SER A  57      11.541   9.078  13.005  1.00 13.02           C
ATOM    449  OG  SER A  57      12.275   7.871  12.757  1.00 16.49           O
ATOM    877  N   LEU B 278      13.003 -13.579  11.217  1.00 14.16           N
ATOM    878  CA  LEU B 278      11.645 -13.391  10.746  1.00 13.77           C
ATOM    879  C   LEU B 278      11.240 -11.932  10.544  1.00 12.73           C
ATOM    880  O   LEU B 278      10.118 -11.639  10.140  1.00 19.80           O
ATOM    881  CB  LEU B 278      10.621 -14.010  11.721  1.00 17.07           C
ATOM    882  CG  LEU B 278      10.887 -15.612  11.784  1.00 20.72           C
ATOM    883  CD1 LEU B 278       9.743 -16.058  12.768  1.00 26.78           C
ATOM    884  CD2 LEU B 278      10.513 -16.229  10.192  1.00 22.51           C
ATOM    885  N   THR B 279      12.124 -11.019  10.844  1.00 10.85           N
ATOM    886  CA  THR B 279      11.888  -9.580  10.658  1.00 10.91           C
ATOM    887  C   THR B 279      12.501  -9.102   9.356  1.00 11.12           C
ATOM    888  O   THR B 279      13.671  -9.407   9.078  1.00 12.89           O
ATOM    889  CB  THR B 279      12.517  -8.801  11.813  1.00 10.60           C
ATOM    890  OG1 THR B 279      11.721  -8.935  12.994  1.00 11.57           O
ATOM    891  CG2 THR B 279      12.676  -7.301  11.552  1.00 12.09           C
ATOM    892  N   ILE B 280      11.699  -8.402   8.572  1.00 10.77           N
ATOM    893  CA  ILE B 280      12.101  -7.808   7.306  1.00 10.70           C
ATOM    894  C   ILE B 280      11.929  -6.297   7.452  1.00  9.56           C
ATOM    895  O   ILE B 280      10.802  -5.815   7.480  1.00 11.05           O
ATOM    896  CB  ILE B 280      11.283  -8.353   6.135  1.00 11.04           C
ATOM    897  CG1 ILE B 280      11.443  -9.854   5.977  1.00 12.99           C
ATOM    898  CG2 ILE B 280      11.674  -7.630   4.848  1.00 13.91           C
ATOM    899  CD1 ILE B 280      10.627 -10.530   4.933  1.00 15.29           C
ATOM    900  N   TYR B 281      13.017  -5.563   7.612  1.00  9.95           N
ATOM    901  CA  TYR B 281      12.918  -4.104   7.622  1.00 10.00           C
ATOM    902  C   TYR B 281      12.476  -3.631   6.240  1.00 10.83           C
ATOM    903  O   TYR B 281      13.016  -4.065   5.216  1.00 13.82           O
ATOM    904  CB  TYR B 281      14.242  -3.422   8.111  1.00 11.29           C
ATOM    905  CG  TYR B 281      14.359  -3.643   9.634  1.00 11.38           C
ATOM    906  CD1 TYR B 281      15.128  -4.632  10.167  1.00 12.02           C
ATOM    907  CD2 TYR B 281      13.622  -2.828  10.483  1.00 12.75           C
ATOM    908  CE1 TYR B 281      15.185  -4.790  11.579  1.00 12.84           C
ATOM    909  CE2 TYR B 281      13.646  -2.973  11.857  1.00 13.88           C
ATOM    910  CZ  TYR B 281      14.427  -3.954  12.373  1.00 14.15           C
ATOM    911  OH  TYR B 281      14.404  -4.084  13.775  1.00 16.24           O
ATOM    912  N   ALA B 282      11.500  -2.767   6.208  1.00 10.01           N
ATOM    913  CA  ALA B 282      10.815  -2.397   4.984  1.00 11.13           C
ATOM    914  C   ALA B 282      10.577  -0.889   4.965  1.00 10.30           C
ATOM    915  O   ALA B 282      10.663  -0.156   5.937  1.00 10.83           O
ATOM    916  CB  ALA B 282       9.496  -3.180   4.899  1.00 14.45           C
"""
def tst_00():
  print "Finding sheets, splitting and merging...",
  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(std_text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())
  records=fss.annotation.as_pdb_str()
  import iotbx.pdb.secondary_structure as ioss
  annotation=ioss.annotation.from_records(records=flex.split_lines(records))
  f=StringIO()
  print >>f, "New records: \n",annotation.as_pdb_str()
  spl=annotation.split_sheets()
  print >>f, "After split_sheets: \n",spl.as_pdb_str()
  merged=spl.merge_sheets()
  print >>f, "After merge_sheets: \n",merged.as_pdb_str()
  print >>f, "\nSpl:\n",spl.as_pdb_str()
  assert merged.is_same_as(annotation)
  print >>f, "\nComparing merged and spl:"
  print >>f, "\nMerged:\n",merged.as_pdb_str()
  print >>f, "\nSpl:\n",spl.as_pdb_str()
  print >>f, "\nFINAL PDB selections:\n",merged.as_atom_selections()
  assert merged.is_same_as(spl)
  found_text=f.getvalue()

  expected_text="""
New records: 
SHEET    1   1 3 HISAa  32  LEUAa  36  0
SHEET    2   1 3 VALAa  17  LEUAa  22 -1  N  GLYAa  21   O  HISAa  32
SHEET    3   1 3 ALAAa  52  VALAa  55 -1  N  LYSAa  54   O  ILEAa  20
SHEET    1   2 4 GLUAa  40  GLNAa  45  0
SHEET    2   2 4 PHEAa   7  ALAAa  12 -1  N  ALAAa  12   O  GLUAa  40
SHEET    3   2 4 LYSAa  58  THRAa  63 -1  N  GLNAa  62   O  VALAa   9
SHEET    4   2 4 GLYAa  66  GLUAa  71 -1  N  SERAa  70   O  ALAAa  59
After split_sheets: 
SHEET    1   1 2 HISAa  32  LEUAa  36  0
SHEET    2   1 2 VALAa  17  LEUAa  22 -1  N  GLYAa  21   O  HISAa  32
SHEET    1   2 2 VALAa  17  LEUAa  22  0
SHEET    2   2 2 ALAAa  52  VALAa  55 -1  N  LYSAa  54   O  ILEAa  20
SHEET    1   3 2 GLUAa  40  GLNAa  45  0
SHEET    2   3 2 PHEAa   7  ALAAa  12 -1  N  ALAAa  12   O  GLUAa  40
SHEET    1   4 2 PHEAa   7  ALAAa  12  0
SHEET    2   4 2 LYSAa  58  THRAa  63 -1  N  GLNAa  62   O  VALAa   9
SHEET    1   5 2 LYSAa  58  THRAa  63  0
SHEET    2   5 2 GLYAa  66  GLUAa  71 -1  N  SERAa  70   O  ALAAa  59
After merge_sheets: 
SHEET    1   1 3 HISAa  32  LEUAa  36  0
SHEET    2   1 3 VALAa  17  LEUAa  22 -1  N  GLYAa  21   O  HISAa  32
SHEET    3   1 3 ALAAa  52  VALAa  55 -1  N  LYSAa  54   O  ILEAa  20
SHEET    1   2 4 GLUAa  40  GLNAa  45  0
SHEET    2   2 4 PHEAa   7  ALAAa  12 -1  N  ALAAa  12   O  GLUAa  40
SHEET    3   2 4 LYSAa  58  THRAa  63 -1  N  GLNAa  62   O  VALAa   9
SHEET    4   2 4 GLYAa  66  GLUAa  71 -1  N  SERAa  70   O  ALAAa  59

Spl:
SHEET    1   1 2 HISAa  32  LEUAa  36  0
SHEET    2   1 2 VALAa  17  LEUAa  22 -1  N  GLYAa  21   O  HISAa  32
SHEET    1   2 2 VALAa  17  LEUAa  22  0
SHEET    2   2 2 ALAAa  52  VALAa  55 -1  N  LYSAa  54   O  ILEAa  20
SHEET    1   3 2 GLUAa  40  GLNAa  45  0
SHEET    2   3 2 PHEAa   7  ALAAa  12 -1  N  ALAAa  12   O  GLUAa  40
SHEET    1   4 2 PHEAa   7  ALAAa  12  0
SHEET    2   4 2 LYSAa  58  THRAa  63 -1  N  GLNAa  62   O  VALAa   9
SHEET    1   5 2 LYSAa  58  THRAa  63  0
SHEET    2   5 2 GLYAa  66  GLUAa  71 -1  N  SERAa  70   O  ALAAa  59

Comparing merged and spl:

Merged:
SHEET    1   1 3 HISAa  32  LEUAa  36  0
SHEET    2   1 3 VALAa  17  LEUAa  22 -1  N  GLYAa  21   O  HISAa  32
SHEET    3   1 3 ALAAa  52  VALAa  55 -1  N  LYSAa  54   O  ILEAa  20
SHEET    1   2 4 GLUAa  40  GLNAa  45  0
SHEET    2   2 4 PHEAa   7  ALAAa  12 -1  N  ALAAa  12   O  GLUAa  40
SHEET    3   2 4 LYSAa  58  THRAa  63 -1  N  GLNAa  62   O  VALAa   9
SHEET    4   2 4 GLYAa  66  GLUAa  71 -1  N  SERAa  70   O  ALAAa  59

Spl:
SHEET    1   1 2 HISAa  32  LEUAa  36  0
SHEET    2   1 2 VALAa  17  LEUAa  22 -1  N  GLYAa  21   O  HISAa  32
SHEET    1   2 2 VALAa  17  LEUAa  22  0
SHEET    2   2 2 ALAAa  52  VALAa  55 -1  N  LYSAa  54   O  ILEAa  20
SHEET    1   3 2 GLUAa  40  GLNAa  45  0
SHEET    2   3 2 PHEAa   7  ALAAa  12 -1  N  ALAAa  12   O  GLUAa  40
SHEET    1   4 2 PHEAa   7  ALAAa  12  0
SHEET    2   4 2 LYSAa  58  THRAa  63 -1  N  GLNAa  62   O  VALAa   9
SHEET    1   5 2 LYSAa  58  THRAa  63  0
SHEET    2   5 2 GLYAa  66  GLUAa  71 -1  N  SERAa  70   O  ALAAa  59

FINAL PDB selections:
["chain 'Aa' and resid 32  through 36 ", "chain 'Aa' and resid 17  through 22 ", "chain 'Aa' and resid 52  through 55 ", "chain 'Aa' and resid 40  through 45 ", "chain 'Aa' and resid 7  through 12 ", "chain 'Aa' and resid 58  through 63 ", "chain 'Aa' and resid 66  through 71 "]
  """
  if remove_blank(found_text)!=remove_blank(expected_text):
    print "Expected: \n%s \nFound: \n%s" %(expected_text,found_text)
    raise AssertionError, "FAILED"


  print "OK"


def tst_01():
  print "Finding helices...",
  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(two_helix_text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())

  expected_text="""
Model 1  N: 8  Start: 1 End: 8
Class:  Alpha helix  N: 8 Start: 1 End: 8  Rise: 1.56 A Dot: 0.98

Model 2  N: 16  Start: 11 End: 26
Class:  Alpha helix  N: 16 Start: 11 End: 26  Rise: 1.58 A Dot: 0.98

FINAL PDB RECORDS:
HELIX    1   1 GLY A    1  VAL A    8  1                                   8
HELIX    2   2 THR A   11  GLN A   26  1                                  16

FINAL PDB selections:
" ( chain 'A' and resid 1 through 8 )  or  ( chain 'A' and resid 11 through 26 ) "

"""
  f=StringIO()
  fss.show_summary(out=f,verbose=True)
  found_text=f.getvalue()
  #assert not test_utils.show_diff(found_text, expected_text)
  if remove_blank(found_text)!=remove_blank(expected_text):
    print "Expected: \n%s \nFound: \n%s" %(expected_text,found_text)
    raise AssertionError, "FAILED"
  print "OK"

def tst_02():
  text="""
ATOM      2  CA  GLY A   1      43.603 -11.488  24.325  1.00 35.57
ATOM      6  CA  ILE A   2      44.200  -8.183  22.475  1.00 27.55
ATOM     14  CA  GLY A   3      43.999 -10.264  19.329  1.00 21.05
ATOM     18  CA  ALA A   4      40.378 -11.260  20.106  1.00 21.80
ATOM     23  CA  VAL A   5      39.355  -7.658  21.083  1.00 19.34
ATOM     30  CA  LEU A   6      41.062  -6.432  17.957  1.00 17.59
ATOM     38  CA  LYS A   7      39.079  -8.646  15.636  1.00 22.55
ATOM     47  CA  VAL A   8      35.792  -7.369  17.211  1.00 20.52
ATOM     69  CA  THR A  11      34.132  -6.405  12.343  1.00 24.14
ATOM     76  CA  GLY A  12      31.584  -6.595  15.140  1.00 24.17
ATOM     80  CA  LEU A  13      31.923  -2.919  16.364  1.00 23.24
ATOM     88  CA  PRO A  14      31.026  -1.278  13.030  1.00 17.52
ATOM     95  CA  ALA A  15      27.822  -3.418  12.724  1.00 17.10
ATOM    100  CA  LEU A  16      26.958  -2.649  16.351  1.00 18.20
ATOM    108  CA  ILE A  17      27.343   1.056  15.618  1.00 20.41
ATOM    116  CA  SER A  18      24.825   0.827  12.744  1.00 19.98
ATOM    122  CA  TRP A  19      22.492  -1.085  15.081  1.00 15.72
ATOM    136  CA  ILE A  20      22.628   1.633  17.766  1.00 15.67
ATOM    144  CA  LYS A  21      21.888   4.236  15.157  1.00 19.84
ATOM    153  CA  ARG A  22      18.740   2.273  14.020  1.00 20.38
ATOM    164  CA  LYS A  23      17.500   1.928  17.550  1.00 22.62
ATOM    173  CA  ARG A  24      18.059   5.674  18.276  1.00 27.11
ATOM    184  CA  GLN A  25      15.836   6.730  15.339  1.00 37.50
ATOM    193  CA  GLN A  26      13.132   4.360  16.583  1.00 46.66
"""
  print "Finding helices...",
  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())

  expected_text="""
Model 1  N: 8  Start: 1 End: 8
Class:  Alpha helix  N: 8 Start: 1 End: 8  Rise: 1.56 A Dot: 0.98

Model 2  N: 16  Start: 11 End: 26
Class:  Alpha helix  N: 16 Start: 11 End: 26  Rise: 1.58 A Dot: 0.98

FINAL PDB RECORDS:
HELIX    1   1 GLY A    1  VAL A    8  1                                   8
HELIX    2   2 THR A   11  GLN A   26  1                                  16



FINAL PDB selections:
" ( chain 'A' and resid 1  through 8 )  or  ( chain 'A' and resid 11  through 26 ) "
"""
  f=StringIO()
  fss.show_summary(out=f,verbose=True)
  found_text=f.getvalue()
  #assert not test_utils.show_diff(found_text, expected_text)
  if remove_blank(found_text)!=remove_blank(expected_text):
    print "Expected: \n%s \nFound: \n%s" %(expected_text,found_text)
    raise AssertionError, "FAILED"
  print "OK"

def tst_03():
  print "Finding alpha,3-10 and pi helices...",
  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(helices_text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())

  expected_text="""
Model 1  N: 16  Start: 1 End: 16
Class:  Alpha helix  N: 16 Start: 1 End: 16  Rise: 1.51 A Dot: 0.98

Model 2  N: 21  Start: 2 End: 22
Class:     Pi helix  N: 21 Start: 2 End: 22  Rise: 0.96 A Dot: 0.98

Model 3  N: 21  Start: 2 End: 22
Class:   3-10 helix  N: 20 Start: 2 End: 21  Rise: 1.99 A Dot: 1.00

FINAL PDB RECORDS:
HELIX    1   1 ALA A    1  ALA A   16  1                                  16
HELIX    1   1 ALA C    2  ALA C   21  5                                  20
HELIX    1   1 ALA B    2  ALA B   22  3                                  21



FINAL PDB selections:
" ( chain 'A' and resid 1  through 16 )  or  ( chain 'C' and resid 2  through 21 )  or  ( chain 'B' and resid 2  through 22 ) "
"""
  f=StringIO()
  fss.show_summary(out=f,verbose=True)
  found_text=f.getvalue()
  #assert not test_utils.show_diff(found_text, expected_text)
  if remove_blank(found_text)!=remove_blank(expected_text):
    print "Expected: \n%s \nFound: \n%s" %(expected_text,found_text)
    raise AssertionError, "FAILED"
  print "OK"

def tst_04():
  text="""
ATOM      2  CA  THRAa   3     186.743 125.884 251.259  1.00100.00           C
ATOM      5  CA  ASNAa   4     189.629 123.742 252.763  1.00100.00           C
ATOM      8  CA  SERAa   5     191.072 126.112 255.320  1.00100.00           C
ATOM     11  CA  ASPAa   6     192.080 124.928 258.848  1.00100.00           C
ATOM     14  CA  PHEAa   7     189.384 124.585 261.530  1.00100.00           C
ATOM     17  CA  VALAa   8     189.248 124.466 265.315  1.00100.00           C
ATOM     20  CA  VALAa   9     187.059 122.294 267.547  1.00100.00           C
ATOM     23  CA  ILEAa  10     185.534 123.893 270.679  1.00100.00           C
ATOM     26  CA  LYSAa  11     183.570 122.134 273.450  1.00100.00           C
ATOM     29  CA  ALAAa  12     181.897 124.298 276.085  1.00100.00           C
ATOM     32  CA  LEUAa  13     182.733 123.145 279.601  1.00100.00           C
ATOM     35  CA  GLUAa  14     180.241 125.609 281.156  1.00100.00           C
ATOM     38  CA  ASPAa  15     177.155 127.540 279.985  1.00100.00           C
ATOM     41  CA  GLYAa  16     177.637 130.843 278.162  1.00100.00           C
ATOM     44  CA  VALAa  17     180.958 130.212 276.395  1.00100.00           C
ATOM     47  CA  ASNAa  18     181.477 132.715 273.547  1.00100.00           C
ATOM     50  CA  VALAa  19     183.320 131.753 270.320  1.00100.00           C
ATOM     53  CA  ILEAa  20     184.043 135.156 268.674  1.00100.00           C
ATOM     56  CA  GLYAa  21     185.054 135.558 264.994  1.00100.00           C
ATOM     59  CA  LEUAa  22     187.345 138.529 264.419  1.00100.00           C
ATOM     62  CA  THRAa  23     187.310 140.218 261.033  1.00100.00           C
ATOM     65  CA  ARGAa  24     189.831 139.523 258.335  1.00100.00           C
ATOM     68  CA  GLYAa  25     191.359 142.673 256.805  1.00100.00           C
ATOM     71  CA  ALAAa  26     192.794 146.041 257.837  1.00100.00           C
ATOM     74  CA  ASPAa  27     190.126 146.289 260.564  1.00100.00           C
ATOM     77  CA  THRAa  28     189.912 143.928 263.570  1.00100.00           C
ATOM     80  CA  ARGAa  29     186.413 143.856 265.033  1.00100.00           C
ATOM     83  CA  PHEAa  30     183.873 141.240 266.091  1.00100.00           C
ATOM     86  CA  HISAa  31     181.625 140.079 263.343  1.00100.00           C
ATOM     89  CA  HISAa  32     179.931 137.209 265.203  1.00100.00           C
ATOM     92  CA  SERAa  33     179.805 135.702 268.677  1.00100.00           C
ATOM     95  CA  GLUAa  34     178.501 132.109 268.857  1.00100.00           C
ATOM     98  CA  CYSAa  35     177.222 131.284 272.342  1.00100.00           C
ATOM    101  CA  LEUAa  36     177.646 127.700 273.502  1.00100.00           C
ATOM    104  CA  ASPAa  37     175.969 125.990 276.438  1.00100.00           C
ATOM    107  CA  LYSAa  38     177.682 123.298 278.488  1.00100.00           C
ATOM    110  CA  GLYAa  39     178.623 120.300 276.385  1.00100.00           C
ATOM    113  CA  GLUAa  40     177.892 121.761 272.941  1.00100.00           C
ATOM    116  CA  VALAa  41     180.597 121.439 270.276  1.00100.00           C
ATOM    119  CA  LEUAa  42     181.492 123.998 267.594  1.00100.00           C
ATOM    122  CA  ILEAa  43     183.793 123.155 264.645  1.00100.00           C
ATOM    125  CA  ALAAa  44     184.701 126.388 262.889  1.00100.00           C
ATOM    128  CA  GLNAa  45     186.987 127.209 259.959  1.00100.00           C
ATOM    131  CA  PHEAa  46     189.115 130.161 259.157  1.00100.00           C
ATOM    134  CA  THRAa  47     187.356 131.901 256.203  1.00100.00           C
ATOM    137  CA  GLUAa  48     187.180 134.953 253.965  1.00100.00           C
ATOM    140  CA  HISAa  49     185.578 136.805 256.905  1.00100.00           C
ATOM    143  CA  THRAa  50     187.343 135.292 259.938  1.00100.00           C
ATOM    146  CA  SERAa  51     191.129 135.327 260.339  1.00100.00           C
ATOM    149  CA  ALAAa  52     191.231 135.094 264.170  1.00100.00           C
ATOM    152  CA  ILEAa  53     188.989 133.390 266.744  1.00100.00           C
ATOM    155  CA  LYSAa  54     188.770 134.368 270.428  1.00100.00           C
ATOM    158  CA  VALAa  55     187.303 131.970 273.016  1.00100.00           C
ATOM    161  CA  ARGAa  56     185.817 133.382 276.214  1.00100.00           C
ATOM    164  CA  GLYAa  57     184.672 131.065 278.997  1.00100.00           C
ATOM    167  CA  LYSAa  58     185.698 127.553 280.004  1.00100.00           C
ATOM    170  CA  ALAAa  59     186.172 125.294 276.966  1.00100.00           C
ATOM    173  CA  TYRAa  60     188.258 122.444 275.620  1.00100.00           C
ATOM    176  CA  ILEAa  61     189.863 123.277 272.265  1.00100.00           C
ATOM    179  CA  GLNAa  62     191.492 121.098 269.577  1.00100.00           C
ATOM    182  CA  THRAa  63     193.550 122.431 266.653  1.00100.00           C
ATOM    185  CA  ARGAa  64     196.271 121.116 264.358  1.00100.00           C
ATOM    188  CA  HISAa  65     198.826 122.305 266.995  1.00100.00           C
ATOM    191  CA  GLYAa  66     197.443 120.330 269.914  1.00100.00           C
ATOM    194  CA  VALAa  67     194.865 120.679 272.646  1.00100.00           C
ATOM    197  CA  ILEAa  68     194.232 123.486 275.120  1.00100.00           C
ATOM    200  CA  GLUAa  69     191.576 124.693 277.564  1.00100.00           C
ATOM    203  CA  SERAa  70     190.301 128.219 277.907  1.00100.00           C
ATOM    206  CA  GLUAa  71     189.167 129.249 281.377  1.00100.00           C
ATOM    209  CA  GLYAa  72     186.003 131.073 282.428  1.00100.00           C
"""
  print "Finding sheets...",
  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())

  expected_text="""
Model 1  N: 70  Start: 3 End: 72
Class:  Beta strand  N: 10 Start: 3 End: 12  Rise: 3.32 A Dot: 0.88
Class:  Beta strand  N: 9 Start: 16 End: 24  Rise: 3.24 A Dot: 0.97
Class:  Beta strand  N: 4 Start: 27 End: 30  Rise: 3.34 A Dot: 0.95
Class:  Beta strand  N: 6 Start: 31 End: 36  Rise: 3.29 A Dot: 0.99
Class:  Beta strand  N: 8 Start: 40 End: 47  Rise: 3.30 A Dot: 0.96
Class:  Beta strand  N: 5 Start: 51 End: 55  Rise: 3.41 A Dot: 1.00
Class:  Beta strand  N: 6 Start: 58 End: 63  Rise: 3.41 A Dot: 0.96
Class:  Beta strand  N: 7 Start: 66 End: 72  Rise: 3.41 A Dot: 0.98

FINAL PDB RECORDS:
SHEET    1   1 3 HISAa  32  LEUAa  36  0
SHEET    2   1 3 VALAa  17  LEUAa  22 -1  N  GLYAa  21   O  HISAa  32
SHEET    3   1 3 ALAAa  52  VALAa  55 -1  N  LYSAa  54   O  ILEAa  20
SHEET    1   2 4 GLUAa  40  GLNAa  45  0
SHEET    2   2 4 PHEAa   7  ALAAa  12 -1  N  ALAAa  12   O  GLUAa  40
SHEET    3   2 4 LYSAa  58  THRAa  63 -1  N  GLNAa  62   O  VALAa   9
SHEET    4   2 4 GLYAa  66  GLUAa  71 -1  N  SERAa  70   O  ALAAa  59



FINAL PDB selections:
" ( chain 'Aa' and resid 32  through 36 )  or  ( chain 'Aa' and resid 17  through 22 )  or  ( chain 'Aa' and resid 52  through 55 )  or  ( chain 'Aa' and resid 40  through 45 )  or  ( chain 'Aa' and resid 7  through 12 )  or  ( chain 'Aa' and resid 58  through 63 )  or  ( chain 'Aa' and resid 66  through 71 ) "
"""
  f=StringIO()
  fss.show_summary(out=f,verbose=True)
  found_text=f.getvalue()
  #assert not test_utils.show_diff(found_text, expected_text)
  if remove_blank(found_text)!=remove_blank(expected_text):
    print "Expected: \n%s \nFound: \n%s" %(expected_text,found_text)
    raise AssertionError, "FAILED"
  print "OK"

def tst_05():
  print "Finding sheets with separate chains...",
  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(two_chain_text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())

  expected_text="""
Model 1  N: 8  Start: 50 End: 57
Class:  Beta strand  N: 8 Start: 50 End: 57  Rise: 3.21 A Dot: 0.97

Model 2  N: 5  Start: 278 End: 282
Class:  Beta strand  N: 5 Start: 278 End: 282  Rise: 3.16 A Dot: 0.98

FINAL PDB RECORDS:
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  N  ILE B 280   O  ILE A  51



FINAL PDB selections:
" ( chain 'A' and resid 50 through 54 )  or  ( chain 'B' and resid 278 through 282 ) "

"""
  f=StringIO()
  fss.show_summary(out=f,verbose=True)
  found_text=f.getvalue()
  if remove_blank(found_text)!=remove_blank(expected_text):
    print "Expected: \n%s \nFound: \n%s" %(expected_text,found_text)
    raise AssertionError, "FAILED"
  print "OK"

def tst_06():
  text="""
ATOM      8  CA  GLY A   2      24.485  19.185   6.248  1.00 11.14           C
HETATM   15  CA  23F A   3      26.939  16.455   5.194  1.00  9.61           C
ATOM     33  CA  ALA A   4      29.149  18.888   3.424  1.00  9.96           C
HETATM   43  CA  23F A   5      30.573  19.304   6.910  1.00  6.42           C
HETATM   61  CA  23F A   6      32.558  16.167   6.280  1.00  6.41           C
ATOM     79  CA  ALA A   7      35.089  18.339   4.563  1.00  6.26           C
HETATM   89  CA  23F A   8      36.195  19.092   8.094  1.00  6.38           C
HETATM  107  CA  23F A   9      38.283  15.914   7.621  1.00  7.78           C
ATOM    125  CA  ALA A  10      40.789  18.180   5.892  1.00  8.66           C
ATOM    135  CA  GLY A  11      41.608  19.716   9.325  1.00 10.78           C
ATOM    142  CA  GLY A  12      44.498  17.479   9.975  1.00 17.00           C
ATOM    149  CA  GLY A  13      43.927  17.193  13.603  1.00 13.58           C
ATOM    156  CA  GLY A  14      41.242  17.379  16.363  1.00 11.14           C
HETATM  163  CA  23F A  15      39.608  20.319  14.616  1.00  7.70           C
ATOM    181  CA  ALA A  16      38.402  17.853  12.023  1.00  7.08           C
ATOM    191  CA  LEU A  17      35.810  16.973  14.649  1.00  6.22           C
HETATM  210  CA  23F A  18      34.098  20.219  13.633  1.00  6.81           C
ATOM    228  CA  ALA A  19      32.642  18.019  10.889  1.00  6.28           C
ATOM    238  CA  LEU A  20      30.139  16.927  13.574  1.00  6.81           C
HETATM  257  CA  23F A  21      28.460  20.242  12.654  1.00  8.80           C
ATOM    275  CA  ALA A  22      27.017  18.382   9.700  1.00  7.89           C
"""
  print "Finding sheets with unusual residues...",
  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())

  expected_text="""
Model 1  N: 21  Start: 2 End: 22
Class:  Alpha helix  N: 10 Start: 3 End: 12  Rise: 2.00 A Dot: 0.98
Class:  Alpha helix  N: 10 Start: 13 End: 22  Rise: 1.96 A Dot: 0.97
FINAL PDB RECORDS:
HELIX    1   1 23F A    3  GLY A   12  1                                  10
HELIX    2   2 GLY A   13  ALA A   22  1                                  10
FINAL PDB selections:
" ( chain 'A' and resid 3 through 12 )  or  ( chain 'A' and resid 13 through 22 ) "
"""
  f=StringIO()
  fss.show_summary(out=f,verbose=True)
  found_text=f.getvalue()
  if remove_blank(found_text)!=remove_blank(expected_text):
    print "Expected: \n%s \nFound: \n%s" %(expected_text,found_text)
    raise AssertionError, "FAILED"
  print "OK"

def tst_07():
  text="""
ATOM    651  CA BPRO E   1      14.350   6.490 -29.205  0.50 16.99           C
ATOM    658  CA BPRO E   2      12.612   6.495 -25.864  0.50 14.37           C
ATOM    666  CA AGLY E   3      12.816   7.962 -32.315  0.55 19.29           C
ATOM    667  CA BGLY E   3      13.074   9.621 -23.839  0.45 12.65           C
ATOM    674  CA APRO E   4      14.350   6.490 -29.205  0.50 16.99           C
ATOM    675  CA BPRO E   4      15.262  10.063 -20.808  0.50 15.34           C
ATOM    688  CA APRO E   5      12.612   6.495 -25.864  0.50 14.37           C
ATOM    689  CA BPRO E   5      14.316   8.840 -17.372  0.50 10.66           C
ATOM    702  CA AGLY E   6      13.074   9.621 -23.839  0.50 12.65           C
ATOM    703  CA BGLY E   6      11.932  10.884 -15.276  0.50  7.99           C
ATOM    710  CA APRO E   7      15.262  10.063 -20.808  0.50 15.34           C
ATOM    711  CA BPRO E   7      13.150  12.796 -12.241  0.50  9.73           C  """
  print "Finding sheets with alt confs where there is no A for first res..."
  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,verbose=True,out=null_out())

  expected_text="""
Model 1  N: 5  Start: 3 End: 7
Class:  Beta strand  N: 4 Start: 4 End: 7  Rise: 3.27 A Dot: 0.91"""
  f=StringIO()
  fss.show_summary(out=f,verbose=True)
  found_text=f.getvalue()
  if remove_blank(found_text)!=remove_blank(expected_text):
    print "Expected: \n%s \nFound: \n%s" %(expected_text,found_text)
    raise AssertionError, "FAILED"
  print "OK"

def tst_08():
  print "Checking similar annotations and overlapping annotations"

  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(one_helix_text)).construct_hierarchy()

  ann_one_helix_beg=get_annotation(one_helix_beginning_text)
  ann_one_helix_middle=get_annotation(one_helix_middle_text)
  ann_one_helix_end=get_annotation(one_helix_end_text)
  ann_one_helix=get_annotation(one_helix_text)
  for h1 in ann_one_helix_beg.helices:
    for h2 in ann_one_helix_beg.helices:
       print "Should be same:",h1.is_similar_to(other=h2,hierarchy=hierarchy)
       assert h1.is_similar_to(other=h2,hierarchy=hierarchy)
  for maximum_length_difference in [4,8]:
    for minimum_overlap in [6,10]:
      for h1 in ann_one_helix_beg.helices:
        for h2 in ann_one_helix.helices:
           value=h1.is_similar_to(other=h2,hierarchy=hierarchy,
             maximum_length_difference=maximum_length_difference,
             minimum_overlap=minimum_overlap)
           print "Comparison:",value
           assert (value and maximum_length_difference==8 and
              minimum_overlap==6) or not value

  assert ann_one_helix_beg.overlaps_with(other=ann_one_helix,
     hierarchy=hierarchy)
  assert not ann_one_helix_beg.overlaps_with(other=ann_one_helix_end,
     hierarchy=hierarchy)

  # Now strands and sheets

  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(std_text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())
  records=fss.annotation.as_pdb_str()
  import iotbx.pdb.secondary_structure as ioss


  s1_records="""
SHEET    1   1 3 HISAa  32  LEUAa  36  0
SHEET    2   1 3 VALAa  17  LEUAa  22 -1  N  GLYAa  21   O  HISAa  32
SHEET    3   1 3 ALAAa  52  VALAa  55 -1  N  LYSAa  54   O  ILEAa  20
"""
  s1_not_overlap_records="""
SHEET    1   1 3 HISAa  32  LEUAa  36  0
SHEET    1   2 4 GLUAa  40  GLNAa  45  0
SHEET    3   2 4 LYSAa  58  THRAa  63 -1  
"""

  s1_similar_records="""
SHEET    1   1 3 HISAa  32  LEUAa  36  0
SHEET    2   1 3 VALAa  18  LEUAa  22 -1  N  VALAa  19   O  GLUAa  34
SHEET    3   1 3 ALAAa  50  VALAa  57 -1  N  LYSAa  54   O  ILEAa  20
"""

  s1_diff_records="""
SHEET    1   2 4 GLUAa  40  GLNAa  45  0
SHEET    2   2 4 PHEAa   7  ALAAa  12 -1  N  ALAAa  12   O  GLUAa  40
SHEET    3   2 4 LYSAa  58  THRAa  63 -1  N  GLNAa  62   O  VALAa   9
"""
  s1_reverse_diff_records="""
SHEET    1   2 4 GLUAa  40  GLNAa  45  0
SHEET    2   2 4 PHEAa   7  ALAAa  12  1  N  ALAAa  12   O  GLUAa  40
SHEET    3   2 4 LYSAa  58  THRAa  63 -1  N  GLNAa  62   O  VALAa   9
"""

  s1_similar_reg_records="""
SHEET    1   1 3 HISAa  32  LEUAa  36  0
SHEET    2   1 3 VALAa  17  LEUAa  22 -1  N  ILEAa  20   O  SERAa  33
SHEET    3   1 3 ALAAa  52  VALAa  55 -1  N  LYSAa  54   O  ILEAa  20
"""

  s1_similar_backwards="""
SHEET    2   1 3 VALAa  18  LEUAa  22  0
SHEET    3   1 3 ALAAa  50  VALAa  57 -1  O  ILEAa  20   N  LYSAa  54
SHEET    1   1 3 HISAa  32  LEUAa  36 -1  O  SERAa  33   N  ILEAa  20
"""

  s1_similar_backwards_2="""
SHEET    2   1 3 VALAa  18  LEUAa  22  0
SHEET    3   1 3 ALAAa  50  VALAa  57 -1  O  ILEAa  20   N  LYSAa  54
SHEET    1   1 3 HISAa  32  LEUAa  36 -1  O  SERAa  33   N  ILEAa  20
"""

  s1_full=ioss.annotation.from_records(records=flex.split_lines(s1_records))
  s1_not_overlap=ioss.annotation.from_records(records=flex.split_lines(s1_not_overlap_records))
  s1_similar=ioss.annotation.from_records(records=flex.split_lines(s1_similar_records))
  s1_diff=ioss.annotation.from_records(records=flex.split_lines(s1_diff_records))
  s1_reverse_diff=ioss.annotation.from_records(records=flex.split_lines(s1_reverse_diff_records))

  print "\nChecking overlap:"
  assert s1_full.overlaps_with(other=s1_similar,hierarchy=hierarchy)
  assert not s1_full.overlaps_with(other=s1_diff,hierarchy=hierarchy)
  assert not s1_full.overlaps_with(other=s1_not_overlap,hierarchy=hierarchy)

  print "\nChecking similar strands:",
  f=StringIO()
  for s1 in s1_full.sheets:
    for str1 in s1.strands:
      for s2 in s1_similar.sheets:
        for str2 in s2.strands:
          value=str1.is_similar_to(other=str2,hierarchy=hierarchy,
             maximum_length_difference=4)
          print str1.as_atom_selections(),str2.as_atom_selections(),value
          print >>f,str1.as_atom_selections(),str2.as_atom_selections(),value
  assert f.getvalue()=="""chain 'Aa' and resid 32  through 36  chain 'Aa' and resid 32  through 36  True
chain 'Aa' and resid 32  through 36  chain 'Aa' and resid 18  through 22  False
chain 'Aa' and resid 32  through 36  chain 'Aa' and resid 50  through 57  False
chain 'Aa' and resid 17  through 22  chain 'Aa' and resid 32  through 36  False
chain 'Aa' and resid 17  through 22  chain 'Aa' and resid 18  through 22  True
chain 'Aa' and resid 17  through 22  chain 'Aa' and resid 50  through 57  False
chain 'Aa' and resid 52  through 55  chain 'Aa' and resid 32  through 36  False
chain 'Aa' and resid 52  through 55  chain 'Aa' and resid 18  through 22  False
chain 'Aa' and resid 52  through 55  chain 'Aa' and resid 50  through 57  True
"""

  print "\nChecking different strands:",
  for s1 in s1_full.sheets:
    for str1 in s1.strands:
      for s2 in s1_diff.sheets:
        for str2 in s2.strands:
          print str1.as_atom_selections(),str2.as_atom_selections(),\
            str1.is_similar_to(other=str2,hierarchy=hierarchy,
             maximum_length_difference=4)

  print "\nChecking similar sheets:",
  for s1 in s1_full.sheets:
    for s2 in s1_similar.sheets:
      value=s1.is_similar_to(other=s2,hierarchy=hierarchy,
            maximum_length_difference=4)
      print value
      assert value

  print "\nChecking non-similar sheets:",
  for s1 in s1_full.sheets:
    for s2 in s1_diff.sheets:
      value=s1.is_similar_to(other=s2,hierarchy=hierarchy,
            maximum_length_difference=4)
      print value
      assert not value

  print "\nChecking similar overall annotations:",
  value=s1_full.is_similar_to(other=s1_similar,hierarchy=hierarchy,
            maximum_length_difference=4)
  print value
  assert value

  print "\nChecking different overall annotations:",
  value=s1_full.is_similar_to(other=s1_diff,hierarchy=hierarchy,
            maximum_length_difference=4)
  print value
  assert not value

  print "\nChecking different overall directions:",
  value=s1_full.is_similar_to(other=s1_reverse_diff,hierarchy=hierarchy,
            maximum_length_difference=4)
  print value
  assert not value


  # parallel strands
  print "\n\nChecking parallel strands..."

  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(two_chain_text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())
  records=fss.annotation.as_pdb_str()
  import iotbx.pdb.secondary_structure as ioss


  s2_records="""
FINAL PDB RECORDS:
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  N  ILE B 280   O  ILE A  51
"""

  s2_similar_records="""
FINAL PDB RECORDS:
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  N  ALA B 282   O  THR A  53
"""

  s2_similar_records_2="""
FINAL PDB RECORDS:
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  O  LEU B 278   N  ILE A  51
"""

  s2_different_records="""
FINAL PDB RECORDS:
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  O  ILE B 280   N  ILE A  51
"""

  s2_full=ioss.annotation.from_records(records=flex.split_lines(s2_records))
  s2_similar=ioss.annotation.from_records(records=flex.split_lines(s2_similar_records))
  s2_similar_2=ioss.annotation.from_records(records=flex.split_lines(s2_similar_records_2))
  s2_different=ioss.annotation.from_records(records=flex.split_lines(s2_different_records))

  print "\nChecking similar overall annotations (offset by 2):",
  value=s2_full.is_similar_to(other=s2_similar,hierarchy=hierarchy,
            maximum_length_difference=4)
  print value
  assert value

  print "\nChecking similar overall annotations (switch N/O):",
  value=s2_full.is_similar_to(other=s2_similar_2,hierarchy=hierarchy,
            maximum_length_difference=4)
  print value
  assert value

  print "\nChecking different overall annotations (offset by 1):",
  value=s2_full.is_similar_to(other=s2_different,hierarchy=hierarchy,
            maximum_length_difference=4)
  print value
  assert not value

  print "\nOK"



def tst_09():
  print "Comparing sheets and helices...",

  helix_1="""
HELIX    1   1 GLY A    1  VAL A    8  1                                   8
"""
  helix_2="""
HELIX    2   2 THR A   11  GLN A   26  1                                  16
"""
  sheet_1="""
SHEET    1   1 3 HISAa  32  LEUAa  36  0
SHEET    2   1 3 VALAa  17  LEUAa  22 -1  N  GLYAa  21   O  HISAa  32
SHEET    3   1 3 ALAAa  52  VALAa  55  1  N  LYSAa  54   O  ILEAa  20
"""
  sheet_2="""
SHEET    1   2 4 GLUAa  40  GLNAa  45  0
SHEET    2   2 4 PHEAa   7  ALAAa  12 -1  N  ALAAa  12   O  GLUAa  40
SHEET    3   2 4 LYSAa  58  THRAa  63  1  N  GLNAa  62   O  VALAa   9
SHEET    4   2 4 GLYAa  66  GLUAa  71 -1  N  SERAa  70   O  ALAAa  59
"""
  import iotbx.pdb.secondary_structure as ioss
  from cctbx.array_family import flex

  h1=ioss.annotation.from_records(records=flex.split_lines(helix_1))
  h2=ioss.annotation.from_records(records=flex.split_lines(helix_2))
  s1=ioss.annotation.from_records(records=flex.split_lines(sheet_1))
  s2=ioss.annotation.from_records(records=flex.split_lines(sheet_2))
  assert h1.is_same_as(h1)
  assert h2.is_same_as(h2)
  assert not h1.is_same_as(h2)
  assert not h1.is_same_as(s1)
  assert not s1.is_same_as(s2)
  assert s1.is_same_as(s1)
  for a in s1.sheets:
    for b in s1.sheets:
      assert (a==b and a.is_same_as(b)) or (not a.is_same_as(b))
      for sa in a.strands:
        for sb in b.strands:
          assert (sa==sb and sa.is_same_as(sb)) or (not sa.is_same_as(sb))
  print "OK"


def get_annotation(text):
  import iotbx.pdb
  from cctbx.array_family import flex
  import iotbx.pdb.secondary_structure as ioss
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())
  records=fss.annotation.as_pdb_str()
  return ioss.annotation.from_records(records=flex.split_lines(records))

def tst_10():

  import iotbx.pdb
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(one_full_helix_text+two_chain_text)).construct_hierarchy()

  text_helix_1="""
HELIX    1   1 ALA A   15  LYS A   21  1                                   7
"""
  text_helix_2="""
HELIX    1   1 LEU A   16  LYS A   21  1                                   6
"""
  text_sheet_1="""
SHEET    1   1 2 ILE A  51  TYR A  54  0
SHEET    2   1 2 THR B 279  ALA B 282  1  N  ILE B 280   O  ILE A  51
"""
  text_sheet_2="""
SHEET    1   1 2 TYR A  50  TYR A  54  0
SHEET    2   1 2 LEU B 278  ALA B 282  1  N  ILE B 280   O  ILE A  51
"""
  import iotbx.pdb.secondary_structure as ioss
  from cctbx.array_family import flex
  h1=ioss.annotation.from_records(records=flex.split_lines(text_helix_1))
  h2=ioss.annotation.from_records(records=flex.split_lines(text_helix_2))
  s1=ioss.annotation.from_records(records=flex.split_lines(text_sheet_1))
  s2=ioss.annotation.from_records(records=flex.split_lines(text_sheet_2))

  hs1=ioss.annotation.from_records(records=flex.split_lines(text_helix_1+text_sheet_1))
  hs2=ioss.annotation.from_records(records=flex.split_lines(text_helix_2+text_sheet_2))

  print "\nCombining annotations"

  ann_all=get_annotation(one_full_helix_text+two_chain_text)
  print "\nFull annotation\n",ann_all.as_pdb_str()

  print "\nCombining annotations from two parts"
  ann_one_full_helix=get_annotation(one_full_helix_text)
  print "\nAnnotation for helix:\n",ann_one_full_helix.as_pdb_str()
  ann_two_chain=get_annotation(two_chain_text)
  print "\nAnnotation for two chains:\n",ann_two_chain.as_pdb_str()

  ann_combined=ann_one_full_helix.combine_annotations(other=ann_two_chain,
    hierarchy=hierarchy)
  if ann_combined:
    print "Combined: \n",ann_combined.as_pdb_str()

  print "\nCombining annotations from overlapping helix annotations"
  print "\nHelix 1 and 2: \n",h1.as_pdb_str(),"\n",h2.as_pdb_str()
  ann_combined=h1.combine_annotations(other=h2,hierarchy=hierarchy)
  print "\nCombined: \n",ann_combined.as_pdb_str()

  print "\nCombining annotations from overlapping strand annotations"
  print "\nStrand 1 and 2: \n",s1.as_pdb_str(),"\n",s2.as_pdb_str()
  ann_combined=s1.combine_annotations(other=s2,hierarchy=hierarchy,
     minimum_overlap=3,out=sys.stdout)
  print "\nCombined: \n",ann_combined.as_pdb_str()

  print "\nCombining annotations from overlapping strand and helix annotations"
  print "\nStrand/helix 1:\n",hs1.as_pdb_str(),"Strand/helix 2:\n",hs2.as_pdb_str()
  ann_combined=hs1.combine_annotations(other=hs2,hierarchy=hierarchy,
     minimum_overlap=3,out=sys.stdout)
  print "\nCombined: \n",ann_combined.as_pdb_str()


  print "OK"

def tst_11():

  print "\nCounting H-bonds"

  import iotbx.pdb
  import iotbx.pdb.secondary_structure as ioss
  from cctbx.array_family import flex
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(two_chain_text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())
  ann=fss.get_annotation()
  print ann.as_pdb_str()

  print "Good H-bonds: %d  Poor H-Bonds: %d" %(
         fss.number_of_good_h_bonds,
         fss.number_of_poor_h_bonds,)
  assert fss.number_of_good_h_bonds==4 and fss.number_of_poor_h_bonds==0

  print "\nCounting H-bonds using ioss.annotation:"

  number_of_good_h_bonds,number_of_poor_h_bonds=ann.count_h_bonds(
    hierarchy=hierarchy)
  print "Good H-bonds: %d  Poor H-Bonds: %d" %(
         fss.number_of_good_h_bonds,
         fss.number_of_poor_h_bonds,)
  assert fss.number_of_good_h_bonds==4 and fss.number_of_poor_h_bonds==0

  print "\nCounting residues in secondary structure:",
  print ann.count_residues(hierarchy=hierarchy)
  assert ann.count_residues(hierarchy=hierarchy)==10

  print "\nCounting H-bonds in helix:"

  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(one_full_helix_text)).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())
  ann=fss.get_annotation()
  print ann.as_pdb_str()

  print "\nH-bonds with cutoff=3.5 (default):\n"
  number_of_good_h_bonds,number_of_poor_h_bonds=ann.count_h_bonds(
    hierarchy=hierarchy)
  print "Good H-bonds: %d  Poor H-Bonds: %d" %(
         number_of_good_h_bonds,
         number_of_poor_h_bonds,)
  assert number_of_good_h_bonds==3 and number_of_poor_h_bonds==0

  print "\nH-bonds with cutoff=3.0:\n"
  number_of_good_h_bonds,number_of_poor_h_bonds=ann.count_h_bonds(
    hierarchy=hierarchy,max_h_bond_length=3.0)
  print "Good H-bonds: %d  Poor H-Bonds: %d" %(
         number_of_good_h_bonds,
         number_of_poor_h_bonds,)
  assert number_of_good_h_bonds==1 and number_of_poor_h_bonds==2

  print "\nCount number of residues in secondary structure:",
  print ann.count_residues(hierarchy=hierarchy)
  assert ann.count_residues(hierarchy=hierarchy) ==7

  print "\nH-bonds in mixed helix/strand"

  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(two_chain_text+one_full_helix_text)
         ).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,out=null_out())
  ann=fss.get_annotation()
  print ann.as_pdb_str()

  print "\nH-bonds with cutoff=3.0 :\n"
  number_of_good_h_bonds,number_of_poor_h_bonds=ann.count_h_bonds(
    hierarchy=hierarchy,max_h_bond_length=3.0)
  print "Good H-bonds: %d  Poor H-Bonds: %d" %(
         number_of_good_h_bonds,
         number_of_poor_h_bonds,)
  assert number_of_good_h_bonds==5 and number_of_poor_h_bonds==2

  print "\nCount number of residues in secondary structure:",
  print ann.count_residues(hierarchy=hierarchy)
  assert ann.count_residues(hierarchy=hierarchy) ==17

  print "\nMake sure force and original ss are equivalent"
  force_fss=find_secondary_structure(hierarchy=hierarchy,
      user_annotation_text=ss_text,
      force_secondary_structure_input=True,
      combine_annotations=False,
      out=null_out())
  number_of_good_h_bonds,number_of_poor_h_bonds=\
      force_fss.get_annotation().count_h_bonds(
      hierarchy=hierarchy,max_h_bond_length=3.0)
  print "Good H-bonds: %d  Poor H-Bonds: %d" %(
         number_of_good_h_bonds,
         number_of_poor_h_bonds,)
  assert number_of_good_h_bonds==5 and number_of_poor_h_bonds==2

  print "\nInput annotation:"
  print fss.get_annotation().as_pdb_str()
  print "\nOutput annotation:"
  print force_fss.get_annotation().as_pdb_str()
  print "\nIs same: ",fss.get_annotation().is_similar_to(
     other=force_fss.get_annotation(),hierarchy=hierarchy)

  print "\nCorrect bad H-bond register in input"
  fix_fss=find_secondary_structure(hierarchy=hierarchy,
      user_annotation_text=bad_two_chain_helix_ss,
      force_secondary_structure_input=False,
      combine_annotations=False,
      search_secondary_structure=False,out=null_out())
  fss=find_secondary_structure(hierarchy=hierarchy,
      combine_annotations=False,
      out=null_out())
  print "\nInput:"
  print bad_two_chain_helix_ss
  print "\nFixed:"
  print fix_fss.get_annotation().as_pdb_str()
  print "\nGood:"
  print fss.get_annotation().as_pdb_str()
  print "Is same: ",  fix_fss.get_annotation().is_similar_to(
    hierarchy=hierarchy,other=fss.get_annotation())
  assert fix_fss.get_annotation().is_similar_to(
    hierarchy=hierarchy,other=fss.get_annotation())

  print "\nForce bad H-bond register in input"

  import iotbx.pdb.secondary_structure as ioss
  bad_anno=ioss.annotation.from_records(records=flex.split_lines(
      bad_two_chain_helix_ss_correct_resname))

  no_fix_fss=find_secondary_structure(hierarchy=hierarchy,
      user_annotation_text=bad_anno.as_pdb_str(),
      force_secondary_structure_input=True,
      combine_annotations=False,
      search_secondary_structure=False,out=null_out())
  print "\nInput:"
  print bad_anno.as_pdb_str()
  print "\nNot fixed:"
  print no_fix_fss.get_annotation().as_pdb_str()
  print "\nGood:"
  print fss.get_annotation().as_pdb_str()
  print "Is same as unfixed: ",  no_fix_fss.get_annotation().is_similar_to(
    hierarchy=hierarchy,other=bad_anno)
  assert no_fix_fss.get_annotation().is_similar_to(
    hierarchy=hierarchy,other=bad_anno)


  print "\nNow for antiparallel:Make sure force and original ss are equivalent"
  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(antiparallel_text)
         ).construct_hierarchy()
  fss=find_secondary_structure(hierarchy=hierarchy,
      combine_annotations=False,
      out=null_out())
  force_fss=find_secondary_structure(hierarchy=hierarchy,
      user_annotation_text=antiparallel_ss,
      force_secondary_structure_input=True,
      combine_annotations=False,
      out=null_out())
  number_of_good_h_bonds,number_of_poor_h_bonds=\
      force_fss.get_annotation().count_h_bonds(
      hierarchy=hierarchy,max_h_bond_length=3.0)
  print "Good H-bonds: %d  Poor H-Bonds: %d" %(
         number_of_good_h_bonds,
         number_of_poor_h_bonds,)
  assert number_of_good_h_bonds==3 and number_of_poor_h_bonds==1

  print "\nInput annotation:"
  print fss.get_annotation().as_pdb_str()
  print "\nOutput annotation:"
  print force_fss.get_annotation().as_pdb_str()
  print "\nIs same: ",fss.get_annotation().is_similar_to(
     other=force_fss.get_annotation(),hierarchy=hierarchy)


def tst_12():

  text="""
ATOM      8  CA  GLY A   2      24.485  19.185   6.248  1.00 11.14           C
HETATM   15  CA  23F A   3      26.939  16.455   5.194  1.00  9.61           C
ATOM     33  CA  ALA A   4      29.149  18.888   3.424  1.00  9.96           C
HETATM   43  CA  23F A   5      30.573  19.304   6.910  1.00  6.42           C
HETATM   61  CA  23F A   6      32.558  16.167   6.280  1.00  6.41           C
ATOM     79  CA  ALA A   7      35.089  18.339   4.563  1.00  6.26           C
HETATM   89  CA  23F A   8      36.195  19.092   8.094  1.00  6.38           C
HETATM  107  CA  23F A   9      38.283  15.914   7.621  1.00  7.78           C
ATOM    125  CA  ALA A  10      40.789  18.180   5.892  1.00  8.66           C
ATOM    135  CA  GLY A  11      41.608  19.716   9.325  1.00 10.78           C
ATOM    142  CA  GLY A  12      44.498  17.479   9.975  1.00 17.00           C
ATOM    149  CA  GLY A  13      43.927  17.193  13.603  1.00 13.58           C
ATOM    156  CA  GLY A  14      41.242  17.379  16.363  1.00 11.14           C
HETATM  163  CA  23F A  15      39.608  20.319  14.616  1.00  7.70           C
ATOM    181  CA  ALA A  16      38.402  17.853  12.023  1.00  7.08           C
ATOM    191  CA  LEU A  17      35.810  16.973  14.649  1.00  6.22           C
HETATM  210  CA  23F A  18      34.098  20.219  13.633  1.00  6.81           C
ATOM    228  CA  ALA A  19      32.642  18.019  10.889  1.00  6.28           C
ATOM    238  CA  LEU A  20      30.139  16.927  13.574  1.00  6.81           C
HETATM  257  CA  23F A  21      28.460  20.242  12.654  1.00  8.80           C
ATOM    275  CA  ALA A  22      27.017  18.382   9.700  1.00  7.89           C
"""

def tst_12():
  pdb_text="""
ATOM   3265  N   LYS A  11     -14.874  -4.165   7.826  1.00 14.62           N
ATOM   3266  CA  LYS A  11     -16.168  -3.852   7.241  1.00 15.85           C
ATOM   3267  C   LYS A  11     -16.310  -4.478   5.853  1.00 16.45           C
ATOM   3268  O   LYS A  11     -17.075  -5.419   5.680  1.00 17.01           O
ATOM   3269  CB  LYS A  11     -16.375  -2.333   7.183  1.00 15.92           C
ATOM   3279  N   ALA A  12     -15.570  -3.971   4.870  1.00 16.88           N
ATOM   3280  CA  ALA A  12     -15.727  -4.395   3.487  1.00 17.42           C
ATOM   3281  C   ALA A  12     -14.354  -4.610   2.875  1.00 17.46           C
ATOM   3282  O   ALA A  12     -13.333  -4.252   3.459  1.00 16.02           O
ATOM   3283  CB  ALA A  12     -16.525  -3.371   2.681  1.00 18.05           C
ATOM   3286  N   VAL A  13     -14.338  -5.186   1.671  1.00 16.89           N
ATOM   3287  CA  VAL A  13     -13.093  -5.691   1.103  1.00 17.82           C
ATOM   3288  C   VAL A  13     -12.694  -4.871  -0.112  1.00 17.45           C
ATOM   3289  O   VAL A  13     -13.105  -5.157  -1.241  1.00 17.89           O
ATOM   3290  CB  VAL A  13     -13.228  -7.182   0.746  1.00 17.97           C
ATOM   3292  N   GLY A  14     -11.871  -3.863   0.111  1.00 16.43           N
ATOM   3293  CA  GLY A  14     -11.449  -2.983  -0.958  1.00 15.97           C
ATOM   3294  C   GLY A  14      -9.986  -3.186  -1.252  1.00 15.81           C
ATOM   3295  O   GLY A  14      -9.221  -3.645  -0.406  1.00 15.35           O
ATOM   3303  N   LYS A  15      -9.601  -2.849  -2.479  1.00 15.98           N
ATOM   3304  CA  LYS A  15      -8.222  -2.951  -2.936  1.00 16.09           C
ATOM   3305  C   LYS A  15      -7.563  -1.610  -2.666  1.00 15.49           C
ATOM   3306  O   LYS A  15      -8.222  -0.574  -2.732  1.00 15.59           O
ATOM   3307  CB  LYS A  15      -8.149  -3.328  -4.412  1.00 16.75           C
ATOM    191  N   GLY A  16      -6.280  -1.630  -2.332  1.00 33.75           N
ATOM    192  CA  GLY A  16      -5.558  -0.433  -1.960  1.00 33.31           C
ATOM    193  C   GLY A  16      -4.172  -0.442  -2.546  1.00 31.97           C
ATOM    194  O   GLY A  16      -3.854  -1.323  -3.340  1.00 30.11           O
ATOM    199  N   ILE A  17      -3.342   0.521  -2.175  1.00 31.75           N
ATOM    200  CA  ILE A  17      -1.957   0.575  -2.628  1.00 31.88           C
ATOM    201  C   ILE A  17      -1.127   1.136  -1.486  1.00 31.99           C
ATOM    202  O   ILE A  17      -1.509   2.125  -0.859  1.00 31.57           O
ATOM    203  CB  ILE A  17      -1.800   1.416  -3.903  1.00 32.40           C
ATOM    204  N   VAL A  18       0.004   0.509  -1.198  1.00 32.65           N
ATOM    205  CA  VAL A  18       0.896   0.990  -0.150  1.00 33.76           C
ATOM    206  C   VAL A  18       1.576   2.251  -0.664  1.00 33.35           C
ATOM    207  O   VAL A  18       1.822   2.385  -1.864  1.00 32.40           O
ATOM    208  CB  VAL A  18       1.921  -0.084   0.242  1.00 34.81           C
ATOM    214  N   ALA A  19       1.864   3.189   0.235  1.00 33.49           N
ATOM    215  CA  ALA A  19       2.476   4.453  -0.156  1.00 33.94           C
ATOM    216  C   ALA A  19       3.647   4.826   0.744  1.00 33.82           C
ATOM    217  O   ALA A  19       4.665   5.324   0.270  1.00 34.04           O
ATOM    218  CB  ALA A  19       1.424   5.566  -0.161  1.00 33.76           C
ATOM      5  N   LYS A  20       3.524   4.588   2.035  1.00 20.21           N
ATOM      6  CA  LYS A  20       4.589   4.865   2.977  1.00 19.04           C
ATOM      7  C   LYS A  20       4.900   3.577   3.721  1.00 20.37           C
ATOM      8  O   LYS A  20       3.998   2.918   4.200  1.00 17.74           O
ATOM      9  CB  LYS A  20       4.180   5.980   3.946  1.00 22.23           C
ATOM   1297  N   GLY A  21       6.167   3.188   3.771  1.00 21.17           N
ATOM   1298  CA  GLY A  21       6.567   1.981   4.467  1.00 22.82           C
ATOM   1299  C   GLY A  21       7.532   2.314   5.576  1.00 24.28           C
ATOM   1300  O   GLY A  21       8.482   3.050   5.360  1.00 27.83           O
ATOM   1305  N   LYS A  22       7.291   1.774   6.768  1.00 26.26           N
ATOM   1306  CA  LYS A  22       8.105   2.113   7.923  1.00 27.25           C
ATOM   1307  C   LYS A  22       9.402   1.326   7.995  1.00 27.39           C
ATOM   1308  O   LYS A  22      10.038   1.312   9.052  1.00 29.75           O
ATOM   1309  CB  LYS A  22       7.323   1.893   9.220  1.00 26.82           C
ATOM   3906  N   LYS A  23       9.821   0.689   6.909  1.00 32.62           N
ATOM   3907  CA  LYS A  23      11.000  -0.160   6.913  1.00 33.45           C
ATOM   3908  C   LYS A  23      12.234   0.608   6.475  1.00 33.95           C
ATOM   3909  O   LYS A  23      12.243   1.267   5.436  1.00 34.22           O
ATOM   3910  CB  LYS A  23      10.814  -1.365   5.994  1.00 33.95           C
ATOM   3913  N   LYS A  24      13.291   0.499   7.271  1.00 33.95           N
ATOM   3914  CA  LYS A  24      14.615   0.840   6.781  1.00 32.30           C
ATOM   3915  C   LYS A  24      15.027  -0.172   5.724  1.00 31.52           C
ATOM   3916  O   LYS A  24      14.201  -0.949   5.241  1.00 29.72           O
ATOM   3917  CB  LYS A  24      15.613   0.857   7.933  1.00 34.60           C
ATOM   3920  N   ALA A  25      16.304  -0.163   5.349  1.00 27.55           N
ATOM   3921  CA  ALA A  25      16.838  -1.114   4.366  1.00 25.34           C
ATOM   3922  C   ALA A  25      16.151  -0.996   3.006  1.00 23.20           C
ATOM   3923  O   ALA A  25      16.799  -1.059   1.963  1.00 24.26           O
ATOM   3924  CB  ALA A  25      16.750  -2.552   4.874  1.00 26.43           C
ATOM   3932  N   ILE A  26      14.832  -0.838   3.002  1.00 20.88           N
ATOM   3933  CA  ILE A  26      14.048  -0.875   1.759  1.00 23.21           C
ATOM   3934  C   ILE A  26      14.475   0.341   0.951  1.00 21.96           C
ATOM   3935  O   ILE A  26      13.782   1.356   0.859  1.00 22.39           O
ATOM   3936  CB  ILE A  26      12.544  -0.903   2.023  1.00 20.20           C
ATOM   2399  N   GLY A  27      15.640   0.227   0.329  1.00 10.32           N
ATOM   2400  CA  GLY A  27      16.116   1.315  -0.491  1.00 10.62           C
ATOM   2401  C   GLY A  27      16.940   0.819  -1.650  1.00 10.75           C
ATOM   2402  O   GLY A  27      17.880   0.042  -1.462  1.00 10.08           O
ATOM   2407  N   GLY A  28      16.611   1.269  -2.854  1.00 11.47           N
ATOM   2408  CA  GLY A  28      17.308   0.770  -4.022  1.00 12.20           C
ATOM   2409  C   GLY A  28      17.197   1.622  -5.270  1.00 11.92           C
ATOM   2410  O   GLY A  28      16.494   1.244  -6.216  1.00 12.26           O
ATOM   2415  N   GLY A  29      17.894   2.762  -5.282  1.00 12.31           N
ATOM   2416  CA  GLY A  29      18.014   3.611  -6.460  1.00 12.71           C
ATOM   2417  C   GLY A  29      19.359   4.295  -6.410  1.00 12.69           C
ATOM   2418  O   GLY A  29      20.288   3.888  -7.087  1.00 13.22           O
ATOM    449  N   ILE A  30      19.449   5.350  -5.610  1.00 23.48           N
ATOM    450  CA  ILE A  30      20.728   5.833  -5.100  1.00 22.97           C
ATOM    451  C   ILE A  30      20.902   5.094  -3.760  1.00 23.25           C
ATOM    452  O   ILE A  30      20.443   3.960  -3.612  1.00 24.94           O
ATOM    453  N   LYS A  31      21.544   5.715  -2.779  1.00 22.86           N
ATOM    454  CA  LYS A  31      21.646   5.092  -1.470  1.00 22.95           C
ATOM    455  C   LYS A  31      20.766   5.753  -0.426  1.00 21.87           C
ATOM    456  O   LYS A  31      21.050   5.626   0.766  1.00 21.87           O
ATOM    457  CB  LYS A  31      23.094   5.108  -0.988  1.00 23.61           C
ATOM    459  N   VAL A  32      19.716   6.454  -0.841  1.00 19.42           N
ATOM    460  CA  VAL A  32      18.826   7.113   0.099  1.00 18.30           C
ATOM    461  C   VAL A  32      17.907   6.077   0.728  1.00 18.42           C
ATOM    462  O   VAL A  32      18.040   4.876   0.474  1.00 18.87           O
ATOM    463  CB  VAL A  32      18.032   8.215  -0.613  1.00 18.52           C
ATOM   1237  N   ILE A  33      16.962   6.536   1.539  1.00  9.62           N
ATOM   1238  CA  ILE A  33      15.980   5.673   2.178  1.00  8.49           C
ATOM   1239  C   ILE A  33      15.027   6.551   2.974  1.00  9.76           C
ATOM   1240  O   ILE A  33      15.455   7.295   3.858  1.00  8.68           O
ATOM   1241  CB  ILE A  33      16.645   4.634   3.086  1.00  8.36           C
ATOM   1245  N   ARG A  34      13.739   6.460   2.675  1.00 10.12           N
ATOM   1246  CA  ARG A  34      12.720   7.097   3.493  1.00 11.50           C
ATOM   1247  C   ARG A  34      12.176   6.092   4.497  1.00 11.68           C
ATOM   1248  O   ARG A  34      12.576   4.927   4.492  1.00 12.46           O
ATOM   1249  CB  ARG A  34      11.597   7.637   2.617  1.00 11.89           C
ATOM   1252  N   ALA A  35      11.261   6.542   5.359  1.00 12.69           N
ATOM   1253  CA  ALA A  35      10.695   5.705   6.407  1.00 12.80           C
ATOM   1254  C   ALA A  35       9.704   6.492   7.245  1.00 12.75           C
ATOM   1255  O   ALA A  35      10.102   7.213   8.159  1.00 10.48           O
ATOM   1256  CB  ALA A  35      11.786   5.152   7.326  1.00 13.55           C
ATOM   1260  N   GLY A  36       8.419   6.317   6.969  1.00 12.49           N
ATOM   1261  CA  GLY A  36       7.413   7.124   7.633  1.00 14.21           C
ATOM   1262  C   GLY A  36       6.724   6.371   8.750  1.00 14.40           C
ATOM   1263  O   GLY A  36       7.125   6.436   9.918  1.00 13.51           O
ATOM   1264  N   ILE A  37       5.631   5.667   8.361  1.00 14.51           N
ATOM   1265  CA  ILE A  37       4.757   4.897   9.247  1.00 15.20           C
ATOM   1266  C   ILE A  37       3.531   4.471   8.455  1.00 15.16           C
ATOM   1267  O   ILE A  37       2.628   5.268   8.222  1.00 15.72           O
ATOM   1268  CB  ILE A  37       4.357   5.694  10.504  1.00 14.18           C
ATOM   2971  N   VAL A  38       3.481   3.184   8.101  1.00  9.75           N
ATOM   2972  CA  VAL A  38       2.765   2.611   6.949  1.00 10.34           C
ATOM   2973  C   VAL A  38       1.415   3.251   6.635  1.00  9.75           C
ATOM   2974  O   VAL A  38       0.701   3.685   7.540  1.00 10.53           O
ATOM   2975  CB  VAL A  38       2.595   1.089   7.128  1.00 11.46           C
ATOM    263  N   GLY A  39       1.054   3.302   5.349  1.00 16.54           N
ATOM    264  CA  GLY A  39      -0.179   3.934   4.919  1.00 17.07           C
ATOM    265  C   GLY A  39      -0.606   3.526   3.528  1.00 16.93           C
ATOM    266  O   GLY A  39       0.234   3.196   2.695  1.00 17.75           O
ATOM    273  N   LYS A  40      -1.905   3.551   3.256  1.00 16.86           N
ATOM    274  CA  LYS A  40      -2.430   2.997   2.011  1.00 17.62           C
ATOM    275  C   LYS A  40      -3.416   3.986   1.407  1.00 18.44           C
ATOM    276  O   LYS A  40      -3.964   4.825   2.121  1.00 18.27           O
ATOM    277  CB  LYS A  40      -3.100   1.654   2.268  1.00 17.83           C
ATOM      5  N   VAL A  41      -3.644   3.888   0.105  1.00 20.21           N
ATOM      6  CA  VAL A  41      -4.654   4.679  -0.580  1.00 19.04           C
ATOM      7  C   VAL A  41      -5.536   3.711  -1.345  1.00 20.37           C
ATOM      8  O   VAL A  41      -5.039   2.917  -2.149  1.00 17.74           O
ATOM      9  CB  VAL A  41      -4.021   5.719  -1.517  1.00 22.23           C
ATOM   1969  N   LYS A  42      -6.836   3.764  -1.090  1.00 12.88           N
ATOM   1970  CA  LYS A  42      -7.784   2.830  -1.684  1.00 14.47           C
ATOM   1971  C   LYS A  42      -7.782   3.004  -3.194  1.00 13.46           C
ATOM   1972  O   LYS A  42      -7.234   3.982  -3.705  1.00 14.70           O
ATOM   1973  CB  LYS A  42      -9.180   3.041  -1.109  1.00 15.03           C
ATOM   1976  N   VAL A  43      -8.373   2.053  -3.908  1.00 12.97           N
ATOM   1977  CA  VAL A  43      -8.322   2.024  -5.361  1.00 14.42           C
ATOM   1978  C   VAL A  43      -9.555   1.303  -5.878  1.00 14.78           C
ATOM   1979  O   VAL A  43     -10.114   0.446  -5.188  1.00 14.65           O
ATOM   1980  CB  VAL A  43      -7.043   1.339  -5.875  1.00 13.91           C
ATOM   1984  N   SER A  44     -10.000   1.673  -7.073  1.00 15.03           N
ATOM   1985  CA  SER A  44     -11.023   0.891  -7.741  1.00 15.75           C
ATOM   1986  C   SER A  44     -10.368  -0.303  -8.413  1.00 15.86           C
ATOM   1987  O   SER A  44      -9.147  -0.360  -8.551  1.00 15.75           O
ATOM   1988  CB  SER A  44     -11.768   1.745  -8.762  1.00 16.01           C
ATOM   1989  N   LYS A  45     -11.179  -1.267  -8.826  1.00 16.93           N
ATOM   1990  CA  LYS A  45     -10.625  -2.460  -9.445  1.00 17.52           C
ATOM   1991  C   LYS A  45     -10.218  -2.198 -10.892  1.00 17.12           C
ATOM   1992  O   LYS A  45      -9.270  -2.810 -11.391  1.00 18.20           O
ATOM   1993  CB  LYS A  45     -11.629  -3.607  -9.366  1.00 18.01           C
ATOM   1881  N   ASP A  46     -10.915  -1.298 -11.583  1.00 20.72           N
ATOM   1882  CA  ASP A  46     -10.523  -0.966 -12.946  1.00 21.11           C
ATOM   1883  C   ASP A  46      -9.778   0.363 -13.015  1.00 21.62           C
ATOM   1884  O   ASP A  46      -8.732   0.469 -13.665  1.00 20.59           O
ATOM   1885  CB  ASP A  46     -11.747  -0.928 -13.857  1.00 21.60           C
ATOM   1893  N   ALA A  47     -10.301   1.380 -12.347  1.00 20.82           N
ATOM   1894  CA  ALA A  47      -9.733   2.713 -12.424  1.00 20.91           C
ATOM   1895  C   ALA A  47      -8.475   2.824 -11.574  1.00 20.66           C
ATOM   1896  O   ALA A  47      -7.683   1.879 -11.483  1.00 22.58           O
ATOM   1897  CB  ALA A  47     -10.756   3.761 -11.979  1.00 20.41           C
ATOM   1901  N   VAL A  48      -8.294   4.001 -10.974  1.00 20.80           N
ATOM   1902  CA  VAL A  48      -7.114   4.275 -10.166  1.00 21.07           C
ATOM   1903  C   VAL A  48      -7.477   4.641  -8.728  1.00 21.38           C
ATOM   1904  O   VAL A  48      -7.724   3.749  -7.915  1.00 22.41           O
ATOM   1905  CB  VAL A  48      -6.270   5.380 -10.817  1.00 21.52           C
ATOM   1909  N   ALA A  49      -7.528   5.927  -8.391  1.00 21.20           N
ATOM   1910  CA  ALA A  49      -7.793   6.318  -7.011  1.00 22.10           C
ATOM   1911  C   ALA A  49      -9.288   6.274  -6.724  1.00 22.33           C
ATOM   1912  O   ALA A  49     -10.084   5.954  -7.606  1.00 22.72           O
ATOM   1913  CB  ALA A  49      -7.230   7.708  -6.733  1.00 22.39           C
ATOM   1293  N   ILE A  50      -9.665   6.569  -5.482  1.00 15.59           N
ATOM   1294  CA  ILE A  50     -11.064   6.537  -5.061  1.00 14.93           C
ATOM   1295  C   ILE A  50     -11.437   7.694  -4.146  1.00 14.02           C
ATOM   1296  O   ILE A  50     -12.402   7.562  -3.377  1.00 13.06           O
ATOM   1297  CB  ILE A  50     -11.418   5.198  -4.382  1.00 14.73           C
ATOM   1300  N   LYS A  51     -10.693   8.799  -4.187  1.00 12.35           N
ATOM   1301  CA  LYS A  51     -10.992  10.061  -3.519  1.00 11.94           C
ATOM   1302  C   LYS A  51      -9.740  10.921  -3.593  1.00 12.47           C
ATOM   1303  O   LYS A  51      -8.663  10.442  -3.947  1.00 12.54           O
ATOM   1304  CB  LYS A  51     -11.426   9.877  -2.064  1.00 12.38           C
ATOM   1312  N   GLY A  52      -9.892  12.204  -3.270  1.00 12.56           N
ATOM   1313  CA  GLY A  52      -8.751  13.100  -3.195  1.00 12.72           C
ATOM   1314  C   GLY A  52      -8.035  13.020  -1.860  1.00 13.42           C
ATOM   1315  O   GLY A  52      -8.581  13.435  -0.839  1.00 14.00           O
ATOM   1319  N   ASP A  53      -6.808  12.510  -1.855  1.00 12.19           N
ATOM   1320  CA  ASP A  53      -6.110  12.121  -0.631  1.00 13.93           C
ATOM   1321  C   ASP A  53      -5.430  13.323  -0.005  1.00 13.79           C
ATOM   1322  O   ASP A  53      -5.474  14.428  -0.540  1.00 14.44           O
ATOM   1323  CB  ASP A  53      -5.076  11.043  -0.931  1.00 14.33           C
ATOM   2041  N   GLY A  54      -4.774  13.101   1.124  1.00 17.99           N
ATOM   2042  CA  GLY A  54      -3.898  14.102   1.699  1.00 18.66           C
ATOM   2043  C   GLY A  54      -4.412  14.606   3.025  1.00 18.49           C
ATOM   2044  O   GLY A  54      -5.322  14.033   3.626  1.00 17.63           O
ATOM   2786  N   GLY A  55      -3.802  15.690   3.480  1.00 11.04           N
ATOM   2787  CA  GLY A  55      -4.206  16.360   4.695  1.00 10.44           C
ATOM   2788  C   GLY A  55      -3.005  16.632   5.581  1.00 11.03           C
ATOM   2789  O   GLY A  55      -1.986  17.154   5.145  1.00 10.97           O
ATOM   2792  N   GLY A  56      -3.165  16.290   6.857  1.00 13.14           N
ATOM   2793  CA  GLY A  56      -2.044  16.293   7.770  1.00 14.46           C
ATOM   2794  C   GLY A  56      -1.169  15.067   7.652  1.00 15.15           C
ATOM   2795  O   GLY A  56      -0.106  15.017   8.280  1.00 19.82           O
ATOM    363  N   ALA A  57      -1.583  14.078   6.862  1.00 20.15           N
ATOM    364  CA  ALA A  57      -0.839  12.836   6.718  1.00 20.14           C
ATOM    365  C   ALA A  57      -0.498  12.547   5.266  1.00 19.98           C
ATOM    366  O   ALA A  57      -0.530  11.393   4.844  1.00 19.91           O
ATOM    367  CB  ALA A  57      -1.620  11.670   7.325  1.00 20.73           C
ATOM    371  N   GLY A  58      -0.166  13.569   4.495  1.00 19.39           N
ATOM    372  CA  GLY A  58       0.160  13.363   3.105  1.00 19.02           C
ATOM    373  C   GLY A  58       1.646  13.352   2.847  1.00 19.48           C
ATOM    374  O   GLY A  58       2.311  14.384   2.950  1.00 18.91           O
ATOM    377  N   ILE A  59       2.177  12.185   2.519  1.00 20.12           N
ATOM    378  CA  ILE A  59       3.568  12.028   2.124  1.00 21.09           C
ATOM    379  C   ILE A  59       3.733  10.627   1.556  1.00 21.27           C
ATOM    380  O   ILE A  59       3.966   9.675   2.301  1.00 22.08           O
ATOM    381  CB  ILE A  59       4.525  12.267   3.300  1.00 21.22           C
ATOM   2210  N   LYS A  60       3.590  10.492   0.247  1.00 30.93           N
ATOM   2211  CA  LYS A  60       3.884   9.238  -0.415  1.00 30.78           C
ATOM   2212  C   LYS A  60       5.392   9.069  -0.462  1.00 30.67           C
ATOM   2213  O   LYS A  60       6.118   9.757   0.257  1.00 30.90           O
ATOM   2214  CB  LYS A  60       3.289   9.232  -1.818  1.00 31.02           C
ATOM   2221  N   ALA A  61       5.871   8.169  -1.309  1.00 30.33           N
ATOM   2222  CA  ALA A  61       7.299   7.964  -1.493  1.00 30.26           C
ATOM   2223  C   ALA A  61       7.651   8.280  -2.938  1.00 30.68           C
ATOM   2224  O   ALA A  61       6.856   8.027  -3.844  1.00 30.49           O
ATOM   2225  CB  ALA A  61       7.697   6.538  -1.137  1.00 29.87           C
ATOM   2224  N   ARG A  62       8.845   8.826  -3.154  1.00 25.61           N
ATOM   2225  CA  ARG A  62       9.290   9.085  -4.515  1.00 25.59           C
ATOM   2226  C   ARG A  62       9.350   7.805  -5.330  1.00 25.38           C
ATOM   2227  O   ARG A  62       9.267   7.852  -6.561  1.00 25.11           O
ATOM   2228  CB  ARG A  62      10.655   9.771  -4.506  1.00 26.01           C
ATOM   2229  N   ALA A  63       9.489   6.657  -4.669  1.00 25.45           N
ATOM   2230  CA  ALA A  63       9.487   5.394  -5.392  1.00 25.77           C
ATOM   2231  C   ALA A  63       8.192   5.196  -6.167  1.00 25.02           C
ATOM   2232  O   ALA A  63       8.186   4.511  -7.193  1.00 24.90           O
ATOM   2233  CB  ALA A  63       9.715   4.237  -4.424  1.00 26.08           C
ATOM   2238  N   LYS A  64       7.093   5.809  -5.724  1.00 24.57           N
ATOM   2239  CA  LYS A  64       5.841   5.665  -6.455  1.00 24.50           C
ATOM   2240  C   LYS A  64       5.925   6.269  -7.845  1.00 24.15           C
ATOM   2241  O   LYS A  64       5.025   6.053  -8.661  1.00 24.20           O
ATOM   2242  CB  LYS A  64       4.691   6.281  -5.665  1.00 24.19           C
ATOM    149  N   LYS A  65       7.006   6.976  -8.153  1.00 20.45           N
ATOM    150  CA  LYS A  65       7.282   7.415  -9.513  1.00 20.20           C
ATOM    151  C   LYS A  65       7.482   6.227 -10.444  1.00 20.10           C
ATOM    152  O   LYS A  65       7.850   6.397 -11.607  1.00 21.12           O
ATOM    153  CB  LYS A  65       8.514   8.322  -9.538  1.00 19.83           C
ATOM    154  N   LYS A  66       7.263   5.025  -9.938  1.00 17.29           N
ATOM    155  CA  LYS A  66       7.155   3.819 -10.749  1.00 17.32           C
ATOM    156  C   LYS A  66       5.686   3.638 -11.116  1.00 19.29           C
ATOM    157  O   LYS A  66       5.181   2.514 -11.159  1.00 18.79           O
ATOM    158  CB  LYS A  66       7.687   2.606 -10.000  1.00 17.96           C
ATOM    161  N   GLY A  67       4.994   4.753 -11.343  1.00 19.37           N
ATOM    162  CA  GLY A  67       3.673   4.711 -11.935  1.00 21.34           C
ATOM    163  C   GLY A  67       2.563   5.305 -11.110  1.00 21.74           C
ATOM    164  O   GLY A  67       1.532   4.657 -10.943  1.00 22.38           O
ATOM    165  N   GLY A  68       2.723   6.521 -10.607  1.00 20.48           N
ATOM    166  CA  GLY A  68       1.738   7.091  -9.712  1.00 19.86           C
ATOM    167  C   GLY A  68       0.960   8.276 -10.250  1.00 20.71           C
ATOM    168  O   GLY A  68       1.521   9.347 -10.495  1.00 20.81           O
ATOM    781  N   GLY A  69      -0.344   8.089 -10.439  1.00 16.86           N
ATOM    782  CA  GLY A  69      -1.254   9.192 -10.679  1.00 17.03           C
ATOM    783  C   GLY A  69      -1.751   9.734  -9.357  1.00 17.13           C
ATOM    784  O   GLY A  69      -2.764  10.436  -9.287  1.00 17.67           O
ATOM    789  N   LYS A  70      -1.039   9.362  -8.294  1.00 16.95           N
ATOM    790  CA  LYS A  70      -1.236   9.895  -6.951  1.00 17.08           C
ATOM    791  C   LYS A  70      -0.354  11.127  -6.811  1.00 16.68           C
ATOM    792  O   LYS A  70       0.540  11.180  -5.967  1.00 16.80           O
ATOM    793  CB  LYS A  70      -0.908   8.845  -5.897  1.00 17.17           C
ATOM    797  N   LYS A  71      -0.582  12.110  -7.679  1.00 16.94           N
ATOM    798  CA  LYS A  71      -0.103  13.471  -7.489  1.00 17.08           C
ATOM    799  C   LYS A  71      -1.061  14.233  -6.590  1.00 17.51           C
ATOM    800  O   LYS A  71      -1.126  15.461  -6.633  1.00 17.76           O
ATOM    801  CB  LYS A  71       0.064  14.193  -8.823  1.00 16.48           C
ATOM    804  N   SER A  72      -1.826  13.498  -5.787  1.00 17.36           N
ATOM    805  CA  SER A  72      -2.715  14.065  -4.790  1.00 17.64           C
ATOM    806  C   SER A  72      -2.081  14.099  -3.406  1.00 17.95           C
ATOM    807  O   SER A  72      -2.789  14.304  -2.419  1.00 19.26           O
ATOM    808  CB  SER A  72      -4.030  13.284  -4.760  1.00 16.94           C
ATOM    814  N   GLY A  73      -0.767  13.914  -3.311  1.00 17.32           N
ATOM    815  CA  GLY A  73      -0.067  13.999  -2.048  1.00 17.70           C
ATOM    816  C   GLY A  73       0.799  15.236  -1.978  1.00 18.50           C
ATOM    817  O   GLY A  73       0.720  16.131  -2.820  1.00 18.13           O
ATOM    818  N   ALA A  74       1.640  15.288  -0.948  1.00 18.71           N
ATOM    819  CA  ALA A  74       2.639  16.339  -0.801  1.00 19.65           C
ATOM    820  C   ALA A  74       3.987  15.786  -0.345  1.00 20.21           C
ATOM    821  O   ALA A  74       4.488  16.159   0.714  1.00 20.94           O
ATOM    822  CB  ALA A  74       2.147  17.406   0.168  1.00 19.63           C
ATOM    829  N   LYS A  75       4.578  14.893  -1.132  1.00 20.07           N
ATOM    830  CA  LYS A  75       5.874  14.306  -0.815  1.00 19.78           C
ATOM    831  C   LYS A  75       6.973  15.359  -0.868  1.00 19.42           C
ATOM    832  O   LYS A  75       6.975  16.315  -0.095  1.00 19.47           O
ATOM    833  CB  LYS A  75       6.202  13.162  -1.779  1.00 19.85           C
TER
ATOM      1  N   ARG A  81     -10.933  -1.719  10.506  1.00 27.82           N
ATOM      2  CA  ARG A  81     -11.823  -1.081   9.549  1.00 23.15           C
ATOM      3  C   ARG A  81     -11.988  -1.971   8.326  1.00 24.44           C
ATOM      4  O   ARG A  81     -12.205  -3.166   8.454  1.00 23.56           O
ATOM      5  N   ILE A  82     -11.875  -1.381   7.142  1.00 20.21           N
ATOM      6  CA  ILE A  82     -12.024  -2.097   5.881  1.00 19.04           C
ATOM      7  C   ILE A  82     -10.960  -3.191   5.811  1.00 20.37           C
ATOM      8  O   ILE A  82      -9.946  -3.125   6.503  1.00 17.74           O
ATOM      9  CB  ILE A  82     -11.921  -1.138   4.692  1.00 22.23           C
ATOM    546  N   VAL A  83     -11.184  -4.199   4.975  1.00 22.37           N
ATOM    547  CA  VAL A  83     -10.271  -5.334   4.882  1.00 26.00           C
ATOM    548  C   VAL A  83      -9.683  -5.376   3.480  1.00 30.26           C
ATOM    549  O   VAL A  83     -10.257  -5.985   2.576  1.00 35.19           O
ATOM    550  CB  VAL A  83     -10.987  -6.648   5.223  1.00 25.74           C
ATOM    555  N   VAL A  84      -8.519  -4.763   3.306  1.00 24.40           N
ATOM    556  CA  VAL A  84      -7.998  -4.413   1.994  1.00 26.29           C
ATOM    557  C   VAL A  84      -7.173  -5.555   1.420  1.00 28.06           C
ATOM    558  O   VAL A  84      -6.494  -6.285   2.134  1.00 29.61           O
ATOM    559  CB  VAL A  84      -7.159  -3.125   2.053  1.00 31.28           C
ATOM    566  N   ILE A  85      -7.231  -5.697   0.103  1.00 30.54           N
ATOM    567  CA  ILE A  85      -6.344  -6.591  -0.621  1.00 29.29           C
ATOM    568  C   ILE A  85      -5.288  -5.732  -1.291  1.00 31.77           C
ATOM    569  O   ILE A  85      -5.224  -5.656  -2.519  1.00 31.74           O
ATOM    570  CB  ILE A  85      -7.097  -7.446  -1.645  1.00 30.40           C
ATOM    574  N   ILE A  86      -4.461  -5.091  -0.486  1.00 28.71           N
ATOM    575  CA  ILE A  86      -3.466  -4.149  -0.972  1.00 31.03           C
ATOM    576  C   ILE A  86      -2.529  -4.827  -1.953  1.00 32.44           C
ATOM    577  O   ILE A  86      -2.334  -6.037  -1.912  1.00 36.01           O
ATOM    578  CB  ILE A  86      -2.679  -3.530   0.199  1.00 25.27           C
ATOM    718  N   GLY A  87      -1.968  -4.055  -2.861  1.00  9.32           N
ATOM    719  CA  GLY A  87      -0.932  -4.502  -3.767  1.00  7.48           C
ATOM    720  C   GLY A  87      -0.251  -3.320  -4.410  1.00  7.50           C
ATOM    721  O   GLY A  87      -0.783  -2.757  -5.368  1.00 10.36           O
ATOM    726  N   GLY A  88       0.919  -2.932  -3.888  1.00  9.75           N
ATOM    727  CA  GLY A  88       1.563  -1.693  -4.258  1.00  9.75           C
ATOM    728  C   GLY A  88       3.052  -1.667  -3.956  1.00 10.39           C
ATOM    729  O   GLY A  88       3.761  -2.663  -4.113  1.00 11.83           O
ATOM    734  N   ILE A  89       3.521  -0.493  -3.507  1.00 10.14           N
ATOM    735  CA  ILE A  89       4.944  -0.178  -3.331  1.00 12.16           C
ATOM    736  C   ILE A  89       5.495  -0.650  -1.987  1.00  8.45           C
ATOM    737  O   ILE A  89       5.766   0.166  -1.097  1.00 13.94           O
ATOM    738  CB  ILE A  89       5.204   1.331  -3.485  1.00 15.51           C
ATOM    746  N   LYS A  90       5.681  -1.967  -1.845  1.00 10.12           N
ATOM    747  CA  LYS A  90       6.148  -2.597  -0.617  1.00  8.93           C
ATOM    748  C   LYS A  90       5.631  -4.028  -0.556  1.00  6.60           C
ATOM    749  O   LYS A  90       5.807  -4.788  -1.504  1.00  9.21           O
ATOM      5  N   VAL A  91       5.002  -4.404   0.553  1.00 20.21           N
ATOM      6  CA  VAL A  91       4.298  -5.673   0.720  1.00 19.04           C
ATOM      7  C   VAL A  91       5.176  -6.898   0.503  1.00 20.37           C
ATOM      8  O   VAL A  91       5.212  -7.447  -0.599  1.00 17.74           O
ATOM      9  CB  VAL A  91       3.087  -5.740  -0.219  1.00 22.23           C
ATOM   3961  N   LYS A  92       5.856  -7.361   1.551  1.00 27.85           N
ATOM   3962  CA  LYS A  92       6.534  -8.646   1.492  1.00 28.85           C
ATOM   3963  C   LYS A  92       5.486  -9.714   1.271  1.00 29.89           C
ATOM   3964  O   LYS A  92       4.298  -9.472   1.464  1.00 29.91           O
ATOM   3965  N   ALA A  93       5.914 -10.896   0.865  1.00 31.04           N
ATOM   3966  CA  ALA A  93       4.991 -11.881   0.329  1.00 32.00           C
ATOM   3967  C   ALA A  93       4.826 -13.092   1.236  1.00 32.74           C
ATOM   3968  O   ALA A  93       5.773 -13.537   1.890  1.00 32.70           O
ATOM   3969  CB  ALA A  93       5.448 -12.347  -1.048  1.00 32.14           C
ATOM   3972  N   LYS A  94       3.604 -13.615   1.256  1.00 33.67           N
ATOM   3973  CA  LYS A  94       3.306 -14.983   1.651  1.00 34.45           C
ATOM   3974  C   LYS A  94       2.420 -15.578   0.567  1.00 34.91           C
ATOM   3975  O   LYS A  94       1.197 -15.637   0.717  1.00 34.86           O
ATOM   3976  CB  LYS A  94       2.616 -15.036   3.006  1.00 34.55           C
ATOM   3981  N   ILE A  95       3.040 -15.999  -0.525  1.00 35.68           N
ATOM   3982  CA  ILE A  95       2.350 -16.583  -1.663  1.00 36.06           C
ATOM   3983  C   ILE A  95       3.326 -16.436  -2.814  1.00 36.64           C
ATOM   3984  O   ILE A  95       4.488 -16.084  -2.602  1.00 36.89           O
ATOM   3985  N   GLY A  96       2.876 -16.714  -4.028  1.00 37.18           N
ATOM   3986  CA  GLY A  96       3.567 -16.234  -5.207  1.00 37.54           C
ATOM   3987  C   GLY A  96       2.749 -15.074  -5.715  1.00 37.30           C
ATOM   3988  O   GLY A  96       1.682 -15.285  -6.291  1.00 37.64           O
ATOM   2898  N   ALA A  97       3.190 -13.847  -5.478  1.00 10.14           N
ATOM   2899  CA  ALA A  97       2.185 -12.800  -5.494  1.00 11.76           C
ATOM   2900  C   ALA A  97       2.720 -11.537  -6.141  1.00 11.70           C
ATOM   2901  O   ALA A  97       3.610 -10.879  -5.596  1.00 11.58           O
ATOM   2902  CB  ALA A  97       1.697 -12.502  -4.074  1.00 13.45           C
ATOM   2904  N   LYS A  98       2.143 -11.204  -7.307  1.00 11.11           N
ATOM   2905  CA  LYS A  98       2.267  -9.877  -7.899  1.00 11.97           C
ATOM   2906  C   LYS A  98       1.355  -8.867  -7.224  1.00 13.33           C
ATOM   2907  O   LYS A  98       1.823  -7.792  -6.847  1.00 13.19           O
ATOM   2908  CB  LYS A  98       1.962  -9.920  -9.390  1.00 11.60           C
ATOM   2910  N   LYS A  99       0.074  -9.165  -7.073  1.00 14.27           N
ATOM   2911  CA  LYS A  99      -0.777  -8.405  -6.169  1.00 16.74           C
ATOM   2912  C   LYS A  99      -0.888  -9.174  -4.863  1.00 17.34           C
ATOM   2913  O   LYS A  99      -1.407 -10.286  -4.829  1.00 18.30           O
ATOM   2914  CB  LYS A  99      -2.171  -8.161  -6.763  1.00 18.21           C
ATOM   2918  N   VAL A 100      -0.362  -8.593  -3.784  1.00 18.48           N
ATOM   2919  CA  VAL A 100      -0.280  -9.286  -2.501  1.00 18.43           C
ATOM   2920  C   VAL A 100      -1.650  -9.810  -2.116  1.00 18.02           C
ATOM   2921  O   VAL A 100      -2.308  -9.283  -1.206  1.00 17.17           O
ATOM   2922  CB  VAL A 100       0.300  -8.382  -1.401  1.00 19.81           C
ATOM   9078  N   GLY A 101      -2.064 -10.885  -2.791  1.00 14.81           N
ATOM   9079  CA  GLY A 101      -3.396 -11.459  -2.697  1.00 14.61           C
ATOM   9080  C   GLY A 101      -3.816 -11.831  -1.300  1.00 15.70           C
ATOM   9081  O   GLY A 101      -4.495 -12.837  -1.075  1.00 19.52           O
ATOM   9086  N   GLY A 102      -3.405 -11.010  -0.355  1.00 15.31           N
ATOM   9087  CA  GLY A 102      -3.685 -11.285   1.022  1.00 16.53           C
ATOM   9088  C   GLY A 102      -4.695 -10.267   1.436  1.00 13.65           C
ATOM   9089  O   GLY A 102      -4.825  -9.244   0.768  1.00 13.71           O
ATOM   9095  N   VAL A 103      -5.429 -10.520   2.508  1.00 17.42           N
ATOM   9096  CA  VAL A 103      -6.373  -9.523   2.953  1.00 17.66           C
ATOM   9097  C   VAL A 103      -5.844  -8.885   4.220  1.00 17.97           C
ATOM   9098  O   VAL A 103      -6.282  -9.213   5.327  1.00 16.61           O
ATOM   9099  CB  VAL A 103      -7.763 -10.141   3.142  1.00 17.30           C
ATOM   9102  N   ILE A 104      -4.890  -7.966   4.061  1.00 14.21           N
ATOM   9103  CA  ILE A 104      -4.452  -7.082   5.130  1.00 15.11           C
ATOM   9104  C   ILE A 104      -5.597  -6.134   5.455  1.00 16.87           C
ATOM   9105  O   ILE A 104      -6.647  -6.165   4.813  1.00 15.71           O
ATOM   9106  CB  ILE A 104      -3.180  -6.311   4.746  1.00 15.53           C
ATOM   9110  N   LYS A 105      -5.399  -5.278   6.449  1.00 16.52           N
ATOM   9111  CA  LYS A 105      -6.520  -4.544   7.031  1.00 17.93           C
ATOM   9112  C   LYS A 105      -6.201  -3.052   7.074  1.00 17.88           C
ATOM   9113  O   LYS A 105      -5.045  -2.646   7.092  1.00 18.77           O
ATOM   9114  CB  LYS A 105      -6.824  -5.102   8.410  1.00 18.90           C
ATOM      5  N   ALA A 106      -7.232  -2.216   7.115  1.00 20.21           N
ATOM      6  CA  ALA A 106      -7.056  -0.781   6.956  1.00 19.04           C
ATOM      7  C   ALA A 106      -7.931   0.002   7.928  1.00 20.37           C
ATOM      8  O   ALA A 106      -9.066  -0.386   8.200  1.00 17.74           O
ATOM      9  CB  ALA A 106      -7.372  -0.379   5.523  1.00 22.23           C
ATOM   4765  N   ILE A 107      -7.413   1.116   8.427  1.00 15.76           N
ATOM   4766  CA  ILE A 107      -8.037   1.869   9.505  1.00 16.10           C
ATOM   4767  C   ILE A 107      -8.385   3.260   8.981  1.00 16.16           C
ATOM   4768  O   ILE A 107      -7.719   4.245   9.315  1.00 16.39           O
ATOM   4769  CB  ILE A 107      -7.129   1.951  10.734  1.00 16.21           C
ATOM   4772  N   ARG A 108      -9.446   3.365   8.184  1.00 16.03           N
ATOM   4773  CA  ARG A 108      -9.875   4.668   7.688  1.00 16.68           C
ATOM   4774  C   ARG A 108     -10.775   4.501   6.471  1.00 16.75           C
ATOM   4775  O   ARG A 108     -10.508   3.666   5.608  1.00 17.20           O
ATOM   4776  N   ARG A 109     -11.843   5.288   6.384  1.00 16.99           N
ATOM   4777  CA  ARG A 109     -12.827   5.134   5.322  1.00 17.03           C
ATOM   4778  C   ARG A 109     -13.169   6.448   4.638  1.00 16.97           C
ATOM   4779  O   ARG A 109     -14.132   7.110   5.019  1.00 17.08           O
ATOM   4780  N   GLY A 110     -12.410   6.827   3.628  1.00 16.68           N
ATOM   4781  CA  GLY A 110     -12.642   8.085   2.962  1.00 16.30           C
ATOM   4782  C   GLY A 110     -11.689   8.321   1.812  1.00 15.96           C
ATOM   4783  O   GLY A 110     -11.854   7.791   0.716  1.00 15.78           O
ATOM    806  N   ILE A 111     -10.649   9.116   2.095  1.00 15.21           N
ATOM    807  CA  ILE A 111      -9.750   9.578   1.038  1.00 15.25           C
ATOM    808  C   ILE A 111      -8.321   9.099   1.283  1.00 14.48           C
ATOM    809  O   ILE A 111      -7.801   8.237   0.566  1.00 13.95           O
ATOM    810  CB  ILE A 111      -9.818  11.109   0.914  1.00 18.69           C
ATOM    817  N   LYS A 112      -7.659   9.668   2.288  1.00 13.23           N
ATOM    818  CA  LYS A 112      -6.223   9.478   2.464  1.00 12.29           C
ATOM    819  C   LYS A 112      -5.854   8.095   2.963  1.00 11.93           C
ATOM    820  O   LYS A 112      -4.663   7.826   3.179  1.00 12.30           O
ATOM    821  CB  LYS A 112      -5.666  10.517   3.435  1.00 13.42           C
ATOM    826  N   VAL A 113      -6.841   7.227   3.178  1.00 11.35           N
ATOM    827  CA  VAL A 113      -6.604   5.842   3.569  1.00 10.38           C
ATOM    828  C   VAL A 113      -5.998   5.810   4.962  1.00 11.79           C
ATOM    829  O   VAL A 113      -5.491   6.818   5.458  1.00 13.75           O
ATOM    830  N   GLY A 114      -6.049   4.653   5.606  1.00 10.10           N
ATOM    831  CA  GLY A 114      -5.425   4.485   6.899  1.00  9.84           C
ATOM    832  C   GLY A 114      -4.098   3.765   6.757  1.00 10.25           C
ATOM    833  O   GLY A 114      -3.749   3.273   5.691  1.00  9.82           O
ATOM      5  N   GLY A 115      -3.373   3.728   7.868  1.00 20.21           N
ATOM      6  CA  GLY A 115      -2.267   2.805   7.963  1.00 19.04           C
ATOM      7  C   GLY A 115      -2.770   1.375   7.931  1.00 20.37           C
ATOM      8  O   GLY A 115      -3.792   1.040   8.528  1.00 17.74           O
ATOM    775  N   GLY A 116      -2.062   0.527   7.203  1.00 16.60           N
ATOM    776  CA  GLY A 116      -2.402  -0.870   7.202  1.00 17.27           C
ATOM    777  C   GLY A 116      -2.317  -1.462   8.594  1.00 19.96           C
ATOM    778  O   GLY A 116      -1.650  -0.942   9.481  1.00 18.97           O
ATOM    786  N   LYS A 117      -3.011  -2.575   8.793  1.00 20.70           N
ATOM    787  CA  LYS A 117      -2.870  -3.317  10.035  1.00 20.75           C
ATOM    788  C   LYS A 117      -2.072  -4.590   9.793  1.00 26.23           C
ATOM    789  O   LYS A 117      -2.473  -5.451   9.007  1.00 38.53           O
ATOM    790  CB  LYS A 117      -4.236  -3.637  10.639  1.00 23.72           C
ATOM   1832  N   ILE A 118      -0.938  -4.698  10.472  1.00 12.23           N
ATOM   1833  CA  ILE A 118      -0.002  -5.792  10.295  1.00 12.84           C
ATOM   1834  C   ILE A 118       1.212  -5.529  11.182  1.00 12.33           C
ATOM   1835  O   ILE A 118       1.098  -5.094  12.329  1.00 11.94           O
ATOM   1836  CB  ILE A 118       0.416  -5.975   8.818  1.00 13.17           C
ATOM   2465  N   ALA A 119       2.387  -5.797  10.617  1.00 13.65           N
ATOM   2466  CA  ALA A 119       3.683  -5.570  11.236  1.00 12.43           C
ATOM   2467  C   ALA A 119       4.432  -4.444  10.535  1.00 13.72           C
ATOM   2468  O   ALA A 119       5.295  -4.711   9.697  1.00 14.32           O
ATOM   2469  CB  ALA A 119       4.520  -6.843  11.180  1.00 12.02           C
ATOM     31  N   VAL A 120       4.126  -3.185  10.860  1.00  5.87           N
ATOM     32  CA  VAL A 120       4.852  -2.058  10.280  1.00  6.28           C
ATOM     33  C   VAL A 120       6.325  -2.200  10.613  1.00  6.30           C
ATOM     34  O   VAL A 120       6.767  -1.822  11.701  1.00  6.82           O
ATOM     35  CB  VAL A 120       4.289  -0.729  10.794  1.00  6.30           C
ATOM     43  N   LYS A 121       7.090  -2.731   9.665  1.00  6.85           N
ATOM     44  CA  LYS A 121       8.324  -3.457   9.940  1.00  7.33           C
ATOM     45  C   LYS A 121       9.432  -2.496  10.352  1.00  7.22           C
ATOM     46  O   LYS A 121       9.532  -1.393   9.814  1.00  8.07           O
ATOM     47  CB  LYS A 121       8.721  -4.287   8.725  1.00  7.37           C
ATOM     51  N   ILE A 122      10.245  -2.915  11.332  1.00  7.60           N
ATOM     52  CA  ILE A 122      11.466  -2.211  11.718  1.00  8.54           C
ATOM     53  C   ILE A 122      12.686  -3.134  11.750  1.00  9.00           C
ATOM     54  O   ILE A 122      13.814  -2.661  11.938  1.00 10.14           O
ATOM    636  N   GLY A 123      12.493  -4.436  11.572  1.00 22.14           N
ATOM    637  CA  GLY A 123      13.615  -5.356  11.617  1.00 21.89           C
ATOM    638  C   GLY A 123      14.000  -5.831  10.227  1.00 19.25           C
ATOM    639  O   GLY A 123      13.170  -6.364   9.480  1.00 19.23           O
ATOM    644  N   GLY A 124      15.285  -5.684   9.913  1.00 17.08           N
ATOM    645  CA  GLY A 124      15.711  -5.611   8.522  1.00 16.06           C
ATOM    646  C   GLY A 124      15.397  -6.863   7.752  1.00 16.14           C
ATOM    647  O   GLY A 124      15.825  -7.969   8.102  1.00 14.51           O
ATOM    652  N   GLY A 125      14.634  -6.699   6.671  1.00 15.60           N
ATOM    653  CA  GLY A 125      14.267  -7.769   5.792  1.00 16.03           C
ATOM    654  C   GLY A 125      15.002  -7.694   4.472  1.00 15.94           C
ATOM    655  O   GLY A 125      16.219  -7.551   4.417  1.00 16.51           O
ATOM      5  N   VAL A 126      14.226  -7.758   3.396  1.00 20.21           N
ATOM      6  CA  VAL A 126      14.787  -7.748   2.047  1.00 19.04           C
ATOM      7  C   VAL A 126      15.479  -6.424   1.772  1.00 20.37           C
ATOM      8  O   VAL A 126      14.821  -5.414   1.530  1.00 17.74           O
ATOM      9  CB  VAL A 126      13.693  -7.995   1.011  1.00 22.23           C
ATOM     14  N   LYS A 127      16.810  -6.434   1.776  1.00 19.31           N
ATOM     15  CA  LYS A 127      17.595  -5.278   1.359  1.00 19.58           C
ATOM     16  C   LYS A 127      17.394  -5.015  -0.125  1.00 19.91           C
ATOM     17  O   LYS A 127      16.414  -5.454  -0.725  1.00 19.76           O
ATOM     18  CB  LYS A 127      19.076  -5.509   1.633  1.00 20.42           C
ATOM     19  N   VAL A 128      18.346  -4.320  -0.729  1.00 17.69           N
ATOM     20  CA  VAL A 128      18.346  -4.201  -2.176  1.00 17.51           C
ATOM     21  C   VAL A 128      19.633  -3.583  -2.668  1.00 14.26           C
ATOM     22  O   VAL A 128      20.715  -3.968  -2.249  1.00 14.38           O
ATOM     23  CB  VAL A 128      17.155  -3.391  -2.675  1.00 17.33           C
TER
ATOM    726  N   LYS A 141       5.819 -10.424   5.061  1.00  9.48           N
ATOM    727  CA  LYS A 141       5.877  -9.822   6.378  1.00  8.99           C
ATOM    728  C   LYS A 141       4.735  -8.852   6.546  1.00  9.97           C
ATOM    729  O   LYS A 141       4.546  -8.280   7.611  1.00 11.19           O
ATOM    730  CB  LYS A 141       7.209  -9.105   6.595  1.00  9.39           C
ATOM    733  N   LYS A 142       3.997  -8.645   5.463  1.00  9.26           N
ATOM    734  CA  LYS A 142       2.855  -7.745   5.445  1.00  8.32           C
ATOM    735  C   LYS A 142       1.682  -8.537   4.918  1.00  8.47           C
ATOM    736  O   LYS A 142       0.694  -7.974   4.451  1.00  8.93           O
ATOM    737  CB  LYS A 142       3.122  -6.513   4.577  1.00  8.23           C
ATOM    744  N   GLY A 143       1.805  -9.853   4.977  1.00  7.76           N
ATOM    745  CA  GLY A 143       0.781 -10.744   4.483  1.00 10.15           C
ATOM    746  C   GLY A 143      -0.489 -10.662   5.291  1.00 10.23           C
ATOM    747  O   GLY A 143      -0.914  -9.570   5.664  1.00 10.32           O
ATOM    748  N   VAL A 144      -1.074 -11.811   5.628  1.00 11.54           N
ATOM    749  CA  VAL A 144      -2.418 -11.828   6.194  1.00 12.37           C
ATOM    750  C   VAL A 144      -2.498 -11.028   7.492  1.00 11.94           C
ATOM    751  O   VAL A 144      -3.493 -11.114   8.220  1.00 10.53           O
ATOM    752  CB  VAL A 144      -2.878 -13.285   6.391  1.00 13.66           C
ATOM    757  N   GLY A 145      -1.484 -10.229   7.793  1.00 12.14           N
ATOM    758  CA  GLY A 145      -1.449  -9.459   9.013  1.00 10.62           C
ATOM    759  C   GLY A 145      -2.596  -8.505   9.213  1.00 11.20           C
ATOM    760  O   GLY A 145      -2.822  -8.051  10.324  1.00 10.38           O
TER
ATOM    726  N   GLY A 131      -5.004 -10.220  15.078  1.00  9.48           N
ATOM    727  CA  GLY A 131      -3.704  -9.586  15.089  1.00  8.99           C
ATOM    728  C   GLY A 131      -2.604 -10.549  14.742  1.00  9.97           C
ATOM    729  O   GLY A 131      -1.480 -10.145  14.481  1.00 11.19           O
ATOM    733  N   GLY A 132      -2.948 -11.828  14.740  1.00  9.26           N
ATOM    734  CA  GLY A 132      -2.009 -12.893  14.479  1.00  8.32           C
ATOM    735  C   GLY A 132      -2.675 -14.250  14.440  1.00  8.47           C
ATOM    736  O   GLY A 132      -2.016 -15.279  14.591  1.00  8.93           O
ATOM    744  N   LYS A 133      -3.987 -14.266  14.231  1.00  7.76           N
ATOM    745  CA  LYS A 133      -4.748 -15.497  14.096  1.00 10.15           C
ATOM    746  C   LYS A 133      -4.656 -16.004  12.672  1.00 10.23           C
ATOM    747  O   LYS A 133      -5.505 -16.776  12.235  1.00 10.32           O
ATOM    748  N   LYS A 134      -3.616 -15.577  11.950  1.00 11.54           N
ATOM    749  CA  LYS A 134      -3.415 -15.991  10.565  1.00 12.37           C
ATOM    750  C   LYS A 134      -2.058 -15.549  10.044  1.00 11.94           C
ATOM    751  O   LYS A 134      -1.515 -16.164   9.125  1.00 10.53           O
ATOM    752  CB  LYS A 134      -4.519 -15.426   9.684  1.00 13.66           C
ATOM    757  N   ILE A 135      -1.498 -14.500  10.628  1.00 12.14           N
ATOM    758  CA  ILE A 135      -0.212 -13.942  10.248  1.00 10.62           C
ATOM    759  C   ILE A 135       0.870 -14.998  10.253  1.00 11.20           C
ATOM    760  O   ILE A 135       1.939 -14.786  10.816  1.00 10.38           O
ATOM    761  CB  ILE A 135       0.180 -12.801  11.183  1.00 11.50           C
TER
END
"""
  first_annotation_text="""
SHEET    1   1 2 VAL A  18  GLY A  21  0
SHEET    2   1 2 VAL A  38  VAL A  41 -1
"""

  second_annotation_text="""
SHEET    1   1 4 LYS A  40  VAL A  43  0
SHEET    2   1 4 ALA A  12  VAL A  18 -1  N  ILE A  17   O  VAL A  41
SHEET    3   1 4 ARG A  81  GLY A  87  1  N  VAL A  83   O  ALA A  12
SHEET    4   1 4 VAL A 103  ILE A 107 -1  N  ALA A 106   O  ILE A  82
"""

  import iotbx.pdb
  from cctbx.array_family import flex

  hierarchy=iotbx.pdb.input(source_info='text',
       lines=flex.split_lines(pdb_text)
         ).construct_hierarchy()

  import iotbx.pdb.secondary_structure as ioss
  first_annotation=ioss.annotation.from_records(records=flex.split_lines(first_annotation_text))
  second_annotation=ioss.annotation.from_records(records=flex.split_lines(second_annotation_text))

  print "\nMerging annotations and checking on sheet numbering"
  print "\nFirst annotation: "
  print first_annotation.as_pdb_str()
  print "\nSecond annotation: "
  print second_annotation.as_pdb_str()
  merged=second_annotation.combine_annotations(other=first_annotation, hierarchy=hierarchy)
  print "\nMerged: "
  print merged.as_pdb_str()
  assert merged.is_similar_to(other=second_annotation,hierarchy=hierarchy)


if __name__=="__main__":
  import sys
  tst_00()
  tst_01()
  tst_02()
  tst_03()
  tst_04()
  tst_05()
  tst_06()
  tst_07()
  tst_08()
  tst_09()
  tst_10()
  tst_11()
  tst_12()
  print "OK"
