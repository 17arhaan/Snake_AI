import React, { useState, useEffect } from 'react';
import './App.css';

const SNAKE_SIZE = 10;
const WIDTH = 600;
const HEIGHT = 400;
const DIRECTIONS = {
  37: { x: -SNAKE_SIZE, y: 0 },  // Left
  38: { x: 0, y: -SNAKE_SIZE },  // Up
  39: { x: SNAKE_SIZE, y: 0 },   // Right
  40: { x: 0, y: SNAKE_SIZE }    // Down
};

function App() {
  const [webcamFeed, setWebcamFeed] = useState(null); // State for webcam feed
  const [snake, setSnake] = useState([{ x: WIDTH / 2, y: HEIGHT / 2 }]);
  const [direction, setDirection] = useState(DIRECTIONS[39]);
  const [food, setFood] = useState(getRandomFoodPosition());
  const [speed, setSpeed] = useState(150);
  const [isGameOver, setIsGameOver] = useState(false);
  const [score, setScore] = useState(0); // State for score

  // Handle keypress to change direction
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (DIRECTIONS[e.keyCode]) {
        setDirection(DIRECTIONS[e.keyCode]);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Move the snake at intervals
  useEffect(() => {
    if (isGameOver) return;
    const interval = setInterval(() => {
      moveSnake();
    }, speed);
    return () => clearInterval(interval);
  }, [snake, direction, isGameOver]);

  // Connect to WebSocket for webcam feed (optional, replace with real feed)
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000');
    ws.onmessage = (event) => {
      setWebcamFeed(event.data); // Assuming base64 image is sent via WebSocket
    };
    return () => ws.close();
  }, []);

  const moveSnake = () => {
    const newSnake = [...snake];
    const head = {
      x: newSnake[0].x + direction.x,
      y: newSnake[0].y + direction.y
    };

    // Check if the snake hits the wall or itself
    if (
      head.x >= WIDTH || head.x < 0 ||
      head.y >= HEIGHT || head.y < 0 ||
      isCollision(newSnake, head)
    ) {
      setIsGameOver(true);
      return;
    }

    newSnake.unshift(head);

    // Check if the snake eats the food
    if (head.x === food.x && head.y === food.y) {
      setFood(getRandomFoodPosition());
      setSpeed(speed => Math.max(50, speed - 10)); // Speed up the game
      setScore(score + 10); // Increment score
    } else {
      newSnake.pop();
    }

    setSnake(newSnake);
  };

  const isCollision = (snake, head) => {
    for (let i = 1; i < snake.length; i++) {
      if (snake[i].x === head.x && snake[i].y === head.y) {
        return true;
      }
    }
    return false;
  };

  const resetGame = () => {
    setSnake([{ x: WIDTH / 2, y: HEIGHT / 2 }]);
    setDirection(DIRECTIONS[39]);
    setFood(getRandomFoodPosition());
    setSpeed(150);
    setIsGameOver(false);
    setScore(0); // Reset score
  };

  return (
    <div className="game-container">
      <h1>Snake Game - Nokia Style</h1>
      <div className="score">Score: {score}</div> {/* Display score */}
      <div className="game-area">
        {snake.map((segment, index) => (
          <div
            key={index}
            className="snake-segment"
            style={{ top: segment.y, left: segment.x }}
          ></div>
        ))}
        <div
          className="food"
          style={{ top: food.y, left: food.x }}
        ></div>
        {isGameOver && (
          <div className="game-over">
            <h2>Game Over</h2>
            <button onClick={resetGame}>Play Again</button>
          </div>
        )}
      </div>
      <div className="webcam-feed">
        <h2>Webcam Feed</h2>
        {webcamFeed && (
          <img
            src={`data:image/jpeg;base64,${webcamFeed}`}
            alt="webcam"
          />
        )}
      </div>
    </div>
  );
}

// Function to get a random food position
const getRandomFoodPosition = () => {
  const x = Math.floor(Math.random() * (WIDTH / SNAKE_SIZE)) * SNAKE_SIZE;
  const y = Math.floor(Math.random() * (HEIGHT / SNAKE_SIZE)) * SNAKE_SIZE;
  return { x, y };
};

export default App;
