chi2plookup
===========

The `chi2plookup` package provides a simple interface for creating
C++ header file that contains pregenerated array(s) of p-values for chi-square
distribution for varying degrees of freedom.

Why?
====

Need a way to calculate p-value for different degrees of freedom for a given chi2 value
and bypass third-party dependencies:

   * boost_
   * gsl_ (GNU Scientific Library)

Inspired by:

   * https://stackoverflow.com/questions/795972/chi-squared-probability-function-in-c
   * http://rmflight.github.io/posts/2013/10/precalcLookup.html

.. _boost: http://www.boost.org/doc/libs/1_65_1/libs/math/doc/html/math_toolkit/dist_ref/dists/chi_squared_dist.html
.. _gsl: http://www.gnu.org/software/gsl/doc/html/randist.html?highlight=chi#the-chi-squared-distribution