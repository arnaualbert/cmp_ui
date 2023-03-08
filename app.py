import json
from webbrowser import get
from flask import Flask, render_template, request,flash,redirect,url_for,Response, send_file
import random
from werkzeug.utils import secure_filename
import os
import shutil
from pathlib import Path
import re

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


@app.route("/")
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/demultiplexing',methods=['GET', 'POST'])
def demultiplexing():
    ''' Demultiplexing 
        This function is used to demultiplex the fastq files.
        It takes all the parameters from the html form.
    '''
    if request.method == 'POST':

        fastas_fwd = request.files.getlist("fastas_fwd")
        fastas_fwd_ls = []
        for f in fastas_fwd:
            if f and allowed_file(f.filename):         
                print(f.filename)
                print(secure_filename(f.filename))
                filename = secure_filename(f.filename)
                fastas_fwd_ls.append(os.path.join(filename))
        fastas_rv = request.files.getlist("fastas_rv")
        fastas_rv_ls = []
        for f in fastas_rv:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                print(f.filename)
                fastas_rv_ls.append(os.path.join(filename))
        output_dir = request.form['output_dir']
        # ref_genome = request.form.getlist('ref_genome')
        ###################################################################
        ref_genome = request.files.getlist('ref_genome')
        ref_genome_ls = []
        for f in ref_genome:
            filename = secure_filename(f.filename)
            ref_genome_ls.append(os.path.join(filename))         
        ##################################################################    
        organism_name = request.form.getlist('organism_name')
        num_of_threads = request.form['num_of_threads']
        reads_per_chunk = request.form['reads_per_chunk']
        # replace = request.files['replace']
        replace = request.files.getlist('replace')
        rpl_ls = []
        for f in replace:
            rpl_ls.append(f.filename)
        skip_removing_tmp_files = request.form['skip_removing_tmp_files']
        wit_db = request.form['wit_db']
        # params = {"fastas_fwd":fastas_fwd_ls,"fastas_rv":fastas_rv_ls,"output_dir":output_dir,"ref_genome":ref_genome,"organism_name":organism_name,"num_of_threads":num_of_threads,"reads_per_chunk":reads_per_chunk,"skip_removing_tmp_files":skip_removing_tmp_files,"wit_db":wit_db}
        params = {"--fastq1":fastas_fwd_ls,"--fastq2":fastas_rv_ls,"--outdir":output_dir,"--refGenomes":ref_genome,"--sampleNames":organism_name,"--trheads":num_of_threads,"--nreads_per_chunk":reads_per_chunk,"--skip_removing_tmp_files":skip_removing_tmp_files,"--wit_db":wit_db}
        print(params)
        print(type(params))
        fastas_fs_ls_string = " ".join(fastas_fwd_ls)
        fastas_rv_ls_string = " ".join(fastas_rv_ls)
        # ref_genome_string = " ".join(ref_genome)
        ref_genome_string = " ".join(ref_genome_ls)
        organism_name_string = " ".join(organism_name)
        rpl_ls_str = " ".join(rpl_ls)
        command = f'split_pooledSeqWGS_parallel.py --fastq1 {fastas_fs_ls_string} --fastq2 {fastas_rv_ls_string} --outdir {output_dir} --refGenomes {ref_genome_string} --sampleNames {organism_name_string} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --replace {rpl_ls_str} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
        print(command)
        print(type(command))
        data = {'command':command}
        return render_template('command.html',data=data)
    return render_template('demultiplexing.html')


