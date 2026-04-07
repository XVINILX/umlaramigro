import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("pets", "routes/pets/index.tsx"),
] satisfies RouteConfig;
