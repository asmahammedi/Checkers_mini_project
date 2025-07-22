# 🕹️ Checkers Game – Python OOP Project

This is a full-featured **Checkers game** implemented in Python, showcasing core **Object-Oriented Programming (OOP)** principles: **Encapsulation, Inheritance, Polymorphism,** and **Abstraction**.
It was created as a **group project** for an academic **seminar on OOP applications**.

The game supports **three interfaces**:
- 🖥️ **Command-Line Interface (CLI)** – text-based gameplay  
- 🌐 **REST API** – programmatic control of the game  
- 🎮 **Pygame GUI** – graphical interface with mouse interaction

---

## 🚀 Features

- ✅ Turn-based gameplay
- ♟️ Legal move validation, capturing, and king promotion
- 🔁 Automatic turn switching
- 🧠 Clear OOP structure (Player, Board, Match, Piece, King, Man)
- 🌐 REST API endpoints for programmatic moves
- 🖱️ GUI built with Pygame for interactive play

---

## 🧱 OOP Principles Demonstrated

| OOP Principle | Example |
|---------------|---------|
| **Encapsulation** | Data & methods inside classes like `Player`, using methods to interact with internal state |
| **Inheritance** | `Man` and `King` inherit from base class `Piece` |
| **Polymorphism** | `get_possible_moves()` is overridden in `Man` and `King` |
| **Abstraction** | High-level methods like `make_move()` hide internal game logic |

---


