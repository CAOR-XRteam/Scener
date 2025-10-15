# Scener (3D Scene Generation Platform)

This project provides an open-source interactive system for generating and visualizing 3D objects and scenes.  
It consists of two main components:  

1. **Client (Unity Application)** – User-facing application for interaction, visualization, and 3D rendering.  
2. **Server (Python WebSocket Application)** – Backend managing connections, routing user requests through an agentic AI, and returning structured results (text, JSON descriptions of 3D scenes, binary assets).  

---

## 1. Architecture Overview

                                      User (Text/Voice)
                                             ↓
      Deserialize & Render 3D Scene <── Unity Client ── WebSocket ──> Python Server ──> Agentic AI Pipelines
                                             ↑
                  Text / Structured JSON / Binary Data (from pipelines) <────────────────────────┘


## 2. Client

Detailed documentation is available in the [dedicated repository](https://github.com/CAOR-XRteam/scener_unity).

## 3. Server

Detailed documentation is available in the [dedicated repository](https://github.com/CAOR-XRteam/scener_server).

---

<div align="center">
  <p>
    Developed at the <a href="https://www.caor.minesparis.psl.eu/">Center for Robotics (CAOR), Mines Paris, PSL University</a></strong>
  </p>
  <p>
    <a href="https://creativecommons.org/licenses/by-sa/4.0/">
      <img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-sa.png" alt="CC BY-SA 4.0" width="88" height="31">
    </a>
    <br>
    This project is licensed under the <a href="https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
  </p>
</div>
