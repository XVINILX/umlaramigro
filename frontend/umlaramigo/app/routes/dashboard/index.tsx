// routes/dashboard/index.tsx
import { Box, Grid, Paper, Typography, Card, CardContent } from "@mui/material";
import { useAppSelector } from "~/store/hooks";
import {
  Pets as PetsIcon,
  Favorite as FavoriteIcon,
  People as PeopleIcon,
} from "@mui/icons-material";

export default function DashboardHome() {
  const { user } = useAppSelector((state) => state.auth);
  const { pets } = useAppSelector((state) => state.pets);

  const stats = [
    {
      title: "Total de Pets",
      value: pets.length,
      icon: <PetsIcon sx={{ fontSize: 40, color: "#D4622A" }} />,
      color: "#FFF5E8",
    },
    {
      title: "Adoções Realizadas",
      value: 0,
      icon: <FavoriteIcon sx={{ fontSize: 40, color: "#D4622A" }} />,
      color: "#FFE8E8",
    },
    {
      title: "Visualizações",
      value: 0,
      icon: <PeopleIcon sx={{ fontSize: 40, color: "#D4622A" }} />,
      color: "#E8F5E8",
    },
  ];

  return (
    <Box>
      {/* Welcome Banner */}
      <Paper
        sx={{
          p: 4,
          mb: 4,
          borderRadius: "24px",
          background: "linear-gradient(135deg, #D4622A 0%, #E87E47 100%)",
          color: "#fff",
        }}
      >
        <Typography
          variant="h4"
          sx={{
            fontFamily: "'Fraunces', serif",
            fontWeight: 900,
            mb: 1,
          }}
        >
          Olá, {user?.full_name?.split(" ")[0]}! 👋
        </Typography>
        <Typography
          sx={{
            fontFamily: "'DM Sans', sans-serif",
            opacity: 0.9,
          }}
        >
          Bem-vindo ao seu dashboard. Aqui você pode gerenciar seus pets e
          acompanhar as adoções.
        </Typography>
      </Paper>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card
              sx={{
                borderRadius: "16px",
                background: stat.color,
                transition: "transform 0.2s",
                "&:hover": {
                  transform: "translateY(-4px)",
                },
              }}
            >
              <CardContent>
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <Box>
                    <Typography
                      variant="h3"
                      sx={{
                        fontFamily: "'Fraunces', serif",
                        fontWeight: 900,
                        color: "#5C3D2E",
                      }}
                    >
                      {stat.value}
                    </Typography>
                    <Typography
                      sx={{
                        fontFamily: "'DM Sans', sans-serif",
                        color: "#6B4A3A",
                        mt: 1,
                      }}
                    >
                      {stat.title}
                    </Typography>
                  </Box>
                  {stat.icon}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Recent Activity */}
      <Paper
        sx={{
          p: 3,
          borderRadius: "16px",
          background: "#FFFBF5",
          border: "1px solid rgba(92,61,46,.08)",
        }}
      >
        <Typography
          variant="h6"
          sx={{
            fontFamily: "'Fraunces', serif",
            fontWeight: 700,
            color: "#5C3D2E",
            mb: 2,
          }}
        >
          Atividades Recentes
        </Typography>

        {pets.length === 0 ? (
          <Box sx={{ textAlign: "center", py: 4 }}>
            <Typography sx={{ color: "#8B6555" }}>
              Nenhuma atividade recente. Comece cadastrando um pet!
            </Typography>
          </Box>
        ) : (
          <Box>
            {pets.slice(0, 5).map((pet) => (
              <Box
                key={pet.id}
                sx={{
                  py: 2,
                  borderBottom: "1px solid rgba(92,61,46,.08)",
                  "&:last-child": {
                    borderBottom: "none",
                  },
                }}
              >
                <Typography
                  sx={{ fontFamily: "'DM Sans', sans-serif", color: "#5C3D2E" }}
                >
                  🐾 Pet <strong>{pet.name}</strong> foi cadastrado
                </Typography>
                <Typography
                  sx={{ fontSize: "12px", color: "#8B6555", mt: 0.5 }}
                >
                  {new Date(pet.created_at).toLocaleDateString("pt-BR")}
                </Typography>
              </Box>
            ))}
          </Box>
        )}
      </Paper>
    </Box>
  );
}
