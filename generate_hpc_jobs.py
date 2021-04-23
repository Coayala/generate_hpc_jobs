#!/usr/bin/env python3
"""
Author : Christian Ayala <cayalaortiz@email.arizona.edu>
Date   : 2021-04-19
Purpose: Generate jobs scripts to be submitted to the UA HPC clusters
"""

import argparse


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Generate jobs scripts to be submitted to the UA HPC clusters',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('cluster',
                        metavar='CLUSTER',
                        help='Cluster where the job will be submitted',
                        choices=['puma', 'ocelote', 'elgato'])

    parser.add_argument('-o',
                        '--outfile',
                        help='Name for the script generated',
                        metavar='OUTFILE',
                        type=str,
                        default='my_script')

    parser.add_argument('-j',
                        '--job_name',
                        help='Name for the job',
                        metavar='JOBNAME',
                        type=str,
                        default='job')

    parser.add_argument('-q',
                        '--queue',
                        help='Queue/partition to use',
                        metavar='QUEUE',
                        type=str,
                        default='standard')

    parser.add_argument('-w',
                        '--walltime',
                        help='Number of hours for the job to run',
                        metavar='INT',
                        type=int,
                        default=5)

    parser.add_argument('-n',
                        '--nodes',
                        help='Number of nodes',
                        metavar='INT',
                        type=int,
                        default=1)

    parser.add_argument('-t',
                        '--tasks',
                        help='Number of tasks per node',
                        metavar='INT',
                        type=int,
                        default=30)

    parser.add_argument('-m',
                        '--memory',
                        help='Gb of cpu memory. If not set up, the default amount of memory for the number of nodes and tasks '
                             'will be requested',
                        metavar='INT',
                        type=int,
                        default=None)

    parser.add_argument('-e',
                        '--email',
                        help='Email address for the job',
                        metavar='EMAIL',
                        type=str,
                        default='cayalaortiz@email.arizona.edu')

    parser.add_argument('-a',
                        '--account',
                        help='Account for the job (PI name)',
                        metavar='ACCOUNT',
                        type=str,
                        default='tfaily')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    job_body = '#!/bin/bash\n'

    if args.cluster == 'puma':
        job_body += '#SBATCH --job-name={}\n'.format(args.job_name)
        job_body += '#SBATCH --partition={}\n'.format(args.queue)
        job_body += '#SBATCH --time={}:00:00\n'.format(args.walltime)
        job_body += '#SBATCH --nodes={}\n'.format(args.nodes)
        job_body += '#SBATCH --ntasks={}\n'.format(args.tasks)
        job_body += '#SBATCH --mem={}gb\n'.format(args.memory) if args.memory else ''
        job_body += '#SBATCH --mail-user={}\n'.format(args.email)
        job_body += '#SBATCH --account={}\n'.format(args.account)
        job_body += '#SBATCH --mail-type=ALL\n'
        job_body += '#SBATCH -o %x-%j.out\n'
        filename = args.outfile + '.slurm'
    else:
        job_body += '#PBS -N {}\n'.format(args.job_name)
        job_body += '#PBS -q {}\n'.format(args.queue)
        job_body += '#PBS -l walltime={}:00:00\n'.format(args.walltime)
        job_body += '#PBS -l select={}:ncpus={}:mem={}\n'.format(args.nodes, args.tasks, args.memory) \
            if args.memory else '#PBS -l select={}:ncpus={}\n'.format(args.nodes, args.tasks)
        job_body += '#PBS -M {}\n'.format(args.email)
        job_body += '#PBS -W group_list={}\n'.format(args.account)
        job_body += '#PBS -m be\n'
        job_body += '#PBS -j oe\n'
        job_body += '\ncd $PBS_O_WORKDIR\n'
        filename = args.outfile + '.pbs'

    with open(filename, 'w') as out:
        out.write(job_body + '\n')

    print('Job script {} generated'.format(filename))


# --------------------------------------------------
if __name__ == '__main__':
    main()
