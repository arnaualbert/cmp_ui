from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import re
import paramiko
from threading import Thread
import random
module_name = __name__
app = Flask(__name__)

# Get current path
path = os.getcwd()
print(path)

# file Upload
DEMULTIPLEXING_FOLDER = os.path.join(path, 'demultiplexing')
CROSSMAPER_FOLDER = os.path.join(path, 'crossmaper')

if not os.path.isdir(DEMULTIPLEXING_FOLDER):
    os.mkdir(DEMULTIPLEXING_FOLDER)

if not os.path.isdir(CROSSMAPER_FOLDER):
    os.mkdir(CROSSMAPER_FOLDER)

app.config['DEMULTIPLEXING_FOLDER'] = DEMULTIPLEXING_FOLDER
app.config['CROSSMAPER_FOLDER'] = CROSSMAPER_FOLDER

ALLOWED_EXTENSIONS = set(['fastq','fastq.gz','fq','fq.gz','.fastq', '.fastq.gz', '.fq', '.fq.gz'])

def chck(filename):
    return filename.endswith(tuple(ALLOWED_EXTENSIONS))


def is_logged():
    all_var = globals()
    if "host" in all_var:
        return True
    else:
        return False
    
# Show the ssh login page
@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        global host 
        global username
        global password
        global ssh
        host = request.form['HOST']
        username = request.form['USERNAME']
        password = request.form['PASSWORD']
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=username, password=password)
            print("Connection Successful")
            return render_template('index.html')
        except paramiko.AuthenticationException:
            print("Wrong Credentials")
            data = "Wrong Credentials"
            return render_template('sshlogin.html', data=data)
    return render_template('sshlogin.html')

# Show the home page
@app.route("/home",methods=['GET','POST'])
def home():
    if request.method == 'GET' and is_logged():
        return render_template('index.html')
    if request.method == 'POST' and is_logged():
        return render_template('index.html')
    elif is_logged() != True:
        return render_template('sshlogin.html')
    
