
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.json.JsonMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import java.io.IOException;
import org.apache.flink.api.common.serialization.AbstractDeserializationSchema;
//Objects are coming in as JSON and we need to convert them to Stock java class like objects.

// To convert byte streams into objects of type Stock.
public class StockSchemaDeserializer extends AbstractDeserializationSchema<Stock>{
    private static final long serialVersionUUID = 1L;
    private transient ObjectMapper objectMapper;


    //Initialization: open method initializes the ObjectMapper with the necessary configuration to handle Java 8 date and time types.
    @Override
    public void open(InitializationContext context){
        objectMapper=JsonMapper.builder().build().registerModule(new JavaTimeModule());
    }

    @Override
    public Stock deserialize(byte[] message) throws IOException {
        return objectMapper.readValue(message, Stock.class);
    }
}


