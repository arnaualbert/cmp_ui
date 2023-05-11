from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import re
import paramiko
from threading import Thread

module_name = __name__
app = Flask(__name__)

# Get current path
path = os.getcwd()
print(path)

# file Upload
DEMULTIPLEXING_FOLDER = os.path.join(path, 'demultiplexing')
FWD_FOLDER = os.path.join(path, 'demultiplexing/fwd')
RV_FOLDER = os.path.join(path, 'demultiplexing/rv')

if not os.path.isdir(DEMULTIPLEXING_FOLDER):
    os.mkdir(DEMULTIPLEXING_FOLDER)

if not os.path.isdir(FWD_FOLDER):
    os.mkdir(FWD_FOLDER)

if not os.path.isdir(RV_FOLDER):
    os.mkdir(RV_FOLDER)

app.config['DEMULTIPLEXING_FOLDER'] = DEMULTIPLEXING_FOLDER
app.config['DEMULTIPLEXING_FWD_FOLDER'] = FWD_FOLDER
app.config['DEMULTIPLEXING_RV_FOLDER'] = RV_FOLDER

# ALLOWED_EXTENSIONS = set(['*fasta.*','fastaq.gz','gz','fq.gz','*fq.*','*','.fasta','fasta','fastq.gz'])
# ALLOWED_EXTENSIONS = set(['fastaq','.fastaq','.fastq','*fasta.*','fastaq.gz','gz','fq.gz','*fq.*','*','.fasta','fasta','fastq.gz'])
# ALLOWED_EXTENSIONS = set(['fastaq','.fastaq','.fastq','*fasta.*','fastaq.gz','gz','fq.gz','*fq.*','*','.fasta','fasta','fastq.gz','fastqc.html','fastqc.zip'])
ALLOWED_EXTENSIONS = set(['fastq','fastq.gz','fq','fq.gz','.fastq', '.fastq.gz', '.fq', '.fq.gz'])

def chck(filename):
    return filename.endswith(tuple(ALLOWED_EXTENSIONS))

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
        # ssh.close()
    return render_template('sshlogin.html')

# Show the home page
@app.route("/home",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('index.html')

@app.route('/demultiplexing',methods=['GET', 'POST'])
def demultiplexing():
    ''' Demultiplexing 
        This function is used to demultiplex the fastq files.
        It takes all the parameters from the html form.
    '''

    if request.method == 'GET':
        return render_template('demultiplexing.html')

    if request.method == 'POST':
        data = request.get_data(as_text=True)
        print(data)
        data =  data
        ref_genome_list = []
        organism_name_list = []
        path_files_list=[]
        lines = data.strip().split('\n')
        print(len(data))
        print(type(lines))
        print(lines)
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
            print(command)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}demultiplexing.sh;echo "#!/bin/bash" > {store_com}demultiplexing.sh; echo {command} >> {store_com}demultiplexing.sh')
            output = stdout.readlines()
            error = stderr.readlines()
            data = {'command':command}
            return render_template('command.html',data=data)
        elif fastas_fwd != "" and fastas_rv != "" and output_dir != "" and path_file != "" and ref_genome_list != [] and organism_name_list != [] and store_com != "" and path_files_list != "" :
            ref_gen_ls = []
            print(ref_genome_list)
            print(organism_name_list)
            print(path_files_list)
            fastas_fs_ls_string = os.path.join(path_file,fastas_fwd)
            fastas_rv_ls_string = os.path.join(path_file,fastas_rv)
            for path,gen_ref in zip(path_files_list,ref_genome_list):
                ref_gen_ls.append(os.path.join(path,gen_ref))
            organism_name_string = " ".join(organism_name_list)
            ref_genome_string = " ".join(ref_gen_ls)
            rpl_ls_str = replace
            command = f'split_pooledSeqWGS_parallel.py --fastq1 {fastas_fs_ls_string} --fastq2 {fastas_rv_ls_string} --outdir {output_dir} --refGenomes {ref_genome_string} --sampleNames {organism_name_string} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --replace {rpl_ls_str} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
            print(command)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}demultiplexing.sh;echo "#!/bin/bash" > {store_com}demultiplexing.sh; echo {command} >> {store_com}demultiplexing.sh')
            output = stdout.readlines()
            error = stderr.readlines()
            data = {'command':command}
            return render_template('command.html',data=data)
        else:
            return render_template('demultiplexing.html',data="Please fill all the fields")
        return render_template('command.html',data=data)
    return render_template('demultiplexing.html')

