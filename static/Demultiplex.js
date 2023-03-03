class  Demultiplex{
    fastq1;
    fastq2;
    outdir;
    refGenomes;
    organismName;
    threads;
    nreadsPerChunk;
    replace;
    skipRemovingTmpFiles;
    witDB;
    // constructor
    constructor(fastq1, fastq2, outdir, refGenomes,organismName, threads, nreadsPerChunk, replace, skipRemovingTmpFiles, wtDB) {
        this.fastq1 = fastq1;
        this.fastq2 = fastq2;
        this.outdir = outdir;
        this.refGenomes = refGenomes;
        this.organismName = organismName;
        this.threads = threads;
        this.nreadsPerChunk = nreadsPerChunk;
        this.replace = replace;
        this.skipRemovingTmpFiles = skipRemovingTmpFiles;
        this.witDB = wtDB;
    }

    //getters
    getFastq1() {
        return this.fastq1;
    }

    getFastq2() {
        return this.fastq2;
    }

    getOutdir() {
        return this.outdir;
    }

    getRefGenomes() {
        return this.refGenomes;
    }
    getorganismName() {
        return this.organismName;
    }
    getThreads() {
        return this.threads;
    }
    getNreadsPerChunk() {
        return this.nreadsPerChunk;
    }
    getReplace() {
        return this.replace;
    }
    getSkipRemovingTmpFiles() {
        return this.skipRemovingTmpFiles;
    }
    getWitDB() {
        return this.witDB;
    }
    //setters
    setFastq1(fastq1) {
        this.fastq1 = fastq1;
    }
    setFastq2(fastq2) {
        this.fastq2 = fastq2;
    }
    setOutdir(outdir) {
        this.outdir = outdir;
    }
    setRefGenomes(refGenomes) {
        this.refGenomes = refGenomes;
    }
    setorganismName(organismName) {
        this.organismName = organismName;
    }
    setThreads(threads) {
        this.threads = threads;
    }
    setNreadsPerChunk(nreadsPerChunk) {
        this.nreadsPerChunk = nreadsPerChunk;
    }
    setReplace(replace) {
        this.replace = replace;
    }
    setSkipRemovingTmpFiles(skipRemovingTmpFiles) {
        this.skipRemovingTmpFiles = skipRemovingTmpFiles;
    }
    setWitDB(witDB) {
        this.witDB = witDB;
    }
}