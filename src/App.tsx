import StockContainer from "./components/StockContainer";

function App() {
  return (
    <main className="main-container">
      <article className="article-container">
        <h1 className="main-title">What is it ?</h1>
        <p className="main-text">
          Stock predictions of different companies for today's closing price.
          Predictions are made with a neural network trained on approximately 10
          years of data.
        </p>
      </article>
      <br />
      <div className="stocks">
        <StockContainer ticker={"AAPL"} />
        <StockContainer ticker={"MSFT"} />
        <StockContainer ticker={"META"} />
        <StockContainer ticker={"NFLX"} />
        <StockContainer ticker={"NVDA"} />
        <StockContainer ticker={"SPY"} />
        <StockContainer ticker={"TSLA"} />
        <StockContainer ticker={"GOOG"} />
        <StockContainer ticker={"AMZN"} />
      </div>
    </main>
  );
}

export default App;
