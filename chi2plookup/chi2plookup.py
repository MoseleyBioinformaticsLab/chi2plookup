#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from scipy.stats import chi2


HEADERFILE_TEMPLATE = """#ifndef CHI2PVALUES_H
#define CHI2PVALUES_H


struct Chi2PValues
{{
    static const double * pValues[];
    static const int cutoff[];
    static const int divisor;

    inline double getPValue(double statistic, int df) {{
        return((statistic >= cutoff[df-1]) ? 0.0 : pValues[df-1][int(divisor * statistic)]);
    }}
    
}};

{0}
{1}

{2}
{3}

#endif // CHI2PVALUES_H
"""

TESTFILE_TEMPLATE = """#include <iostream>
#include "Chi2PValues.h"

int main() {{
    
    Chi2PValues chi2_plookup_table;
    double x = {0};
    int df = {1};
    double outvalue;

    outvalue = chi2_plookup_table.getPValue(x, df);
    std::cout << "Estimated value: " << outvalue << "\\n";

    return 0;
}}
"""


def max_chi_value(df=1, start_chi=25):
    """Determine maximum chi2 value statistic for a given degree of freedom.

    :param int df: Degree of freedom.
    :param int start_chi: Maximum chi2 value for given degree of freedom.
    :return: Maximum chi value statistic for a given degree of freedom.
    :rtype: int
    """
    if df == 1:
        return start_chi

    start_p_value = 1 - chi2.cdf(start_chi, 1)
    max_chi = start_chi
    p_value = 1 - chi2.cdf(max_chi, df)

    while p_value >= start_p_value:
        max_chi += 1
        p_value = 1 - chi2.cdf(max_chi, df)

    return max_chi


def generate_headerfile(template, n_division=10000, df=6, start_chi=25, filepath="Chi2PValues.h", verbose=True):
    """Generate C++ header file that contain pre-generated array of arrays of p-values for specified
    degrees of freedom.

    :param str template: Header file template.
    :param int n_division: Precision.
    :param tuple df: Degrees of freedom.
    :param int start_chi: Maximum chi value for degree of freedom = 1.
    :param str filepath: Path where header file will be saved.
    :return: None
    :rtype: None
    """
    divisor = "const int Chi2PValues::divisor = {};".format(n_division)

    names = []
    cutoff = []
    p_values_arrays = []
    degrees_of_freedom = range(1, df+1)

    if verbose:
        print("Generating p-value arrays...")

    for df in degrees_of_freedom:
        var_name = "pValues_{}".format(df)
        names.append(var_name)
        max_chi = max_chi_value(df=df, start_chi=start_chi)
        cutoff.append(max_chi)
        n_elements = max_chi * n_division

        chi_values = (val / n_division for val in range(0, n_elements + 1))
        p_values = (str(1 - chi2.cdf(val, df)) for val in chi_values)

        if verbose:
            print("    Adding p-values array to template for degree of freedom = {} ...".format(df))

        p_values_arrays.append("double {}[] = {{{}}};".format(var_name, ", ".join(p_values)))

    cutoff_array = "const int Chi2PValues::cutoff[] = {{{}}};".format(", ".join([str(i) for i in cutoff]))
    p_values_array_of_arrays = "const double * Chi2PValues::pValues[] = {{{}}};\n".format(", ".join(names))

    template = template.format(divisor, cutoff_array, "\n".join(p_values_arrays), p_values_array_of_arrays)

    if verbose:
        print("Saving file to: {}".format(os.path.abspath(filepath)))

    with open(filepath, "w") as outfile:
        outfile.write(template)


def test_headerfile(template, testvalue=1, df=1, srcfpath="test.cpp", binfpath="test.out"):
    """Test generated header file.

    :param str template: Template file that contains main() function and imports header file.
    :param testvalue: Chi value.
    :param int df: Degree of freedom.
    :param str srcfpath: Path where source file will be saved.
    :param str binfpath: Path where binary file will be saved.
    :return: None
    :rtype: None
    """
    p_value = 1 - chi2.cdf(testvalue, df)
    print("Actual value:", p_value)

    template = template.format(testvalue, df)
    with open(srcfpath, "w") as outfile:
        outfile.write(template)

    os.system("g++ -std=c++11 {} -o {}".format(srcfpath, binfpath))
    os.system("./{}".format(binfpath))
