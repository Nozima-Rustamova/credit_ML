# Frontend (Vite + React)

This is a minimal React frontend that calls the backend mocked external endpoints at:

- `/api/external/soliq/<inn>/`
- `/api/external/kadastr/<parcel_id>/`

Setup (from repository root):

```powershell
cd frontend
npm install
npm run dev
```

By default the Vite config proxies `/api` to `http://127.0.0.1:8000` so run Django devserver in parallel.
