// routes/login.tsx
import { useState } from "react";
import { useForm } from "react-hook-form";
import {
  Box,
  Container,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  CircularProgress,
  Divider,
  IconButton,
  InputAdornment,
  FormHelperText,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "~/store/hooks";
import { login, register } from "~/store/slices/authSlice";
import type { Route } from "./+types/login";

// Interfaces
interface UserLoginForm {
  email: string;
  password: string;
}

interface UserRegisterForm {
  full_name: string;
  email: string;
  password: string;
  confirmPassword: string;
  user_type: string;
}

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Login | Um Lar Amigo" },
    {
      name: "description",
      content:
        "Faça login ou registre-se para adotar um pet ou cadastrar sua ONG.",
    },
  ];
}

export default function LoginPage() {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { isLoading, error } = useAppSelector((state) => state.auth);
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Login form
  const {
    register: registerLogin,
    handleSubmit: handleLoginSubmit,
    formState: { errors: loginErrors },
  } = useForm<UserLoginForm>();

  // Register form
  const {
    register: registerRegister,
    handleSubmit: handleRegisterSubmit,
    formState: { errors: registerErrors },
    watch,
    setError,
    clearErrors,
  } = useForm<UserRegisterForm>({
    defaultValues: {
      full_name: "",
      email: "",
      password: "",
      confirmPassword: "",
      user_type: "adotante",
    },
  });

  const watchPassword = watch("password");

  const onLoginSubmit = async (data: UserLoginForm) => {
    const result = await dispatch(login(data));
    if (login.fulfilled.match(result)) {
      navigate("/dashboard");
    }
  };

  const onRegisterSubmit = async (data: UserRegisterForm) => {
    // Validação adicional
    if (data.password !== data.confirmPassword) {
      setError("confirmPassword", {
        type: "manual",
        message: "As senhas não coincidem",
      });
      return;
    }

    const { confirmPassword, ...registerData } = data;
    const result = await dispatch(register(registerData));

    if (register.fulfilled.match(result)) {
      navigate("/dashboard");
    }
  };

  return (
    <Container
      sx={{
        backgroundColor: "#FDF6EC",
        padding: "0px",
        minHeight: "100vh",
        minWidth: "100vw",
        display: 'flex',
        flexDirection: "column"
      }}
      style={{ padding: "0px !important" }}
    >
      {/* NAV */}
      <Box
        component="nav"
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "18px 48px",
          background: "rgba(253, 246, 236, 0.88)",
          backdropFilter: "blur(12px)",
          borderBottom: "1px solid rgba(92,61,46,.1)",
          flexShrink: 0, 
          height: "80px"
        }}
      >
        <img
          src="https://umlaramigo-homolog.s3.us-east-1.amazonaws.com/logo_um_lar_amigo.png"
          alt="Um Lar Amigo"
          style={{ height: "44px", cursor: "pointer" }}
          onClick={() => navigate("/")}
        />
        <Button
          onClick={() => navigate("/")}
          sx={{
            fontFamily: "'DM Sans', sans-serif",
            fontWeight: 500,
            fontSize: "14px",
            letterSpacing: ".04em",
            color: "#5C3D2E",
            border: "1.5px solid #8B6555",
            background: "transparent",
            padding: "10px 24px",
            borderRadius: "100px",
            "&:hover": {
              background: "rgba(92,61,46,.06)",
            },
          }}
        >
          Voltar para Home
        </Button>
      </Box>

      {/* FORM SECTION */}
      <Box
        component="section"
        sx={{
          flex:1,
          display: "flex",
          flexDirection: "row",
          backgroundColor: "#FDF6EC",
          justifyContent: "space-between",
          boxSizing: "border-box",
          minHeight: "calc(100vh - 80px)",
          alignItems: "stretch",
        }}
      >
        <div 
          style={{
            display: 'flex', 
            width: "50%", 
            flexDirection: "column", // ← mudado de "row" para "column"
            justifyContent: "flex-end", // ← alinha a imagem no final
            alignItems: "center",
            height: 'calc(100vh - 80px)', // ← Agora vai funcionar porque o pai tem altura definida
          }}
        >
          <img
            style={{ maxWidth: "50%", maxHeight: "450px" }}
            src="8634007.png"
          />
        </div>
        <Box
          sx={{
            width: "50%",
            overflowY: "auto",
            height: 'calc(100vh - 80px)',
            alignItems: "center",
            display: "flex"
          }}
          style={{height: "100%"}}
        >
          <div
            style={{
              overflowY: "auto",
              maxHeight: '80vh',
              width: "80%",
              background: "#FFFBF5",
              borderRadius: "32px",
              padding: "20px",
              display: "flex",
              flexDirection: "column",
              boxShadow: "0 4px 24px rgba(44,24,16,.08)",
              border: "1px solid rgba(92,61,46,.08)",
            }}
          >
            {/* Header */}
            <Box sx={{ textAlign: "center", marginBottom: "10px" }}>
              <h1
                style={{
                  fontFamily: "'Fraunces', serif",
                  fontSize: "clamp(32px, 5vw, 48px)",
                  fontWeight: 900,
                  color: "#5C3D2E",
                  marginBottom: "4px",
                }}
              >
                {isLogin ? "Boas-vindas" : "Criar conta"}
              </h1>
              <p
                style={{
                  fontSize: "16px",
                  color: "#6B4A3A",
                  fontWeight: 300,
                }}
              >
                {isLogin
                  ? "Entre para encontrar seu novo melhor amigo"
                  : "Junte-se a nós e faça a diferença"}
              </p>
            </Box>

            {/* Error Message */}
            {error && (
              <Alert
                severity="error"
                sx={{
                  marginBottom: "24px",
                  borderRadius: "12px",
                  "& .MuiAlert-message": {
                    fontFamily: "'DM Sans', sans-serif",
                  },
                }}
              >
                {error}
              </Alert>
            )}

            {/* Login Form */}
            {isLogin && (
              <form onSubmit={handleLoginSubmit(onLoginSubmit)}>
                <TextField
                  fullWidth
                  label="E-mail"
                  type="email"
                  {...registerLogin("email", {
                    required: "E-mail é obrigatório",
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: "E-mail inválido",
                    },
                  })}
                  error={!!loginErrors.email}
                  helperText={loginErrors.email?.message}
                  sx={{
                    marginBottom: "20px",
                    "& .MuiOutlinedInput-root": {
                      borderRadius: "12px",
                      fontFamily: "'DM Sans', sans-serif",
                      "&:hover fieldset": {
                        borderColor: "#D4622A",
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: "#D4622A",
                      },
                    },
                    "& .MuiInputLabel-root": {
                      fontFamily: "'DM Sans', sans-serif",
                      color: "#8B6555",
                      "&.Mui-focused": {
                        color: "#D4622A",
                      },
                    },
                  }}
                />

                <TextField
                  fullWidth
                  label="Senha"
                  type={showPassword ? "text" : "password"}
                  {...registerLogin("password", {
                    required: "Senha é obrigatória",
                    minLength: {
                      value: 6,
                      message: "Senha deve ter no mínimo 6 caracteres",
                    },
                  })}
                  error={!!loginErrors.password}
                  helperText={loginErrors.password?.message}
                  sx={{
                    marginBottom: "28px",
                    "& .MuiOutlinedInput-root": {
                      borderRadius: "12px",
                      fontFamily: "'DM Sans', sans-serif",
                      "&:hover fieldset": {
                        borderColor: "#D4622A",
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: "#D4622A",
                      },
                    },
                    "& .MuiInputLabel-root": {
                      fontFamily: "'DM Sans', sans-serif",
                      color: "#8B6555",
                      "&.Mui-focused": {
                        color: "#D4622A",
                      },
                    },
                  }}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={() => setShowPassword(!showPassword)}
                          edge="end"
                          sx={{ color: "#8B6555" }}
                        >
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />

                <Button
                  type="submit"
                  fullWidth
                  disabled={isLoading}
                  sx={{
                    background: "#D4622A",
                    color: "#fff",
                    fontFamily: "'DM Sans', sans-serif",
                    fontSize: "16px",
                    fontWeight: 600,
                    padding: "14px",
                    borderRadius: "100px",
                    transition: "all .2s",
                    boxShadow: "0 8px 32px rgba(212,98,42,.3)",
                    "&:hover": {
                      background: "#E87E47",
                      transform: "translateY(-2px)",
                    },
                    "&:disabled": {
                      background: "#D4622A",
                      opacity: 0.7,
                    },
                  }}
                >
                  {isLoading ? (
                    <CircularProgress size={24} sx={{ color: "#fff" }} />
                  ) : (
                    "Entrar 🐾"
                  )}
                </Button>
              </form>
            )}

            {/* Register Form */}
            {!isLogin && (
              <form onSubmit={handleRegisterSubmit(onRegisterSubmit)}>
                <TextField
                  fullWidth
                  label="Nome completo"
                  {...registerRegister("full_name", {
                    required: "Nome completo é obrigatório",
                    minLength: {
                      value: 3,
                      message: "Nome deve ter no mínimo 3 caracteres",
                    },
                  })}
                  error={!!registerErrors.full_name}
                  helperText={registerErrors.full_name?.message}
                  sx={{
                    marginBottom: "20px",
                    "& .MuiOutlinedInput-root": {
                      borderRadius: "12px",
                      fontFamily: "'DM Sans', sans-serif",
                      "&:hover fieldset": {
                        borderColor: "#D4622A",
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: "#D4622A",
                      },
                    },
                    "& .MuiInputLabel-root": {
                      fontFamily: "'DM Sans', sans-serif",
                      color: "#8B6555",
                      "&.Mui-focused": {
                        color: "#D4622A",
                      },
                    },
                  }}
                />

              <TextField
                fullWidth
                label="Nome do abrigo/organização"
                {...registerRegister("organization_name", {
                  required: "Nome do abrigo é obrigatório para ONGs e protetores",
                  minLength: {
                    value: 3,
                    message: "Nome deve ter no mínimo 3 caracteres",
                  },
                })}
                error={!!registerErrors.organization_name}
                helperText={registerErrors.organization_name?.message} sx={{
                  marginBottom: "20px",
                  "& .MuiOutlinedInput-root": {
                    borderRadius: "12px",
                    fontFamily: "'DM Sans', sans-serif",
                    "&:hover fieldset": {
                      borderColor: "#D4622A",
                    },
                    "&.Mui-focused fieldset": {
                      borderColor: "#D4622A",
                    },
                  },
                  "& .MuiInputLabel-root": {
                    fontFamily: "'DM Sans', sans-serif",
                    color: "#8B6555",
                    "&.Mui-focused": {
                      color: "#D4622A",
                    },
                  },
                }}
              />

               <TextField
          fullWidth
          label="Descrição do abrigo"
          multiline
          rows={3}
          {...registerRegister("organization_description")}
          placeholder="Conte um pouco sobre o abrigo, sua missão, quantos animais acolhe, etc."
          sx={{
            marginBottom: "20px",
            "& .MuiOutlinedInput-root": {
              borderRadius: "12px",
              fontFamily: "'DM Sans', sans-serif",
              "&:hover fieldset": {
                borderColor: "#D4622A",
              },
              "&.Mui-focused fieldset": {
                borderColor: "#D4622A",
              },
            },
            "& .MuiInputLabel-root": {
              fontFamily: "'DM Sans', sans-serif",
              color: "#8B6555",
              "&.Mui-focused": {
                color: "#D4622A",
              },
            },
          }}
        />

                <TextField
                  fullWidth
                  label="E-mail"
                  type="email"
                  {...registerRegister("email", {
                    required: "E-mail é obrigatório",
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: "E-mail inválido",
                    },
                  })}
                  error={!!registerErrors.email}
                  helperText={registerErrors.email?.message}
                  sx={{
                    marginBottom: "20px",
                    "& .MuiOutlinedInput-root": {
                      borderRadius: "12px",
                      fontFamily: "'DM Sans', sans-serif",
                      "&:hover fieldset": {
                        borderColor: "#D4622A",
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: "#D4622A",
                      },
                    },
                    "& .MuiInputLabel-root": {
                      fontFamily: "'DM Sans', sans-serif",
                      color: "#8B6555",
                      "&.Mui-focused": {
                        color: "#D4622A",
                      },
                    },
                  }}
                />

                <TextField
                  fullWidth
                  label="Senha"
                  type={showPassword ? "text" : "password"}
                  {...registerRegister("password", {
                    required: "Senha é obrigatória",
                    minLength: {
                      value: 6,
                      message: "Senha deve ter no mínimo 6 caracteres",
                    },
                  })}
                  error={!!registerErrors.password}
                  helperText={registerErrors.password?.message}
                  sx={{
                    marginBottom: "20px",
                    "& .MuiOutlinedInput-root": {
                      borderRadius: "12px",
                      fontFamily: "'DM Sans', sans-serif",
                      "&:hover fieldset": {
                        borderColor: "#D4622A",
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: "#D4622A",
                      },
                    },
                    "& .MuiInputLabel-root": {
                      fontFamily: "'DM Sans', sans-serif",
                      color: "#8B6555",
                      "&.Mui-focused": {
                        color: "#D4622A",
                      },
                    },
                  }}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={() => setShowPassword(!showPassword)}
                          edge="end"
                          sx={{ color: "#8B6555" }}
                        >
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />

                <TextField
                  fullWidth
                  label="Confirmar senha"
                  type={showConfirmPassword ? "text" : "password"}
                  {...registerRegister("confirmPassword", {
                    required: "Confirme sua senha",
                    validate: (value) =>
                      value === watchPassword || "As senhas não coincidem",
                  })}
                  error={!!registerErrors.confirmPassword}
                  helperText={registerErrors.confirmPassword?.message}
                  sx={{
                    marginBottom: "28px",
                    "& .MuiOutlinedInput-root": {
                      borderRadius: "12px",
                      fontFamily: "'DM Sans', sans-serif",
                      "&:hover fieldset": {
                        borderColor: "#D4622A",
                      },
                      "&.Mui-focused fieldset": {
                        borderColor: "#D4622A",
                      },
                    },
                    "& .MuiInputLabel-root": {
                      fontFamily: "'DM Sans', sans-serif",
                      color: "#8B6555",
                      "&.Mui-focused": {
                        color: "#D4622A",
                      },
                    },
                  }}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={() =>
                            setShowConfirmPassword(!showConfirmPassword)
                          }
                          edge="end"
                          sx={{ color: "#8B6555" }}
                        >
                          {showConfirmPassword ? (
                            <VisibilityOff />
                          ) : (
                            <Visibility />
                          )}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />

                <Button
                  type="submit"
                  fullWidth
                  disabled={isLoading}
                  sx={{
                    background: "#D4622A",
                    color: "#fff",
                    fontFamily: "'DM Sans', sans-serif",
                    fontSize: "16px",
                    fontWeight: 600,
                    padding: "14px",
                    borderRadius: "100px",
                    transition: "all .2s",
                    boxShadow: "0 8px 32px rgba(212,98,42,.3)",
                    "&:hover": {
                      background: "#E87E47",
                      transform: "translateY(-2px)",
                    },
                    "&:disabled": {
                      background: "#D4622A",
                      opacity: 0.7,
                    },
                  }}
                >
                  {isLoading ? (
                    <CircularProgress size={24} sx={{ color: "#fff" }} />
                  ) : (
                    "Criar conta 🐕"
                  )}
                </Button>
              </form>
            )}

            {/* Switch between login and register */}
            <Box sx={{ marginTop: "32px", textAlign: "center" }}>
              <p
                style={{
                  fontSize: "14px",
                  color: "#6B4A3A",
                  fontFamily: "'DM Sans', sans-serif",
                }}
              >
                {isLogin ? "Não tem uma conta?" : "Já tem uma conta?"}
                <Button
                  onClick={() => {
                    setIsLogin(!isLogin);
                  }}
                  sx={{
                    background: "none",
                    border: "none",
                    color: "#D4622A",
                    fontWeight: 600,
                    marginLeft: "8px",
                    textTransform: "none",
                    fontFamily: "'DM Sans', sans-serif",
                    fontSize: "14px",
                    "&:hover": {
                      background: "none",
                      opacity: 0.8,
                    },
                  }}
                >
                  {isLogin ? "Registre-se grátis" : "Fazer login"}
                </Button>
              </p>
            </Box>
          </div>
        </Box>
      </Box>
    </Container>
  );
}
