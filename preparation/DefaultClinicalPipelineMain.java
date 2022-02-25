import org.apache.ctakes.core.config.ConfigParameterConstants;
import org.apache.ctakes.core.pipeline.PipelineBuilder;
import org.apache.ctakes.core.pipeline.PiperFileReader;
import org.apache.ctakes.dictionary.lookup2.util.UmlsUserApprover;

public class DefaultClinicalPipelineMain {
    // parameter for the clinical pipeline
    // piper-file of the pipeline
    public static final String PIPER_FILE = "path_to_cTakes/bin/DefaultFastPipeline.piper";
    // input directory of the clinical notes
    public static final String INPUT_DIR = "input-directory";
    // output directory
    public static final String OUTPUT_DIR = "output-directory";
    // UMLS key
    public static final String UMLS_KEY = "";

    public static void main(String[] args) throws Exception {
        PiperFileReader piperReader = new PiperFileReader();
        PipelineBuilder builder = piperReader.getBuilder();

        // set the parameters
        builder.set(UmlsUserApprover.KEY_PARAM, UMLS_KEY);
        builder.set(ConfigParameterConstants.PARAM_INPUTDIR, INPUT_DIR);
        builder.set(ConfigParameterConstants.PARAM_OUTPUTDIR, OUTPUT_DIR);

        // add the default CR and CC
        builder.readFiles(INPUT_DIR);
        builder.writeXMIs(OUTPUT_DIR);

        // Load the piper file
        piperReader.loadPipelineFile(PIPER_FILE);

        builder.run();
    }
}

