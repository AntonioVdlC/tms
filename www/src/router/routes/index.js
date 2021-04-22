import appRoutes from "@/router/routes/app";
import authRoutes from "@/router/routes/auth";
import landingRoutes from "@/router/routes/landing";

const routes = [
  ...appRoutes,
  ...authRoutes,
  ...landingRoutes,
  {
    path: "/:pathMatch(.*)",
    name: "NotFound",
    component: () => import("@/pages/app/NotFound.vue"),
  },
];

export default routes;
