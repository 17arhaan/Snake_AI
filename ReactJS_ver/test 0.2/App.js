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
  const [snake, setSnake] = useState([{ x: WIDTH / 2, y: HEIGHT / 2 }]);
  const [direction, setDirection] = useState(DIRECTIONS[39]);
  const [food, setFood] = useState(getRandomFoodPosition());
  const [speed, setSpeed] = useState(150);
  const [isGameOver, setIsGameOver] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (DIRECTIONS[e.keyCode]) {
        setDirection(DIRECTIONS[e.keyCode]);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    if (isGameOver) return;

    const interval = setInterval(() => {
      moveSnake();
    }, speed);

    return () => clearInterval(interval);
  }, [snake, direction, isGameOver]);

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

  const getRandomFoodPosition = () => {
    const x = Math.floor(Math.random() * (WIDTH / SNAKE_SIZE)) * SNAKE_SIZE;
    const y = Math.floor(Math.random() * (HEIGHT / SNAKE_SIZE)) * SNAKE_SIZE;
    return { x, y };
  };

  const resetGame = () => {
    setSnake([{ x: WIDTH / 2, y: HEIGHT / 2 }]);
    setDirection(DIRECTIONS[39]);
    setFood(getRandomFoodPosition());
    setSpeed(150);
    setIsGameOver(false);
  };

  return (
    <div className="game-container">
      <h1>Snake Game - Nokia Style</h1>
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
    </div>
  );
}

export default App;
