'''
Created by Daniel Le Corre (1,2)* 
Last edited on 07/07/2023
1   Centre for Astrophysics and Planetary Science, University of Kent, Canterbury, United Kingdom
2   Centres d'Etudes et de Recherches de Grasse, ACRI-ST, Grasse, France
*   Correspondence: dl387@kent.ac.uk
    Website: https://www.danlecorre.com/
'''

import os
import argparse
import logging
import matplotlib.pyplot as plt
import numpy as np

# Configure logger
logging.basicConfig(level = logging.INFO,
                    format='| %(asctime)s | %(levelname)s | Message: %(message)s',
                    datefmt='%d/%m/%y @ %H:%M:%S')

'''
Optional arguments:

-r (--raw):     Plot the raw apparent depth measurements which have not been corrected for a non-zero
                satellite emission angle at the time when the image was taken.
                (Default: False / Type: bool)

DO NOT CHANGE THESE VARIABLES:

OUTPUT_DIR:     Path to the output directory where all of the results and plots will be saved. (Type: str)

'''

# Initialise arguments parser and define arguments
PARSER = argparse.ArgumentParser()
PARSER.add_argument("-r", "--raw", action=argparse.BooleanOptionalAction, default=False, help = "Should the observed apparent depths also be plotted? [--raw|--no-raw]")
ARGS = PARSER.parse_args()

# Do not change these variables
OUTPUT_DIR = '/data/output/'

def main(raw,
        output_dir):
    
    # Create the directory to save plots
    plots_dir = os.path.join(output_dir, 'figures/')
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
        logging.info("Plots output folder created")
    
    # Define the directory where the h profiles should be saved
    profiles_dir = os.path.join(output_dir, 'profiles/')
        
    # Find all h profile CSV files
    filenames = [file for file in os.listdir(profiles_dir) if file.endswith('profile.csv')]
    
    for filename in filenames:
        
        # Get product name of file
        name = os.path.splitext(filename)[0]
        
        # Define the path to the h profile CSV file
        profile_path = os.path.join(profiles_dir, filename)
        
        # Read the profile CSV file
        L_obs, h_obs, pos_h_obs, neg_h_obs, L_true, h_true, pos_h_true, neg_h_true = np.genfromtxt(profile_path, delimiter=',', unpack=True, skip_header=1, dtype=float)
    
        # Find the maximum apparent depth
        max_depth = max(np.amax(h_true) + pos_h_true[np.argmax(h_true)], np.amax(h_obs) + pos_h_obs[np.argmax(h_obs)])
    
        # Find the ratio to scale the x and y axis by
        ratio = max_depth / (L_true[-1] - L_true[0])
        fig, ax = plt.subplots(figsize=(5,5))
        ax.set_aspect('equal')
        
        # If the uncorrected apparent depth should also be plotted
        if raw:
            ax.plot(L_obs, h_obs, 'r--', alpha=0.5, label=r'$h_{obs}$')
            ax.fill_between(L_obs, h_obs - neg_h_obs, h_obs + pos_h_obs, alpha=0.1, color='red', label=r'$\Delta h_{obs}$')
        
        # Plot the apparent depth profile
        ax.plot(L_true, h_true, color='green', label=r'$h$')
        ax.fill_between(L_true, h_true - neg_h_true, h_true + pos_h_true, alpha=0.4, color='green', label=r'$\Delta h$')

        # Format the axes
        ax.set_xlabel(r"Shadow Length ($L$) [m]")
        ax.set_ylabel(r"Apparent depth ($h$) [m]")
        ax.set_ylim(0, np.ceil(max_depth/10)*10)
        ax.invert_yaxis()
        ax.grid('both')
        if raw:
            ax.legend(loc='lower left', bbox_to_anchor=(0, 1), ncol=4, frameon=False)
            ax.set_xlim(min(L_obs[0], L_true[0]), max(L_obs[-1], L_true[-1]))
        else:
            ax.legend(loc='lower left', bbox_to_anchor=(0, 1), ncol=2, frameon=False)
            ax.set_xlim(L_true[0], L_true[-1])

        # Save the figure to the output path
        fig.savefig(os.path.join(plots_dir, name + '.pdf'), bbox_inches='tight')
    
if __name__ == '__main__':
    main(ARGS.raw,
        OUTPUT_DIR)