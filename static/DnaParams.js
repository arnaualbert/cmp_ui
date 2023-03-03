class DnaParams {
    fastaq;
    genomeName;
    readLength;
    readConfiguration;
    numberOfReads;
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
    minSeedLength;
    matchingScore;
    mismatchPenalty;
    // constructor
    constructor(fastaq, genomeName, readLength, readConfiguration, numberOfReads, numberofcores, baseerorrate, outerDistance, standarDeviation, coverage, mutationRate, indelFraction, indelExtended, seedRandomGenerator, Discarambiguous,
        haplotypeMode, outputDirectory, verboseMode, groupBarChart, reportCross, mapperTemplatePath, minSeedLength, matchingScore, mismatchPenalty) {
        this.fastaq = fastaq;
        this.genomeName = genomeName;
        this.readLength = readLength;
        this.readConfiguration = readConfiguration;
        this.numberOfReads = numberOfReads;
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
        this.minSeedLength = minSeedLength;
        this.matchingScore = matchingScore
        this.mismatchPenalty = mismatchPenalty;
    }



    // getters and setters
    getfastaq() { return this.fastaq; }
    setfastaq(fastaq) { this.fastaq = fastaq; }
    getgenomeName() { return this.genomeName; }
    setgenomeName(genomeName) { this.genomeName = genomeName; }
    getreadLength() { return this.readLength; }
    setreadLength(readLength) { this.readLength = readLength; }
    getreadConfiguration() { return this.readConfiguration; }
    setreadConfiguration(readConfiguration) { this.readConfiguration = readConfiguration; }
    getnumberOfReads() { return this.numberOfReads; }
    setnumberOfReads(numberOfReads) { this.numberOfReads = numberOfReads; }
    getnumberofcores() { return this.numberofcores; }
    setnumberofcores(numberofcores) { this.numberofcores = numberofcores }
    getbaseerorrate() { return this.baseerorrate; }
    setbaseerorrate(baseerorrate) { this.baseerorrate = baseerorrate }
    getouterDistance() { return this.outerDistance; }
    setouterDistance(outerDistance) { this.outerDistance = outerDistance; }
    getstandarDeviation() { return this.standarDeviation; }
    setstandarDeviation(standarDeviation) { this.standarDeviation = standarDeviation; }
    getcoverage() { return this.coverage; }
    setcoverage(coverage) { this.coverage = coverage; }
    getmutationRate() { return this.mutationRate; }
    setmutationRate(mutationRate) { this.mutationRate = mutationRate; }
    getindelFraction() { return this.indelFraction; }
    setindelFraction(indelFraction) { this.indelFraction = indelFraction }
    getindelExtended() { return this.indelExtended; }
    setindelExtended(indelExtended) { this.indelExtended = indelExtended; }
    getseedRandomGenerator() { return this.seedRandomGenerator; }
    setseedRandomGenerator(seedRandomGenerator) { this.seedRandomGenerator = seedRandomGenerator; }
    getDiscarambiguous() { return this.Discarambiguous; }
    setDiscarambiguous(Discarambiguous) { this.Discarambig = Discarambiguous; }
    gethaplotypeMode() { return this.haplotypeMode; }
    sethaplotypeMode(haplotypeMode) { this.haplotypeMode = haplotypeMode; }
    getoutputDirectory() { return this.outputDirectory; }
    setoutputDirectory(outputDirectory) { this.outputDirectory = outputDirectory; }
    getverboseMode() { return this.verboseMode; }
    setverboseMode(verboseMode) { this.verboseMode = verboseMode; }
    getgroupBarChart() { return this.groupBarChart; }
    setgroupBarChart(groupBarChart) { this.groupBarChart = groupBarChart; }
    getreportCross() { return this.reportCross; }
    setreportCross(reportCross) { this.reportCross = reportCross; }
    getmapperTemplatePath() { return this.mapperTemplatePath; }
    setmapperTemplatePath(mapperTemplatePath) { this.mapperTemplatePath = mapperTemplatePath; }
    getminSeedLength() { return this.minSeedLength; }
    setminSeedLength(minSeedLength) { this.minSeedLength = minSeedLength; }
    getmatchingScore() { return this.matchingScore; }
    setmatchingScore(matchingScore) { this.matchingScore = matchingScore; }
    getmismatchPenalty() { return this.mismatchPenalty; }
    setmismatchPenalty(mismatchPenalty) { this.mismatchPenalty = mismatchPenalty; }
}