@app.route('/demultiplexing_batch',methods=['GET', 'POST'])
def demultiplexing_batch():
    if request.method == 'POST':
        output_dir = request.form['output_dir']
        fastas_fwd = request.files.getlist("fastas")
        fastas_fwd_ls = []
        for f in fastas_fwd:
            if f and allowed_file(f.filename):
                print(f.filename)
                print(secure_filename(f.filename))
                reg = r'\w+\/?\w+R1\.\w*\.\w+'
                compiled_reg = re.compile(reg)
                if compiled_reg.match(f.filename):
                    fastas_fwd_ls.append(os.path.join(f.filename))
        fastas_rv = request.files.getlist("fastas")
        fastas_rv_ls = []
        for f in fastas_rv:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                print(f.filename)
                reg = r'\w+\/?\w+R2\.\w*\.\w+'
                compiled_reg = re.compile(reg)
                if compiled_reg.match(f.filename):
                    fastas_rv_ls.append(os.path.join(f.filename))
        # ref_genome = request.form.getlist('ref_genome')
        ref_genome = request.files.getlist('ref_genome')
        ref_genome_ls = []
        for f in ref_genome:
            filename = secure_filename(f.filename)
            ref_genome_ls.append(os.path.join(filename))         

        organism_name = request.form.getlist('organism_name')
        num_of_threads = request.form['num_of_threads']
        reads_per_chunk = request.form['reads_per_chunk']
        replace = request.files.getlist('replace')
        rpl_ls = []
        for f in replace:
            rpl_ls.append(f.filename)
        skip_removing_tmp_files = request.form['skip_removing_tmp_files']
        wit_db = request.form['wit_db']
        # params = {"fastas_fwd":fastas_fwd_ls,"fastas_rv":fastas_rv_ls,"output_dir":output_dir,"ref_genome":ref_genome,"organism_name":organism_name,"num_of_threads":num_of_threads,"reads_per_chunk":reads_per_chunk,"skip_removing_tmp_files":skip_removing_tmp_files,"wit_db":wit_db}
        params = {"split_pooledSeqWGS_parallel.py --fastq1":fastas_fwd_ls,"--fastq2":fastas_rv_ls,"--outdir":output_dir,"--refGenomes":ref_genome,"--sampleNames":organism_name,"--trheads":num_of_threads,"--nreads_per_chunk":reads_per_chunk,"--skip_removing_tmp_files":skip_removing_tmp_files,"--wit_db":wit_db}
        print(params)
        print(type(params))
        #for rout in fastas_fwd_ls:
        fastas_fs_ls_string = " ".join(fastas_fwd_ls)
        fastas_rv_ls_string = " ".join(fastas_rv_ls)
        # ref_genome_string = " ".join(ref_genome)
        ref_genome_string = " ".join(ref_genome_ls)
        organism_name_string = " ".join(organism_name)
        rpl_ls_str = " ".join(rpl_ls)
        command = f'split_pooledSeqWGS_parallel.py --fastq1 {fastas_fs_ls_string} --fastq2 {fastas_rv_ls_string} --outdir {output_dir} --refGenomes {ref_genome_string} --sampleNames {organism_name_string} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --replace {rpl_ls_str} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
        print(command)
        print(type(command))
        data = {'command':command}
        return render_template('command.html',data=data)
    return render_template('demultiplexing_batch.html')


@app.route('/crossmaper')
def crossmaper():
    return render_template('crossmaper.html')


@app.route('/command')
def command():
    return render_template('command.html',data={})


@app.route('/crossmaper/dna',methods=['GET','POST'])
def crossmaperdna():
    if request.method == 'GET':
        return render_template('crossmaperdna.html')
    if request.method == 'POST':
        fastq = request.files.getlist("fastaq")
        fastq_ls = []
        for f in fastq:
            fastq_ls.append(f.filename)

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
        fastq_ls_string = " ".join(fastq_ls)
        genome_name_string = " ".join(genome_name)
        number_of_reads_string = " ".join(number_of_reads)
        read_length_string = ",".join(read_length)
        command = f"crossmapper DNA -g {fastq_ls_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -k {min_seed_length} -A {matching_score} -B {missmatch_penalty}"
        data = {'command':command}
        return render_template('command.html',data=data)


@app.route('/crossmaper/rna',methods=['GET','POST'])
def crossmaperrna():
    if request.method == 'GET':
        return render_template('crossmaperna.html')
    if request.method == 'POST':
        fastq = request.files.getlist("fastaq")
        fastq_ls = []
        for f in fastq:
            fastq_ls.append(f.filename)
        genome_name = request.form.getlist('genome_name')
        number_of_reads = request.form.getlist('number_of_reads')
        read_length = request.form.getlist('read_length')
        read_configuration = request.form['read_configuration']
        annotations_gtf = request.form.getlist('annotations_gtf')
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
        annotations_gtf_ls_str = " ".join(annotations_gtf)
        command = f"crossmapper RNA -g {fastq_ls_string} -gn {genome_name_string} -rlen {read_length_string} -rlay {read_configuration} -N {number_of_reads_string} -a {annotations_gtf_ls_str} -t {number_of_cores} -e {base_error_rate} -d {oouter_distance} -s {standar_deviation} -C {coverage} -r {mutation_rate} -R {indel_fraction} -X {indel_extended} -S {seed_random_generator} -AMB {discard_ambiguos} -hapl {haplotype_mode} -o {output_directory} --verbose {verbose_mode} -gb {group_bar_chart} -rc {report_cross_mapped} --mapper-template {mapper_template_path} -max_mismatch_per_len {max_mismatch_per_len} -bact_mode {bact_mode} -max_mismatch {max_mismatch} -star_tmp {star_tmp}"
        data = {'command':command}
        return render_template('command.html',data=data)


def search_files(root_dir, extension):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extension):
                print(os.path.join(root, file))


if __name__ == "__main__":
    # activate the source venv: source ./venv/bin/activate
    # deactivate the source venv: deactivate
    # run in debug mode: flask --app app --debug run
    app.run(debug=True)
    #app.run(debug=True, port=5000)
    # app.run(host="127.0.0.1", port=8080, debug=True)