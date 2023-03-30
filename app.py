from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import re
import paramiko


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

ALLOWED_EXTENSIONS = set(['*fasta.*','fastaq.gz','gz','fq.gz','*fq.*'])

# Show the ssh login page
@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        global host 
        global username
        global password
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
        ssh.close()
    return render_template('sshlogin.html')

# Show the home page
@app.route("/home",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('index.html')

# Allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Show the demultiplexing page
@app.route('/demultiplexing',methods=['GET', 'POST'])
def demultiplexing():
    ''' Demultiplexing 
        This function is used to demultiplex the fastq files.
        It takes all the parameters from the html form.
    '''
    if request.method == 'POST':
        fastas_fwd = request.files.getlist("fastas_fwd")
        fastas_fwd_ls = []
        file_path = request.form['path_file']
        for f in fastas_fwd:
            if f and allowed_file(f.filename):         
                print(f.filename)
                print(secure_filename(f.filename))
                filename = secure_filename(f.filename)
                fastas_fwd_ls.append(os.path.join(file_path,filename))
        fastas_rv = request.files.getlist("fastas_rv")
        fastas_rv_ls = []
        for f in fastas_rv:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                fastas_rv_ls.append(os.path.join(file_path,filename))
        output_dir = request.form['output_dir']
        getoption = request.form.get('getoption')
        # if getoption == 'on':
        #     ref_genome = request.files.getlist('ref_genome')
        #     path_file_unique = request.form['path_file_unique']
        #     ref_genome_ls = []
        #     for f in ref_genome:
        #         filename = secure_filename(f.filename)
        #         ref_genome_ls.append(os.path.join(path_file_unique,filename))   
        # else:
        #     ref_genome = request.files.getlist('ref_genome')
        #     path_files = request.form.getlist('path_files')
        #     print(path_files)
        #     ref_genome_ls = []
        #     listoffiles = []
        #     for f in ref_genome:
        #         filename = secure_filename(f.filename)
        #         print(filename)
        #         listoffiles.append(filename)
        #     for path,file in zip(path_files,listoffiles):
        #         ref_genome_ls.append(os.path.join(path,filename)) 
        if getoption == 'on':
        # if getoption == True:
            print("same path")
            ref_genome = request.files.getlist('ref_genome')
            path_file_unique = request.form['path_file_unique']
            ref_genome_ls = []
            for f in ref_genome:
                filename = secure_filename(f.filename)
                ref_genome_ls.append(os.path.join(path_file_unique,filename))   
        else:
            ref_genome = request.files.getlist('ref_genome')
            path_files = request.form.getlist('path_files')
            print(path_files)
            ref_genome_ls = []
            listoffiles = []
            for f in ref_genome:
                filename = secure_filename(f.filename)
                print(f'filename: {filename}')
                listoffiles.append(filename)
                print(f'list: {listoffiles}')
            for path,file in zip(path_files,listoffiles):
                ref_genome_ls.append(os.path.join(path,file))
        organism_name = request.form.getlist('organism_name')
        num_of_threads = request.form['num_of_threads']
        reads_per_chunk = request.form['reads_per_chunk']
        replace = request.files.getlist('replace')
        store_com = request.form['store_com']
        rpl_ls = []
        for f in replace:
            rpl_ls.append(f.filename)
        skip_removing_tmp_files = request.form['skip_removing_tmp_files']
        wit_db = request.form['wit_db']
        params = {"--fastq1":fastas_fwd_ls,"--fastq2":fastas_rv_ls,"--outdir":output_dir,"--refGenomes":ref_genome,"--sampleNames":organism_name,"--trheads":num_of_threads,"--nreads_per_chunk":reads_per_chunk,"--skip_removing_tmp_files":skip_removing_tmp_files,"--wit_db":wit_db}
        print(params)
        print(type(params))
        fastas_fs_ls_string = " ".join(fastas_fwd_ls)
        fastas_rv_ls_string = " ".join(fastas_rv_ls)
        ref_genome_string = " ".join(ref_genome_ls)
        organism_name_string = " ".join(organism_name)
        rpl_ls_str = " ".join(rpl_ls)
        command = f'split_pooledSeqWGS_parallel.py --fastq1 {fastas_fs_ls_string} --fastq2 {fastas_rv_ls_string} --outdir {output_dir} --refGenomes {ref_genome_string} --sampleNames {organism_name_string} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --replace {rpl_ls_str} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
        print(command)
        print(type(command))
        data = {'command':command}
        print(f'ip = {request.remote_addr}')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}demultiplexing.txt; echo {command} >> {store_com}demultiplexing.txt')
        output = stdout.readlines()
        error = stderr.readlines()
        ssh.close()
        return render_template('command.html',data=data)
    return render_template('demultiplexing.html')

