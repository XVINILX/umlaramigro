# UmlarAmigo - Pet Donation Application

A React + TypeScript application for managing pet donations using React Router, Material UI, and React Hook Form.

## Project Structure

```
app/
├── interfaces/              # TypeScript types/interfaces
│   ├── index.ts
│   ├── pet.interface.ts    # Pet-related types
│   └── interest-form.interface.ts
├── services/               # API service layer
│   ├── index.ts
│   ├── api-client.ts       # Axios instance with interceptors
│   └── pet-service.ts      # Pet API methods
├── routes/
│   ├── home.tsx
│   ├── pets/
│   │   └── index.tsx       # Pet listing page
│   └── welcome/
├── root.tsx                # Root layout with Material UI theme
├── routes.ts               # Route configuration
├── app.css
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd app
yarn install
```

The following packages are already installed:

- **@mui/material**: Material Design components
- **@emotion/react**, **@emotion/styled**: CSS-in-JS styling
- **react-hook-form**: Form state management
- **axios**: HTTP client for API requests
- **react-router**: Client-side routing
- **typescript**: Type safety

### 2. Environment Configuration

Create a `.env.local` file in the project root:

```bash
cp .env.example .env.local
```

Then edit `.env.local` with your API base URL:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 3. Development Server

```bash
yarn dev
```

The application will be available at `http://localhost:5173`

### 4. Type Checking

```bash
yarn typecheck
```

### 5. Build for Production

```bash
yarn build
```

## Architecture

### Interfaces (`app/interfaces/`)

TypeScript types are organized based on the Pydantic models from the backend:

- **PetType**: Enum for dog/cat types
- **PetBase**: Base pet properties (name, type, description)
- **PetCreate**: Pet creation payload
- **PetUpdate**: Pet update payload
- **PetResponse**: Pet data returned from API
- **PetResponseWithInterests**: Pet with associated interest forms

### Services (`app/services/`)

**api-client.ts**

- Axios instance configured with base URL
- Request interceptor for authentication token
- Response interceptor for error handling (401 redirects to login)

**pet-service.ts**

- `getAllPets()`: Fetch all available pets
- `getPetsByOrganization(orgId)`: Fetch pets by organization
- `getPetById(petId)`: Fetch specific pet with interests
- `createPet(pet, orgId)`: Create new pet (requires auth)
- `updatePet(petId, petUpdate)`: Update pet (requires auth)
- `deletePet(petId)`: Delete pet (requires auth)

### Pages

**Pets Listing (`/pets`)**

- Responsive grid layout showing all available pets
- Displays pet name, type, description, organization, and creation date
- Placeholder images (use real image URLs from your API)
- Loading and error states
- Material UI styling with hover effects

## API Integration

The application communicates with the backend API at the endpoint specified in `VITE_API_BASE_URL`:

### Endpoints Used

- `GET /pets` - List all pets
- `GET /pets/{pet_id}` - Get pet details
- `GET /pets/organization/{org_id}` - Get organization pets
- `POST /pets` - Create pet (requires auth)
- `PUT /pets/{pet_id}` - Update pet (requires auth)
- `DELETE /pets/{pet_id}` - Delete pet (requires auth)

## Authentication

The app expects an `access_token` to be stored in `localStorage`. The token will be automatically included in API requests via the request interceptor.

If a 401 response is received, the user is redirected to `/login`.

## Material UI Customization

The theme is configured in [root.tsx](app/root.tsx):

```typescript
const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" },
    secondary: { main: "#dc004e" },
  },
});
```

To customize colors, fonts, or other theme properties, modify the theme configuration.

## Next Steps

1. **Add pet detail page**: Create a route for viewing full pet details
2. **Implement authentication**: Add login/signup pages
3. **Add pet filtering**: Filter by type, organization, etc.
4. **Implement search**: Add search functionality
5. **Add interest form submission**: Allow users to express interest in pets
6. **Upload pet photos**: Integrate image upload functionality
7. **Add responsive navigation**: Create a header/navbar component

## Troubleshooting

### API requests fail with CORS errors

- Ensure the backend is running and the `VITE_API_BASE_URL` is correct
- Check that the backend has CORS headers configured

### TypeScript errors

- Run `yarn typecheck` to see all type errors
- Ensure all types are imported from `app/interfaces`

### Material UI components not styling correctly

- Verify `ThemeProvider` wraps the app in [root.tsx](app/root.tsx)
- Check that `CssBaseline` is included

## Technologies

- **React 19**: UI library
- **React Router 7**: Client-side routing
- **TypeScript 5**: Type safety
- **Material UI 7**: Component library
- **React Hook Form 7**: Form management
- **Axios 1**: HTTP client
- **Vite 8**: Build tool
- **Tailwind CSS 4**: Utility-first CSS (optional, alongside Material UI)
