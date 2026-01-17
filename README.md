🚀 AI-Driven Bitcoin Trading Bot
Module E: AI Applications - Individual Open Project

📌 Project Overview
This project implements an automated, high-frequency trading system designed to remove emotional bias from cryptocurrency trading. By utilizing a Hybrid Rule-Based AI with RSI-based confidence scoring, the bot identifies market exhaustion points to execute disciplined "Mean Reversion" trades on the BTC-USD pair.

📂 Repository Structure
AI_Trading_Bot_Submission.ipynb: The Primary Evaluation Artifact containing problem definition, data exploration, system design, and final performance analysis.

day12_integrated_service.py: The core Python "Brain" logic using Flask to process real-time signals.

live_trading_logs.csv: Persistent state management logs used for trade recovery and audit history.

🧠 System Architecture
The system operates through a multi-terminal pipeline to ensure modularity and zero-latency execution:

Heartbeat (Data Ingestion): Streams real-time 1-minute OHLCV data via the Yahoo Finance API.

The Brain (Inference Logic): A Flask API that calculates a dynamic Confidence Score (0-100%) based on RSI momentum.

Audit Dashboard (UI): A live terminal providing real-time PnL monitoring and session summaries.

📊 Key Results
Strategy: Mean Reversion (Buy Oversold / Sell Overbought).

Sample Trade: Successfully captured a cycle from $95,069.17 to $95,259.01.

Performance: Achieved a 0.18% ROI in a single scalping cycle with 100% automated execution.

⚖️ Ethical Considerations & Safety
Risk Management: Includes a 1% Hard Stop-Loss logic to protect capital during "Black Swan" events.

Bias Mitigation: Uses objective mathematical oscillators (RSI) to eliminate human FOMO and panic-selling.

Responsible AI: Designed as a decision-support tool with automated safety protocols.