@app.route('/demultiplexing',methods=['GET', 'POST'])
def demultiplexing():
    ''' Demultiplexing 
        This function is used to demultiplex the fastq files.
        It takes all the parameters from the html form.
    '''

    if request.method == 'GET' and is_logged():
        return render_template('demultiplexing.html')

    if request.method == 'POST' and is_logged():
        data = request.get_data(as_text=True)
        print(data)
        data =  data
        ref_genome_list = []
        organism_name_list = []
        path_files_list=[]
        lines = data.strip().split('\n')
        have_getoption = "getoption=on\r" in lines

        if have_getoption:
            for line in lines:
                if line.startswith("ref_genome="):
                    ref_genome_list.append(line.split('=')[1].rstrip())
                elif line.startswith("organism_name="):
                    organism_name_list.append(line.split('=')[1].rstrip())
                elif line.startswith("path_files="):
                    path_files_list.append(line.split("=")[1].rstrip())
                elif line.startswith("fastas_fwd="):
                    fastas_fwd = line.split("=")[1].rstrip()
                elif line.startswith("fastas_rv="):
                    fastas_rv = line.split("=")[1].rstrip()
                elif line.startswith("output_dir="):
                    output_dir = line.split("=")[1].rstrip()
                elif line.startswith("path_file="):
                    path_file = line.split("=")[1].rstrip()
                elif line.startswith("path_file_unique="):
                    path_file_unique = line.split("=")[1].rstrip()
                elif line.startswith("num_of_threads="):
                    num_of_threads = line.split("=")[1].rstrip()
                elif line.startswith("reads_per_chunk="):
                    reads_per_chunk = line.split("=")[1].rstrip()
                elif line.startswith("replace="):
                    replace = line.split("=")[1].rstrip()
                elif line.startswith("skip_removing_tmp_files=True"):
                    skip_removing_tmp_files = line.split("=")[1].rstrip()
                elif line.startswith("wit_db="):
                    wit_db = line.split("=")[1].rstrip()
                elif line.startswith("getoption="):
                    getoption = line.split("=")[1].rstrip()
                elif line.startswith("store_com="):
                    store_com = line.split("=")[1].rstrip()
        else:
            print("No getoption")
            for line in lines:
                if line.startswith("ref_genome="):
                    ref_genome_list.append(line.split('=')[1].rstrip())
                elif line.startswith("organism_name="):
                    organism_name_list.append(line.split('=')[1].rstrip())
                elif line.startswith("path_files="):
                    path_files_list.append(line.split("=")[1].rstrip())
                elif line.startswith("fastas_fwd="):
                    fastas_fwd = line.split("=")[1].rstrip()
                elif line.startswith("fastas_rv="):
                    fastas_rv = line.split("=")[1].rstrip()
                elif line.startswith("output_dir="):
                    output_dir = line.split("=")[1].rstrip()
                elif line.startswith("path_file="):
                    path_file = line.split("=")[1].rstrip()
                elif line.startswith("path_file_unique="):
                    path_file_unique = line.split("=")[1].rstrip()
                elif line.startswith("num_of_threads="):
                    num_of_threads = line.split("=")[1].rstrip()
                elif line.startswith("reads_per_chunk="):
                    reads_per_chunk = line.split("=")[1].rstrip()
                elif line.startswith("replace="):
                    replace = line.split("=")[1].rstrip()
                elif line.startswith("skip_removing_tmp_files=True"):
                    skip_removing_tmp_files = line.split("=")[1].rstrip()
                elif line.startswith("wit_db="):
                    wit_db = line.split("=")[1].rstrip()
                elif line.startswith("getoption="):
                    getoption = line.split("=")[1].rstrip()
                elif line.startswith("store_com="):
                    store_com = line.split("=")[1].rstrip()
        id = random.randint(1,100000)
        if have_getoption and fastas_fwd != "" and fastas_rv != "" and output_dir != "" and path_file != "" and ref_genome_list != [] and organism_name_list != [] and store_com != "" and path_file_unique != "":
            ref_gen_l = []
            fastas_fs_ls_string = os.path.join(path_file,fastas_fwd)
            fastas_rv_ls_string = os.path.join(path_file,fastas_rv)
            for gen in ref_genome_list:
                gen = os.path.join(path_file_unique,gen)
                ref_gen_l.append(gen)
            ref_genome_string = " ".join(ref_gen_l)
            organism_name_string = " ".join(organism_name_list)
            rpl_ls_str = replace
            command = f'split_pooledSeqWGS_parallel.py --fastq1 {fastas_fs_ls_string} --fastq2 {fastas_rv_ls_string} --outdir {output_dir} --refGenomes {ref_genome_string} --sampleNames {organism_name_string} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --replace {rpl_ls_str} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
            with open(os.path.join(DEMULTIPLEXING_FOLDER,"demultiplexing.sh"), 'w') as f:
                f.write(f"""#!/bin/bash
#SBATCH --job-name=multiplex.{id}
#SBATCH --chdir=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/
#SBATCH --output=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.out
#SBATCH --error=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.err
#SBATCH --time=0:30:00
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --qos=debug
{command}""")    
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=username, password=password)
                sftp = ssh.open_sftp()
                sftp.put(os.path.join(DEMULTIPLEXING_FOLDER, "demultiplexing.sh"), store_com + "/demultiplexing.sh")
                sftp.close()
                ssh.close()
                os.remove(os.path.join(DEMULTIPLEXING_FOLDER, "demultiplexing.sh"))
            except paramiko.AuthenticationException:
                print("Authentication failed. Please check your credentials.")
            except paramiko.SSHException as ssh_exception:
                print(f"SSH connection failed: {str(ssh_exception)}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            data = {'command':command}
            return render_template('command.html',data=data)
        elif fastas_fwd != "" and fastas_rv != "" and output_dir != "" and path_file != "" and ref_genome_list != [] and organism_name_list != [] and store_com != "" and path_files_list != "" :
            ref_gen_ls = []
            fastas_fs_ls_string = os.path.join(path_file,fastas_fwd)
            fastas_rv_ls_string = os.path.join(path_file,fastas_rv)
            for path,gen_ref in zip(path_files_list,ref_genome_list):
                ref_gen_ls.append(os.path.join(path,gen_ref))
            organism_name_string = " ".join(organism_name_list)
            ref_genome_string = " ".join(ref_gen_ls)
            rpl_ls_str = replace
            command = f'split_pooledSeqWGS_parallel.py --fastq1 {fastas_fs_ls_string} --fastq2 {fastas_rv_ls_string} --outdir {output_dir} --refGenomes {ref_genome_string} --sampleNames {organism_name_string} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --replace {rpl_ls_str} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
            print(command)
            with open(os.path.join(DEMULTIPLEXING_FOLDER,"demultiplexing.sh"), 'w') as f:
                f.write(f"""#!/bin/bash
#SBATCH --job-name=multiplex.{id}
#SBATCH --chdir=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/
#SBATCH --output=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.out
#SBATCH --error=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.err
#SBATCH --time=0:30:00
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --qos=debug
{command}""")    
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=username, password=password)
                sftp = ssh.open_sftp()
                sftp.put(os.path.join(DEMULTIPLEXING_FOLDER, "demultiplexing.sh"), store_com + "/demultiplexing.sh")
                sftp.close()
                ssh.close()
                os.remove(os.path.join(DEMULTIPLEXING_FOLDER, "demultiplexing.sh"))
            except paramiko.AuthenticationException:
                print("Authentication failed. Please check your credentials.")
            except paramiko.SSHException as ssh_exception:
                print(f"SSH connection failed: {str(ssh_exception)}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            data = {'command':command}
            return render_template('command.html',data=data)
        else:
            return render_template('demultiplexing.html',data="Please fill all the fields")
    elif is_logged() != True:
        return render_template('sshlogin.html')

# Show the demultiplexing batch page
@app.route('/demultiplexing_batch',methods=['GET', 'POST'])
def demultiplexing_batch():
    if request.method == 'GET' and is_logged():
        return render_template('demultiplexing_batch.html')
    if request.method == 'POST' and is_logged():
        data = request.get_data(as_text=True)
        print(data)
        data =  data
        ref_genome_list = []
        organism_name_list = []
        path_files_list=[]
        lines = data.strip().split('\n')
        have_getoption = "getoption=on\r" in lines
        fastas = []

        if have_getoption:
            for line in lines:
                if line.startswith("ref_genome="):
                    ref_genome_list.append(line.split('=')[1].rstrip())
                elif line.startswith("organism_name="):
                    organism_name_list.append(line.split('=')[1].rstrip())
                elif line.startswith("path_files="):
                    path_files_list.append(line.split("=")[1].rstrip())
                elif line.startswith("fastas="):
                    fastas.append(line.split("=")[1].rstrip())
                elif line.startswith("output_dir="):
                    output_dir = line.split("=")[1].rstrip()
                elif line.startswith("path_file="):
                    path_file = line.split("=")[1].rstrip()
                elif line.startswith("path_file_unique="):
                    path_file_unique = line.split("=")[1].rstrip()
                elif line.startswith("num_of_threads="):
                    num_of_threads = line.split("=")[1].rstrip()
                elif line.startswith("reads_per_chunk="):
                    reads_per_chunk = line.split("=")[1].rstrip()
                elif line.startswith("replace="):
                    replace = line.split("=")[1].rstrip()
                elif line.startswith("skip_removing_tmp_files=True"):
                    skip_removing_tmp_files = line.split("=")[1].rstrip()
                elif line.startswith("wit_db="):
                    wit_db = line.split("=")[1].rstrip()
                elif line.startswith("getoption="):
                    getoption = line.split("=")[1].rstrip()
                elif line.startswith("store_com="):
                    store_com = line.split("=")[1].rstrip()
        else:
            print("No getoption")
            for line in lines:
                if line.startswith("ref_genome="):
                    ref_genome_list.append(line.split('=')[1].rstrip())
                elif line.startswith("organism_name="):
                    organism_name_list.append(line.split('=')[1].rstrip())
                elif line.startswith("path_files="):
                    path_files_list.append(line.split("=")[1].rstrip())
                elif line.startswith("fastas="):
                    fastas.append(line.split("=")[1].rstrip())
                elif line.startswith("output_dir="):
                    output_dir = line.split("=")[1].rstrip()
                elif line.startswith("path_file="):
                    path_file = line.split("=")[1].rstrip()
                elif line.startswith("path_file_unique="):
                    path_file_unique = line.split("=")[1].rstrip()
                elif line.startswith("num_of_threads="):
                    num_of_threads = line.split("=")[1].rstrip()
                elif line.startswith("reads_per_chunk="):
                    reads_per_chunk = line.split("=")[1].rstrip()
                elif line.startswith("replace="):
                    replace = line.split("=")[1].rstrip()
                elif line.startswith("skip_removing_tmp_files=True"):
                    skip_removing_tmp_files = line.split("=")[1].rstrip()
                elif line.startswith("wit_db="):
                    wit_db = line.split("=")[1].rstrip()
                elif line.startswith("getoption="):
                    getoption = line.split("=")[1].rstrip()
                elif line.startswith("store_com="):
                    store_com = line.split("=")[1].rstrip()

        fastas_forward = []
        fastas_reversed = []
        reg = r'[12].{1,3}fast'
        reg_r1 = r'.*R1.*|.*r1.*'
        compile_reg_r1 = re.compile(reg_r1)
        reg_r2 = r'.*R2.*|.*r2.*'
        compile_reg_r2 = re.compile(reg_r2)
        for fasta in fastas:
            if chck(fasta):
                matched = re.search(reg, fasta)
                if compile_reg_r1.match(fasta):
                    fastas_forward.append(fasta)
                elif compile_reg_r2.match(fasta):
                    fastas_reversed.append(fasta)
                elif matched:
                    if "1" in matched.group():
                        fastas_forward.append(fasta)
                    elif "2" in matched.group():
                        fastas_reversed.append(fasta)

        fastas_fwd = sorted(fastas_forward)
        fastas_rv = sorted(fastas_reversed)
        id = random.randint(1,100000)
        if have_getoption and fastas_fwd != [] and fastas_rv != [] and output_dir != "" and path_file != "" and ref_genome_list != [''] and organism_name_list != [''] and store_com != "" and path_file_unique != "":
            ref_gen_l = []
            path_fasta_fwd = []
            path_fasta_rv = []
            for fasta in fastas_fwd:
                path_fasta_fwd.append(os.path.join(path_file,fasta))
            for fasta in fastas_rv:
                path_fasta_rv.append(os.path.join(path_file,fasta))            
            for gen in ref_genome_list:
                gen = os.path.join(path_file_unique,gen)
                ref_gen_l.append(gen)
            ref_genome_string = " ".join(ref_gen_l)
            organism_name_string = " ".join(organism_name_list)
            rpl_ls_str = replace
            i = 0
            commands = []
            while i < len(path_fasta_fwd):
                command = f'split_pooledSeqWGS_parallel.py --fastq1 {path_fasta_fwd[i]} --fastq2 {path_fasta_rv[i]} --outdir {output_dir} --refGenomes {ref_genome_string} --sampleNames {organism_name_string} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --replace {rpl_ls_str} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
                # print(command)
                commands.append(command)
                i = i + 1
            ntask = len(commands)
            with open(os.path.join(DEMULTIPLEXING_FOLDER,"demultiplexing.sh"), 'w') as f:
                f.write(f"""#!/bin/bash
#SBATCH --job-name=multiplex.{id}
#SBATCH --chdir=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/
#SBATCH --output=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.out
#SBATCH --error=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.err
#SBATCH --time=0:30:00
#SBATCH --ntasks={ntask}
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --qos=debug
""") 
                for com in commands:
                    f.write(f'{com}\n')
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=username, password=password)
                sftp = ssh.open_sftp()
                sftp.put(os.path.join(DEMULTIPLEXING_FOLDER, "demultiplexing.sh"), store_com + "/demultiplexing.sh")
                sftp.close()
                ssh.close()
                os.remove(os.path.join(DEMULTIPLEXING_FOLDER, "demultiplexing.sh"))
            except paramiko.AuthenticationException:
                print("Authentication failed. Please check your credentials.")
            except paramiko.SSHException as ssh_exception:
                print(f"SSH connection failed: {str(ssh_exception)}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            data = {'command':commands}
            return render_template('commands.html',data=data)
        elif fastas_fwd != [] and fastas_rv != [] and output_dir != "" and path_file != "" and ref_genome_list != [''] and organism_name_list != [] and store_com != "" and path_files_list != "" :
            ref_gen_ls = []
            path_fasta_fwd = []
            path_fasta_rv = []
            for fasta in fastas_fwd:
                path_fasta_fwd.append(os.path.join(path_file,fasta))
            for fasta in fastas_rv:
                path_fasta_rv.append(os.path.join(path_file,fasta))   
            for path,gen_ref in zip(path_files_list,ref_genome_list):
                ref_gen_ls.append(os.path.join(path,gen_ref))
            organism_name_string = " ".join(organism_name_list)
            ref_genome_string = " ".join(ref_gen_ls)
            rpl_ls_str = replace
            i = 0
            commands = []
            while i < len(path_fasta_fwd):
                command = f'split_pooledSeqWGS_parallel.py --fastq1 {path_fasta_fwd[i]} --fastq2 {path_fasta_rv[i]} --outdir {output_dir} --refGenomes {ref_genome_string} --sampleNames {organism_name_string} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --replace {rpl_ls_str} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
                print(command)
                commands.append(command)
                i = i + 1
            print(len(commands))
            ntask = len(commands)
            with open(os.path.join(DEMULTIPLEXING_FOLDER,"demultiplexing.sh"), 'w') as f:
                f.write(f"""#!/bin/bash
#SBATCH --job-name=multiplex.{id}
#SBATCH --chdir=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/
#SBATCH --output=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.out
#SBATCH --error=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.err
#SBATCH --time=0:30:00
#SBATCH --ntasks={ntask}
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --qos=debug
""")    
                for com in commands:
                    f.write(f'{com}\n')
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=username, password=password)

                sftp = ssh.open_sftp()
                sftp.put(os.path.join(DEMULTIPLEXING_FOLDER, "demultiplexing.sh"), store_com + "/demultiplexing.sh")
                sftp.close()
                ssh.close()
                os.remove(os.path.join(DEMULTIPLEXING_FOLDER, "demultiplexing.sh"))
            except paramiko.AuthenticationException:
                print("Authentication failed. Please check your credentials.")
            except paramiko.SSHException as ssh_exception:
                print(f"SSH connection failed: {str(ssh_exception)}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            data = {'command':commands}
            return render_template('commands.html',data=data)
        else:
            return render_template('demultiplexing_batch.html',data="Please fill all the fields")
    elif is_logged() != True:
        return render_template('sshlogin.html')

# Show the Crossmaper page
@app.route('/crossmaper')
def crossmaper():
    if request.method == 'GET' and is_logged():
        return render_template('crossmaper.html')
    if request.method == 'POST' and is_logged():
        return render_template('crossmaper.html')
    elif is_logged() != True:
        return render_template('sshlogin.html')
# Show the command page
@app.route('/command')
def command():
    return render_template('command.html',data={})

# Show the Crossmaper DNA page and get all the parameters from the form
@app.route('/crossmaper/dna',methods=['GET','POST'])
def crossmaperdna():
    if request.method == 'GET' and is_logged():
        return render_template('crossmaperdna.html')
    if request.method == 'POST' and is_logged():
        data = request.get_data(as_text=True)
        # print(data)
        lines = data.strip().split('\n')
        fastaq_list = []
        genome_name_list = []
        number_of_reads_list = []
        path_file_list = []
        read_len_list = []
        for line in lines:
            if line.startswith("fastaq="):
                fastaq_list.append(line.split('=')[1].rstrip())
            elif line.startswith("genome_name="):
                genome_name_list.append(line.split('=')[1].rstrip())
            elif line.startswith("number_of_reads="):
                number_of_reads_list.append(line.split('=')[1].rstrip())
            elif line.startswith("path_file="):
                path_file_list.append(line.split('=')[1].rstrip())
            elif line.startswith("read_length="):
                read_len_list.append(line.split('=')[1].rstrip())
            elif line.startswith("read_configuration="):
                read_configuration = line.split('=')[1].rstrip()
            elif line.startswith("number_of_cores="):
                number_of_cores = line.split('=')[1].rstrip()
            elif line.startswith("base_error_rate="):
                base_error_rate = line.split('=')[1].rstrip()
            elif line.startswith("outer_distance="):
                outer_distance = line.split('=')[1].rstrip()
            elif line.startswith("standar_deviation="):
                standar_deviation = line.split('=')[1].rstrip()
            elif line.startswith("coverage="):
                coverage = line.split('=')[1].rstrip()
            elif line.startswith("mutation_rate="):
                mutation_rate = line.split('=')[1].rstrip()
            elif line.startswith("indel_fraction="):
                indel_fraction = line.split('=')[1].rstrip()
            elif line.startswith("indel_extended="):
                indel_extended = line.split('=')[1].rstrip()
            elif line.startswith("seed_random_generator="):
                seed_random_generator = line.split('=')[1].rstrip()
            elif line.startswith("discard_ambiguos="):
                discard_ambiguos = line.split('=')[1].rstrip()
            elif line.startswith("haplotype_mode="):
                haplotype_mode = line.split('=')[1].rstrip()
            elif line.startswith("output_directory="):
                output_directory = line.split('=')[1].rstrip()
            elif line.startswith("verbose_mode="):
                verbose_mode = line.split('=')[1].rstrip()
            elif line.startswith("group_bar_chart="):
                group_bar_chart = line.split('=')[1].rstrip()
            elif line.startswith("report_cross_mapped="):
                report_cross_mapped = line.split('=')[1].rstrip()
            elif line.startswith("mapper_template_path="):
                mapper_template_path = line.split('=')[1].rstrip()
            elif line.startswith("min_seed_length="):
                min_seed_length = line.split('=')[1].rstrip()
            elif line.startswith("matching_score="):
                matching_score = line.split('=')[1].rstrip()
            elif line.startswith("mismatch_penalty="):
                mismatch_penalty = line.split('=')[1].rstrip()
            elif line.startswith("store_com="):
                store_com = line.split('=')[1].rstrip()

        fastqpath_list = []
        for fastq,path in zip(fastaq_list,path_file_list):
            print(os.path.join(path,fastq))
            fastqpath_list.append(os.path.join(path,fastq))
        list_files_string = ' '.join(fastqpath_list)
        genome_name_string = ' '.join(genome_name_list)
        read_length_string = ",".join(read_len_list)
        number_of_reads_string = " ".join(number_of_reads_list)
        id = random.randint(1,100000)
        print(data)
        print(f"mapper_template_path: {mapper_template_path}")
        if fastqpath_list != [''] and genome_name_list != [''] and read_len_list != [''] and number_of_reads_list != ['']:
            if mapper_template_path == "":
                command = f"/gpfs/projects/bsc40/project/pipelines/anaconda3/envs/crossmapper_v111/bin/crossmapper DNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -t {number_of_cores} -e {base_error_rate} -d {outer_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} -k {min_seed_length} -A {matching_score} -B {mismatch_penalty}"
                with open(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"),"w") as f:
                    f.write(f"""#!/bin/bash
#SBATCH --job-name=crossmaper.{id}
#SBATCH --chdir=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/
#SBATCH --output=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.out
#SBATCH --error=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.err
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --qos=debug

module load ANACONDA/5.0.1
source /gpfs/projects/bsc40/project/pipelines/anaconda3/etc/profile.d/conda.sh
conda activate crossmapper_v111
{command}""") 
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=host, username=username, password=password)
                    sftp = ssh.open_sftp()
                    print(store_com)
                    if store_com.endswith("/"):
                        store_com = store_com[:-1]
                    print(store_com)
                    sftp.put(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"), store_com + "/crossmaper.sh")
                    sftp.close()
                    ssh.exec_command(f"sbatch {store_com}/crossmaper.sh")
                    ssh.close()
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except paramiko.AuthenticationException:
                    print("Authentication failed. Please check your credentials.")
                    command = "Authentication failed. Please check your credentials."
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except paramiko.SSHException as ssh_exception:
                    print(f"SSH connection failed: {str(ssh_exception)}")
                    command = "SSH connection failed: " + str(ssh_exception)
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    command = "An error occurred: " + str(e)
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)            
            elif mapper_template_path != "":
                command = f"/gpfs/projects/bsc40/project/pipelines/anaconda3/envs/crossmapper_v111/bin/crossmapper DNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -t {number_of_cores} -e {base_error_rate} -d {outer_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -k {min_seed_length} -A {matching_score} -B {mismatch_penalty}"
                with open(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"),"w") as f:
                    f.write(f"""#!/bin/bash
#SBATCH --job-name=crossmaper.{id}
#SBATCH --chdir=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/
#SBATCH --output=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.out
#SBATCH --error=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.err
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --qos=debug

module load ANACONDA/5.0.1
source /gpfs/projects/bsc40/project/pipelines/anaconda3/etc/profile.d/conda.sh
conda activate crossmapper_v111
{command}""") 
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=host, username=username, password=password)
                    sftp = ssh.open_sftp()
                    print(store_com)
                    if store_com.endswith("/"):
                        store_com = store_com[:-1]
                    print(store_com)
                    sftp.put(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"), store_com + "/crossmaper.sh")
                    sftp.close()
                    ssh.exec_command(f"sbatch {store_com}/crossmaper.sh")
                    ssh.close()
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except paramiko.AuthenticationException:
                    print("Authentication failed. Please check your credentials.")
                    command = "Authentication failed. Please check your credentials."
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except paramiko.SSHException as ssh_exception:
                    print(f"SSH connection failed: {str(ssh_exception)}")
                    command = "SSH connection failed: " + str(ssh_exception)
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    command = "An error occurred: " + str(e)
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)        
        else:
            return render_template('crossmaperdna.html',error="Please fill all fields")
    elif is_logged() != True:
        return render_template('sshlogin.html')
            # return render_template('crossmaperdna.html')


# Show the Crossmaper RNA page and get all the parameters from the form
@app.route('/crossmaper/rna',methods=['GET','POST'])
def crossmaperrna():
    if request.method == 'GET' and is_logged():
        return render_template('crossmaperna.html')
    if request.method == 'POST' and is_logged():
        data = request.get_data(as_text=True)
        print(data)
        fastaq_list = []
        genome_name_list = []
        number_of_reads_list = []
        annotations_gtf_list = []
        path_file_list = []
        read_len_list = []
        lines = data.strip().split('\n')
        for line in lines:
            if line.startswith("fastaq="):
                fastaq_list.append(line.split('=')[1].rstrip())
            elif line.startswith("genome_name="):
                genome_name_list.append(line.split('=')[1].rstrip())
            elif line.startswith("number_of_reads="):
                number_of_reads_list.append(line.split('=')[1].rstrip())
            elif line.startswith("annotations_gtf="):
                annotations_gtf_list.append(line.split('=')[1].rstrip())
            elif line.startswith("path_file="):
                path_file_list.append(line.split('=')[1].rstrip())
            elif line.startswith("read_length="):
                read_len_list.append(line.split('=')[1].rstrip())
            elif line.startswith("read_configuration="):
                read_configuration = line.split('=')[1].rstrip()
            elif line.startswith("number_of_cores="):
                number_of_cores = line.split('=')[1].rstrip()
            elif line.startswith("base_error_rate="):
                base_error_rate = line.split('=')[1].rstrip()
            elif line.startswith("outer_distance="):
                outer_distance = line.split('=')[1].rstrip()
            elif line.startswith("standar_deviation="):
                standar_deviation = line.split('=')[1].rstrip()
            elif line.startswith("coverage="):
                coverage = line.split('=')[1].rstrip()
            elif line.startswith("mutation_rate="):
                mutation_rate = line.split('=')[1].rstrip()
            elif line.startswith("indel_fraction="):
                indel_fraction = line.split('=')[1].rstrip()
            elif line.startswith("indel_extended="):
                indel_extended = line.split('=')[1].rstrip()
            elif line.startswith("seed_random_generator="):
                seed_random_generator = line.split('=')[1].rstrip()
            elif line.startswith("discard_ambiguos="):
                discard_ambiguos = line.split('=')[1].rstrip()
            elif line.startswith("haplotype_mode="):
                haplotype_mode = line.split('=')[1].rstrip()
            elif line.startswith("output_directory="):
                output_directory = line.split('=')[1].rstrip()
            elif line.startswith("verbose_mode="):
                verbose_mode = line.split('=')[1].rstrip()
            elif line.startswith("group_bar_chart="):
                group_bar_chart = line.split('=')[1].rstrip()
            elif line.startswith("report_cross_mapped="):
                report_cross_mapped = line.split('=')[1].rstrip()
            elif line.startswith("mapper_template_path="):
                mapper_template_path = line.split('=')[1].rstrip()
            elif line.startswith("max_mismatch_per_len="):
                max_mismatch_per_len = line.split('=')[1].rstrip()
            elif line.startswith("bact_mode="):
                bact_mode = line.split('=')[1].rstrip()
            elif line.startswith("max_mismatch="):
                max_mismatch = line.split('=')[1].rstrip()
            elif line.startswith("star_temp="):
                star_temp = line.split('=')[1].rstrip()
            elif line.startswith("store_com="):
                store_com = line.split('=')[1].rstrip()

        fastqpath_list = []
        for fastq,path in zip(fastaq_list,path_file_list):
            print(os.path.join(path,fastq))
            fastqpath_list.append(os.path.join(path,fastq))
        annotationspath_list = []
        for annotations,path in zip(annotations_gtf_list,path_file_list):
            print(os.path.join(path,annotations))
            annotationspath_list.append(os.path.join(path,annotations))
        list_files_string = ' '.join(fastqpath_list)
        genome_name_string = ' '.join(genome_name_list)
        read_length_string = ",".join(read_len_list)
        number_of_reads_string = " ".join(number_of_reads_list)
        annotations_gtf_ls_str = " ".join(annotationspath_list)
        id = random.randint(1,100000)
        if fastqpath_list != [''] and genome_name_list != [''] and read_len_list != [''] and number_of_reads_list != [''] and annotations_gtf_list != ['']:
            if mapper_template_path == "":
                command = f"/gpfs/projects/bsc40/project/pipelines/anaconda3/envs/crossmapper_v111/bin/crossmapper RNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -a {annotations_gtf_ls_str} -t {number_of_cores} -e {base_error_rate} -d {outer_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} -max_mismatch_per_len {max_mismatch_per_len} -bact_mode {bact_mode} -max_mismatch {max_mismatch}" # same without -star_tmp
                with open(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"),"w") as f:
                    f.write(f"""#!/bin/bash
#SBATCH --job-name=crossmaper.{id}
#SBATCH --chdir=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/
#SBATCH --output=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.out
#SBATCH --error=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.err
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --qos=debug

module load ANACONDA/5.0.1
source /gpfs/projects/bsc40/project/pipelines/anaconda3/etc/profile.d/conda.sh
conda activate crossmapper_v111
{command}""")  
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=host, username=username, password=password)
                    sftp = ssh.open_sftp()
                    print(store_com)
                    if store_com.endswith("/"):
                        store_com = store_com[:-1]
                    print(store_com)
                    sftp.put(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"), store_com + "/crossmaper.sh")
                    sftp.close()
                    ssh.exec_command(f"sbatch {store_com}/crossmaper.sh")
                    ssh.close()
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except paramiko.AuthenticationException:
                    print("Authentication failed. Please check your credentials.")
                    command = "Authentication failed. Please check your credentials."
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except paramiko.SSHException as ssh_exception:
                    print(f"SSH connection failed: {str(ssh_exception)}")
                    command = "SSH connection failed: " + str(ssh_exception)
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    command = "An error occurred: " + str(e)
                    with open(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"),"r") as f:
                        lines = f.readlines()
                        print(lines)
                    # os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
            elif mapper_template_path != "":       
                command = f"/gpfs/projects/bsc40/project/pipelines/anaconda3/envs/crossmapper_v111/bin/crossmapper RNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -a {annotations_gtf_ls_str} -t {number_of_cores} -e {base_error_rate} -d {outer_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -max_mismatch_per_len {max_mismatch_per_len} -bact_mode {bact_mode} -max_mismatch {max_mismatch}" # same without -star_tmp
                with open(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"),"w") as f:
                    f.write(f"""#!/bin/bash
#SBATCH --job-name=crossmaper.{id}
#SBATCH --chdir=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/
#SBATCH --output=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.out
#SBATCH --error=/gpfs/projects/bsc40/project/pipelines/multiplex/jobs/%j.err
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --qos=debug

module load ANACONDA/5.0.1
source /gpfs/projects/bsc40/project/pipelines/anaconda3/etc/profile.d/conda.sh
conda activate crossmapper_v111
{command}""")  
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=host, username=username, password=password)
                    sftp = ssh.open_sftp()
                    print(store_com)
                    if store_com.endswith("/"):
                        store_com = store_com[:-1]
                    print(store_com)
                    sftp.put(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"), store_com + "/crossmaper.sh")
                    sftp.close()
                    ssh.exec_command(f"sbatch {store_com}/crossmaper.sh")
                    ssh.close()
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except paramiko.AuthenticationException:
                    print("Authentication failed. Please check your credentials.")
                    command = "Authentication failed. Please check your credentials."
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except paramiko.SSHException as ssh_exception:
                    print(f"SSH connection failed: {str(ssh_exception)}")
                    command = "SSH connection failed: " + str(ssh_exception)
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    command = "An error occurred: " + str(e)
                    os.remove(os.path.join(CROSSMAPER_FOLDER,"crossmaper.sh"))
                    data = {'command':command}
                    return render_template('command.html',data=data)
        else:
            render_template('crossmaperna.html',message="Please fill all the fields")
    elif is_logged() != True:
        return render_template('sshlogin.html')


# Create the app
def create_app():
    return app

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='127.0.0.1', port=5001)


    # app.run()
    # serve(app, host='0.0.0.0', port=8080)


    # activate the source venv: source ./venv/bin/activate
    # deactivate the source venv: deactivate
    # run in debug mode: flask --app app --debug run
    # app.run(debug=True) ### functiona
    # app.run() ### functiona
    # app.run(debug=True, port=5000)
    # app.run(host="127.0.0.1", port=8080, debug=True)docke