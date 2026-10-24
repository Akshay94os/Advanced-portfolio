# Advanced Portfolio

A highly functional, robust **Django-based portfolio web application** designed for students and professionals to showcase their academic achievements, technical expertise, and projects while keeping sensitive documents secure.

---

## 🚀 Key Features

*   **Profile Showcase:** Displays a prominent profile photo alongside a concise, impactful professional summary.
*   **Academic & Technical Highlights:** Organized sections for academic details, technical skill matrices, and verified certificates.
*   **Integrated Social Profiles:** Direct connectivity links to GitHub, LinkedIn, Instagram, and other networks.
*   **Project Repository:** Dynamic display of completed works containing direct source code repository links and live deployment previews.
*   **Password-Protected Vault:** High-security, encrypted document storage feature to safekeep confidential files and personal credentials.
*   **Automated Workflows:** Built-in CI/CD pipelines managed via GitHub Actions.

---

## 🛠️ Tech Stack

*   **Backend Framework:** Django (Python)
*   **Frontend:** HTML5, CSS3, JavaScript (Bootstrap/Tailwind)
*   **Database:** SQLite (Development) / PostgreSQL (Production ready)
*   **CI/CD:** GitHub Actions

---

## 📸 Project Interface

Below are snapshots demonstrating the various features, interfaces, and responsive layouts of the project:

### Main Application Views

| Dashboard & Overview | Academic & Profile Setup | Skill Matrix & Social Links |
| :---: | :---: | :---: |
| ![Dashboard](./project%20images/Screenshot%20(326).png) | ![Profile Details](./project%20images/Screenshot%20(327).png) | ![Skills & Certificates](./project%20images/Screenshot%20(328).png) |

### Advanced & High Functionality Features

| Document Storage Vault | Project Links Management | Additional Layout Context |
| :---: | :---: | :---: |
| ![Password Protected Vault](./project%20images/Screenshot%20(329).png) | ![GitHub & Live Previews](./project%20images/Screenshot%20(330).png) | ![Responsive Interface](./project%20images/Screenshot%20(331).png) |

---

## ⚙️ Getting Started

### Prerequisites
*   Python 3.10 or higher installed.
*   Pip package manager.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd Advanced-portfolio
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

2. **Create a superuser account (Admin panel access):**
   ```bash
   python manage.py createsuperuser
   ```

3. **Launch the development server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0`.

---

## 🔒 Security Configuration
To utilize the password-protected document vault safely, ensure your production secret key and environment configurations are set up in a `.env` file rather than hardcoded in `settings.py`.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
