// routes/dashboard/pets/index.tsx
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Container,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Alert,
  CircularProgress,
} from "@mui/material";
import { useAppDispatch, useAppSelector } from "~/store/hooks";
import {
  fetchOrganizationPets,
  deletePet,
  clearError,
} from "~/store/slices/petSlice";
import { PetType } from "~/interfaces/pet.interface";
import type { Route } from "./+types/index";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Meus Pets | Um Lar Amigo" },
    {
      name: "description",
      content: "Gerencie seus pets cadastrados",
    },
  ];
}

export default function PetsListPage() {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { pets, isLoading, error } = useAppSelector((state) => state.pets);
  const { user } = useAppSelector((state) => state.auth);

  useEffect(() => {
    if (user?.organization_id) {
      dispatch(fetchOrganizationPets(user.organization_id));
    }
  }, [dispatch, user]);

  const handleDelete = async (id: string) => {
    if (window.confirm("Tem certeza que deseja remover este pet?")) {
      await dispatch(deletePet(id));
    }
  };

  const getPetIcon = (type: PetType) => {
    return type === PetType.DOG ? "🐕" : "🐱";
  };

  const getPetTypeLabel = (type: PetType) => {
    return type === PetType.DOG ? "Cão" : "Gato";
  };

  if (isLoading && pets.length === 0) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "400px",
        }}
      >
        <CircularProgress sx={{ color: "#D4622A" }} />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper
        elevation={0}
        sx={{
          p: 4,
          borderRadius: "24px",
          background: "#FFFBF5",
          border: "1px solid rgba(92,61,46,.08)",
        }}
      >
        {/* Header */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mb: 4,
          }}
        >
          <Box>
            <Typography
              variant="h4"
              component="h1"
              sx={{
                fontFamily: "'Fraunces', serif",
                fontWeight: 900,
                color: "#5C3D2E",
                mb: 1,
              }}
            >
              Meus Pets 🐾
            </Typography>
            <Typography
              sx={{
                color: "#6B4A3A",
                fontFamily: "'DM Sans', sans-serif",
              }}
            >
              Gerencie os pets cadastrados para adoção
            </Typography>
          </Box>

          <Button
            variant="contained"
            onClick={() => navigate("/dashboard/pets/novo")}
            sx={{
              background: "#D4622A",
              fontFamily: "'DM Sans', sans-serif",
              borderRadius: "100px",
              padding: "10px 24px",
              "&:hover": {
                background: "#E87E47",
              },
            }}
          >
            + Novo Pet
          </Button>
        </Box>

        {/* Error Message */}
        {error && (
          <Alert
            severity="error"
            sx={{ mb: 3, borderRadius: "12px" }}
            onClose={() => dispatch(clearError())}
          >
            {error}
          </Alert>
        )}

        {/* Pets Grid */}
        {pets.length === 0 ? (
          <Box
            sx={{
              textAlign: "center",
              py: 8,
              px: 4,
              background: "rgba(92,61,46,.02)",
              borderRadius: "16px",
            }}
          >
            <Typography
              variant="h6"
              sx={{
                fontFamily: "'Fraunces', serif",
                color: "#8B6555",
                mb: 2,
              }}
            >
              Nenhum pet cadastrado ainda
            </Typography>
            <Typography
              sx={{
                color: "#6B4A3A",
                mb: 3,
                fontFamily: "'DM Sans', sans-serif",
              }}
            >
              Comece cadastrando seu primeiro pet para adoção
            </Typography>
            <Button
              variant="contained"
              onClick={() => navigate("/dashboard/pets/novo")}
              sx={{
                background: "#D4622A",
                borderRadius: "100px",
                "&:hover": {
                  background: "#E87E47",
                },
              }}
            >
              Cadastrar primeiro pet
            </Button>
          </Box>
        ) : (
          <Grid container spacing={3}>
            {pets.map((pet) => (
              <Grid item xs={12} sm={6} md={4} key={pet.id}>
                <Card
                  sx={{
                    borderRadius: "16px",
                    transition: "transform 0.2s, box-shadow 0.2s",
                    "&:hover": {
                      transform: "translateY(-4px)",
                      boxShadow: "0 8px 24px rgba(44,24,16,.12)",
                    },
                  }}
                >
                  <CardContent>
                    <Box
                      sx={{
                        display: "flex",
                        alignItems: "center",
                        gap: 1,
                        mb: 2,
                      }}
                    >
                      <Typography sx={{ fontSize: "32px" }}>
                        {getPetIcon(pet.pet_type)}
                      </Typography>
                      <Typography
                        variant="h6"
                        sx={{
                          fontFamily: "'Fraunces', serif",
                          fontWeight: 700,
                          color: "#5C3D2E",
                          flex: 1,
                        }}
                      >
                        {pet.name}
                      </Typography>
                      <Chip
                        label={getPetTypeLabel(pet.pet_type)}
                        size="small"
                        sx={{
                          background:
                            pet.pet_type === PetType.DOG
                              ? "#c5e0d4"
                              : "#d4c5e8",
                          color: "#5C3D2E",
                          fontWeight: 500,
                        }}
                      />
                    </Box>

                    <Typography
                      sx={{
                        color: "#6B4A3A",
                        fontSize: "14px",
                        mb: 2,
                        fontFamily: "'DM Sans', sans-serif",
                        display: "-webkit-box",
                        WebkitLineClamp: 3,
                        WebkitBoxOrient: "vertical",
                        overflow: "hidden",
                      }}
                    >
                      {pet.description || "Sem descrição cadastrada"}
                    </Typography>

                    <Typography
                      sx={{
                        color: "#8B6555",
                        fontSize: "12px",
                        fontFamily: "'DM Sans', sans-serif",
                      }}
                    >
                      Cadastrado em:{" "}
                      {new Date(pet.created_at).toLocaleDateString("pt-BR")}
                    </Typography>
                  </CardContent>

                  <CardActions sx={{ padding: "16px", pt: 0, gap: 1 }}>
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() =>
                        navigate(`/dashboard/pets/${pet.id}/editar`)
                      }
                      sx={{
                        flex: 1,
                        borderRadius: "100px",
                        fontFamily: "'DM Sans', sans-serif",
                        borderColor: "#8B6555",
                        color: "#5C3D2E",
                        "&:hover": {
                          borderColor: "#D4622A",
                          background: "rgba(92,61,46,.05)",
                        },
                      }}
                    >
                      Editar
                    </Button>
                    <Button
                      size="small"
                      variant="outlined"
                      color="error"
                      onClick={() => handleDelete(pet.id)}
                      sx={{
                        flex: 1,
                        borderRadius: "100px",
                        fontFamily: "'DM Sans', sans-serif",
                      }}
                    >
                      Remover
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Paper>
    </Container>
  );
}
