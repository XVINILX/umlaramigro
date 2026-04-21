import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { useState, useRef } from "react";
import {
  Box,
  Container,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Paper,
  Typography,
  FormHelperText,
  Grid,
  IconButton,
  InputAdornment,
} from "@mui/material";
import { CloudUpload, Close } from "@mui/icons-material";
import { useAppDispatch, useAppSelector } from "~/store/hooks";
import { createPet, uploadPetImage, clearError, clearSuccess } from "~/store/slices/petSlice";
import { PetType, type PetCreate } from "~/interfaces/pet.interface";
import type { Route } from "./+types/novo";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Cadastrar Pet | Um Lar Amigo" },
    {
      name: "description",
      content: "Cadastre um novo pet para adoção",
    },
  ];
}

export default function NovoPetPage() {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { isLoading, error, successMessage } = useAppSelector(
    (state) => state.pets,
  );
  const { user } = useAppSelector((state) => state.auth);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<PetCreate>({
    defaultValues: {
      name: "",
      pet_type: PetType.DOG,
      description: "",
    },
  });

  const onSubmit = async (data: PetCreate) => {
    const petData = { ...data };
    delete petData.image;
    
    const result = await dispatch(createPet(petData));

    if (createPet.fulfilled.match(result) && selectedImage) {
      await dispatch(uploadPetImage({
        petId: result.payload.id,
        file: selectedImage,
      }));
    }

    if (createPet.fulfilled.match(result)) {
      setTimeout(() => {
        reset();
        dispatch(clearSuccess());
        handleRemoveImage();
      }, 2000);

      setTimeout(() => {
        navigate("/dashboard/pets");
      }, 3000);
    }
  };

  const handleClearMessages = () => {
    dispatch(clearError());
    dispatch(clearSuccess());
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith("image/")) {
        dispatch(clearError());
        return;
      }
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemoveImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

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
        <Box sx={{ mb: 4 }}>
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
            Cadastrar novo pet 🐾
          </Typography>
          <Typography
            sx={{
              color: "#6B4A3A",
              fontFamily: "'DM Sans', sans-serif",
            }}
          >
            Preencha as informações abaixo para adicionar um pet para adoção
          </Typography>
        </Box>

        {/* Messages */}
        {error && (
          <Alert
            severity="error"
            sx={{ mb: 3, borderRadius: "12px" }}
            onClose={handleClearMessages}
          >
            {error}
          </Alert>
        )}

        {successMessage && (
          <Alert
            severity="success"
            sx={{ mb: 3, borderRadius: "12px" }}
            onClose={handleClearMessages}
          >
            {successMessage}
          </Alert>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Nome do pet"
                {...register("name", {
                  required: "Nome é obrigatório",
                  minLength: {
                    value: 2,
                    message: "Nome deve ter no mínimo 2 caracteres",
                  },
                  maxLength: {
                    value: 50,
                    message: "Nome deve ter no máximo 50 caracteres",
                  },
                })}
                error={!!errors.name}
                helperText={errors.name?.message}
                sx={{
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
            </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth error={!!errors.pet_type}>
                <InputLabel
                  sx={{
                    fontFamily: "'DM Sans', sans-serif",
                    color: "#8B6555",
                    "&.Mui-focused": {
                      color: "#D4622A",
                    },
                  }}
                >
                  Tipo de pet
                </InputLabel>
                <Select
                  {...register("pet_type", {
                    required: "Tipo de pet é obrigatório",
                  })}
                  label="Tipo de pet"
                  sx={{
                    borderRadius: "12px",
                    fontFamily: "'DM Sans', sans-serif",
                    "&:hover .MuiOutlinedInput-notchedOutline": {
                      borderColor: "#D4622A",
                    },
                    "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
                      borderColor: "#D4622A",
                    },
                  }}
                >
                  <MenuItem value={PetType.DOG}>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <span>🐕</span> Cão
                    </Box>
                  </MenuItem>
                  <MenuItem value={PetType.CAT}>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <span>🐱</span> Gato
                    </Box>
                  </MenuItem>
                </Select>
                {errors.pet_type && (
                  <FormHelperText>{errors.pet_type.message}</FormHelperText>
                )}
              </FormControl>
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Descrição"
                multiline
                rows={4}
                {...register("description", {
                  maxLength: {
                    value: 500,
                    message: "Descrição deve ter no máximo 500 caracteres",
                  },
                })}
                error={!!errors.description}
                helperText={
                  errors.description?.message ||
                  "Conte um pouco sobre a personalidade do pet"
                }
                sx={{
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
            </Grid>

            {/* Image Upload */}
            <Grid item xs={12}>
              <input
                type="file"
                accept="image/*"
                ref={fileInputRef}
                onChange={handleImageChange}
                style={{ display: "none" }}
              />
              {!imagePreview ? (
                <Box
                  onClick={() => fileInputRef.current?.click()}
                  sx={{
                    border: "2px dashed rgba(92,61,46,.3)",
                    borderRadius: "12px",
                    p: 4,
                    textAlign: "center",
                    cursor: "pointer",
                    transition: "all 0.2s",
                    "&:hover": {
                      borderColor: "#D4622A",
                      background: "rgba(212,98,42,.05)",
                    },
                  }}
                >
                  <CloudUpload sx={{ fontSize: 48, color: "#8B6555", mb: 1 }} />
                  <Typography
                    sx={{
                      fontFamily: "'DM Sans', sans-serif",
                      color: "#5C3D2E",
                    }}
                  >
                    Clique para adicionar uma foto do pet
                  </Typography>
                  <Typography
                    sx={{
                      fontFamily: "'DM Sans', sans-serif",
                      fontSize: "12px",
                      color: "#8B6555",
                      mt: 0.5,
                    }}
                  >
                    PNG, JPG ou GIF (máx. 5MB)
                  </Typography>
                </Box>
              ) : (
                <Box
                  sx={{
                    position: "relative",
                    borderRadius: "12px",
                    overflow: "hidden",
                    width: 200,
                    height: 200,
                  }}
                >
                  <Box
                    component="img"
                    src={imagePreview}
                    alt="Preview"
                    sx={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                    }}
                  />
                  <IconButton
                    onClick={handleRemoveImage}
                    sx={{
                      position: "absolute",
                      top: 8,
                      right: 8,
                      background: "rgba(0,0,0,0.5)",
                      color: "#fff",
                      "&:hover": {
                        background: "rgba(0,0,0,0.7)",
                      },
                    }}
                    size="small"
                  >
                    <Close fontSize="small" />
                  </IconButton>
                </Box>
              )}
            </Grid>
          </Grid>

          {/* Action Buttons */}
          <Box
            sx={{
              display: "flex",
              gap: 2,
              justifyContent: "flex-end",
              mt: 4,
              pt: 2,
              borderTop: "1px solid rgba(92,61,46,.1)",
            }}
          >
            <Button
              variant="outlined"
              onClick={() => navigate("/dashboard/pets")}
              sx={{
                fontFamily: "'DM Sans', sans-serif",
                fontSize: "14px",
                fontWeight: 500,
                color: "#5C3D2E",
                borderColor: "#8B6555",
                borderRadius: "100px",
                padding: "10px 24px",
                "&:hover": {
                  borderColor: "#D4622A",
                  background: "rgba(92,61,46,.05)",
                },
              }}
            >
              Cancelar
            </Button>

            <Button
              type="submit"
              variant="contained"
              disabled={isLoading}
              sx={{
                background: "#D4622A",
                fontFamily: "'DM Sans', sans-serif",
                fontSize: "14px",
                fontWeight: 500,
                borderRadius: "100px",
                padding: "10px 32px",
                "&:hover": {
                  background: "#E87E47",
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
                "Cadastrar Pet 🐾"
              )}
            </Button>
          </Box>
        </form>
      </Paper>
    </Container>
  );
}
