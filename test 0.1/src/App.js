import React, { useState, useEffect } from 'react';
import './App.css';
const SIZE = 20;
const Front = ({ onStart }) => (
  <div className="front">
    <h1>Snake Xenia</h1>
    <button onClick={onStart}>Start</button></div>
);
const GameOver = ({ onRestart, score }) => (
  <div className="game-over">
    <h1>Game Over!</h1>
    <p>Score: {score}</p>
    <button onClick={onRestart}>Restart</button>
  </div>
);
const App = () => {
  const [page, setPage] = useState('front');
  const [grid, setGrid] = useState([]);
  const [snake, setSnake] = useState([{ x: 10, y: 10 }]);
  const [food, setFood] = useState({ x: 15, y: 15 });
  const [direction, setDirection] = useState('RIGHT');
  const [score, setScore] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  useEffect(() => {
    const updateGrid = () => {
      const newGrid = [];
      for (let i = 0; i < SIZE; i++) {
        const row = [];
        for (let j = 0; j < SIZE; j++) {
          row.push(0);
        }
        newGrid.push(row);
      }
      snake.forEach(segment => {
        newGrid[segment.y][segment.x] = 1;
      });
      newGrid[food.y][food.x] = 2;
      setGrid(newGrid);
    };
    updateGrid();
  }, [snake, food]);
  useEffect(() => {
    const interval = setInterval(() => {
      if (!isPaused) moveSnake();
    }, 200);
    return () => clearInterval(interval);
  }, [snake, isPaused]);
  useEffect(() => {
    const handleKeyPress = (event) => {
      switch (event.key) {
        case 'ArrowUp':
          if (direction !== 'DOWN') setDirection('UP');
          break;
        case 'ArrowDown':
          if (direction !== 'UP') setDirection('DOWN');
          break;
        case 'ArrowLeft':
          if (direction !== 'RIGHT') setDirection('LEFT');
          break;
        case 'ArrowRight':
          if (direction !== 'LEFT') setDirection('RIGHT');
          break;
        case 'p':
        case 'P':
          togglePause();
          break;
        default:
          break;
      }
    };
    document.addEventListener('keydown', handleKeyPress);
    return () => {
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, [direction, isPaused]);
  const moveSnake = () => {
    const newSnake = [...snake];
    const head = { ...newSnake[0] };
    switch (direction) {
      case 'UP':
        head.y = (head.y - 1 + SIZE) % SIZE;
        break;
      case 'DOWN':
        head.y = (head.y + 1) % SIZE;
        break;
      case 'LEFT':
        head.x = (head.x - 1 + SIZE) % SIZE;
        break;
      case 'RIGHT':
        head.x = (head.x + 1) % SIZE;
        break;
      default:
        break;
    }
    if (head.x < 0 || head.x >= SIZE || head.y < 0 || head.y >= SIZE) {
      wrapAround(head);
    }
    const collided = newSnake.slice(1).some(segment => segment.x === head.x && segment.y === head.y);
    if (collided) {
      setPage('gameOver');
      return;
    }
    newSnake.unshift(head);
    if (head.x === food.x && head.y === food.y) {
      generateFood();
      setScore(score + 1);
    } else {
      newSnake.pop();
    }
    setSnake(newSnake);
  };
  const wrapAround = (head) => {
    if (head.x < 0) head.x = SIZE - 1;
    if (head.x >= SIZE) head.x = 0;
    if (head.y < 0) head.y = SIZE - 1;
    if (head.y >= SIZE) head.y = 0;
  };
  const generateFood = () => {
    const newFood = {
      x: Math.floor(Math.random() * SIZE),
      y: Math.floor(Math.random() * SIZE)
    };
    setFood(newFood);
  };
  const handleStart = () => {
    setPage('game');
    setScore(0);
  };
  const handleRestart = () => {
    setPage('game');
    setSnake([{ x: 10, y: 10 }]);
    setDirection('RIGHT');
    setScore(0);
    setIsPaused(false);
  };
  const togglePause = () => {
    setIsPaused(!isPaused);
  };
  return (
    <div className="App">
      <div className="game">
        {page === 'front' && <Front onStart={handleStart} />}
        {page === 'gameOver' && <GameOver onRestart={handleRestart} score={score} />}
        {page === 'game' && (
          <>
            <div className="score">Score: {score}</div>
            <button className="pause-button" onClick={togglePause}>
              {isPaused ? 'Resume' : 'Pause'}
            </button>
            <div className="grid">
              {grid.map((row, rowIndex) => (
                <div key={rowIndex} className="row">
                  {row.map((cell, colIndex) => (
                    <div key={colIndex} className={`cell ${cell === 1 ? 'snake' : cell === 2 ? 'food' : ''} ${isPaused && cell === 1 ? 'paused' : ''}`}></div>
                  ))}
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};
export default App;