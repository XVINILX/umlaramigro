import {
  type RouteConfig,
  index,
  layout,
  route,
} from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("login", "routes/login.tsx"),
  route("pets", "routes/pets/index.tsx"),
  route("dashboard", "routes/dashboard/layout.tsx", [
    index("routes/dashboard/index.tsx"), 
    route("pets", "routes/dashboard/pets/index.tsx"), 
    route("pets/novo", "routes/dashboard/pets/novo.tsx"),
  ]),
] satisfies RouteConfig;
