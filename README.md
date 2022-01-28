# denormalize-hebrew
 This repo houses a Python program that undoes some of the indignities that
 Unicode normalization visits upon pointed Hebrew strings.

 In particular, it moves the following marks close up against the letter
 of their cluster:

 * shin dot
 * sin dot
 * dagesh/mapiq

Conceptually, it is a lot like applying Unicode normalization if a nonstandard
(but more sane) set of combining class values were used. In this nonstandard
set of combining classes, the 3 marks above would have the lowest values.

For example, they might have values 10, 11, \& 12, respectively,
instead of their standard values of 24, 25, \& 21, respectively.

In fact, these values of 10, 11, \& 12 correspond to what HarfBuzz uses,
internally. The values of 10, 11, & 21 are what was recommended near
the end of the SBL Hebrew Font User Manual.