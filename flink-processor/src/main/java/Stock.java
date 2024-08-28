import java.util.Objects;
public class Stock {
    public String stockName;
    public Double stockPrice;
    public Double stockChange;
    // public Double stockPriceChange;

    //Default constructor
    public Stock (){}
    public Stock(String stockName,String stockPrice){
        this.stockName=stockName;
        this.stockPrice=Double.valueOf(stockPrice);
        this.stockChange=Double.valueOf(stockChange);
        // this.stockPriceChange=Double.valueOf(stockPriceChange);
    }

    @Override
    public String toString() {
        return "Stock{" +
               "stockName='" + stockName + '\'' +
               ", stockPrice=" + stockPrice +
               ", stockChange= " + stockChange + 
               '}';
    }
    // public String toString(){
    //     final StringBuilder sb = new StringBuilder("Stock Details{");
    //     sb.append("Stock Name: ").append(stockName).append('\'');
    //     sb.append(", Stock Price: ").append(String.valueOf(stockPrice)).append('\'')
    //     sb.append(", Stock Price Change: ").append(String.valueOf(stockPriceChange)).append('\'')
    //     sb.append('}');
    //     return sb.toString();

    // }

    public int hashCode() {
        return Objects.hash(super.hashCode(), stockName, stockPrice, stockChange);
    }


}
