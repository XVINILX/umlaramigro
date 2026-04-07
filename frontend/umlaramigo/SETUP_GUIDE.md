# UmlarAmigo - Pet Donation App - Setup Guide

## ✅ What Has Been Created

### 1. **Folder Structure**

```
app/
├── interfaces/                    # TypeScript types based on Pydantic models
│   ├── pet.interface.ts          # Pet types (PetType, PetCreate, PetResponse, etc.)
│   └── interest-form.interface.ts# Interest form types
├── services/                      # API service layer
│   ├── api-client.ts             # Configured Axios instance with auth & error handling
│   ├── pet-service.ts            # PetService class with all API methods
│   └── index.ts                  # Exports
└── routes/
    ├── home.tsx                  # Landing page with link to pets
    └── pets/
        └── index.tsx             # Pet listing page
```

### 2. **Installed Dependencies**

- ✅ `@mui/material` - Material Design components
- ✅ `@mui/icons-material` - Material Design icons
- ✅ `@emotion/react` & `@emotion/styled` - CSS-in-JS
- ✅ `react-hook-form` - Form state management
- ✅ `axios` - HTTP client
- ✅ `react-router` 7 - Client-side routing
- ✅ `typescript` - Type safety

### 3. **Features Implemented**

#### **Interfaces** (`app/interfaces/`)

- `PetType` enum (DOG, CAT)
- `PetBase`, `PetCreate`, `PetUpdate`, `PetResponse`, `PetResponseWithInterests`
- `InterestFormResponse`
- Fully typed based on your Pydantic models

#### **Services** (`app/services/`)

- **API Client**: Axios instance with:
  - Automatic auth token insertion from localStorage
  - 401 error handling (redirects to /login)
  - Configurable base URL via `VITE_API_BASE_URL`
- **Pet Service**: Methods for:
  - `getAllPets()` - List all available pets
  - `getPetsByOrganization(orgId)` - Filter by organization
  - `getPetById(petId)` - Get pet with interest forms
  - `createPet(pet, orgId)` - Create (auth required)
  - `updatePet(petId, petUpdate)` - Update (auth required)
  - `deletePet(petId)` - Delete (auth required)

#### **Pages**

- **Home** (`/`) - Landing page with CTA to view pets
- **Pets Listing** (`/pets`) - Grid of all pets with:
  - Responsive design (mobile-first)
  - Pet name, type (🐕 🐱), description
  - Organization ID and creation date
  - Loading and error states
  - Material UI styling with hover effects

#### **Material UI Integration**

- `ThemeProvider` with custom theme in `root.tsx`
- `CssBaseline` for consistent styling
- Material Design fonts configured
- Icons support for Material Icons

## 🚀 Quick Start

### 1. Configure Environment

```bash
# Create .env.local file
cp .env.example .env.local

# Edit .env.local with your backend URL
VITE_API_BASE_URL=http://localhost:8000/api
```

### 2. Start Development Server

```bash
# From /home/vinicius/umlaramigo/frontend/umlaramigo
yarn dev
```

The app will be available at `http://localhost:5173`

### 3. Access the App

- **Home**: `http://localhost:5173/`
- **Pets List**: `http://localhost:5173/pets`

## 📝 API Integration Notes

### Backend Requirements

Your backend should be running with:

- Base URL: `http://localhost:8000` (or configured via `VITE_API_BASE_URL`)
- Endpoints:
  - `GET /api/pets` → returns `PetResponse[]`
  - `GET /api/pets/{pet_id}` → returns `PetResponseWithInterests`
  - Other endpoints as per your routers

### Authentication

- Store JWT token in `localStorage` key: `access_token`
- It will be automatically added to all requests via `Authorization: Bearer {token}` header
- 401 responses redirect to `/login`

## 🎨 Customization

### Change Theme Colors

Edit `app/root.tsx`:

```typescript
const theme = createTheme({
  palette: {
    primary: { main: "#YOUR_COLOR" },
    secondary: { main: "#YOUR_COLOR" },
  },
});
```

### Update Pet Images

In `app/routes/pets/index.tsx`, replace:

```typescript
image={`https://via.placeholder.com/300x280?text=${pet.name}`}
```

with your actual image URL or use pet image field from API.

### Add More Routes

Update `app/routes.ts`:

```typescript
export default [
  index("routes/home.tsx"),
  route("pets", "routes/pets/index.tsx"),
  route("pets/:id", "routes/pets/detail.tsx"), // Add new route
] satisfies RouteConfig;
```

## 🔧 TypeScript Support

### Environment Variables

`vite-env.d.ts` provides typing for environment variables:

```typescript
import.meta.env.VITE_API_BASE_URL;
```

### Type Checking

```bash
yarn typecheck
```

### Full Type Safety

All API responses are typed via service methods:

```typescript
const pets: PetResponse[] = await petService.getAllPets();
const pet: PetResponseWithInterests = await petService.getPetById(id);
```

## 📚 Project Files Reference

| File                              | Purpose                            |
| --------------------------------- | ---------------------------------- |
| `app/root.tsx`                    | Main layout with Material UI theme |
| `app/routes.ts`                   | Route configuration                |
| `app/routes/home.tsx`             | Landing page                       |
| `app/routes/pets/index.tsx`       | Pet listing page                   |
| `app/interfaces/pet.interface.ts` | Pet types                          |
| `app/services/api-client.ts`      | Axios configuration                |
| `app/services/pet-service.ts`     | Pet API methods                    |
| `vite-env.d.ts`                   | Environment types                  |
| `.env.example`                    | Configuration template             |
| `PETAPP_README.md`                | Detailed documentation             |

## ⚡ Next Steps

1. **Test with Backend**: Ensure your backend API is running and accessible
2. **Update Image URLs**: Replace placeholder images with real URLs from API
3. **Add Authentication**: Implement login/signup pages
4. **Add Pet Detail Page**: Create detailed pet view
5. **Add Filtering**: Filter pets by type, organization, etc.
6. **Add Search**: Implement search functionality
7. **Create Header/Navigation**: Add app navigation bar
8. **Form Implementation**: Use react-hook-form for pet creation/update

## 🐛 Troubleshooting

### CORS Errors

- Ensure backend is running on configured URL
- Check backend CORS configuration

### API Connection Failed

- Verify `VITE_API_BASE_URL` is correct in `.env.local`
- Check backend is running: `curl http://localhost:8000/api/pets`

### Material UI Styles Not Applied

- Verify `ThemeProvider` wraps app in `root.tsx`
- Clear browser cache and reload

### Type Errors

- Run `yarn typecheck` to see all issues
- Ensure imports use full paths: `from '../interfaces'`

## 📞 Support

For detailed information on any component or concept, refer to:

- `PETAPP_README.md` - Comprehensive project documentation
- React Router: https://reactrouter.com/
- Material UI: https://mui.com/
- React Hook Form: https://react-hook-form.com/
