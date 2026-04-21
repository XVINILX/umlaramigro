// routes/dashboard/layout.tsx
import { useState } from "react";
import { Outlet, useNavigate, useLocation } from "react-router-dom";
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Typography,
  Avatar,
  Menu,
  MenuItem,
  Divider,
  useTheme,
  useMediaQuery,
  Collapse,
  Button,
} from "@mui/material";
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Pets as PetsIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
  ExpandLess,
  ExpandMore,
  Favorite as FavoriteIcon,
  Home as HomeIcon,
} from "@mui/icons-material";
import { useAppDispatch, useAppSelector } from "~/store/hooks";
import { logout } from "~/store/slices/authSlice";

const DRAWER_WIDTH = 280;
const COLLAPSED_DRAWER_WIDTH = 80;

export default function DashboardLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useAppDispatch();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  const { user } = useAppSelector((state) => state.auth);

  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [petsOpen, setPetsOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = async () => {
    await dispatch(logout());
    navigate("/login");
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      setMobileOpen(false);
    }
  };

  const menuItems = [
    { text: "Dashboard", icon: <DashboardIcon />, path: "/dashboard" },
    {
      text: "Pets",
      icon: <PetsIcon />,
      path: "/dashboard/pets",
      subItems: [
        { text: "Meus Pets", path: "/dashboard/pets" },
        { text: "Novo Pet", path: "/dashboard/pets/novo" },
      ],
    },
    { text: "Favoritos", icon: <FavoriteIcon />, path: "/dashboard/favoritos" },
    { text: "Perfil", icon: <PersonIcon />, path: "/dashboard/perfil" },
    {
      text: "Configurações",
      icon: <SettingsIcon />,
      path: "/dashboard/configuracoes",
    },
  ];

  const drawerContent = (
    <Box sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
      {/* Logo */}
      <Box
        sx={{
          p: 3,
          display: "flex",
          alignItems: "center",
          justifyContent: sidebarCollapsed ? "center" : "flex-start",
          gap: 2,
          borderBottom: "1px solid rgba(92,61,46,.1)",
        }}
      >
        <img
          src="https://umlaramigo-homolog.s3.us-east-1.amazonaws.com/logo_um_lar_amigo.png"
          alt="Um Lar Amigo"
          style={{ height: "40px" }}
        />
        {!sidebarCollapsed && (
          <Typography
            variant="h6"
            sx={{
              fontFamily: "'Fraunces', serif",
              fontWeight: 700,
              color: "#5C3D2E",
            }}
          >
            Um Lar Amigo
          </Typography>
        )}
      </Box>

      {/* Menu */}
      <List sx={{ flex: 1, px: 2, py: 2 }}>
        {menuItems.map((item) => (
          <Box key={item.text}>
            {item.subItems ? (
              <>
                <ListItem disablePadding>
                  <ListItemButton
                    onClick={() => setPetsOpen(!petsOpen)}
                    sx={{
                      borderRadius: "12px",
                      mb: 0.5,
                      justifyContent: sidebarCollapsed
                        ? "center"
                        : "flex-start",
                      px: sidebarCollapsed ? 0 : 2,
                      "&:hover": {
                        background: "rgba(212,98,42,.08)",
                      },
                    }}
                  >
                    <ListItemIcon sx={{ minWidth: sidebarCollapsed ? 0 : 40 }}>
                      {item.icon}
                    </ListItemIcon>
                    {!sidebarCollapsed && (
                      <>
                        <ListItemText
                          primary={item.text}
                          primaryTypographyProps={{
                            sx: { fontFamily: "'DM Sans', sans-serif" },
                          }}
                        />
                        {petsOpen ? <ExpandLess /> : <ExpandMore />}
                      </>
                    )}
                  </ListItemButton>
                </ListItem>
                <Collapse
                  in={petsOpen && !sidebarCollapsed}
                  timeout="auto"
                  unmountOnExit
                >
                  <List component="div" disablePadding>
                    {item.subItems.map((subItem) => (
                      <ListItemButton
                        key={subItem.text}
                        onClick={() => handleNavigation(subItem.path)}
                        selected={location.pathname === subItem.path}
                        sx={{
                          pl: 4,
                          borderRadius: "12px",
                          mb: 0.5,
                          "&.Mui-selected": {
                            background: "#D4622A",
                            color: "#fff",
                            "&:hover": {
                              background: "#E87E47",
                            },
                            "& .MuiListItemIcon-root": {
                              color: "#fff",
                            },
                          },
                          "&:hover": {
                            background: "rgba(212,98,42,.08)",
                          },
                        }}
                      >
                        <ListItemText
                          primary={subItem.text}
                          primaryTypographyProps={{
                            sx: {
                              fontFamily: "'DM Sans', sans-serif",
                              fontSize: "14px",
                            },
                          }}
                        />
                      </ListItemButton>
                    ))}
                  </List>
                </Collapse>
              </>
            ) : (
              <ListItem disablePadding>
                <ListItemButton
                  onClick={() => handleNavigation(item.path)}
                  selected={location.pathname === item.path}
                  sx={{
                    borderRadius: "12px",
                    mb: 0.5,
                    justifyContent: sidebarCollapsed ? "center" : "flex-start",
                    px: sidebarCollapsed ? 0 : 2,
                    "&.Mui-selected": {
                      background: "#D4622A",
                      color: "#fff",
                      "&:hover": {
                        background: "#E87E47",
                      },
                      "& .MuiListItemIcon-root": {
                        color: "#fff",
                      },
                    },
                    "&:hover": {
                      background: "rgba(212,98,42,.08)",
                    },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: sidebarCollapsed ? 0 : 40 }}>
                    {item.icon}
                  </ListItemIcon>
                  {!sidebarCollapsed && (
                    <ListItemText
                      primary={item.text}
                      primaryTypographyProps={{
                        sx: { fontFamily: "'DM Sans', sans-serif" },
                      }}
                    />
                  )}
                </ListItemButton>
              </ListItem>
            )}
          </Box>
        ))}
      </List>

      {/* Footer do menu */}
      <Box sx={{ p: 2, borderTop: "1px solid rgba(92,61,46,.1)" }}>
        <ListItem disablePadding>
          <ListItemButton
            onClick={handleLogout}
            sx={{
              borderRadius: "12px",
              justifyContent: sidebarCollapsed ? "center" : "flex-start",
              px: sidebarCollapsed ? 0 : 2,
              "&:hover": {
                background: "rgba(212,98,42,.08)",
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: sidebarCollapsed ? 0 : 40 }}>
              <LogoutIcon />
            </ListItemIcon>
            {!sidebarCollapsed && (
              <ListItemText
                primary="Sair"
                primaryTypographyProps={{
                  sx: { fontFamily: "'DM Sans', sans-serif" },
                }}
              />
            )}
          </ListItemButton>
        </ListItem>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: "flex", bgcolor: "#FDF6EC", minHeight: "100vh" }}>
      {/* App Bar (Mobile) */}
      <AppBar
        position="fixed"
        sx={{
          display: { xs: "block", md: "none" },
          background: "rgba(253, 246, 236, 0.95)",
          backdropFilter: "blur(12px)",
          boxShadow: "none",
          borderBottom: "1px solid rgba(92,61,46,.1)",
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ color: "#5C3D2E" }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            sx={{
              flex: 1,
              fontFamily: "'Fraunces', serif",
              color: "#5C3D2E",
            }}
          >
            Um Lar Amigo
          </Typography>
          <IconButton onClick={handleMenuOpen} sx={{ color: "#5C3D2E" }}>
            <Avatar
              sx={{
                bgcolor: "#D4622A",
                width: 32,
                height: 32,
                fontFamily: "'DM Sans', sans-serif",
              }}
            >
              {user?.full_name?.charAt(0).toUpperCase() || "U"}
            </Avatar>
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* Drawer Desktop */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", md: "block" },
          width: sidebarCollapsed ? COLLAPSED_DRAWER_WIDTH : DRAWER_WIDTH,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: sidebarCollapsed ? COLLAPSED_DRAWER_WIDTH : DRAWER_WIDTH,
            boxSizing: "border-box",
            background: "#FFFBF5",
            borderRight: "1px solid rgba(92,61,46,.1)",
            transition: "width 0.2s",
          },
        }}
        open
      >
        {drawerContent}
      </Drawer>

      {/* Drawer Mobile */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: "block", md: "none" },
          "& .MuiDrawer-paper": {
            width: DRAWER_WIDTH,
            background: "#FFFBF5",
          },
        }}
      >
        {drawerContent}
      </Drawer>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: { xs: 2, sm: 3, md: 4 },
          width: {
            xs: "100%",
            md: `calc(100% - ${sidebarCollapsed ? COLLAPSED_DRAWER_WIDTH : DRAWER_WIDTH}px)`,
          },
          mt: { xs: "64px", md: 0 },
        }}
      >
        {/* Header Desktop */}
        <Box
          sx={{
            display: { xs: "none", md: "flex" },
            justifyContent: "flex-end",
            alignItems: "center",
            mb: 3,
            pb: 2,
            borderBottom: "1px solid rgba(92,61,46,.1)",
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
            <IconButton
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              sx={{ color: "#8B6555" }}
            >
              <MenuIcon />
            </IconButton>

            <Button
              onClick={handleMenuOpen}
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 1,
                textTransform: "none",
                color: "#5C3D2E",
              }}
            >
              <Avatar
                sx={{
                  bgcolor: "#D4622A",
                  width: 36,
                  height: 36,
                  fontFamily: "'DM Sans', sans-serif",
                }}
              >
                {user?.full_name?.charAt(0).toUpperCase() || "U"}
              </Avatar>
              <Box sx={{ textAlign: "left" }}>
                <Typography
                  sx={{
                    fontFamily: "'DM Sans', sans-serif",
                    fontWeight: 600,
                    fontSize: "14px",
                  }}
                >
                  {user?.full_name || "Usuário"}
                </Typography>
              </Box>
            </Button>
          </Box>
        </Box>

        {/* User Menu */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          transformOrigin={{ horizontal: "right", vertical: "top" }}
          anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
          PaperProps={{
            sx: {
              mt: 1,
              borderRadius: "12px",
              minWidth: 200,
              background: "#FFFBF5",
              boxShadow: "0 4px 24px rgba(44,24,16,.12)",
            },
          }}
        >
          <MenuItem
            onClick={() => {
              handleMenuClose();
              navigate("/dashboard/perfil");
            }}
          >
            <ListItemIcon>
              <PersonIcon fontSize="small" sx={{ color: "#D4622A" }} />
            </ListItemIcon>
            <ListItemText>Meu Perfil</ListItemText>
          </MenuItem>
          <MenuItem
            onClick={() => {
              handleMenuClose();
              navigate("/dashboard/configuracoes");
            }}
          >
            <ListItemIcon>
              <SettingsIcon fontSize="small" sx={{ color: "#D4622A" }} />
            </ListItemIcon>
            <ListItemText>Configurações</ListItemText>
          </MenuItem>
          <Divider />
          <MenuItem onClick={handleLogout}>
            <ListItemIcon>
              <LogoutIcon fontSize="small" sx={{ color: "#D4622A" }} />
            </ListItemIcon>
            <ListItemText>Sair</ListItemText>
          </MenuItem>
        </Menu>

        {/* Page Content */}
        <Outlet />
      </Box>
    </Box>
  );
}
