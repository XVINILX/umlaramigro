import type { Route } from "./+types/home";
import { Container, Box, Typography, Button, Stack } from "@mui/material";
import { Link as RouterLink } from "react-router";
import PetsIcon from "@mui/icons-material/Pets";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "UmlarAmigo - Pet Adoption" },
    {
      name: "description",
      content: "Find your perfect pet companion for adoption",
    },
  ];
}

export default function Home() {
  return (
    <Container maxWidth="md">
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh",
          textAlign: "center",
        }}
      >
        <PetsIcon sx={{ fontSize: 80, color: "primary.main", mb: 2 }} />

        <Typography
          variant="h2"
          component="h1"
          sx={{ fontWeight: "bold", mb: 2 }}
        >
          UmlarAmigo
        </Typography>

        <Typography
          variant="h5"
          color="text.secondary"
          sx={{ mb: 4, maxWidth: 500 }}
        >
          Find your perfect companion for adoption. Give a loving pet a second
          chance at a happy home.
        </Typography>

        <Stack direction="row" spacing={2}>
          <Button
            variant="contained"
            size="large"
            component={RouterLink}
            to="/pets"
            sx={{ px: 4, py: 1.5 }}
          >
            View Available Pets
          </Button>
          <Button variant="outlined" size="large" sx={{ px: 4, py: 1.5 }}>
            Learn More
          </Button>
        </Stack>

        <Box
          sx={{ mt: 8, pt: 4, borderTop: "1px solid #e0e0e0", width: "100%" }}
        >
          <Typography variant="body2" color="text.secondary">
            Find your perfect furry friend today
          </Typography>
        </Box>
      </Box>
    </Container>
  );
}