# Show the demultiplexing batch page
@app.route('/demultiplexing_batch',methods=['GET', 'POST'])
def demultiplexing_batch():
    if request.method == 'GET':
        return render_template('demultiplexing_batch.html')
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        # print(data)
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

        for fasta in fastas:
            if chck(fasta):
               matched = re.search(reg, fasta)
               if matched:
                    if "1" in matched.group():
                        fastas_forward.append(fasta)
                    elif "2" in matched.group():
                        fastas_reversed.append(fasta)
        fastas_fwd = sorted(fastas_forward)
        fastas_rv = sorted(fastas_reversed)


        if have_getoption and fastas_fwd != [] and fastas_rv != [] and output_dir != "" and path_file != "" and ref_genome_list != [] and organism_name_list != [] and store_com != "" and path_file_unique != "":
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
                print(command)
                commands.append(command)
                i = i + 1
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}demultiplexingbatch.sh')
            stdin, stdout, stderr = ssh.exec_command(f'echo "#!/bin/bash" > {store_com}demultiplexingbatch.sh')           
            for com in commands:       
                # stdin, stdout, stderr = ssh.exec_command(f'echo {com} >> {store_com}demultiplexingbatch.txt')
                stdin, stdout, stderr = ssh.exec_command(f'echo {com} >> {store_com}demultiplexingbatch.sh')               
            output = stdout.readlines()
            error = stderr.readlines()
            ssh.close()
            data = {'command':commands}
            return render_template('commands.html',data=data)
        elif fastas_fwd != [] and fastas_rv != [] and output_dir != "" and path_file != "" and ref_genome_list != [] and organism_name_list != [] and store_com != "" and path_files_list != "" :
            ref_gen_ls = []
            print(ref_genome_list)
            print(organism_name_list)
            print(path_files_list)
            # fastas_fs_ls_string = os.path.join(path_file,fastas_fwd)
            # fastas_rv_ls_string = os.path.join(path_file,fastas_rv)
            path_fasta_wd = []
            path_fasta_rv = []
            for fasta in fastas_fwd:
                path_fasta_wd.append(os.path.join(path_file,fasta))
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
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}demultiplexingbatch.sh')
            stdin, stdout, stderr = ssh.exec_command(f'echo "#!/bin/bash" > {store_com}demultiplexingbatch.sh')           
            for com in commands:       
                # stdin, stdout, stderr = ssh.exec_command(f'echo {com} >> {store_com}demultiplexingbatch.txt')
                stdin, stdout, stderr = ssh.exec_command(f'echo {com} >> {store_com}demultiplexingbatch.sh')               
            output = stdout.readlines()
            error = stderr.readlines()
            ssh.close()
            data = {'command':commands}
            return render_template('commands.html',data=data)
        else:
            return render_template('demultiplexing.html',data="Please fill all the fields")
    return render_template('demultiplexing.html')

# Show the Crossmaper page
@app.route('/crossmaper')
def crossmaper():
    return render_template('crossmaper.html')

# Show the command page
@app.route('/command')
def command():
    return render_template('command.html',data={})

