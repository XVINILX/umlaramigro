import type { Route } from "./+types/home";
import { useState, useEffect } from "react";
import { Box, Container } from "@mui/material";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Um Lar Amigo - Pet Adoption" },
    {
      name: "description",
      content:
        "Conectamos ONGs, abrigos e protetores independentes a famílias que querem dar uma segunda chance a um pet especial.",
    },
  ];
}

export default function Home() {
  const [carouselIndex, setCarouselIndex] = useState(0);
  const CARD_WIDTH = 380 + 24;
  const TOTAL_CARDS = 6;

  useEffect(() => {
    const timer = setInterval(() => {
      setCarouselIndex((prev) => (prev + 1) % TOTAL_CARDS);
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  const goToSlide = (idx: number) => {
    setCarouselIndex((idx + TOTAL_CARDS) % TOTAL_CARDS);
  };

  const handlePrev = () => {
    setCarouselIndex((prev) => (prev - 1 + TOTAL_CARDS) % TOTAL_CARDS);
  };

  const handleNext = () => {
    setCarouselIndex((prev) => (prev + 1) % TOTAL_CARDS);
  };

  const pets = [
    {
      name: "Bolinha",
      desc: "Caramelo de 2 anos, vacinado e castrado. Adora crianças e é ótimo com outros cães!",
      emoji: "🐕",
      tag: "Adoção",
      chips: ["🐶 Cão", "2 anos", "Médio porte"],
      bg: "linear-gradient(135deg,#f5dfc0,#e0b07a)",
    },
    {
      name: "Luna",
      desc: "Gatinha cinza de 1 ano, super carinhosa. Ótima companheira para apartamento.",
      emoji: "🐈",
      tag: "Adoção",
      chips: ["🐱 Gato", "1 ano", "Fêmea"],
      bg: "linear-gradient(135deg,#d4c5e8,#b09ac8)",
    },
    {
      name: "Thor",
      desc: "Pastor misturado de 4 anos, protetor e leal. Precisa de um lar urgente com espaço.",
      emoji: "🐕‍🦺",
      tag: "Urgente",
      chips: ["🐶 Cão", "4 anos", "Grande porte"],
      bg: "linear-gradient(135deg,#c5e0d4,#7ab09a)",
    },
    {
      name: "Pipoca",
      desc: "Gatinha preta de 8 meses, muito brincalhona. Adora dormir no colo e ronronar.",
      emoji: "🐈‍⬛",
      tag: "Adoção",
      chips: ["🐱 Gato", "8 meses", "Filhote"],
      bg: "linear-gradient(135deg,#f5e4c0,#e8c070)",
    },
    {
      name: "Belinha",
      desc: "Poodle de 3 anos resgatada de maus-tratos. Já está recuperada e cheia de amor para dar.",
      emoji: "🐩",
      tag: "Adoção",
      chips: ["🐶 Cão", "3 anos", "Pequeno porte"],
      bg: "linear-gradient(135deg,#e8d0c0,#c4906a)",
    },
    {
      name: "Mochi",
      desc: "Coelhinho branco de 1 ano, manso e dócil. Perfeito para quem quer um pet diferente.",
      emoji: "🐇",
      tag: "Adoção",
      chips: ["🐰 Coelho", "1 ano", "Macho"],
      bg: "linear-gradient(135deg,#d0e8c0,#90c470)",
    },
  ];

  return (
    <Container
      sx={{ backgroundColor: "#FDF6EC", padding: 0, maxWidth: "100%" }}
      style={{ backgroundColor: "#FDF6EC", padding: 0, maxWidth: "100%" }}
    >
      <Box
        sx={{
          backgroundColor: "#FDF6EC",
          overflow: "hidden",
        }}
      >
        {/* NAV */}
        <Box
          component="nav"
          sx={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            zIndex: 100,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "18px 48px",
            background: "rgba(253, 246, 236, 0.88)",
            backdropFilter: "blur(12px)",
            borderBottom: "1px solid rgba(92,61,46,.1)",
          }}
        >
          <img
            src="https://umlaramigo-homolog.s3.us-east-1.amazonaws.com/logo_um_lar_amigo.png"
            alt="Um Lar Amigo"
            style={{ height: "44px" }}
          />
          <button
            style={{
              fontFamily: "'DM Sans', sans-serif",
              fontWeight: 500,
              fontSize: "14px",
              letterSpacing: ".04em",
              color: "#5C3D2E",
              border: "1.5px solid #8B6555",
              background: "transparent",
              padding: "10px 24px",
              borderRadius: "100px",
              cursor: "not-allowed",
              opacity: 0.65,
              position: "relative",
              transition: "opacity .2s",
            }}
          >
            Login
            <span
              style={{
                position: "absolute",
                top: "-8px",
                right: "-8px",
                background: "#F2A541",
                color: "#5C3D2E",
                fontSize: "9px",
                fontWeight: 700,
                letterSpacing: ".06em",
                padding: "2px 6px",
                borderRadius: "100px",
                textTransform: "uppercase",
              }}
            >
              Em Breve
            </span>
          </button>
        </Box>

        {/* HERO */}
        <Box
          component="section"
          sx={{
            minHeight: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
            padding: "120px 48px 80px",
            textAlign: "center",
            position: "relative",
            overflow: "hidden",
            "@media (max-width: 640px)": {
              padding: "100px 20px 60px",
            },
          }}
        >
          <Box sx={{ fontSize: "56px", margin: "0 28px" }}>
            🐾 Plataforma de Adoção de Pets
          </Box>
          <h1
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "clamp(52px, 8vw, 110px)",
              fontWeight: 900,
              lineHeight: 0.95,
              color: "#5C3D2E",
              maxWidth: 900,
              marginBottom: 24,
            }}
          >
            Todo pet merece
            <em
              style={{
                fontStyle: "italic",
                color: "#D4622A",
                display: "block",
              }}
            >
              um lar amigo.
            </em>
          </h1>
          <p
            style={{
              fontSize: "clamp(16px, 2vw, 20px)",
              color: "#6B4A3A",
              maxWidth: 540,
              lineHeight: 1.6,
              marginTop: 24,
              fontWeight: 300,
            }}
          >
            Conectamos ONGs, abrigos e protetores independentes a famílias que
            querem dar uma segunda chance a um pet especial.
          </p>

          <Box
            sx={{
              marginTop: "44px",
              display: "flex",
              gap: "16px",
              flexWrap: "wrap",
              justifyContent: "center",
            }}
          >
            <button
              style={{
                background: "#D4622A",
                color: "#fff",
                border: "none",
                fontFamily: "'DM Sans', sans-serif",
                fontSize: "16px",
                fontWeight: 500,
                padding: "16px 36px",
                borderRadius: "100px",
                cursor: "pointer",
                transition: "background .2s, transform .15s",
                boxShadow: "0 8px 32px rgba(212,98,42,.3)",
              }}
              onMouseEnter={(e) => {
                (e.target as HTMLElement).style.background = "#E87E47";
                (e.target as HTMLElement).style.transform = "translateY(-2px)";
              }}
              onMouseLeave={(e) => {
                (e.target as HTMLElement).style.background = "#D4622A";
                (e.target as HTMLElement).style.transform = "translateY(0)";
              }}
            >
              Encontrar meu pet 🐶
            </button>
            <button
              style={{
                background: "transparent",
                color: "#5C3D2E",
                border: "1.5px solid #8B6555",
                fontFamily: "'DM Sans', sans-serif",
                fontSize: "16px",
                fontWeight: 500,
                padding: "16px 36px",
                borderRadius: "100px",
                cursor: "pointer",
                transition: "background .2s",
              }}
              onMouseEnter={(e) =>
                ((e.target as HTMLElement).style.background =
                  "rgba(92,61,46,.06)")
              }
              onMouseLeave={(e) =>
                ((e.target as HTMLElement).style.background = "transparent")
              }
            >
              Cadastrar minha ONG
            </button>
          </Box>

          <Box
            sx={{
              marginTop: "60px",
              display: "flex",
              gap: "10px",
              justifyContent: "center",
              opacity: 0.3,
            }}
          >
            {[...Array(5)].map((_, i) => (
              <span key={i} style={{ fontSize: "20px" }}>
                🐾
              </span>
            ))}
          </Box>
        </Box>

        {/* STATS */}
        <Box
          sx={{
            display: "flex",
            gap: 0,
            flexWrap: "wrap",
            background: "#2C1810",
            color: "#fff",
          }}
        >
          {[
            { num: "1.200+", label: "Pets cadastrados" },
            { num: "340+", label: "ONGs parceiras" },
            { num: "890+", label: "Adoções realizadas" },
            { num: "52", label: "Cidades atendidas" },
          ].map((stat, i) => (
            <Box
              key={i}
              sx={{
                flex: 1,
                minWidth: 200,
                padding: "40px 48px",
                borderRight: i < 3 ? "1px solid rgba(255,255,255,.1)" : "none",
                textAlign: "center",
                transition: "background .2s",
                "&:hover": { background: "#D4622A" },
              }}
            >
              <Box
                sx={{
                  fontFamily: "'Fraunces', serif",
                  fontSize: "52px",
                  fontWeight: 900,
                  color: "#F2A541",
                  lineHeight: 1,
                }}
              >
                {stat.num}
              </Box>
              <Box
                sx={{
                  fontSize: "13px",
                  letterSpacing: ".06em",
                  textTransform: "uppercase",
                  opacity: 0.7,
                  marginTop: "6px",
                }}
              >
                {stat.label}
              </Box>
            </Box>
          ))}
        </Box>

        {/* CAROUSEL */}
        <Box
          component="section"
          sx={{ background: "#FFFBF5", padding: "100px 0" }}
        >
          <Box sx={{ padding: "0 48px", marginBottom: "52px" }}>
            <h2
              style={{
                fontFamily: "'Fraunces', serif",
                fontSize: "clamp(36px, 5vw, 64px)",
                fontWeight: 900,
                color: "#5C3D2E",
                lineHeight: 1.05,
                marginBottom: 16,
              }}
            >
              Pets esperando{" "}
              <em style={{ fontStyle: "italic", color: "#D4622A" }}>
                por você
              </em>
            </h2>
            <p
              style={{
                fontSize: "18px",
                color: "#6B4A3A",
                fontWeight: 300,
                lineHeight: 1.6,
              }}
            >
              Cada um tem uma história. Qual deles vai mudar a sua?
            </p>
          </Box>

          <Box sx={{ position: "relative", overflow: "hidden" }}>
            <Box
              sx={{
                display: "flex",
                gap: "24px",
                padding: "0 48px 24px",
                transition: "transform .5s cubic-bezier(.4,0,.2,1)",
                transform: `translateX(-${carouselIndex * CARD_WIDTH}px)`,
                willChange: "transform",
              }}
            >
              {pets.map((pet, idx) => (
                <Box
                  key={idx}
                  sx={{
                    flex: "0 0 380px",
                    borderRadius: "24px",
                    overflow: "hidden",
                    position: "relative",
                    background: "#FDF6EC",
                    boxShadow: "0 4px 24px rgba(44,24,16,.08)",
                    transition: "transform .3s, box-shadow .3s",
                    cursor: "pointer",
                    "&:hover": {
                      transform: "translateY(-6px)",
                      boxShadow: "0 16px 48px rgba(44,24,16,.14)",
                    },
                  }}
                >
                  <Box
                    sx={{
                      width: "100%",
                      height: "260px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "72px",
                      background: pet.bg,
                      position: "relative",
                    }}
                  >
                    {pet.emoji}
                    <Box
                      sx={{
                        position: "absolute",
                        top: "16px",
                        left: "16px",
                        background: "#D4622A",
                        color: "#fff",
                        fontSize: "11px",
                        fontWeight: 700,
                        letterSpacing: ".08em",
                        textTransform: "uppercase",
                        padding: "4px 12px",
                        borderRadius: "100px",
                      }}
                    >
                      {pet.tag}
                    </Box>
                  </Box>
                  <Box sx={{ padding: "24px" }}>
                    <Box
                      sx={{
                        fontFamily: "'Fraunces', serif",
                        fontSize: "26px",
                        fontWeight: 700,
                        color: "#5C3D2E",
                        marginBottom: "6px",
                      }}
                    >
                      {pet.name}
                    </Box>
                    <Box
                      sx={{
                        fontSize: "14px",
                        color: "#6B4A3A",
                        lineHeight: 1.5,
                      }}
                    >
                      {pet.desc}
                    </Box>
                    <Box
                      sx={{
                        display: "flex",
                        gap: "12px",
                        marginTop: "16px",
                        flexWrap: "wrap",
                      }}
                    >
                      {pet.chips.map((chip, i) => (
                        <span
                          key={i}
                          style={{
                            background: "#FDF6EC",
                            border: "1px solid rgba(92,61,46,.15)",
                            color: "#8B6555",
                            fontSize: "12px",
                            padding: "4px 12px",
                            borderRadius: "100px",
                          }}
                        >
                          {chip}
                        </span>
                      ))}
                    </Box>
                  </Box>
                </Box>
              ))}
            </Box>
          </Box>

          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "16px",
              marginTop: "40px",
              padding: "0 48px",
            }}
          >
            <button
              onClick={handlePrev}
              style={{
                width: "48px",
                height: "48px",
                borderRadius: "50%",
                border: "1.5px solid #8B6555",
                background: "transparent",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "18px",
                color: "#5C3D2E",
                transition: "all .2s",
              }}
              onMouseEnter={(e) => {
                (e.target as HTMLElement).style.background = "#D4622A";
                (e.target as HTMLElement).style.borderColor = "#D4622A";
                (e.target as HTMLElement).style.color = "#fff";
              }}
              onMouseLeave={(e) => {
                (e.target as HTMLElement).style.background = "transparent";
                (e.target as HTMLElement).style.borderColor = "#8B6555";
                (e.target as HTMLElement).style.color = "#5C3D2E";
              }}
            >
              ←
            </button>
            <Box sx={{ display: "flex", gap: "8px" }}>
              {pets.map((_, idx) => (
                <button
                  key={idx}
                  onClick={() => goToSlide(idx)}
                  style={{
                    width: idx === carouselIndex ? "24px" : "8px",
                    height: "8px",
                    borderRadius: "100px",
                    background: idx === carouselIndex ? "#D4622A" : "#8B6555",
                    opacity: idx === carouselIndex ? 1 : 0.3,
                    cursor: "pointer",
                    transition: "all .3s",
                    border: "none",
                  }}
                />
              ))}
            </Box>
            <button
              onClick={handleNext}
              style={{
                width: "48px",
                height: "48px",
                borderRadius: "50%",
                border: "1.5px solid #8B6555",
                background: "transparent",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "18px",
                color: "#5C3D2E",
                transition: "all .2s",
              }}
              onMouseEnter={(e) => {
                (e.target as HTMLElement).style.background = "#D4622A";
                (e.target as HTMLElement).style.borderColor = "#D4622A";
                (e.target as HTMLElement).style.color = "#fff";
              }}
              onMouseLeave={(e) => {
                (e.target as HTMLElement).style.background = "transparent";
                (e.target as HTMLElement).style.borderColor = "#8B6555";
                (e.target as HTMLElement).style.color = "#5C3D2E";
              }}
            >
              →
            </button>
          </Box>
        </Box>

        {/* HOW IT WORKS */}
        <Box component="section" sx={{ padding: "100px 48px" }}>
          <h2
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "clamp(36px, 5vw, 64px)",
              fontWeight: 900,
              color: "#5C3D2E",
              lineHeight: 1.05,
              marginBottom: 16,
            }}
          >
            Como{" "}
            <em style={{ fontStyle: "italic", color: "#D4622A" }}>funciona</em>
          </h2>
          <p
            style={{
              fontSize: "18px",
              color: "#6B4A3A",
              fontWeight: 300,
              lineHeight: 1.6,
            }}
          >
            Simples, rápido e com muito amor.
          </p>

          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
              gap: "32px",
              marginTop: "64px",
            }}
          >
            {[
              {
                num: "01",
                icon: "🏠",
                title: "ONGs cadastram seus pets",
                text: "Abrigos e protetores criam perfis completos com fotos, personalidade e necessidades de cada animal.",
              },
              {
                num: "02",
                icon: "🔍",
                title: "Famílias encontram seu match",
                text: "Filtre por espécie, porte, idade e localidade. Encontre o pet ideal para o seu estilo de vida.",
              },
              {
                num: "03",
                icon: "💬",
                title: "Conectamos vocês",
                text: "Nossa plataforma facilita o contato direto entre adotante e organização para agilizar o processo.",
              },
              {
                num: "04",
                icon: "❤️",
                title: "Um novo começo",
                text: "Pet vai para o lar, família ganha um amigo para a vida. Todo mundo sai ganhando — especialmente eles!",
              },
            ].map((item, i) => (
              <Box
                key={i}
                sx={{
                  background: "#FFFBF5",
                  borderRadius: "20px",
                  padding: "36px",
                  position: "relative",
                  border: "1px solid rgba(92,61,46,.08)",
                  transition: "transform .3s",
                  "&:hover": { transform: "translateY(-4px)" },
                }}
              >
                <Box
                  sx={{
                    fontFamily: "'Fraunces', serif",
                    fontSize: "72px",
                    fontWeight: 900,
                    color: "#D4622A",
                    opacity: 0.15,
                    lineHeight: 1,
                    position: "absolute",
                    top: "20px",
                    right: "24px",
                  }}
                >
                  {item.num}
                </Box>
                <Box sx={{ fontSize: "36px", marginBottom: "16px" }}>
                  {item.icon}
                </Box>
                <Box
                  sx={{
                    fontFamily: "'Fraunces', serif",
                    fontSize: "22px",
                    fontWeight: 700,
                    color: "#5C3D2E",
                    marginBottom: "10px",
                  }}
                >
                  {item.title}
                </Box>
                <Box
                  sx={{ fontSize: "15px", color: "#6B4A3A", lineHeight: 1.6 }}
                >
                  {item.text}
                </Box>
              </Box>
            ))}
          </Box>
        </Box>

        {/* CTA BAND */}
        <Box
          component="section"
          sx={{
            background: "#D4622A",
            color: "#fff",
            textAlign: "center",
            padding: "100px 48px",
            position: "relative",
            overflow: "hidden",
            "&::before": {
              content: '"🐾"',
              fontSize: "300px",
              position: "absolute",
              top: "-60px",
              right: "-40px",
              opacity: 0.06,
              pointerEvents: "none",
              lineHeight: 1,
            },
          }}
        >
          <h2
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "clamp(40px, 6vw, 80px)",
              fontWeight: 900,
              lineHeight: 1,
              marginBottom: "20px",
            }}
          >
            Sua ONG pode
            <br />
            salvar vidas.
          </h2>
          <p
            style={{
              fontSize: "18px",
              opacity: 0.85,
              maxWidth: 480,
              margin: "0 auto 40px",
              fontWeight: 300,
            }}
          >
            Cadastre seus pets gratuitamente e alcance centenas de potenciais
            adotantes em todo o Brasil.
          </p>
          <button
            style={{
              background: "#fff",
              color: "#D4622A",
              border: "none",
              fontFamily: "'DM Sans', sans-serif",
              fontSize: "16px",
              fontWeight: 600,
              padding: "16px 40px",
              borderRadius: "100px",
              cursor: "pointer",
              transition: "transform .2s, box-shadow .2s",
              boxShadow: "0 8px 32px rgba(0,0,0,.15)",
            }}
            onMouseEnter={(e) => {
              (e.target as HTMLElement).style.transform = "translateY(-2px)";
              (e.target as HTMLElement).style.boxShadow =
                "0 12px 48px rgba(0,0,0,.2)";
            }}
            onMouseLeave={(e) => {
              (e.target as HTMLElement).style.transform = "translateY(0)";
              (e.target as HTMLElement).style.boxShadow =
                "0 8px 32px rgba(0,0,0,.15)";
            }}
          >
            Quero cadastrar minha ONG 🐾
          </button>
        </Box>

        {/* FOOTER */}
        <footer
          style={{
            background: "#2C1810",
            color: "rgba(255,255,255,.5)",
            textAlign: "center",
            padding: "40px 48px",
            fontSize: "13px",
          }}
        >
          <img
            src="https://umlaramigo-homolog.s3.us-east-1.amazonaws.com/logo_um_lar_amigo.png"
            alt="Um Lar Amigo"
            style={{
              height: "32px",
              opacity: 0.6,
              marginBottom: "16px",
              display: "block",
              marginInline: "auto",
            }}
          />
          <p>© 2025 Um Lar Amigo · Feito com ❤️ para os pets do Brasil</p>
        </footer>
      </Box>
    </Container>
  );
}
