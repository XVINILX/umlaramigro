import { useEffect, useState } from "react";
import {
  Container,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Chip,
} from "@mui/material";
import type { PetResponse } from "../../interfaces";
import { PetType } from "../../interfaces";
import { petService } from "../../services";

export default function PetsListing() {
  const [pets, setPets] = useState<PetResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadPets = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await petService.getAllPets();
        setPets(data);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to load pets";
        setError(message);
        console.error("Error loading pets:", err);
      } finally {
        setLoading(false);
      }
    };

    loadPets();
  }, []);

  const getPetTypeLabel = (petType: PetType): string => {
    return petType === PetType.DOG ? "🐕 Dog" : "🐱 Cat";
  };

  const getPetTypeColor = (
    petType: PetType,
  ):
    | "default"
    | "primary"
    | "secondary"
    | "error"
    | "info"
    | "success"
    | "warning" => {
    return petType === PetType.DOG ? "primary" : "secondary";
  };

  if (loading) {
    return (
      <Container sx={{ display: "flex", justifyContent: "center", py: 8 }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h3"
          component="h1"
          sx={{ fontWeight: "bold", mb: 2 }}
        >
          Available Pets for Adoption
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Find your perfect companion from our list of wonderful pets waiting
          for a home
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      {pets.length === 0 && !error && (
        <Alert severity="info" sx={{ mb: 4 }}>
          No pets available at the moment. Please check back later!
        </Alert>
      )}

      <Grid container spacing={3}>
        {pets.map((pet) => (
          <Grid item xs={12} sm={6} md={4} key={pet.id} component="div">
            <Card
              sx={{
                height: "100%",
                display: "flex",
                flexDirection: "column",
                transition: "transform 0.2s, box-shadow 0.2s",
                "&:hover": {
                  transform: "translateY(-4px)",
                  boxShadow: 4,
                },
              }}
            >
              <CardMedia
                component="img"
                height="280"
                image={`https://via.placeholder.com/300x280?text=${pet.name}`}
                alt={pet.name}
                sx={{ objectFit: "cover" }}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    mb: 1,
                  }}
                >
                  <Typography variant="h6" component="h2">
                    {pet.name}
                  </Typography>
                  <Chip
                    label={getPetTypeLabel(pet.pet_type)}
                    color={getPetTypeColor(pet.pet_type)}
                    size="small"
                    variant="outlined"
                  />
                </Box>

                {pet.description && (
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mb: 2, minHeight: "40px" }}
                  >
                    {pet.description}
                  </Typography>
                )}

                <Box sx={{ mt: 2, pt: 2, borderTop: "1px solid #e0e0e0" }}>
                  <Typography variant="caption" color="text.secondary">
                    Organization ID: {pet.organization_id}
                  </Typography>
                  <br />
                  <Typography variant="caption" color="text.secondary">
                    Added:{" "}
                    {new Date(pet.created_at).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    })}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}
