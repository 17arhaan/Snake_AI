<img src="https://www.sify.com/wp-content/uploads/2022/09/snake_game_1200x574.gif">
---

# Snake Game Project

Welcome to the Snake Game Project! This project contains two versions of the Snake game:
1. A **JavaScript (React)** version.
2. A **Python (Pygame)** version.

Both versions are independent of each other and provide different ways to experience the classic Snake game. Below are the steps to set up and run both versions.

---

## JavaScript (React) Version

This version of the game was built using **React**. Follow the instructions below to set it up and run.

### Getting Started

1. Navigate to the `react_version` folder.

   ```bash
   cd react_version
   ```

2. Install the necessary dependencies by running:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to play the game.

### Available Scripts

- **npm start**: Runs the app in development mode.
- **npm run build**: Builds the app for production.

For more details, check the [Create React App Documentation](https://facebook.github.io/create-react-app/docs/getting-started).

---

## Python (Pygame) Version

The Python version of the Snake game uses **Pygame** for the game interface. It includes an AI-based version where the snake is controlled using Q-learning.

### Getting Started

1. Navigate to the `python_version` folder:

   ```bash
   cd python_version
   ```

2. Install the required Python dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Snake game using:

   ```bash
   python SnakePygame.py
   ```

   This will launch the Snake game in a separate window. Control the snake using the arrow keys.

### Q-Learning AI

The AI version of the game uses Q-learning to control the snake. The AI model is stored as a `.pickle` file. The game will load the pre-trained model and run the snake using the AI.

To train your own model, you can implement your Q-learning code and save the Q-table in the `Q_table_results` folder.

### Dependencies

- **Pygame**: Required for the graphical interface.
- **Numpy**: For managing the game's internal state and logic.
- **Pickle**: For loading and saving AI models.

---

## Enhancement Details

- **React Version Enhancements**:
  - Added a live score feature.
  - Implemented movement using both keyboard input and future AI gestures.
  - The game automatically speeds up as you score higher.

- **Python Version Enhancements**:
  - Includes AI-based Q-learning control for the snake.
  - Displays survival time and dynamic scoring.
  - You can run the game manually or let the AI play using the pre-trained model.

---

## How to Play

### React Version
- Control the snake using the arrow keys.
- The goal is to eat food, and each time the snake eats, it grows longer.
- Be careful not to collide with the walls or the snake itself!

### Python Version
- Control the snake using the arrow keys in manual mode.
- For AI mode, the snake will autonomously try to navigate the grid and eat food.
- Avoid collisions with walls or the snake's body.

---

## Contributions

Feel free to contribute to this project by adding more features, fixing bugs, or optimizing the AI model.

---
