import { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

const values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"];

function App() {
  const initialDeck = {
    open: null,
    deck: values.map(() => 4),
    failPercent: 0,
    pristine: true,
  };

  const [deck, setDeck] = useState(initialDeck);

  const reveal = (e) => {
    const i = values.indexOf(e);
    if (deck.deck[i] < 0) return; // cannot play any more of this card
    deck.deck[i]--;

    const cardsLower = deck.deck.slice(0, i).reduce((a, b) => a + b, 0);
    const cardsHigher = deck.deck.slice(i + 1).reduce((a, b) => a + b, 0);
    const cardsTotal = deck.deck.reduce((a, b) => a + b);

    // evavu fails if we have a higher card
    const evavuFail = cardsHigher / cardsTotal;
    const tyranuFail = cardsLower / cardsTotal;

    let [bestChoice, failPercent] =
      evavuFail < tyranuFail ? ["Evavu", evavuFail] : ["Tyranu", tyranuFail];

    setDeck({
      open: e,
      deck: deck.deck,
      bestChoice,
      failPercent,
      successPercent: 1 - failPercent,
      pristine: false,
    });
  };

  const reset = () => setDeck(initialDeck);

  const format = (d) => (d * 100).toFixed();

  return (
    <div className="counter">
      {deck.pristine ? (
        "Click the first card to begin"
      ) : (
        <>
          <span>You should pick</span>
          <span className="choice">{deck.bestChoice}</span>
          <span className="odds">
            {format(deck.successPercent)}% chance of success
          </span>
          <span>On top: {deck.open}</span>
        </>
      )}
      <div className="buttons">
        {values.map((e) => (
          <button key={e} onClick={() => reveal(e)}>
            {e}
          </button>
        ))}
      </div>
      <button className="start-over" onClick={reset}>
        Start over
      </button>
      <details>
        <summary>Stats</summary>
        {JSON.stringify(deck, null, 4)}
      </details>
    </div>
  );
}

export default App;
