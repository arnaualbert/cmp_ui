document.addEventListener("DOMContentLoaded", function () {

    // select all the optional arguments
    var optionalArguments = document.querySelectorAll('#optional_arguments');
    // loop the array of all the optional arguments and hide them
    for (var i = 0; i < optionalArguments.length; i++) {
        var options = optionalArguments[i];
        options.style.display = "none";
    }

})

// when the button is clicked hide all the optional arguments if they are present or show all the optional arguments if they are not shown
function showHide() {
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

// clone the first form and add it to the div
function addForm() {
    var original = document.getElementById("form_demultiplex");
    var new_form = original.cloneNode(true);

    var where_form = document.getElementById("forms");
    where_form.appendChild(new_form);
}

// only fasta,gz files are allowed
var _validFileExtensions = ["fastq.gz"];    
function Validate(oForm) {
    var arrInputs = oForm.getElementsByTagName("input");
    for (var i = 0; i < arrInputs.length; i++) {
        var oInput = arrInputs[i];
        if (oInput.type == "file") {
            var sFileName = oInput.value;
            if (sFileName.length > 0) {
                var blnValid = false;
                for (var j = 0; j < _validFileExtensions.length; j++) {
                    var sCurExtension = _validFileExtensions[j];
                    if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                        blnValid = true;
                        break;
                    }
                }
                
                if (!blnValid) {
                    alert("Sorry, " + sFileName + " is invalid, allowed extensions are: " + _validFileExtensions.join(", "));
                    return false;
                }
            }
        }
    }
  
    return true;
}

function addFormReferenceOrganism() {
    var original = document.getElementById("reference_organism");
    var new_form = original.cloneNode(true);
    var where_form = document.getElementById("references_organisms");
    where_form.appendChild(new_form);
}




// get all the parameters and create the Demultiplex object , then add it to the array
function sendDemultiplexing() {
    var objects = [];

    var total_forms = document.querySelectorAll("#form_demultiplex");
    var fasta0 = document.querySelectorAll("#fasta0");
    var fasta1 = document.querySelectorAll("#fasta1");
    var output_dir = document.querySelectorAll("#output_dir");
    var refGenomes = document.querySelectorAll("#ref_genome");
    var organismName = document.querySelectorAll("#organism_name");
    var numberofthreads = document.querySelectorAll("#num_of_threads");
    var readsperchunk = document.querySelectorAll("#reads_per_chunk");
    var replacements = document.querySelectorAll("#replace");
    var skipRemovingTmpFilesFrom = document.querySelectorAll("#skip_removing_tmp_files");
    var witDB = document.querySelectorAll("#wit_db");
    var total_obj = total_forms.length;
    var organismNamearray = [];
    var referencesgenomesarray = [];
    for(let i = 0;i<refGenomes.length;i++){
        referencesgenomesarray.push(refGenomes[i].value);
    }
    for(let i = 0;i < organismName.length;i++){
        organismNamearray.push(organismName[i].value);    
    }


    for (let i = 0; i < total_obj; i++) {
        if (fasta0[i].value != "" && fasta1[i].value != "" && output_dir[i].value != "" && refGenomes[i].value != "" && organismName[i].value != "" && !isNaN(numberofthreads[i].value) && !isNaN(readsperchunk[i].value)) {
            if (!isNaN(numberofthreads[i].value) && !isNaN(readsperchunk[i].value)) {
                var demultiplex_params = new Demultiplex(fasta0[i].value, fasta1[i].value, output_dir[i].value, referencesgenomesarray, organismNamearray, numberofthreads[i].value, readsperchunk[i].value, replacements[i].value, skipRemovingTmpFilesFrom[i].value, witDB[i].value)
                objects.push(demultiplex_params);
            } else {
                numberofthreads[i].value = "16";
                readsperchunk[i].value = "";
                var demultiplex_params = new Demultiplex(fasta0[i].value, fasta1[i].value, output_dir[i].value, refGenomes[i].value, organismName[i].value, numberofthreads[i].value, readsperchunk[i].value, replacements[i].value, skipRemovingTmpFilesFrom[i].value, witDB[i].value)
                var demultiplexJSON = JSON.stringify(demultiplex_params);
                objects.push(demultiplexJSON);

                
                const data = { name: "John Doe", email: "johndoe@example.com" };

                fetch("http://localhost:5000/send-data", {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json"
                  },
                  body: JSON.stringify(data)
                })
                  .then(res => res.json())
                  .then(response => console.log("Success:", JSON.stringify(response)))
                  .catch(error => console.error("Error:", error));


            }
        } else {
            alert("Please fill in all the required fields");
            objects = null;
        }
    }
    console.log(objects);


}