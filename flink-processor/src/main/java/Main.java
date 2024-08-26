import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.api.common.functions.MapFunction;

public class Main {
    public static final String BROKERS = "kafka:9092";
    public static final String TOPIC = "stockPrice";
    
    public static void main(String[] args) {
        try {
            // Create the execution environment
            StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
            System.out.println("Environment created");

            // Define the Kafka source
            KafkaSource<Stock> kafkaSource = KafkaSource.<Stock>builder()
                .setBootstrapServers(BROKERS)
                .setGroupId("groupId-919292")
                .setTopics(TOPIC)
                .setValueOnlyDeserializer(new StockSchemaDeserializer()) // Ensure StockSchemaDeserializer is properly implemented
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setProperty("partition.discovery.interval.ms", "1000")
                .build();

            // Create a DataStream from the Kafka source
            DataStreamSource<Stock> kafkaStream = env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "kafka");

            System.out.println("Kafka source created");

            // Define the DataStream for calculating average price and change
            DataStream<Tuple2<MyAverage, Double>> stockStream = kafkaStream
                .keyBy(stock -> stock.stockName) // Ensure stockName is a valid field
                .window(TumblingProcessingTimeWindows.of(Time.seconds(60)))
                .aggregate(new AverageAggregator());

            DataStream<Tuple2<String, Double>> stockAndValueStream = stockStream
                .map(new MapFunction<Tuple2<MyAverage, Double>, Tuple2<String, Double>>() {
                @Override
                public Tuple2<String, Double> map(Tuple2<MyAverage, Double> input) throws Exception {
                    return new Tuple2<>(input.f0.name, input.f1);
                }
                }); 

            System.out.println("Aggregation created");
            stockAndValueStream.print();
            // Execute the Flink job
            env.execute("Stock Price Aggregation Job");
        } catch (Exception e) {
            System.err.println("An error occurred during Flink job execution:");
            e.printStackTrace();
        }
    }

    public static class AverageAggregator implements AggregateFunction<Stock, MyAverage, Tuple2<MyAverage, Double>> {

        // Create an initial accumulator
        @Override
        public MyAverage createAccumulator() {
            return new MyAverage();
        }

        // Add a stock object to the accumulator
        @Override
        public MyAverage add(Stock stock, MyAverage myAverage) {
            try {
                myAverage.name = stock.stockName;          // Accumulate the Name
                myAverage.count = myAverage.count + 1;   // Increment the count
                myAverage.priceSum = myAverage.priceSum + stock.stockPrice; // Accumulate the price change
            } catch (Exception e) {
                System.err.println("An error occurred while adding to the accumulator:");
                e.printStackTrace();
            }
            return myAverage;
        }

        // Compute the result from the accumulator
        @Override
        public Tuple2<MyAverage, Double> getResult(MyAverage myAverage) {
            return new Tuple2<>(myAverage, myAverage.priceSum / myAverage.count);
        }

        // Merge two accumulators (used in case of session windows)
        @Override
        public MyAverage merge(MyAverage acc1, MyAverage acc2) {
            acc1.priceSum = acc1.priceSum + acc2.priceSum;
            acc1.count = acc1.count + acc2.count;
            return acc1;
        }
    }

    public static class MyAverage {

        public String name;
        public Integer count = 0;
        public Double priceSum = 0d;

        @Override
        public String toString() {
            return "MyAverage{" +
                    "name='" + name + '\'' +
                    ", count=" + count +
                    ", sum=" + priceSum +
                    '}';
        }
    }
}
