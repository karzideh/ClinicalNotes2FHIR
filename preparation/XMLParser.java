import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class XMLParser {
    private static final String filename = "path_to_dataset";

    public static void main(String[] args){
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        try{
            dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(new File(filename));
            doc.getDocumentElement().normalize();
            System.out.println("Root Element :" + doc.getDocumentElement().getNodeName());
            System.out.println("------");
            NodeList list = doc.getElementsByTagName("doc");
            for(int temp = 0; temp < list.getLength();temp++){
                Node node = list.item(temp);
                if (node.getNodeType() == Node.ELEMENT_NODE) {
                    Element element = (Element) node;
                    String id = element.getAttribute("id");
                    String text = element.getElementsByTagName("text").item(0).getTextContent();
                    BufferedWriter writer = new BufferedWriter(new FileWriter(new File("output_directory/patient-"+id)));
                    writer.write(text);
                    writer.close();
                }
            }
        } catch (ParserConfigurationException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (SAXException e) {
            e.printStackTrace();
        }
    }
}