# Show the demultiplexing batch page
@app.route('/demultiplexing_batch',methods=['GET', 'POST'])
def demultiplexing_batch():
    if request.method == 'POST':
        output_dir = request.form['output_dir']
        fastas_fwd = request.files.getlist("fastas")
        fastas_fwd_ls = []
        file_path = request.form['path_file']
        for f in fastas_fwd:
            if f and allowed_file(f.filename):
                print(f.filename)
                reg = r'.*R1.*|.*r1.*'
                compiled_reg = re.compile(reg)
                if compiled_reg.match(f.filename):
                    fastas_fwd_ls.append(os.path.join(file_path,f.filename))
        fastas_rv = request.files.getlist("fastas")
        fastas_rv_ls = []
        for f in fastas_rv:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                reg = r'.*R2.*|.*r2.*'
                compiled_reg = re.compile(reg)
                if compiled_reg.match(f.filename):
                    fastas_rv_ls.append(os.path.join(file_path,f.filename))
        getoption = request.form.get('getoption')
        print(getoption)
        if getoption == 'on':
        # if getoption == True:
            print("same path")
            ref_genome = request.files.getlist('ref_genome')
            path_file_unique = request.form['path_file_unique']
            ref_genome_ls = []
            for f in ref_genome:
                filename = secure_filename(f.filename)
                ref_genome_ls.append(os.path.join(path_file_unique,filename))   
        else:
            ref_genome = request.files.getlist('ref_genome')
            path_files = request.form.getlist('path_files')
            print(path_files)
            ref_genome_ls = []
            listoffiles = []
            for f in ref_genome:
                filename = secure_filename(f.filename)
                print(f'filename: {filename}')
                listoffiles.append(filename)
                print(f'list: {listoffiles}')
            for path,file in zip(path_files,listoffiles):
                ref_genome_ls.append(os.path.join(path,file))
        organism_name = request.form.getlist('organism_name')
        num_of_threads = request.form['num_of_threads']
        reads_per_chunk = request.form['reads_per_chunk']
        replace = request.files.getlist('replace')
        store_com = request.form['store_com']
        rpl_ls = []
        for f in replace:
            rpl_ls.append(f.filename)
        skip_removing_tmp_files = request.form['skip_removing_tmp_files']
        wit_db = request.form['wit_db']
        params = {"split_pooledSeqWGS_parallel.py --fastq1":fastas_fwd_ls,"--fastq2":fastas_rv_ls,"--outdir":output_dir,"--refGenomes":ref_genome,"--sampleNames":organism_name,"--trheads":num_of_threads,"--nreads_per_chunk":reads_per_chunk,"--skip_removing_tmp_files":skip_removing_tmp_files,"--wit_db":wit_db}
        print(params)
        ref_genome_string = " ".join(ref_genome_ls)
        organism_name_string = " ".join(organism_name)
        rpl_ls_str = " ".join(rpl_ls)
        commands = []
        print(len(fastas_fwd))
        ls_fwd = fastas_fwd_ls
        sort_ls_fwd = sorted(fastas_fwd_ls)
        sort_ls_rv = sorted(fastas_rv_ls)
        print(fastas_fwd_ls)
        print(ls_fwd)
        print(len(ls_fwd))
        i = 0
        while i < len(ls_fwd):
            command = f'split_pooledSeqWGS_parallel.py --fastq1 {sort_ls_fwd[i]} --fastq2 {sort_ls_rv[i]} --outdir {output_dir} --refGenomes {ref_genome_string} --sampleNames {organism_name_string} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --replace {rpl_ls_str} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
            commands.append(command)
            i += 1
        data = {'command':commands}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}demultiplexingbatch.txt')
        stdin, stdout, stderr = ssh.exec_command(f'echo '' > {store_com}demultiplexingbatch.txt')           
        for com in commands:       
            stdin, stdout, stderr = ssh.exec_command(f'echo {com} >> {store_com}demultiplexingbatch.txt')        
        output = stdout.readlines()
        error = stderr.readlines()
        ssh.close()
        return render_template('commands.html',data=data)
    return render_template('demultiplexing_batch.html')

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
        path_file = request.form['path_file']
        fastq = request.files.getlist("fastaq")
        fastq_ls = []
        for f in fastq:
            fastq_ls.append(path_file+f.filename)

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
        fastq_ls_string = " ".join(fastq_ls)
        genome_name_string = " ".join(genome_name)
        number_of_reads_string = " ".join(number_of_reads)
        read_length_string = ",".join(read_length)
        command = f"crossmapper DNA -g {fastq_ls_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -k {min_seed_length} -A {matching_score} -B {missmatch_penalty}"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(f'touch {store_com}crossmapperdna.txt; echo {command} >> {store_com}crossmapperdna.txt')
        output = stdout.readlines()
        error = stderr.readlines()
        ssh.close()
        data = {'command':command}
        return render_template('command.html',data=data)

# Show the Crossmaper RNA page and get all the parameters from the form
@app.route('/crossmaper/rna',methods=['GET','POST'])
def crossmaperrna():
    if request.method == 'GET':
        return render_template('crossmaperna.html')
    if request.method == 'POST':
        path_file = request.form['path_file']
        fastq = request.files.getlist("fastaq")
        fastq_ls = []
        for f in fastq:
            fastq_ls.append(path_file+f.filename)
            
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
        star_tmp = request.form['star_temp']
        fastq_ls_string = " ".join(fastq_ls)
        genome_name_string = " ".join(genome_name)
        number_of_reads_string = " ".join(number_of_reads)
        read_length_string = ",".join(read_length)
        annotations_gtf_ls_str = " ".join(annotations_gtf_ls)
        command = f"crossmapper RNA -g {fastq_ls_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -a {annotations_gtf_ls_str} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -max_mismatch_per_len {max_mismatch_per_len} -bact_mode {bact_mode} -max_mismatch {max_mismatch} -star_tmp {star_tmp}"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(f'touch crossmapperrna.txt; echo {command} >> crossmapperrna.txt')
        output = stdout.readlines()
        error = stderr.readlines()
        ssh.close()
        data = {'command':command}
        return render_template('command.html',data=data)

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