# Show the Crossmaper DNA page and get all the parameters from the form
@app.route('/crossmaper/dna',methods=['GET','POST'])
def crossmaperdna():
    if request.method == 'GET':
        return render_template('crossmaperdna.html')
    if request.method == 'POST':
        # path_file = request.form['path_file']
        path_file = request.form.getlist('path_file')
        fastq = request.files.getlist("fastaq")
        fastq_ls = []
        # NEW
        list_files = []
        #####
        ##old
        # for f in fastq:
            # fastq_ls.append(path_file+f.filename)
        ###
        ### NEW VERSION 
        for f in fastq:
            fastq_ls.append(f.filename)
        ###
        # NEW
        for path,file in zip(path_file,fastq_ls):
            list_files.append(os.path.join(path,file))
        print(list_files)
        #####
        genome_name = request.form.getlist('genome_name')
        number_of_reads = request.form.getlist('number_of_reads')
        read_length = request.form.getlist('read_length')
        read_configuration = request.form['read_configuration']
        number_of_cores = request.form['number_of_cores']
        base_error_rate = request.form['base_error_rate']
        oouter_distance = request.form['outer_distance']
        standar_deviation = request.form['standar_deviation']
        coverage = request.form['coverage']
        mutation_rate = request.form['mutation_rate']
        indel_fraction = request.form['indel_fraction']
        indel_extended = request.form['indel_extended']
        seed_random_generator = request.form['seed_random_generator']
        discard_ambiguos = request.form['discard_ambiguos']
        haplotype_mode = request.form['haplotype_mode']
        output_directory = request.form['output_directory']
        verbose_mode = request.form['verbose_mode']
        group_bar_chart = request.form['group_bar_chart']
        report_cross_mapped = request.form['report_cross_mapped']
        mapper_template_path = request.form['mapper_template_path']
        min_seed_length = request.form['min_seed_length']
        matching_score = request.form['matching_score']
        missmatch_penalty = request.form['mismatch_penalty']
        store_com = request.form['store_com']
        # NEW
        list_files_string = " ".join(list_files)
        #####
        # fastq_ls_string = " ".join(fastq_ls)
        genome_name_string = " ".join(genome_name)
        number_of_reads_string = " ".join(number_of_reads)
        read_length_string = ",".join(read_length)
        # command = f"crossmapper DNA -g {fastq_ls_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -k {min_seed_length} -A {matching_score} -B {missmatch_penalty}"
        # command = f"crossmapper DNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -k {min_seed_length} -A {matching_score} -B {missmatch_penalty}"
        if list_files == [''] or genome_name == [''] or store_com == "" or number_of_reads == ['']:
            data = 'Please fill all the fields'
            return render_template('crossmaperdna.html', data=data)
        else:
            if mapper_template_path == "":
                command = f"crossmapper DNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} -k {min_seed_length} -A {matching_score} -B {missmatch_penalty}"
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=username, password=password)
                # stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperdna.txt; echo {command} >> {store_com}crossmapperdna.txt')
                # stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperdna.sh; echo {command} >> {store_com}crossmapperdna.sh')
                stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperdna.sh; echo "#!/bin/bash" > {store_com}crossmapperdna.sh; echo {command} >> {store_com}crossmapperdna.sh')
                output = stdout.readlines()
                error = stderr.readlines()
                ssh.close()
                data = {'command':command}
                return render_template('command.html',data=data)
            else:
                command = f"crossmapper DNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -k {min_seed_length} -A {matching_score} -B {missmatch_penalty}"
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=username, password=password)
                # stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperdna.txt; echo {command} >> {store_com}crossmapperdna.txt')
                # stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperdna.sh; echo {command} >> {store_com}crossmapperdna.sh')
                stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperdna.sh; echo "#!/bin/bash" > {store_com}crossmapperdna.sh; echo {command} >> {store_com}crossmapperdna.sh')
                output = stdout.readlines()
                error = stderr.readlines()
                ssh.close()
                data = {'command':command}
                return render_template('command.html',data=data)
 
            # return render_template('crossmaperdna.html')


