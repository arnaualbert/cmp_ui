class RnaParams {
    fastaq;
    genomeName;
    readLength;
    readConfiguration;
    numberOfReads;
    annotationsgtf;
    numberofcores;
    baseerorrate;
    outerDistance;
    standarDeviation;
    coverage;
    mutationRate;
    indelFraction;
    indelExtended;
    seedRandomGenerator;
    Discarambiguous;
    haplotypeMode;
    outputDirectory;
    verboseMode;
    groupBarChart;
    reportCross;
    mapperTemplatePath;
    maxMissmatchPerLen;
    bacterialMode;
    maxMissmatch;
    starTmp;
    
    // constructor
    constructor(fastaq, genomeName, readLength, readConfiguration, numberOfReads, annotationsgtf, numberofcores, baseerorrate, outerDistance, standarDeviation, coverage, mutationRate, indelFraction, indelExtended, seedRandomGenerator,
        Discarambiguous, haplotypeMode, outputDirectory, verboseMode, groupBarChart, reportCross, mapperTemplatePath, maxMissmatchPerLen, bacterialMode, maxMissmatch, starTmp) {
        this.fastaq = fastaq;
        this.genomeName = genomeName;
        this.readLength = readLength;
        this.readConfiguration = readConfiguration;
        this.numberOfReads = numberOfReads;
        this.annotationsgtf = annotationsgtf;
        this.numberofcores = numberofcores;
        this.baseerorrate = baseerorrate;
        this.outerDistance = outerDistance;
        this.standarDeviation = standarDeviation;
        this.coverage = coverage;
        this.mutationRate = mutationRate;
        this.indelFraction = indelFraction;
        this.indelExtended = indelExtended;
        this.seedRandomGenerator = seedRandomGenerator;
        this.Discarambiguous = Discarambiguous;
        this.haplotypeMode = haplotypeMode;
        this.outputDirectory = outputDirectory;
        this.verboseMode = verboseMode;
        this.groupBarChart = groupBarChart;
        this.reportCross = reportCross;
        this.mapperTemplatePath = mapperTemplatePath;
        this.maxMissmatchPerLen = maxMissmatchPerLen;
        this.bacterialMode = bacterialMode;
        this.maxMissmatch = maxMissmatch;
        this.starTmp = starTmp;
    }
    //getters
    getfastaq() {
        return this.fastaq;
    }
    getgenomeName() {
        return this.genomeName;
    }
    getreadLength() {
        return this.readLength;
    }
    getreadConfiguration() {
        return this.readConfiguration;
    }
    getnumberOfReads() {
        return this.numberOfReads;
    }
    getannotationsgtf() {
        return this.annotationsgtf;
    }
    getnumberofcores() {
        return this.numberofcores;
    }
    getbaseerorrate() {
        return this.baseerorrate;
    }
    getouterDistance() {
        return this.outerDistance;
    }
    getstandarDeviation() {
        return this.standarDeviation;
    }
    getcoverage() {
        return this.coverage;
    }
    getmutationRate() {
        return this.mutationRate;
    }
    getindelFraction() {
        return this.indelFraction;
    }
    getindelExtended() {
        return this.indelExtended;
    }
    getseedRandomGenerator() {
        return this.seedRandomGenerator;
    }
    getDiscarambiguous() {
        return this.Discarambiguous;
    }
    gethaplotypeMode() {
        return this.haplotypeMode;
    }
    getoutputDirectory() {
        return this.outputDirectory;
    }
    getverboseMode() {
        return this.verboseMode;
    }
    getgroupBarChart() {
        return this.groupBarChart;
    }
    getreportCross() {
        return this.reportCross;
    }
    getmapperTemplatePath() {
        return this.mapperTemplatePath;
    }
    getmaxMissmatchPerLen() {
        return this.maxMissmatchPerLen;
    }
    getbacterialMode() {
        return this.bacterialMode;
    }
    getmaxMissmatch() {
        return this.maxMissmatch;
    }
    getstarTmp() {
        return this.starTmp;
    }
    // setters
    setFastaq(fastaq) {
        this.fastaq = fastaq;
    }
    setgenomeName(genomeName) {
        this.genomeName = genomeName;
    }
    setreadLength(readLength) {
        this.readLength = readLength;
    }
    setreadConfiguration(readConfiguration) {
        this.readConfiguration = readConfiguration;
    }
    setnumberOfReads(numberOfReads) {
        this.numberOfReads = numberOfReads;
    }
    setannotationsgtf(annotationsgtf) {
        this.annotationsgtf = annotationsgtf;
    }
    setnumberofcores(numberofcores) {
        this.numberofcores = numberofcores;
    }
    setbaseerorrate(baseerorrate) {
        this.baseerorrate = baseerorrate;
    }
    setouterDistance(outerDistance) {
        this.outerDistance = outerDistance;
    }
    setstandarDeviation(standarDeviation) {
        this.standarDeviation = standarDeviation;
    }
    setcoverage(coverage) {
        this.coverage = coverage;
    }
    setmutationRate(mutationRate) {
        this.mutationRate = mutationRate;
    }
    setindelFraction(indelFraction) {
        this.indelFraction = indelFraction;
    }
    setindelExtended(indelExtended) {
        this.indelExtended = indelExtended;
    }
    setseedRandomGenerator(seedRandomGenerator) {
        this.seedRandomGenerator = seedRandomGenerator;
    }
    setDiscarambiguous(Discarambiguous) {
        this.Discarambiguous = Discarambiguous;
    }
    sethaplotypeMode(haplotypeMode) {
        this.haplotypeMode = haplotypeMode;
    }
    setoutputDirectory(outputDirectory) {
        this.outputDirectory = outputDirectory;
    }
    setverboseMode(verboseMode) {
        this.verboseMode = verboseMode;
    }
    setgroupBarChart(groupBarChart) {
        this.groupBarChart = groupBarChart;
    }
    setreportCross(reportCross) {
        this.reportCross = reportCross;
    }
    setmapperTemplatePath(mapperTemplatePath) {
        this.mapperTemplatePath = mapperTemplatePath;
    }
    setmaxMissmatchPerLen(maxMissmatchPerLen) {
        this.maxMissmatchPerLen = maxMissmatchPerLen;
    }
    setbacterialMode(bacterialMode) {
        this.bacterialMode = bacterialMode;
    }
    setmaxMissmatch(maxMissmatch) {
        this.maxMissmatch = maxMissmatch;
    }
    setstarTmp(starTmp) {
        this.starTmp = starTmp;
    }

}