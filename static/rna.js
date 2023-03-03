document.addEventListener('DOMContentLoaded', function () {

    // select all the optional arguments
    var optionalArguments = document.querySelectorAll('#optional_arguments');
    // loop the array of all the optional arguments and hide them
    for (var i = 0; i < optionalArguments.length; i++) {
        var options = optionalArguments[i];
        options.style.display = "none";
    }

    fasta_id = 2;


})

// when the button is clicked hide all the optional arguments if they are present or show all the optional arguments if they are not shown
function showHideRna() {
    var optionalArguments = document.querySelectorAll('#optional_arguments');
    for (var i = 0; i < optionalArguments.length; i++) {
        var options = optionalArguments[i];

        if (options.style.display === "none") {
            options.style.display = "block";
        } else {
            options.style.display = "none";
        }
    }
}

function addFormRna() {
    var original = document.getElementById("form_fasta");
    var new_form = original.cloneNode(true);
    var where_form = document.getElementById("fastas");
    where_form.appendChild(new_form);
}

function addFormReadLength() {
    var original = document.getElementById("form_read_length");
    var new_form = original.cloneNode(true);
    var where_form = document.getElementById("read_lengths");
    where_form.appendChild(new_form);
}
// get all the parameters and create the RnaParams object , then add it to the array

function sendRna_v2() {
    var objects = [];

    var form_fasta = document.querySelectorAll("#form_fasta");
    var fastaq = document.querySelectorAll("#fastaq");
    var genomeName = document.querySelectorAll("#genome_name");
    var readLength = document.querySelectorAll("#read_length");
    var readConfiguration = document.getElementById("read_configuration");
    var numberOfReads = document.querySelectorAll("#number_of_reads");
    var annotationsgtf = document.querySelectorAll("#annotations_gtf");
    var numberofcores = document.getElementById("number_of_cores");
    var baseerorrate = document.getElementById("base_error_rate");
    var outerDistance = document.getElementById("outer_distance");
    var standarDeviation = document.getElementById("standar_deviation");
    var coverage = document.getElementById("coverage");
    var mutationRate = document.getElementById("mutation_rate");
    var indelFraction = document.getElementById("indel_fraction");
    var indelExtended = document.getElementById("indel_extended");
    var seedRandomGenerator = document.getElementById("seed_random_generator");
    var discarambiguous = document.getElementById("discard_ambiguos");
    var haplotypeMode = document.getElementById("haplotype_mode");
    var outputDirectory = document.getElementById("output_directory");
    var verboseMode = document.getElementById("verbose_mode");
    var groupBarChart = document.getElementById("group_bar_chart");
    var reportCrossMapped = document.getElementById("report_cross_mapped");
    var mapperTemplatePath = document.getElementById("mapper_template_path");
    var maxMissmatchPerLen = document.getElementById("max_mismatch_per_len");
    var bacterialMode = document.getElementById("bact_mode");
    var maxMissmatch = document.getElementById("max_mismatch");
    var starTmp = document.getElementById("star_temp");
    var total_obj = form_fasta.length;

    for (let i = 0; i < total_obj; i++) {
        var rnaParams = new RnaParams(fastaq[i].value, genomeName[i].value, readLength[0].value, readConfiguration.value, numberOfReads[i].value, annotationsgtf[i].value, numberofcores.value, baseerorrate.value, outerDistance.value, standarDeviation.value, coverage.value, mutationRate.value, indelFraction.value, indelExtended.value, seedRandomGenerator.value, discarambiguous.value, haplotypeMode.value, outputDirectory.value, verboseMode.value, groupBarChart.value, reportCrossMapped.value, mapperTemplatePath.value, maxMissmatchPerLen.value, bacterialMode.value, maxMissmatch.value, starTmp.value)
        console.log(rnaParams);
        
        var rnaJson = JSON.stringify(rnaParams);
        objects.push(rnaJson);
    }

    console.log(objects);
}