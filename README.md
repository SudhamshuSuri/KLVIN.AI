---

# Dynamic Device Status Web App

A full-stack web application for monitoring and displaying the online/offline status of devices associated with companies. Built with **SvelteKit** for the frontend and **Flask** for the backend, with a **PostgreSQL** database.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Build Instructions](#build-instructions)
    - [Frontend (SvelteKit)](#frontend-sveltekit)
    - [Backend (Flask)](#backend-flask)
4. [Folder Structure](#folder-structure)
5. [Svelte Routing](#svelte-routing)
6. [Backend Functionality](#backend-functionality)
7. [Frontend Functionality](#frontend-functionality)

---

## Project Overview

This application tracks the status of devices and determines whether they are **online** or **offline** based on the latest activity timestamp in the database.  
It features:
- A dynamic UI with company selection and real-time device status updates.
- APIs for fetching companies and devices with their statuses.
- A modular and scalable architecture.

---

## Technologies Used
- **Frontend**: SvelteKit (with TypeScript)
- **Backend**: Flask (with PostgreSQL)
- **Database**: PostgreSQL
- **Styling**: Vanilla CSS

---

## Build Instructions

### Frontend (SvelteKit)
1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Run the Development Server**:
   ```bash
   npm run dev
   ```
   Access the app at [http://localhost:5173](http://localhost:5173).

4. **Build for Production**:
   ```bash
   npm run build
   ```
   This generates a static build in the `build/` directory.

---

### Backend (Flask)
1. **Navigate to the Backend Directory**:
   ```bash
   cd backend
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**:
   ```bash
   python -c "from models import init_db; init_db()"
   ```

5. **Run the Flask Server**:
   ```bash
   python app.py
   ```
   The backend will be available at [http://localhost:5000](http://localhost:5000).

---

## Folder Structure

### Overall Structure
```
device-status/
├── backend/                # Flask backend
│   ├── app.py              # Entry point for the Flask app
│   ├── config.py           # Configuration (e.g., database credentials)
│   ├── models.py           # Database models and queries
│   ├── requirements.txt    # Python dependencies
├── frontend/               # SvelteKit frontend
│   ├── src/
│   │   ├── routes/         # SvelteKit routing logic
│   │   │   ├── +page.svelte   # Main dashboard page
│   │   │   ├── api/        # API routes for the frontend to fetch data
│   │   ├── lib/            # Helper utilities (e.g., API logic)
│   ├── static/             # Static assets (e.g., images, favicon)
│   ├── svelte.config.js    # SvelteKit configuration
│   ├── package.json        # Frontend dependencies
├── README.md               # Project documentation
```

### What Each Folder Does
1. **`backend/`**:
   - Handles API requests from the frontend.
   - Interacts with the PostgreSQL database to fetch company and device data.
   - Contains logic for determining device statuses.

2. **`frontend/`**:
   - Implements the user interface for the app.
   - Fetches data from the backend using RESTful APIs.
   - Uses SvelteKit's file-based routing for navigation.

3. **`src/routes/`**:
   - Handles page routing in SvelteKit.
   - Contains `+page.svelte` for rendering the main dashboard.
   - Contains API route handlers like `api/companies/+server.ts`.

4. **`src/lib/`**:
   - Contains reusable helper utilities like `api.ts` for fetching data.

---

## Svelte Routing

SvelteKit uses **file-based routing**, where the folder structure in `src/routes/` determines the URL paths.

1. **Pages (`+page.svelte`)**:
   - `src/routes/+page.svelte`: Renders the dashboard at `/`.

2. **API Routes (`+server.ts`)**:
   - `src/routes/api/companies/+server.ts`: Handles requests to `/api/companies`.
   - `src/routes/api/devices/+server.ts`: Handles requests to `/api/devices`.

**Dynamic Routing**: The API routes can handle dynamic parameters (e.g., `?companyId=1`) to fetch specific data.

---

## Backend Functionality

The Flask backend provides RESTful APIs to:
1. **Fetch Companies**: `/api/companies`
   - Returns a list of all companies (`id` and `name`).

2. **Fetch Devices for a Company**: `/api/companies/<company_id>/devices`
   - Returns a list of devices belonging to a company along with their statuses (`online`/`offline`).

**How Status is Determined**:
- A device is **online** if its last reading timestamp is within 2 minutes of the current time; otherwise, it's **offline**.

**Database Structure**:
- `companies`: Stores company data.
- `devices`: Stores device data associated with companies.
- `device_readings`: Tracks activity timestamps for devices.

---

## Frontend Functionality

The SvelteKit frontend:
1. **Dropdown for Companies**:
   - Dynamically populated with data from `/api/companies`.

2. **Device Tiles**:
   - Displays each device's name and status in a responsive grid.
   - Status is shown in **green** (online) or **red** (offline).

3. **Automatic Refresh**:
   - Device statuses are refreshed every 10 seconds without reloading the page.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Let me know if you’d like any adjustments to the README or further details! 🚀
