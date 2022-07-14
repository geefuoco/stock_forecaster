import StockContainer from "./components/StockContainer";

function App() {
  return (
    <main className="main-container">
      <article className="article-container">
        <h1 className="main-title">What is it ?</h1>
        <p className="main-text">
          Stock predictions for stocks for today's closing price. Predictions
          are made with a neural network.
        </p>
      </article>
      <div className="stocks">
        <StockContainer ticker={"AAPL"} />
      </div>
    </main>
  );
}

export default App;