# Show the Crossmaper RNA page and get all the parameters from the form
@app.route('/crossmaper/rna',methods=['GET','POST'])
def crossmaperrna():
    if request.method == 'GET':
        return render_template('crossmaperna.html')
    if request.method == 'POST':
        # path_file = request.form['path_file']
        path_file = request.form.getlist('path_file')
        fastq = request.files.getlist("fastaq")
        fastq_ls = []
        list_files = []
        # for f in fastq:
            # fastq_ls.append(path_file+f.filename)
        for f in fastq:
            fastq_ls.append(f.filename)
        for path,file in zip(path_file,fastq_ls):
            list_files.append(os.path.join(path,file))
        print(list_files)
        genome_name = request.form.getlist('genome_name')
        number_of_reads = request.form.getlist('number_of_reads')
        read_length = request.form.getlist('read_length')
        read_configuration = request.form['read_configuration']
        annotations_gtf = request.files.getlist('annotations_gtf')
        annotations_gtf_ls = []
        for f in annotations_gtf:
            annotations_gtf_ls.append(f.filename)
        number_of_cores = request.form['number_of_cores']
        base_error_rate = request.form['base_error_rate']
        oouter_distance = request.form['outer_distance']
        standar_deviation = request.form['standar_deviation']
        coverage = request.form['coverage']
        mutation_rate = request.form['mutation_rate']
        indel_fraction = request.form['indel_fraction']
        indel_extended = request.form['indel_extended']
        seed_random_generator = request.form['seed_random_generator']
        discard_ambiguos = request.form['discard_ambiguos']
        haplotype_mode = request.form['haplotype_mode']
        output_directory = request.form['output_directory']
        verbose_mode = request.form['verbose_mode']
        group_bar_chart = request.form['group_bar_chart']
        report_cross_mapped = request.form['report_cross_mapped']
        mapper_template_path = request.form['mapper_template_path']
        max_mismatch_per_len = request.form['max_mismatch_per_len']
        bact_mode = request.form['bact_mode']
        max_mismatch = request.form['max_mismatch']
        store_com = request.form['store_com']
        # star_tmp = request.form['star_temp'] rn not necessary
        # fastq_ls_string = " ".join(fastq_ls) ### old
        list_files_string = " ".join(list_files)
        genome_name_string = " ".join(genome_name)
        number_of_reads_string = " ".join(number_of_reads)
        read_length_string = ",".join(read_length)
        annotations_gtf_ls_str = " ".join(annotations_gtf_ls)
        # command = f"crossmapper RNA -g {fastq_ls_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -a {annotations_gtf_ls_str} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -max_mismatch_per_len {max_mismatch_per_len} -bact_mode {bact_mode} -max_mismatch {max_mismatch} -star_tmp {star_tmp}"
        #it wordks command = f"crossmapper RNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -a {annotations_gtf_ls_str} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -max_mismatch_per_len {max_mismatch_per_len} -bact_mode {bact_mode} -max_mismatch {max_mismatch} -star_tmp {star_tmp}"
        # command = f"crossmapper RNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -a {annotations_gtf_ls_str} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -max_mismatch_per_len {max_mismatch_per_len} -bact_mode {bact_mode} -max_mismatch {max_mismatch}" # same without -star_tmp
        if list_files == [''] or genome_name == [''] or number_of_reads == [''] or read_length == [''] or annotations_gtf_ls == ['']:
            data = "please fill all the fields"
            return render_template('crossmaperna.html', data=data)
        else:
            if mapper_template_path == "":
                command = f"crossmapper RNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -a {annotations_gtf_ls_str} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} -max_mismatch_per_len {max_mismatch_per_len} -bact_mode {bact_mode} -max_mismatch {max_mismatch}" # same without -star_tmp
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=username, password=password)
                # stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperrna.sh; echo {command} >> {store_com}crossmapperrna.sh')
                stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperrna.sh; echo "#!/bin/bash" > {store_com}crossmapperrna.sh ;echo {command} >> {store_com}crossmapperrna.sh')  
                output = stdout.readlines()
                error = stderr.readlines()
                ssh.close()
                data = {'command':command}
                return render_template('command.html',data=data)
            else:
                command = f"crossmapper RNA -g {list_files_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -a {annotations_gtf_ls_str} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -max_mismatch_per_len {max_mismatch_per_len} -bact_mode {bact_mode} -max_mismatch {max_mismatch}" # same without -star_tmp
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, username=username, password=password)
                # stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperrna.sh; echo {command} >> {store_com}crossmapperrna.sh')
                stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperrna.sh; echo "#!/bin/bash" > {store_com}crossmapperrna.sh ;echo {command} >> {store_com}crossmapperrna.sh')

                output = stdout.readlines()
                error = stderr.readlines()
                ssh.close()
                data = {'command':command}
                return render_template('command.html',data=data)

            # return render_template('crossmaperna.html')


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